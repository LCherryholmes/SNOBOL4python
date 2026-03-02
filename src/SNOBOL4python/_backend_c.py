# -*- coding: utf-8 -*-
# _backend_c.py — C/SPIPAT-backed SNOBOL4 pattern engine (Stage 8)
#
# The SNOBOL environment dict is accessed via _env._g — the single shared
# reference.  There is no local _globals_ref here; nothing is duplicated.
#
# Extends Stage 7 with:
#   nPush  nInc  nPop            — integer counter stack (istack)
#   Shift  Reduce  Pop           — parse-tree value stack (vstack)
#
# These six patterns implement a shift-reduce parser infrastructure on top
# of two lists maintained in globals:
#   __vs_istack__  — integer counter stack  (nPush/nInc/nPop)
#   __vs_vstack__  — parse-tree node stack  (Shift/Reduce/Pop)
#
# All six delegate directly to _C.npush() / _C.ninc() / ... which are
# already fully implemented in sno4py.c.
#
# ─────────────────────────────────────────────────────────────────────────────
import re as _re
import sno4py as _C
from . import _env

# ── Exception ─────────────────────────────────────────────────────────────────

class F(Exception): pass

# ── Supporting string types ───────────────────────────────────────────────────

class STRING(str):
    """SNOBOL4 string — str subclass that participates in pattern algebra."""
    def __repr__(self):         return str.__repr__(self)

    def __add__(self, other):
        if isinstance(other, PATTERN):  return σ(self) + other
        return STRING(super().__add__(str(other)))

    def __radd__(self, other):
        if isinstance(other, PATTERN):  return other + σ(self)
        return STRING(str(other).__add__(self))

    def __or__(self, other):
        if isinstance(other, PATTERN):  return σ(self) | other
        return NotImplemented

    def __contains__(self, other):
        if isinstance(other, PATTERN):  return other.__contains__(self)
        return super().__contains__(str(other))


class Ϩ(STRING): pass

NULL = STRING('')

# ── PATTERN base class ────────────────────────────────────────────────────────

class PATTERN:
    """
    Base class for all SNOBOL4 patterns.
    Every instance holds a compiled sno4py.Pattern in self._c.
    """
    __slots__ = ('_c',)

    def __add__(self, other):
        """Concatenation:  P + Q"""
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return _ConcatPat(_C.concat(self._c, other._c))

    def __radd__(self, other):
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return other.__add__(self)

    def __or__(self, other):
        """Alternation:  P | Q"""
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return _AltPat(_C.alt(self._c, other._c))

    def __ror__(self, other):
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return other.__or__(self)

    def __invert__(self):
        """Optional:  ~P  ≡  P | ε"""
        return self | ε()

    def __matmul__(self, other):
        """Immediate assignment:  P @ 'name'  (SNOBOL4: P $ N)"""
        return _AssignImmPat(_C.assign_imm(self._c, str(other)))

    def __mod__(self, other):
        """Conditional assignment:  P % 'name'  (SNOBOL4: P . N)"""
        return _AssignOnmPat(_C.assign_onm(self._c, str(other)))

    def __and__(self, other):
        """Conjunction:  P & Q  — both must match the same span."""
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return ρ(self, other)

    def __rand__(self, other):
        if not isinstance(other, PATTERN):  other = σ(str(other))
        return ρ(other, self)

    def __eq__(self, other):
        """P == subject  →  SEARCH(subject, P, exc=True)"""
        return SEARCH(other, self, exc=True)

    def __contains__(self, other):
        """subject in P  →  bool"""
        return SEARCH(other, self, exc=False) is not None

    def __hash__(self):             return id(self)
    def __repr__(self):             return f'<{type(self).__name__}>'

    def compile(self):
        """Return the underlying sno4py.Pattern — used by sno4py.rpat() callback."""
        return self._c


# ── Internal wrappers ─────────────────────────────────────────────────────────

class _ConcatPat(PATTERN):
    __slots__ = ('_c',)
    def __init__(self, c): self._c = c
    def __repr__(self): return '<Σ>'

class _AltPat(PATTERN):
    __slots__ = ('_c',)
    def __init__(self, c): self._c = c
    def __repr__(self): return '<Π>'

class _AssignImmPat(PATTERN):
    __slots__ = ('_c',)
    def __init__(self, c): self._c = c

class _AssignOnmPat(PATTERN):
    __slots__ = ('_c',)
    def __init__(self, c): self._c = c

class _WrapPat:
    """Minimal wrapper returned by rpat lambdas — has .compile() only."""
    __slots__ = ('_c',)
    def __init__(self, c): self._c = c
    def compile(self): return self._c


# ── Helpers for callable arguments ───────────────────────────────────────────

def _chars(c):
    """Resolve a chars argument: str, set, or callable → str."""
    if callable(c):         return str(c())
    if isinstance(c, set):  return ''.join(sorted(c))
    return str(c)

def _int(n):
    """Resolve an integer argument: int or callable → int."""
    if callable(n): return int(n())
    return int(n)

def _make_int_pat(ctor, n):
    """
    Build a C pattern for a positional/length primitive.
    If n is callable, wrap via rpat so it's evaluated at match time.
    The lambda returns a _WrapPat which has .compile() → sno4py.Pattern.
    """
    if callable(n):
        def _deferred():
            return _WrapPat(ctor(int(n())))
        return _C.rpat(_deferred)
    return ctor(int(n))

def _make_str_pat(ctor, chars):
    """
    Build a C pattern for a char-class primitive.
    If chars is callable, wrap via rpat so it's evaluated at match time.
    """
    if callable(chars):
        def _deferred():
            return _WrapPat(ctor(_chars(chars)))
        return _C.rpat(_deferred)
    return ctor(_chars(chars))


# ── Multi-way Σ / Π ───────────────────────────────────────────────────────────

class Σ(PATTERN):
    """Concatenation of two or more patterns."""
    __slots__ = ('_c', '_n')
    def __init__(self, *AP):
        if len(AP) < 2:
            raise TypeError('Σ requires at least 2 patterns')
        c = AP[0]._c
        for p in AP[1:]:
            c = _C.concat(c, p._c)
        self._c = c
        self._n = len(AP)
    def __repr__(self): return f'Σ(*{self._n})'

class Π(PATTERN):
    """Alternation of two or more patterns."""
    __slots__ = ('_c', '_n')
    def __init__(self, *AP):
        if len(AP) < 2:
            raise TypeError('Π requires at least 2 patterns')
        c = AP[0]._c
        for p in AP[1:]:
            c = _C.alt(c, p._c)
        self._c = c
        self._n = len(AP)
    def __repr__(self): return f'Π(*{self._n})'


# ── Stage 5 leaf patterns ─────────────────────────────────────────────────────

class ε(PATTERN):
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.epsilon()
    def __repr__(self):     return 'ε()'

class σ(PATTERN):
    __slots__ = ('_c', '_s')
    def __init__(self, s):
        s = s() if callable(s) else str(s)
        self._s = s
        self._c = _C.string(s)
    def __repr__(self):     return f'σ({self._s!r})'

class FAIL(PATTERN):
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.fail()
    def __repr__(self):     return 'FAIL()'

class ABORT(PATTERN):
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.abort()
    def __repr__(self):     return 'ABORT()'

class SUCCEED(PATTERN):
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.succeed()
    def __repr__(self):     return 'SUCCEED()'


# ── Stage 6: anchors ──────────────────────────────────────────────────────────

class α(PATTERN):
    """BOL anchor — matches at position 0 or after \\n."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.alpha()
    def __repr__(self):     return 'α()'

class ω(PATTERN):
    """EOL anchor — matches at end of string or before \\n."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.omega()
    def __repr__(self):     return 'ω()'


# ── Stage 6: structural patterns ─────────────────────────────────────────────

class ARB(PATTERN):
    """Matches any string (shortest first)."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.arb()
    def __repr__(self):     return 'ARB()'

class MARB(ARB):
    """Alias for ARB."""
    pass

class BAL(PATTERN):
    """Matches a balanced parenthesised string."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.bal()
    def __repr__(self):     return 'BAL()'

class REM(PATTERN):
    """Matches the remainder of the subject string."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.rem()
    def __repr__(self):     return 'REM()'

class FENCE(PATTERN):
    """
    FENCE — true SNOBOL4/SPITBOL semantics, both forms:

    FENCE()
        The FENCE variable form.  Matches the empty string and stacks an
        abort node — any subsequent backtrack aborts the entire match.
        Use as a commit point:  P + FENCE() + Q  means "once P matched,
        do not backtrack into P even if Q fails".
        Equivalent to SPITBOL's FENCE pattern variable.

    FENCE(P)
        The FENCE function form.  Wraps P in a protected region: if P
        succeeds, backtracking *into* P is forbidden.  However,
        backtracking *past* this whole FENCE(P) node to try an earlier
        alternative is still allowed.
        Equivalent to SPITBOL's FENCE(P) function.

    Example — optional sign before digits, inside an alternation:
        FENCE(σ('+') | σ('-') | ε()) + SPAN(DIGITS)
        If SPAN fails, backtracking past FENCE(P) to the next | branch
        is allowed because FENCE(P) uses fence_function, not fence_simple.
    """
    __slots__ = ('_c',)
    def __init__(self, P: 'PATTERN | None' = None):
        if P is None:
            self._c = _C.fence()           # fence_simple — abort on backtrack
        else:
            self._c = _C.fence(P._c)       # fence_function — block into-P backtrack only
    def __repr__(self): return 'FENCE()' if True else 'FENCE(P)'


# ── Stage 6: char-class patterns ─────────────────────────────────────────────

class ANY(PATTERN):
    """Matches one character from the given set."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.any, chars)
    def __repr__(self): return f'ANY({self._chars!r})'

class NOTANY(PATTERN):
    """Matches one character NOT in the given set."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.notany, chars)
    def __repr__(self): return f'NOTANY({self._chars!r})'

class SPAN(PATTERN):
    """Matches one or more characters from the given set."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.span, chars)
    def __repr__(self): return f'SPAN({self._chars!r})'

class BREAK(PATTERN):
    """Matches zero or more characters up to (not including) a char in the set."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.brk, chars)
    def __repr__(self): return f'BREAK({self._chars!r})'

class BREAKX(PATTERN):
    """Like BREAK but resumes scanning after the break character on backtrack."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.breakx, chars)
    def __repr__(self): return f'BREAKX({self._chars!r})'

class NSPAN(PATTERN):
    """Matches zero or more characters from the given set (non-backtracking)."""
    __slots__ = ('_c', '_chars')
    def __init__(self, chars):
        self._chars = chars
        self._c = _make_str_pat(_C.nspan, chars)
    def __repr__(self): return f'NSPAN({self._chars!r})'


# ── Stage 6: positional & length patterns ────────────────────────────────────

class POS(PATTERN):
    """Succeeds if cursor is at position n (from left)."""
    __slots__ = ('_c', '_n')
    def __init__(self, n):
        self._n = n
        self._c = _make_int_pat(_C.pos, n)
    def __repr__(self): return f'POS({self._n!r})'

class RPOS(PATTERN):
    """Succeeds if cursor is at position n from the right."""
    __slots__ = ('_c', '_n')
    def __init__(self, n):
        self._n = n
        self._c = _make_int_pat(_C.rpos, n)
    def __repr__(self): return f'RPOS({self._n!r})'

class LEN(PATTERN):
    """Matches exactly n characters."""
    __slots__ = ('_c', '_n')
    def __init__(self, n):
        self._n = n
        self._c = _make_int_pat(_C.length, n)
    def __repr__(self): return f'LEN({self._n!r})'

class TAB(PATTERN):
    """Advances cursor to position n (from left)."""
    __slots__ = ('_c', '_n')
    def __init__(self, n):
        self._n = n
        self._c = _make_int_pat(_C.tab, n)
    def __repr__(self): return f'TAB({self._n!r})'

class RTAB(PATTERN):
    """Advances cursor to position n from the right."""
    __slots__ = ('_c', '_n')
    def __init__(self, n):
        self._n = n
        self._c = _make_int_pat(_C.rtab, n)
    def __repr__(self): return f'RTAB({self._n!r})'


# ── Stage 6: repetition ───────────────────────────────────────────────────────

class ARBNO(PATTERN):
    """Matches zero or more repetitions of P (shortest first)."""
    __slots__ = ('_c',)
    def __init__(self, P: PATTERN):
        self._c = _C.arbno(P._c)
    def __repr__(self): return 'ARBNO(...)'

class MARBNO(ARBNO):
    """Alias for ARBNO."""
    pass


# ── Stage 6: optional (unary ~) ───────────────────────────────────────────────

class π(PATTERN):
    """Optional — P | ε  (also written ~P)."""
    __slots__ = ('_c',)
    def __init__(self, P: PATTERN):
        self._c = _C.alt(P._c, _C.epsilon())
    def __repr__(self): return 'π(...)'


# ── Stage 7: explicit assignment classes ──────────────────────────────────────
# δ / Δ are already the result of P @ name / P % name on PATTERN.
# These classes let user code write δ(P, 'name') directly.

class δ(PATTERN):
    """Immediate assignment — P @ name  (SNOBOL4: P $ N)."""
    __slots__ = ('_c',)
    def __init__(self, P: PATTERN, N):
        self._c = _C.assign_imm(P._c, str(N))
    def __repr__(self): return 'δ(...)'

class Δ(PATTERN):
    """Conditional assignment — P % name  (SNOBOL4: P . N)."""
    __slots__ = ('_c',)
    def __init__(self, P: PATTERN, N):
        self._c = _C.assign_onm(P._c, str(N))
    def __repr__(self): return 'Δ(...)'


# ── Stage 7: cursor assignment ────────────────────────────────────────────────

class Θ(PATTERN):
    """Immediate cursor assignment — records cursor position into globals[N]."""
    __slots__ = ('_c', '_N')
    def __init__(self, N):
        self._N = N
        self._c = _C.setcur_imm(str(N))
    def __repr__(self): return f'Θ({self._N!r})'

class θ(PATTERN):
    """Conditional cursor assignment — records cursor position on match."""
    __slots__ = ('_c', '_N')
    def __init__(self, N):
        self._N = N
        self._c = _C.setcur_onm(str(N))
    def __repr__(self): return f'θ({self._N!r})'


# ── Stage 7: predicate & action ───────────────────────────────────────────────

class Λ(PATTERN):
    """
    Immediate predicate / eval — succeeds if expression/callable is truthy.
    Λ(callable)  → called with no args; truthy return = match continues.
    Λ('expr')    → eval'd in globals dict; truthy result = match continues.
    """
    __slots__ = ('_c', '_expr')
    def __init__(self, expression):
        self._expr = expression
        if callable(expression):
            self._c = _C.pred(expression)
        else:
            # eval the string expression in globals at match time
            self._c = _C.pred(lambda: bool(eval(str(expression), _env._g)))
    def __repr__(self): return f'Λ({self._expr!r})'

class λ(PATTERN):
    """
    Conditional action — fires after a successful complete match.
    λ(callable)  → called with matched substring as argument (or no args — wrapped).
    λ('stmt')    → exec'd in globals dict after match.
    """
    __slots__ = ('_c', '_cmd')
    def __init__(self, command):
        self._cmd = command
        if callable(command):
            import inspect
            try:
                sig = inspect.signature(command)
                params = [p for p in sig.parameters.values()
                          if p.default is inspect.Parameter.empty
                          and p.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                             inspect.Parameter.VAR_KEYWORD)]
                if len(params) == 0:
                    # zero-arg callable: wrap to accept the matched substring arg
                    fn = command
                    command = lambda _matched: fn()
            except (ValueError, TypeError):
                pass
        self._c = _C.call_onm(command)
    def __repr__(self): return f'λ({self._cmd!r})'


# ── Stage 7: deferred pattern reference ──────────────────────────────────────

class ζ(PATTERN):
    """
    Deferred pattern reference — re-evaluated at each match attempt.
    ζ('name')     → looks up name in globals dict at match time.
    ζ(callable)   → calls callable() at match time; must return a PATTERN.
    Both paths use sno4py.rpat(), which calls .compile() on the result.
    """
    __slots__ = ('_c', '_N')
    def __init__(self, N):
        self._N = N
        if isinstance(N, str):
            # rpat_cb looks up the string key in globals and calls .compile()
            self._c = _C.rpat(N)
        elif callable(N):
            # rpat_cb calls N() and then calls .compile() on the result
            self._c = _C.rpat(N)
        else:
            self._c = _C.rpat(str(N))
    def __repr__(self): return f'ζ({self._N!r})'


# ── Stage 7: conjunction ──────────────────────────────────────────────────────

class ρ(PATTERN):
    """
    Conjunction (AND) — P & Q: both P and Q must match the exact same span.

    Implemented via setcur_imm + pred (mini-match both patterns anchored at
    the saved cursor into __subject__) + rpat(LEN(matched_len)).

    Requires GLOBALS() to have been called so __subject__ is available.
    """
    __slots__ = ('_c',)
    def __init__(self, P: PATTERN, Q: PATTERN):
        Pc = P._c
        Qc = Q._c
        pos_key = '__rho_pos__'
        len_key = '__rho_len__'

        def _pred():
            g   = _env._g
            pos = g.get(pos_key, 0)
            s   = g.get('__subject__', '')
            sub = s[pos:]
            rP  = _C.sno_match(sub, Pc, g, 1)
            if rP is None: return False
            rQ  = _C.sno_match(sub, Qc, g, 1)
            if rQ is None: return False
            if rP != rQ: return False
            g[len_key] = rP[1] - rP[0]
            return True

        def _len_pat():
            n = (_env._g or {}).get(len_key, 0)
            class _W:
                def compile(self_): return _C.length(n)
            return _W()

        self._c = _C.concat(
            _C.setcur_imm(pos_key),
            _C.concat(_C.pred(_pred), _C.rpat(_len_pat))
        )

    def __repr__(self): return 'ρ(...)'


# ── Stage 7: regex patterns ───────────────────────────────────────────────────

def _make_regex_pat(rex, immediate: bool) -> '_C.Pattern':
    """
    Build a C pattern for Φ (immediate) or φ (conditional) regex matching.

    Uses setcur_imm → pred (run re.match at saved cursor) → rpat(LEN(n)).
    Named groups are assigned into globals immediately in both modes;
    the immediate/conditional distinction is kept for API symmetry.
    """
    pos_key = '__re_pos__'
    len_key = '__re_len__'

    if isinstance(rex, str):
        compiled_re = _re.compile(rex, _re.MULTILINE)
    else:
        compiled_re = rex   # accept pre-compiled pattern too

    def _pred():
        g   = _env._g
        pos = g.get(pos_key, 0)
        s   = g.get('__subject__', '')
        m   = compiled_re.match(s, pos=pos, endpos=len(s))
        if m is None or m.start() != pos:
            return False
        g[len_key] = m.end() - m.start()
        for name, val in m.groupdict().items():
            if val is not None:
                g[name] = STRING(val)
        return True

    def _len_pat():
        n = (_env._g or {}).get(len_key, 0)
        class _W:
            def compile(self_): return _C.length(n)
        return _W()

    return _C.concat(
        _C.setcur_imm(pos_key),
        _C.concat(_C.pred(_pred), _C.rpat(_len_pat))
    )


class Φ(PATTERN):
    """Regex match with immediate capture of named groups into globals."""
    __slots__ = ('_c', '_rex')
    def __init__(self, rex):
        self._rex = rex
        self._c   = _make_regex_pat(rex, immediate=True)
    def __repr__(self): return f'Φ({self._rex!r})'

class φ(PATTERN):
    """Regex match with conditional capture of named groups into globals."""
    __slots__ = ('_c', '_rex')
    def __init__(self, rex):
        self._rex = rex
        self._c   = _make_regex_pat(rex, immediate=False)
    def __repr__(self): return f'φ({self._rex!r})'


# ── Stage 7: deep-copy helper ─────────────────────────────────────────────────

def Γ(P: PATTERN) -> PATTERN:
    """
    Deep-copy a pattern.  For C-backed patterns the underlying C object is
    immutable and shared safely, so this just returns P unchanged.
    Kept for source-level compatibility with code that uses Γ(P).
    """
    return P


# ── Stage 8: integer counter stack ────────────────────────────────────────────
# istack lives in globals['__vs_istack__'] as a Python list of ints.
# sno4py initialises it to [] at the start of each sno_match call.

class nPush(PATTERN):
    """Push 0 onto the integer counter stack (istack)."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.npush()
    def __repr__(self):     return 'nPush()'

class nInc(PATTERN):
    """Increment the top of the integer counter stack."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.ninc()
    def __repr__(self):     return 'nInc()'

class nPop(PATTERN):
    """Pop the top of the integer counter stack."""
    __slots__ = ('_c',)
    def __init__(self):     self._c = _C.npop()
    def __repr__(self):     return 'nPop()'


# ── Stage 8: parse-tree value stack ───────────────────────────────────────────
# vstack lives in globals['__vs_vstack__'] as a Python list of lists.

class Shift(PATTERN):
    """
    Push a node onto the parse-tree value stack (vstack).

    Shift(tag)        → push [tag]
    Shift(tag, var)   → push [tag, eval(var, globals)]
                        var may be a plain name ('x') or an expression ('int(x)').

    The expression is evaluated on-match (deferred), after all % assignments
    have fired, so it can reference variables bound by P % 'name' patterns.
    """
    __slots__ = ('_c', '_t', '_v')
    def __init__(self, t=None, v=None):
        self._t = t
        self._v = v
        if t is None:
            self._c = _C.shift()
        elif v is None:
            self._c = _C.shift(str(t))
        else:
            # We need to eval(v, globals) on-match, AFTER any P%'name' callbacks
            # have fired. We do this via call_onm (fires on-match in order):
            #   1. call_onm  → eval expression → store result in _eval_key
            #   2. shift     → push [tag, globals[_eval_key]]  (also on-match)
            vstr = str(v)
            _eval_key = f'__shiftval_{id(self) & 0xFFFFFFFF:08x}__'

            def _eval_v(_matched):
                g = _env._g
                try:
                    g[_eval_key] = eval(vstr, g)
                except Exception:
                    # Fall back to plain globals lookup
                    g[_eval_key] = g.get(vstr, vstr)

            self._c = _C.concat(
                _C.call_onm(_eval_v),
                _C.shift(str(t), _eval_key)
            )
    def __repr__(self): return f'Shift({self._t!r}, {self._v!r})'

class Reduce(PATTERN):
    """
    Pop n nodes from vstack, wrap as [tag, *children], push back.

    Reduce(tag)       → n taken from top of istack  (n=-1)
    Reduce(tag, n)    → n is explicit integer
    Reduce(tag, -2)   → n taken from second-from-top of istack

    Special: Reduce('Σ', 0) pushes ['ε'] (transparent empty concat).
    Single-child transparent tags (Σ, Π, ρ, …) are passed through unchanged.
    """
    __slots__ = ('_c', '_t', '_x')
    def __init__(self, t, x=-1):
        self._t = t
        self._x = x
        tag = t() if callable(t) else str(t)
        if x == -1:
            self._c = _C.reduce(tag)
        elif x == -2:
            self._c = _C.reduce(tag, -2)
        else:
            self._c = _C.reduce(tag, int(x))
    def __repr__(self): return f'Reduce({self._t!r}, {self._x!r})'

class Pop(PATTERN):
    """
    Pop the top of the parse-tree value stack into globals[key].

    Pop('result')  → globals['result'] = vstack.pop()
    """
    __slots__ = ('_c', '_v')
    def __init__(self, v):
        self._v = v
        self._c = _C.pop(str(v))
    def __repr__(self): return f'Pop({self._v!r})'


# ── Match API ─────────────────────────────────────────────────────────────────

def GLOBALS(g: dict):
    """Register the caller's variable dict as the SNOBOL environment."""
    _env.set(g)

def TRACE(level=None, window=None):
    pass   # tracing handled by sno4py internals; kept for API compatibility

def SEARCH(S, P: PATTERN, exc=False):
    """Search S for P → slice or None.  Raises F if exc=True and no match."""
    g = _env._g
    if g is None:
        raise RuntimeError(
            "GLOBALS(globals()) has not been called.  "
            "Call GLOBALS(globals()) once after importing SNOBOL4python."
        )
    if 'STRING' not in g:
        g['STRING'] = STRING
    s = str(S)
    g['__subject__'] = s          # needed by ρ, Φ, φ at match time
    result = _C.sno_match(s, P._c, g)
    if result is None:
        if exc:
            raise F('FAIL')
        return None
    return slice(result[0], result[1])

def MATCH(S, P: PATTERN, exc=False) -> slice:
    """Anchored at start: POS(0) + P."""
    return SEARCH(S, POS(0) + P, exc)

def FULLMATCH(S, P: PATTERN, exc=False) -> slice:
    """Full string match: POS(0) + P + RPOS(0)."""
    return SEARCH(S, POS(0) + P + RPOS(0), exc)

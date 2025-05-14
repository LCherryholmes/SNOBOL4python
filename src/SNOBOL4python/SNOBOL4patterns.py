# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python -m pip install build
#> python -m pip install twine
#> python -m pip install --upgrade pip
#> python -m pip install --upgrade setuptools wheel build
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> cythonize src/SNOBOL4python/SNOBOL4patterns.pyx
#> python setup.py build_ext --inplace
#> python -m build
#> python -m pip install ./dist/snobol4python-0.4.6.tar.gz
#> python -m pip install ./dist/snobol4python-0.4.6-py3-none-any.whl
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#> python ENG-685/transl8r_pop3.py > ENG-685/pop3.py
#> python -m pip install --index-url https://test.pypi.org/simple SNOBOL4python
#> python -m twine check ./dist/*
#> python -m twine upload ./dist/*
#----------------------------------------------------------------------------------------------------------------------
import re
import copy
import logging
from pprint import pprint, pformat
#----------------------------------------------------------------------------------------------------------------------
class F(Exception): pass
def Γ(P): return copy.deepcopy(P)
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
    def __init__(self):             pass
    def __invert__(self):           return pi(self) # pi, unary '~', optional, zero or one
    def __add__(self, other):       # SIGMA, binary +, subsequent -----------------------------------------------------
                                    if not isinstance(other, PATTERN):  other = sigma(str(other))
                                    if isinstance(self, SIGMA):         return SIGMA(*self.AP, other)
                                    else:                               return SIGMA(self, other)
    def __or__(self, other):        # PI, binary |, alternate ---------------------------------------------------------
                                    if not isinstance(other, PATTERN):  other = sigma(str(other))
                                    if isinstance(self, PI):            return PI(*self.AP, other)
                                    else:                               return PI(self, other)
    def __and__(self, other):       # rho, binary &, conjunction ------------------------------------------------------
                                    if not isinstance(other, PATTERN):  other = sigma(str(other))
                                    if isinstance(self, rho):           return rho(*self.AP, other)
                                    else:                               return rho(self, other)
    def __deepcopy__(self, memo):   return type(self)() # -------------------------------------------------------------
    def __matmul__(self, other):    return delta(self, other) # delta, binary @, immediate assignment
    def __mod__(self, other):       return DELTA(self, other) # DELTA, binary %, conditional assignment
    def __eq__(self, other):        return SEARCH(other, self, exc=True) # equal == operator, returns slice
    def __contains__(self, other):  return SEARCH(other, self, exc=False) # comparison in operator, returns bool
#----------------------------------------------------------------------------------------------------------------------
class STRING(str):
    def __repr__(self):             return str.__repr__(self)
    def __add__(self, other):       # SIGMA
                                    if isinstance(other, SIGMA):        return SIGMA(sigma(self), *other.AP)
                                    elif isinstance(other, PATTERN):    return SIGMA(sigma(self), other)
                                    else:                               return STRING(super().__add__(str(other)))
    def __radd__(self, other):      # SIGMA
                                    if isinstance(other, SIGMA):        return SIGMA(*other.AP, sigma(self))
                                    elif isinstance(other, PATTERN):    return SIGMA(other, sigma(self))
                                    else:                               return STRING(str(other).__add__(self))
    def __or__(self, other):        # PI
                                    if isinstance(other, PI):           return PI(sigma(self), *other.AP)
                                    else:                               return PI(sigma(self), other)
    def __xor__(self, other):       # PI
                                    if isinstance(other, PI):           return PI(*other.AP, sigma(self))
                                    else:                               return PI(other, sigma(self))
    def __contains__(self, other):  # in operator
                                    if isinstance(other, PATTERN):      return other.__contains__(self)
                                    else:                               return super().__contains__(str(other))
#----------------------------------------------------------------------------------------------------------------------
globals()['NULL'] = STRING('')
#----------------------------------------------------------------------------------------------------------------------
class epsilon(PATTERN): # epsilon, null string, zero-length string
    def __init__(self): super().__init__()
    def __repr__(self): return "epsilon()"
    def gamma(self): global Ϣ; yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class FAIL(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "FAIL()"
    def gamma(self): return
#----------------------------------------------------------------------------------------------------------------------
class ABORT(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "ABORT()"
    def gamma(self): raise F("ABORT()")
#----------------------------------------------------------------------------------------------------------------------
class SUCCESS(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "SUCCESS()"
    def gamma(self):
        global Ϣ
        while True:
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class alpha(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "alpha()"
    def gamma(self):
        global Ϣ
        if  (Ϣ[-1].pos == 0) or \
            (Ϣ[-1].pos > 0 and Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos] == '\n'):
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class omega(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "omega()"
    def gamma(self):
        global Ϣ
        if  (Ϣ[-1].pos == len(Ϣ[-1].subject)) or \
            (Ϣ[-1].pos < len(Ϣ[-1].subject) and Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + 1] == '\n'):
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class REM(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "REM()"
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        Ϣ[-1].pos = len(Ϣ[-1].subject)
        yield slice(pos0, Ϣ[-1].pos)
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class ARB(PATTERN): # ARB
    def __init__(self): super().__init__()
    def __repr__(self): return "ARB()"
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        while Ϣ[-1].pos <= len(Ϣ[-1].subject):
            yield slice(pos0, Ϣ[-1].pos)
            Ϣ[-1].pos += 1
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class MARB(ARB): pass
#----------------------------------------------------------------------------------------------------------------------
class zeta(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __repr__(self): return f"zeta({pformat(self.N)})"
    def __deepcopy__(self, memo): return zeta(self.N)
    def gamma(self):
        P = self.N
        if not isinstance(P, str):
            if callable(P): P = P()
            else: P = _globals[str(P)]
        else: P = _globals[P]
        yield from P.gamma()
#----------------------------------------------------------------------------------------------------------------------
class nPush(PATTERN):
    def __init__(self): super().__init__()
    def __repr__(self): return "nPush()"
    def gamma(self):
        global Ϣ
        logger.info("nPush() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop += 1")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.append(0)")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nPush() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nInc(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "nInc()"
    def gamma(self):
        global Ϣ
        logger.info("nInc() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack[Ϣ[-1].itop] += 1")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nInc() backtracking...")
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nPop(PATTERN):
    def __init__(self): super().__init__();
    def __repr__(self): return "nPop()"
    def gamma(self):
        global Ϣ
        logger.info("nPop() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.pop()")
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop -= 1")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("nPop() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Shift(PATTERN):
    def __init__(self, t=None, v=None): super().__init__(); self.t = t; self.v = v
    def __repr__(self): return f"Shift({pformat(self.t)}, {pformat(self.v)})"
    def __deepcopy__(self, memo): return Shift(self.t, self.v)
    def gamma(self):
        global Ϣ
        logger.info("Shift(%r, %r) SUCCESS", self.t, self.v)
        if self.t is None:   Ϣ[-1].cstack.append(f"Ϣ[-1].shift()")
        elif self.v is None: Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}')")
        else:                Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}', {self.v})")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Shift(%r, %r) backtracking...", self.t, self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Reduce(PATTERN):
    def __init__(self, t, n=-1): super().__init__(); self.t = t; self.n = n
    def __repr__(self): return f"Reduce({pformat(self.t)}, {pformat(self.n)})"
    def __deepcopy__(self, memo): return Reduce(self.t, self.n)
    def gamma(self):
        global Ϣ; n = self.n; t = self.t
        if callable(t): t = t()
        else: t = t
        logger.info("Reduce(%r, %r) SUCCESS", t, n)
        if   n == -2: n = "Ϣ[-1].istack[Ϣ[-1].itop + 1]"
        elif n == -1: n = "Ϣ[-1].istack[Ϣ[-1].itop]"
        Ϣ[-1].cstack.append(f"Ϣ[-1].reduce('{t}', {n})")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Reduce(%r, %r) backtracking...", t, n)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Pop(PATTERN):
    def __init__(self, v): super().__init__(); self.v = v
    def __repr__(self): return f"Pop({pformat(self.v)})"
    def __deepcopy__(self, memo): return Pop(self.v)
    def gamma(self):
        global Ϣ
        logger.info("Pop(%s) SUCCESS", self.v)
        Ϣ[-1].cstack.append(f"{self.v} = Ϣ[-1].pop()")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("Pop(%s) backtracking...", self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class BAL(PATTERN): # BAL
    def __init__(self): super().__init__()
    def __repr__(self): return "BAL()"
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos; nest = 0
        Ϣ[-1].pos += 1
        while Ϣ[-1].pos <= len(Ϣ[-1].subject):
            ch = Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos]
            if ch == '(': nest += 1
            elif ch == ')': nest -= 1
            if nest < 0: break
            elif nest > 0 and Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            elif nest == 0: yield slice(pos0, Ϣ[-1].pos)
            Ϣ[-1].pos += 1
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class FENCE(PATTERN): # FENCE and FENCE(P)
    def __init__(self, P:PATTERN=None): super().__init__(); self.P:PATTERN = P
    def __repr__(self): return f"FENCE({pformat(self.P)})"
    def __deepcopy__(self, memo): return FENCE(copy.deepcopy(self.P))
    def gamma(self):
        global Ϣ
        if self.P:
            logger.info("FENCE(%s) SUCCESS", pformat(self.P))
            yield from self.P.gamma()
            logger.warning("FENCE(%s) backtracking...", pformat(self.P))
        else:
            logger.info("FENCE() SUCCESS")
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("FENCE() backtracking...")
#----------------------------------------------------------------------------------------------------------------------
class POS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"POS({pformat(self.n)})"
    def __deepcopy__(self, memo): return POS(self.n)
    def gamma(self):
        global Ϣ
        n = self.n
        if not isinstance(n, int):
            if callable(n): n = int(n())
            else: n = int(n)
        if Ϣ[-1].pos == n:
            logger.info("POS(%d) SUCCESS(%d,%d)=", n, Ϣ[-1].pos, 0)
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("POS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
class RPOS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"RPOS({pformat(self.n)})"
    def __deepcopy__(self, memo): return RPOS(self.n)
    def gamma(self):
        global Ϣ
        n = self.n
        if not isinstance(n, int):
            if callable(n): n = int(n())
            else: n = int(n)
        if Ϣ[-1].pos == len(Ϣ[-1].subject) - n:
            logger.info("RPOS(%d) SUCCESS(%d,%d)=", n, Ϣ[-1].pos, 0)
            yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
            logger.warning("RPOS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
class LEN(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"LEN({pformat(self.n)})"
    def __deepcopy__(self, memo): return LEN(self.n)
    def gamma(self):
        global Ϣ
        n = self.n
        if not isinstance(n, int):
            if callable(n): n = int(n())
            else: n = int(n)
        if Ϣ[-1].pos + n <= len(Ϣ[-1].subject):
            logger.info("LEN(%d) SUCCESS(%d,%d)=%s", n, Ϣ[-1].pos, n, Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + n])
            Ϣ[-1].pos += n
            yield slice(Ϣ[-1].pos - n, Ϣ[-1].pos)
            Ϣ[-1].pos -= n
            logger.warning("LEN(%d) backtracking(%d)...", n, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class TAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"TAB({pformat(self.n)})"
    def __deepcopy__(self, memo): return TAB(self.n)
    def gamma(self):
        global Ϣ
        n = self.n
        if not isinstance(n, int):
            if callable(n): n = int(n())
            else: n = int(n)
        if n <= len(Ϣ[-1].subject):
            if n >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = n
                yield slice(pos0, n)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class RTAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __repr__(self): return f"RTAB({pformat(self.n)})"
    def __deepcopy__(self, memo): return RTAB(self.n)
    def gamma(self):
        global Ϣ
        n = self.n
        if not isinstance(n, int):
            if callable(n): n = int(n())
            else: n = int(n)
        if n <= len(Ϣ[-1].subject):
            n = len(Ϣ[-1].subject) - n
            if n >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = n
                yield slice(pos0, n)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class sigma(PATTERN): # sigma, sigma, sequence of characters, string patttern
    def __init__(self, s): super().__init__(); self.s = s
    def __repr__(self): return f"sigma({pformat(self.s)})"
    def __deepcopy__(self, memo): return sigma(self.s)
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        s = self.s
        if not isinstance(s, str):
            if callable(s): s = str(s())
            else: s = str(s) # might need to raise an exception
        logger.debug("sigma(%r) trying(%d)", s, pos0)
        if pos0 + len(s) <= len(Ϣ[-1].subject):
            if s == Ϣ[-1].subject[pos0:pos0 + len(s)]:
                logger.info("sigma(%r) SUCCESS(%d,%d)=", s, Ϣ[-1].pos, len(s))
                Ϣ[-1].pos += len(s)
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("sigma(%r) backtracking(%d,%d)...", s, pos0, Ϣ[-1].pos)
                Ϣ[-1].pos = pos0
        return None
#----------------------------------------------------------------------------------------------------------------------
class ANY(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"ANY({pformat(self.chars)})"
    def __deepcopy__(self, memo): return ANY(self.chars)
    def gamma(self):
        global Ϣ
        chars = self.chars
        if not isinstance(chars, str):
            if not isinstance(chars, set):
                if callable(chars):
                    chars = chars()
                else: chars = str(chars)
        logger.debug("ANY(%r) trying(%d)", chars, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if Ϣ[-1].subject[Ϣ[-1].pos] in chars:
                logger.info("ANY(%r) SUCCESS(%d,%d)=%s", chars, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield slice(Ϣ[-1].pos - 1, Ϣ[-1].pos)
                logger.warning("ANY(%r) backtracking(%d,%d)...", chars, Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
#----------------------------------------------------------------------------------------------------------------------
class NOTANY(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"NOTANY({pformat(self.chars)})"
    def __deepcopy__(self, memo): return NOTANY(self.chars)
    def gamma(self):
        global Ϣ
        chars = self.chars
        if not isinstance(chars, str):
            if not isinstance(chars, set):
                if callable(chars):
                    chars = chars()
                else: chars = str(chars)
        logger.debug("NOTANY(%r) trying(%d)", chars, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if not Ϣ[-1].subject[Ϣ[-1].pos] in chars:
                logger.info("NOTANY(%r) SUCCESS(%d,%d)=%s", chars, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield slice(Ϣ[-1].pos - 1, Ϣ[-1].pos)
                logger.warning("NOTANY(%r) backtracking(%d,%d)...", chars, Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
#----------------------------------------------------------------------------------------------------------------------
class SPAN(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"SPAN({pformat(self.chars)})"
    def __deepcopy__(self, memo): return SPAN(self.chars)
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        chars = self.chars
        if not isinstance(chars, str):
            if not isinstance(chars, set):
                if callable(chars):
                    chars = chars()
                else: chars = str(chars)
        logger.debug("SPAN(%r) trying(%d)", chars, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if Ϣ[-1].subject[Ϣ[-1].pos] in chars:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos > pos0:
            logger.info("SPAN(%r) SUCCESS(%d,%d)=%s", chars, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield slice(pos0, Ϣ[-1].pos)
            logger.warning("SPAN(%r) backtracking(%d,%d)...", chars, pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
        return None
#----------------------------------------------------------------------------------------------------------------------
class BREAK(PATTERN):
    def __init__(self, chars): super().__init__(); self.chars = chars
    def __repr__(self): return f"BREAK({pformat(self.chars)})"
    def __deepcopy__(self, memo): return BREAK(self.chars)
    def gamma(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        chars = self.chars
        if not isinstance(chars, str):
            if not isinstance(chars, set):
                if callable(chars):
                    chars = chars()
                else: chars = str(chars)
        logger.debug("BREAK(%r) SUCCESS(%d)", chars, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if not Ϣ[-1].subject[Ϣ[-1].pos] in chars:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            logger.info("BREAK(%r) SUCCESS(%d,%d)=%s", chars, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield slice(pos0, Ϣ[-1].pos)
            logger.warning("BREAK(%r) backtracking(%d,%d)...", chars, pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class BREAKX(BREAK): pass
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
class THETA(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __repr__(self): return f"THETA({pformat(self.N)})"
    def __deepcopy__(self, memo): return THETA(self.N)
    def gamma(self):
        global Ϣ, _globals
        N = str(self.N)
        if N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·');
        logger.info("THETA(%s) SUCCESS", N)
        _globals[N] = Ϣ[-1].pos
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("THETA(%s) backtracking...", N)
#----------------------------------------------------------------------------------------------------------------------
# Conditional cursor assignment (after successful complete pattern match)
class theta(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __repr__(self): return f"theta({pformat(self.N)})"
    def __deepcopy__(self, memo): return theta(self.N)
    def gamma(self):
        global Ϣ
        N = str(self.N)
        if N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·')
        logger.info("theta(%s) SUCCESS", N)
        Ϣ[-1].cstack.append(f"{N} = {Ϣ[-1].pos}")
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        logger.warning("theta(%s) backtracking...", N)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
class delta(PATTERN): # delta, binary '@', SNOBOL4: P $ N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __repr__(self): return f"delta({pformat(self.P)}, {pformat(self.N)})"
    def __deepcopy__(self, memo): return delta(copy.deepcopy(self.P), self.N)
    def gamma(self):
        global _globals; N = str(self.N)
        logger.debug("delta(%s, %s)", pformat(self.P), N)
        for _1 in self.P.gamma():
            assert _1 != ""
            v = Ϣ[-1].subject[_1]
            if N == "OUTPUT":
                Ϣ[-1].nl = True
                print(v, end='·')
            logger.debug("%s = delta(%r)", N, v)
            _globals[N] = STRING(v)
            yield _1
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
class DELTA(PATTERN): # DELTA, binary '%', SNOBOL4: P . N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __repr__(self): return f"DELTA({pformat(self.P)}, {pformat(self.N)})"
    def __deepcopy__(self, memo): return DELTA(copy.deepcopy(self.P), self.N)
    def gamma(self):
        global Ϣ; N = str(self.N)
        logger.debug("DELTA(%s, %s)", pformat(self.P), N)
        for _1 in self.P.gamma():
            assert _1 != ""
            logger.info("%s = DELTA(%r) SUCCESS", N, _1)
            if N == "OUTPUT":
                Ϣ[-1].cstack.append(f"print(Ϣ[-1].subject[{_1.start}:{_1.stop}])")
            else: Ϣ[-1].cstack.append(f"{N} = STRING(Ϣ[-1].subject[{_1.start}:{_1.stop}])")
            yield _1
            logger.warning("%s = DELTA(%r) backtracking...", N, _1)
            Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
class LLAMBDA(PATTERN): # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    def __init__(self, expression): super().__init__(); self.expression = expression
    def __repr__(self): return f"LLAMBDA({pformat(self.expression)})"
    def __deepcopy__(self, memo): return LLAMBDA(self.expression)
    def gamma(self):
        global Ϣ, _globals
        if isinstance(self.expression, str):
            logger.debug("LLAMBDA(%r) evaluating...", self.expression)
            try:
                if eval(self.expression, _globals):
                    logger.info("LLAMBDA(%r) SUCCESS", self.expression)
                    yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                    logger.warning("LLAMBDA(%r) backtracking...", self.expression)
                else: logger.warning("LLAMBDA(%r) FAIL!", self.expression)
            except Exception as e:
                logger.error("LLAMBDA(%r) EXCEPTION evaluating. (%r) FAIL!", self.expression, e)
        elif callable(self.expression):
            logger.debug("LLAMBDA(function) evaluating...")
            try:
                if self.expression():
                    logger.info("LLAMBDA(function) SUCCESS")
                    yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                    logger.warning("LLAMBDA(function) backtracking...")
                else: logger.warning("LLAMBDA(function) FAIL!")
            except Exception as e:
                logger.error("LLAMBDA(function) EXCEPTION evaluating. (%r) FAIL!", e)
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
class llambda(PATTERN): # LLAMBDA, P . *exec(), P . tx . *func(tx)
    def __init__(self, command): super().__init__(); self.command = command
    def __repr__(self): return f"llambda({pformat(self.command)})"
    def __deepcopy__(self, memo): return llambda(self.command)
    def gamma(self):
        global Ϣ
        logger.debug("llambda(%r) compiling...", self.command)
        if self.command:
            if isinstance(self.command, str):
                if compile(self.command, '<string>', 'exec'): # 'single', 'eval'
                    logger.info("llambda(%r) SUCCESS", self.command)
                    Ϣ[-1].cstack.append(self.command)
                    yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                    logger.warning("llambda(%r) backtracking...", self.command)
                    Ϣ[-1].cstack.pop()
                else: logger.error("llambda(%r) Error compiling. FAIL", self.command)
            elif callable(self.command):
                logger.info("llambda(function) SUCCESS")
                Ϣ[-1].cstack.append(self.command)
                yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
                logger.warning("llambda(function) backtracking...")
                Ϣ[-1].cstack.pop()
        else: yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching (with immediate assignments)
_rexs = dict()
class PHI(PATTERN):
    def __init__(self, rex): super().__init__(); self.rex = rex
    def __repr__(self): return f"PHI({pformat(self.rex)})"
    def __deepcopy__(self, memo): return PHI(self.rex)
    def gamma(self):
        global Ϣ, _rexs
        rex = self.rex
        if not isinstance(rex, str):
            if callable(rex): rex = str(rex())
            else: rex = str(rex) # should possibly be exception
        if rex not in _rexs:
            _rexs[rex] = re.compile(rex, re.MULTILINE)
        if matches := _rexs[rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
            pos0 = Ϣ[-1].pos
            if pos0 == matches.start():
                Ϣ[-1].pos = matches.end()
                for (N, V) in matches.groupdict().items():
                    _globals[N] = STRING(V)
                yield slice(pos0, Ϣ[-1].pos)
                Ϣ[-1].pos = pos0
            else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching (with conditional assignments)
class phi(PATTERN):
    def __init__(self, rex): super().__init__(); self.rex = rex
    def __repr__(self): return f"phi({pformat(self.rex)})"
    def __deepcopy__(self, memo): return phi(self.rex)
    def gamma(self):
        global Ϣ, _rexs
        rex = self.rex
        if not isinstance(rex, str):
            if callable(rex): rex = str(rex())
            else: rex = str(rex) # should possibly be exception
        if rex not in _rexs:
            _rexs[rex] = re.compile(rex, re.MULTILINE)
        if matches := _rexs[rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
            pos0 = Ϣ[-1].pos
            if pos0 == matches.start():
                Ϣ[-1].pos = matches.end()
                push_count = 0
                for item in matches.re.groupindex.items():
                    N = item[0]
                    span = matches.span(item[1])
                    if span != (-1, -1):
                        push_count += 1
                        Ϣ[-1].cstack.append(f"{N} = STRING(Ϣ[-1].subject[{span[0]}:{span[1]}])")
                yield slice(pos0, Ϣ[-1].pos)
                for i in range(push_count):
                    Ϣ[-1].cstack.pop()
                Ϣ[-1].pos = pos0
            else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
class rho(PATTERN): # rho, AND, conjunction
    def __init__(self, P:PATTERN, Q:PATTERN): super().__init__(); self.P = P; self.Q = Q
    def __repr__(self): return  "rho(*{0})".format(2)
    def __deepcopy__(self, memo): return rho(copy.deepcopy(self.P), copy.deepcopy(self.Q))
    def gamma(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        for _1 in self.P.gamma():
            pos1 = Ϣ[-1].pos
            try:
                Ϣ[-1].pos = pos0
                next(self.Q.gamma())
                if (Ϣ[-1].pos == pos1):
                    yield _1
                    Ϣ[-1].pos = pos0
            except StopIteration:
                Ϣ[-1].pos = pos0
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class pi(PATTERN): # pi, pi, optional, SNOBOL4: P | epsilon
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __repr__(self): return f"pi({pformat(self.P)})"
    def __deepcopy__(self, memo): return pi(copy.deepcopy(self.P))
    def gamma(self):
        global Ϣ
        Ϣ[-1].depth += 1
        yield from self.P.gamma()
        yield slice(Ϣ[-1].pos, Ϣ[-1].pos)
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class PI(PATTERN): # PI, PI, possibilities, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __repr__(self): return  "PI(*{0})".format(len(self.AP))
    def __deepcopy__(self, memo): return PI(*(copy.deepcopy(P) for P in self.AP))
    def gamma(self):
        global Ϣ
        logger.debug("PI(%s) trying(%d)...", " ".join([pformat(P) for P in self.AP]), Ϣ[-1].pos)
        Ϣ[-1].depth += 1
        for P in self.AP: yield from P.gamma()
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class SIGMA(PATTERN): # SIGMA, SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __repr__(self): return "SIGMA(*{0})".format(len(self.AP))
    def __deepcopy__(self, memo): return SIGMA(*(copy.deepcopy(P) for P in self.AP))
    def gamma(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        Ag = [None] * len(self.AP)
        logger.debug("SIGMA(%s) trying(%d)...", " ".join([pformat(P) for P in self.AP]), pos0)
        cursor = 0
        while cursor >= 0:
            if cursor >= len(self.AP):
                logger.info("SIGMA(*) SUCCESS(%d,%d)=%s", pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("SIGMA(*) backtracking(%d,%d)...", pos0, Ϣ[-1].pos)
                cursor -= 1
            if Ag[cursor] is None:
                Ag[cursor] = self.AP[cursor].gamma()
            try:
                next(Ag[cursor])
                cursor += 1
            except StopIteration:
                Ag[cursor] = None
                cursor -= 1
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class ARBNO(PATTERN):
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __repr__(self): return "ARBNO({0})".format(pformat(self.P))
    def __deepcopy__(self, memo): return ARBNO(copy.deepcopy(self.P))
    def gamma(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        logger.debug("ARBNO(%s) trying(%d)...", pformat(self.P), pos0)
        cursor = 0
        Ag = []
        while cursor >= 0:
            if cursor >= len(Ag):
                logger.info("ARBNO(%s) SUCCESS(%d,%d)=%s", pformat(self.P), pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield slice(pos0, Ϣ[-1].pos)
                logger.warning("ARBNO(%s) backtracking(%d)...", pformat(self.P), pos0)
            if cursor >= len(Ag):
                Ag.append(self.P.gamma())
            try:
                next(Ag[cursor])
                cursor += 1
            except StopIteration:
                cursor -= 1
                Ag.pop()
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class MARBNO(ARBNO): pass
#----------------------------------------------------------------------------------------------------------------------
def _push(lyst): Ϣ[-1].vstack.append(lyst)
def _pop(): return Ϣ[-1].vstack.pop()
def _shift(t='', v=None):
    if v is None:
        _push([t])
    else: _push([t, v])
def _reduce(t, n):
    if n == 0 and t == 'SIGMA':
        _push(['epsilon'])
    elif n != 1 or t not in ('SIGMA', 'PI', 'rho', 'snoExprList', '|', '..'):
        x = [t]
        for i in range(n):
            x.insert(1, _pop())
        _push(x)
#----------------------------------------------------------------------------------------------------------------------
class DEBUG_formatter(logging.Formatter):
    def window(self, size):
        global Ϣ
        if len(Ϣ) > 0:
            left  = Ϣ[-1].subject[max(0, Ϣ[-1].pos - size) : Ϣ[-1].pos]
            right = Ϣ[-1].subject[Ϣ[-1].pos : min(Ϣ[-1].pos + size, len(Ϣ[-1].subject))]
            pad_left  = ' ' * max(0, size - len(left))
            pad_right = ' ' * max(0, size - len(right))
            return f"{pformat(pad_left+left)}|{Ϣ[-1].pos:4d}|{pformat(right+pad_right)}"
        else: return " " * (6 + 2 * size)
    def format(self, record):
        global Ϣ, _window_size
        original_message = super().format(record)
        if len(Ϣ) > 0:
            formatted_message = "{0:s} {1:s}".format(self.window(_window_size // 2), original_message) # {2:s} # '  ' * Ϣ[-1].depth,
        else: formatted_message = original_message
        return formatted_message
#----------------------------------------------------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.handlers.clear()
logger.propagate = False
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
handler.setFormatter(DEBUG_formatter("%(message)s"))
logger.addHandler(handler)
#----------------------------------------------------------------------------------------------------------------------
class SNOBOL:
    __slots__ = ['pos', 'subject', 'depth', 'cstack', 'itop', 'istack', 'vstack', 'nl' , 'shift', 'reduce', 'pop']
    def __repr__(self): return f"('SNOBOL', {self.depth}, {self.pos}, {len(self.subject)}, {pformat(self.subject)}, {pformat(self.cstack)})"
    def __init__(self, pos:int, subject:str):
        self.pos:int        = pos
        self.subject:str    = subject
        self.depth:int      = 0
        self.cstack:list    = []
        self.itop:int       = -1
        self.istack:list    = []
        self.vstack:list    = []
        self.nl:bool        = False
        self.shift          = _shift
        self.reduce         = _reduce
        self.pop            = _pop
#----------------------------------------------------------------------------------------------------------------------
Ϣ = [] # SNOBOL stack
_globals = None # global variables
_window_size = 24 # size of sliding window display for tracing
#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import GLOBALS as F_GLOBALS
else: from .SNOBOL4functions import GLOBALS as F_GLOBALS
def GLOBALS(g:dict): F_GLOBALS(g); global _globals; _globals = g
#----------------------------------------------------------------------------------------------------------------------
def TRACE(level:int=None, window:int=None):
    global _window_size, logger, handler
    if window is not None:
        _window_size = window
    if level is not None:
        logger.setLevel(level)
        handler.setLevel(level)
#----------------------------------------------------------------------------------------------------------------------
def MATCH     (S, P:PATTERN, exc=False) -> slice: return SEARCH(S, POS(0) + P, exc)
def FULLMATCH (S, P:PATTERN, exc=False) -> slice: return SEARCH(S, POS(0) + P + RPOS(0), exc)
def SEARCH    (S, P:PATTERN, exc=False) -> slice:
    global _globals, Ϣ; S = str(S)
    if _globals is None:
        _globals = globals()
    slyce = None
    command = None
    Ϣ.append(None)
    for cursor in range(0, 1+len(S)):
        try:
            Ϣ[-1] = SNOBOL(cursor, S)
            slyce = next(P.gamma())
            if Ϣ[-1].nl: print()
            logger.info(f'SEARCH(): "{S}" ? "{slyce}"')
            for command in Ϣ[-1].cstack:
                logger.debug('SEARCH(): %r', command)
            try:
                _globals['Ϣ'] = Ϣ
                _globals['STRING'] = STRING
                for command in Ϣ[-1].cstack:
                    if isinstance(command, str): exec(command, _globals)
                    elif callable(command): command()
            except Exception as e:
                logger.error("SEARCH(): Exception: %r, command: %r", e, command)
            break
        except StopIteration:
            if Ϣ[-1].nl: print()
        except F as e:
            if Ϣ[-1].nl: print()
            logger.error("SEARCH(): FAILURE: %r", e)
            Ϣ.pop()
            raise
        except Exception as e:
            if Ϣ[-1].nl: print()
            logger.critical("SEARCH(): Exception: %r", e)
            Ϣ.pop()
            raise
    Ϣ.pop()
    if exc == True and not slyce: raise F("FAIL")
    return slyce
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import ALPHABET, DIGITS, UCASE, LCASE
    from SNOBOL4functions import DEFINE, REPLACE, SUBSTITUTE
    from SNOBOL4functions import END, RETURN, FRETURN, NRETURN
    GLOBALS(globals())
    TRACE(40)
#   --------------------------------------------------------------------------------------------------------------------
    S = None
    N = None
    V = ANY(LCASE) % "N"      + llambda(lambda: S.append(int(globals()[N])))
    I = SPAN(DIGITS) % "N"    + llambda(lambda: S.append(int(N)))
    E = ( V | I | sigma('(') + zeta("X") + sigma(')'))
    X = ( E + sigma('+') + zeta("X") + llambda(lambda: S.append(S.pop() + S.pop()))
        | E + sigma('-') + zeta("X") + llambda(lambda: S.append(S.pop() - S.pop()))
        | E + sigma('*') + zeta("X") + llambda(lambda: S.append(S.pop() * S.pop()))
        | E + sigma('/') + zeta("X") + llambda(lambda: S.append(S.pop() // S.pop()))
        | sigma('+') + zeta("X")
        | sigma('-') + zeta("X")     + llambda(lambda: S.append(-S.pop()))
        | E
        )
    C = POS(0) + llambda("S = []") + X + llambda(lambda: print(S.pop())) + RPOS(0)
    x = 1; y = 2; z = 3
    for s in ["x+y*z", "x+(y*z)", "(x+y)*z"]:
        if not s in C:
            print("Boo!")
    exit(0)
#   --------------------------------------------------------------------------------------------------------------------
    name = None
    if "SNOBOL4" in POS(0) + (SPAN("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + sigma('4')) % "name" + RPOS(0):
        print(name)
    if "SNOBOL4" in POS(0) + (BREAK("0123456789") + sigma('4')) % "name" + RPOS(0):
        print(name)
    if "001_01C717AB.5C51AFDE ..." in phi(r"(?P<name>[0-9]{3}(_[0-9A-F]{4})?_[0-9A-F]{8}\.[0-9A-F]{8})"):
        print(name)
#   --------------------------------------------------------------------------------------------------------------------
    exit(0)
#-----------------------------------------------------------------------------------------------------------------------

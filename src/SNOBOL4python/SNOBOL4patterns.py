# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python -m pip install --upgrade pip
#> python -m pip install build
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> python -m build
#> python -m pip install ./dist/snobol4python-0.3.0.tar.gz
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#> python ENG-685/transl8r_pop3.py
#----------------------------------------------------------------------------------------------------------------------
import copy
from functools import wraps
#----------------------------------------------------------------------------------------------------------------------
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
    __slots__ = ['func', 'patterns', 'features', 'generator']
    def __init__(self, func, patterns, features):
        self.func = func
        self.patterns = patterns
        self.features = features
        self.generator = self.func(*self.patterns, **self.features)
    def __iter__(self):             # Constructor
                                    self.generator = self.func(*self.patterns, **self.features)
                                    return self.generator
    def __next__(self):             return next(self.generator)
    def __repr__(self):             return f"{self.func}(*{len(self.patterns)})"
    def __invert__(self):           return π(self) # pi, unary '~', optional, zero or one
    def __add__(self, other):       # SIGMA, binary '+', subsequent, '+' is left associative
                                    if self.func.__name__ == "Σ": # ((P + Q) + R) + S, so flatten from the left
                                        return Σ(*self.patterns, other)
                                    else: return Σ(self, other)
    def __or__(self, other):        # PI, binary '|', alternate
                                    if self.func.__name__ == "Π": # ((P | Q) | R) | S, so flatten from the left
                                        return Π(*self.patterns, other)
                                    else: return Π(self, other)
    def __and__(self, other):       # PSI, binary '&', conjunction
                                    if self.func.__name__ == "ξ": # ((P & Q) & R) & S, so flatten from the left
                                        return ξ(*self.patterns, other)
                                    else: return ξ(self, other)
    def __div__(self, other):       return Ω(self, other) # OMEGA, binary '/', immediate assignment (permanent)
    def __rdiv__(self, other):      return Ω(self, other) # OMEGA, binary '/', immediate assignment (permanent)
    def __matmul__(self, other):    return δ(self, other) # delta, binary '@', immediate assignment (backtracking)
    def __mod__(self, other):       return Δ(self, other) # DELTA, binary '%', conditional assignment
    def __contains__(self, other):  return SEARCH(other, self)
#----------------------------------------------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    @wraps(func)
    def _PATTERN(*patterns, **features):
        return PATTERN(func, patterns, features)
    return _PATTERN
#----------------------------------------------------------------------------------------------------------------------
import re
re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    global re_repr_function
    re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
    p = repr(P)
    r = re.fullmatch(re_repr_function, p)
    if r: return f"{r.group(1)}(*{r.group(3)})"
    else: return p
#----------------------------------------------------------------------------------------------------------------------
def FAIL(): raise StopIteration # return?
def ABORT(): raise Exception() # return?
def SUCCESS():
    while True: yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ε() -> PATTERN: yield "" # NULL, epsilon, zero-length string
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
@pattern
def θ(N) -> PATTERN:
    global S, _, _globals
    if N == "OUTPUT": print("", S[_].pos, end="")
    logger.debug("theta(%s) SUCCESS", N)
    _globals[N] = S[_].pos
    yield ""
    logger.debug("theta(%s) backtracking...", N)
    del _globals[N]
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
@pattern
def Ω(P, N) -> PATTERN: # OMEGA, binary '/', SNOBOL4: P $ N
    global _globals
    logger.debug("OMEGA(%s, %s)", PROTOTYPE(P), N)
    for _1 in P:
        if _1 == "": v = ""
        else: v = S[_].subject[_1[0] : _1[1]]
        if N == "OUTPUT": print('', v, end="")
        logger.debug("%s = OMEGA(%s)", N, repr(v))
        _globals[N] = v
        yield _1
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (backtracking)
@pattern
def δ(P, N) -> PATTERN: # delta, binary '@', SNOBOL4: P $ N
    global _globals
    logger.debug("delta(%s, %s)", PROTOTYPE(P), N)
    for _1 in P:
        if _1 == "": v = ""
        else: v = S[_].subject[_1[0] : _1[1]]
        if N == "OUTPUT": print('', v, end="")
        logger.debug("%s = delta(%s)", N, repr(v))
        _globals[N] = v
        yield _1
        logger.debug("%s deleted", N)
        if N in _globals: del _globals[N]
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def Λ(expression) -> PATTERN: # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    global _globals
    logger.debug("lambda(%s) evaluating...", repr(expression))
    match type(expression).__name__:
        case 'str':
            if eval(expression, _globals):
                logger.debug("lambda(%s) SUCCESS", repr(expression))
                yield ""
                logger.debug("lambda(%s) backtracking...", repr(expression))
            else: logger.debug("lambda(%s) Error evaluating. FAIL", repr(expression))
        case 'function':
            if expression():
                logger.debug("lambda(%s) SUCCESS", repr(expression))
                yield ""
                logger.debug("lambda(%s) backtracking...", repr(expression))
            else: logger.debug("lambda(%s) Error evaluating. FAIL", repr(expression))
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
@pattern
def Δ(P, N) -> PATTERN: # DELTA, binary '%', SNOBOL4: P . N
    global S, _
    logger.debug("delta(%s, %s)", PROTOTYPE(P), N)
    for _1 in P:
        logger.debug("%s = delta(%s) SUCCESS", N, repr(_1))
        if _1 == "":
            S[_].cstack.append(f"{N} = ''")
        else: S[_].cstack.append(f"{N} = S[_].subject[{_1[0]} : {_1[1]}]")
        yield _1
        logger.debug("%s = delta(%s) backtracking...", N, repr(_1))
        S[_].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
@pattern
def λ(command) -> PATTERN: # LAMBDA, P . *exec(), P . tx . *func(tx)
    global S, _
    logger.debug("LAMBDA(%s) compiling...", repr(command))
    if command:
        if compile(command, '<string>', 'exec'): # 'single', 'eval'
            logger.debug("LAMBDA(%s) SUCCESS", repr(command))
            S[_].cstack.append(command)
            yield ""
            logger.debug("LAMBDA(%s) backtracking...", repr(command))
            S[_].cstack.pop()
        else: logger.debug("LAMBDA(%s) Error compiling. FAIL", repr(command))
    else: yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def nPush() -> PATTERN:
    global S, _
    logger.debug("nPush() SUCCESS")
    S[_].cstack.append(f"S[_].itop += 1");
    S[_].cstack.append(f"S[_].istack.append(0)");
    yield "";
    logger.debug("nPush() backtracking...")
    S[_].cstack.pop()
    S[_].cstack.pop()
@pattern
def nInc() -> PATTERN:
    global S, _
    logger.debug("nInc() SUCCESS")
    S[_].cstack.append(f"S[_].istack[S[_].itop] += 1");
    yield "";
    logger.debug("nInc() backtracking...")
    S[_].cstack.pop()
@pattern
def nPop() -> PATTERN:
    global S, _
    logger.debug("nPop() SUCCESS")
    S[_].cstack.append(f"S[_].istack.pop()");
    S[_].cstack.append(f"S[_].itop -= 1");
    yield "";
    logger.debug("nPop() backtracking...")
    S[_].cstack.pop()
    S[_].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Shift(t, v='') -> PATTERN:
    global S, _
    logger.debug("Shift(%s, %s) SUCCESS", repr(t), repr(v))
    if v is None:
        S[_].cstack.append(f"S[_].shift('{t}')")
    else: S[_].cstack.append(f"S[_].shift('{t}', {v})")
    yield ""
    logger.debug("Shift(%s, %s) backtracking...", repr(t), repr(v))
    S[_].cstack.pop()
@pattern
def Reduce(t, n=None) -> PATTERN:
    global S, _
    logger.debug("Reduce(%s, %d) SUCCESS", repr(t), n)
    if n is None: n = "S[_].istack[S[_].itop]"
    S[_].cstack.append(f"S[_].reduce('{t}', {n})")
    yield ""
    logger.debug("Reduce(%s, %d) backtracking...", repr(t), n)
    S[_].cstack.pop()
@pattern
def Pop(v) -> PATTERN:
    global S, _
    logger.debug("Pop(%s) SUCCESS", v)
    S[_].cstack.append(f"{v} = S[_].pop()")
    yield ""
    logger.debug("Pop(%s) backtracking...", v)
    S[_].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
@pattern
def FENCE(P=None) -> PATTERN: # FENCE and FENCE(P)
    if P:
        logger.debug("FENCE(%s) SUCCESS", PROTOTYPE(P))
        yield from P
        logger.debug("FENCE(%s) backtracking...", PROTOTYPE(P))
    else:
        logger.debug("FENCE() SUCCESS")
        yield ""
        logger.debug("FENCE() backtracking...")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def POS(n) -> PATTERN:
    global S, _
    if S[_].pos == n:
        logger.debug("POS(%d) SUCCESS(%d,%d)=", n, S[_].pos, 0)
        yield ""
        logger.debug("POS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global S, _
    if S[_].pos == len(S[_].subject) - n:
        logger.debug("RPOS(%d) SUCCESS(%d,%d)=", n, S[_].pos, 0)
        yield ""
        logger.debug("RPOS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def α():
    global S, _
    if (S[_].pos == 0) or \
       (S[_].pos > 0 and S[_].subject[S[_].pos - 1 : S[_].pos] == '\n'):
        yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ω():
    global S, _
    if (S[_].pos == len(S[_].subject)) or \
       (S[_].pos < len(S[_].subject) and S[_].subject[S[_].pos : S[_].pos + 1] == '\n'):
       yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global S, _
    if S[_].pos + n <= len(S[_].subject):
        logger.debug("LEN(%d) SUCCESS(%d,%d)=%s", n, S[_].pos, n, S[_].subject[S[_].pos : S[_].pos + n])
        S[_].pos += n
        yield (S[_].pos - n, S[_].pos) # S[_].subject[S[_].pos - n : S[_].pos]
        S[_].pos -= n
        logger.debug("LEN(%d) backtracking(%d)...", n, S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def σ(s) -> PATTERN: # sigma, sequence of characters, literal string patttern
    global S, _
    logger.debug("sigma(%s) trying(%d)", repr(s), S[_].pos)
    if S[_].pos + len(s) <= len(S[_].subject):
        if s == S[_].subject[S[_].pos : S[_].pos + len(s)]:
            S[_].pos += len(s)
            logger.debug("sigma(%s) SUCCESS(%d,%d)=", repr(s), S[_].pos - len(s), len(s))
            yield (S[_].pos - len(s), S[_].pos) # s
            S[_].pos -= len(s)
            logger.debug("sigma(%s) backtracking(%d)...", repr(s), S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching
import re
_rexs = dict()
@pattern
def φ(rex) -> PATTERN:
    global S, _, _rexs
    if rex not in _rexs:
        _rexs[rex] = re.compile(rex, re.MULTILINE)
    if matches := _rexs[rex].match(S[_].subject, pos = S[_].pos, endpos = len(S[_].subject)):
        if S[_].pos == matches.start():
            pos0 = S[_].pos
            if S[_].pos < matches.end(): #must consume something
                S[_].pos = matches.end()
                for (N, V) in matches.groupdict().items():
                    _globals[N] = V
                yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
                S[_].pos = pos0
            else: raise Exeption("Regular expression can not match epsilon.")
        else: raise Exeption("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Φ(): print("Yikes! Φ()"); yield ""
@pattern
def ψ(): print("Yikes! ψ()"); yield ""
@pattern
def Ψ(): print("Yikes! Ψ()"); yield ""
@pattern
def Ϙ(): print("Yikes! Ϙ()"); yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def TAB(n) -> PATTERN:
    global S, _
    if n <= len(S[_].subject):
        if n >= S[_].pos:
            pos0 = S[_].pos
            S[_].pos = n
            yield (pos0, n) # S[_].subject[pos0 : n]
            S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RTAB(n) -> PATTERN:
    global S, _
    if n <= len(S[_].subject):
        n = len(S[_].subject) - n
        if n >= S[_].pos:
            pos0 = S[_].pos
            S[_].pos = n
            yield (pos0, n) # S[_].subject[pos0 : n]
            S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def REM() -> PATTERN:
    global S, _
    pos0 = S[_].pos
    S[_].pos = len(S[_].subject)
    yield (pos0, S[_].pos) # S[_].subject[pos0:]
    S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ANY(characters) -> PATTERN:
    global S, _
    logger.debug("ANY(%s) trying(%d)", repr(characters), S[_].pos)
    if S[_].pos < len(S[_].subject):
        if S[_].subject[S[_].pos] in characters:
            logger.debug("ANY(%s) SUCCESS(%d,%d)=%s", repr(characters), S[_].pos, 1, S[_].subject[S[_].pos])
            S[_].pos += 1
            yield (S[_].pos - 1, S[_].pos) # S[_].subject[S[_].pos - 1]
            S[_].pos -= 1
            logger.debug("ANY(%s) backtracking(%d)...", repr(characters), S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def NOTANY(characters) -> PATTERN:
    global S, _
    logger.debug("NOTANY(%s) trying(%d)", repr(characters), S[_].pos)
    if S[_].pos < len(S[_].subject):
        if not S[_].subject[S[_].pos] in characters:
            logger.debug("NOTANY(%s) SUCCESS(%d,%d)=%s", repr(characters), S[_].pos, 1, S[_].subject[S[_].pos])
            S[_].pos += 1
            yield (S[_].pos - 1, S[_].pos) # S[_].subject[S[_].pos - 1]
            S[_].pos -= 1
            logger.debug("NOTANY(%s) backtracking(%d)...", repr(characters), S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def SPAN(characters) -> PATTERN:
    global S, _
    pos0 = S[_].pos
    logger.debug("SPAN(%s) trying(%d)", repr(characters), pos0)
    while True:
        if S[_].pos >= len(S[_].subject): break
        if S[_].subject[S[_].pos] in characters:
            S[_].pos += 1
        else: break
    if S[_].pos > pos0:
        logger.debug("SPAN(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, S[_].pos - pos0, S[_].subject[pos0 : S[_].pos])
        yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
        S[_].pos = pos0
        logger.debug("SPAN(%s) backtracking(%d)...", repr(characters), S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAK(characters) -> PATTERN:
    global S, _
    pos0 = S[_].pos
    logger.debug("BREAK(%s) SUCCESS(%d)", repr(characters), pos0)
    while True:
        if S[_].pos >= len(S[_].subject): break
        if not S[_].subject[S[_].pos] in characters:
            S[_].pos += 1
        else: break
    if S[_].pos < len(S[_].subject):
        logger.debug("BREAK(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, S[_].pos - pos0, S[_].subject[pos0 : S[_].pos])
        yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
        S[_].pos = pos0
        logger.debug("BREAK(%s) backtracking(%d)...", repr(characters), S[_].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAKX(characters) -> PATTERN: yield from BREAK(characters)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ARB() -> PATTERN: # ARB
    global S, _
    pos0 = S[_].pos
    while S[_].pos <= len(S[_].subject):
        yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
        S[_].pos += 1
    S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BAL() -> PATTERN: # BAL
    global S, _
    pos0 = S[_].pos
    nest = 0
    S[_].pos += 1
    while S[_].pos <= len(S[_].subject):
        ch = S[_].subject[S[_].pos - 1 : S[_].pos]
        match ch:
            case '(': nest += 1
            case ')': nest -= 1
        if nest < 0: break
        elif nest > 0 and S[_].pos >= len(S[_].subject): break
        elif nest == 0: yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
        S[_].pos += 1
    S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ξ(P, Q) -> PATTERN: # PSI, AND, conjunction
    global S, _
    pos0 = S[_].pos
    for _1 in P:
        pos1 = S[_].pos
        try:
            S[_].pos = pos0
            next(Q)
            if (S[_].pos == pos1):
                yield _1
                S[_].pos = pos0
        except StopIteration:
            S[_].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def π(P) -> PATTERN: # pi, optional, SNOBOL4: P | epsilon
    yield from P
    yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Π(*AP) -> PATTERN: # PI, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    global S, _
    logger.debug("PI([%s]) trying(%d)...",
        "|".join([PROTOTYPE(P) for P in AP]), S[_].pos)
    for P in AP:
        yield from P
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
    global S, _
    pos0 = S[_].pos
    logger.debug("SIGMA([%s]) trying(%d)...",
        " ".join([PROTOTYPE(P) for P in AP]), pos0)
    cursor = 0
    highmark = 0
    while cursor >= 0:
        if cursor >= highmark:
            iter(AP[cursor])
            highmark += 1
        try:
            next(AP[cursor])
            cursor += 1
            if cursor >= len(AP):
                logger.debug("SIGMA(*) SUCCESS(%d,%d)=%s", pos0, S[_].pos - pos0, S[_].subject[pos0 : S[_].pos])
                yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
                logger.debug("SIGMA(*) backtracking(%d)...", pos0)
                cursor -= 1
        except StopIteration:
            cursor -= 1
            highmark -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def MARBNO(P) -> PATTERN: yield from ARBNO(P)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ARBNO(P) -> PATTERN:
    global S, _
    pos0 = S[_].pos
    logger.debug("ARBNO(%s) SUCCESS(%d,%d)=%s", PROTOTYPE(P), pos0, S[_].pos - pos0, S[_].subject[pos0 : S[_].pos])
    yield ""
    logger.debug("ARBNO(*) backtracking(%d)...", pos0)
    AP = []
    cursor = 0
    highmark = 0
    while cursor >= 0:
        if cursor >= highmark:
            AP.append((S[_].pos, copy.copy(P)))
            iter(AP[cursor][1])
            highmark += 1
        try:
            next(AP[cursor][1])
            cursor += 1
            logger.debug("ARBNO(*) SUCCESS(%d,%d)=%s", pos0, S[_].pos - pos0, S[_].subject[pos0 : S[_].pos])
            yield (pos0, S[_].pos) # S[_].subject[pos0 : S[_].pos]
            logger.debug("ARBNO(*) backtracking(%d)...", pos0)
        except StopIteration:
            cursor -= 1
            highmark -= 1
            AP.pop()
#----------------------------------------------------------------------------------------------------------------------
def _push(lyst):
    S[_].vstack.append(lyst)
#----------------------------------------------------------------------------------------------------------------------
def _pop():
    return S[_].vstack.pop()
#----------------------------------------------------------------------------------------------------------------------
def _shift(t, v=None):
    global _globals
    if v is None:
        _push([t])
    else: _push([t, v])
#----------------------------------------------------------------------------------------------------------------------
def _reduce(t, n):
    global _globals
    if n == 0 and t == 'Σ':
        _push(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ξ'):
        x = [t]
        for i in range(n):
            x.insert(1, _pop())
        _push(x)
#----------------------------------------------------------------------------------------------------------------------
class SNOBOL:
    __slots__ = ['pos', 'subject', 'cstack', 'itop', 'istack', 'vstack', 'shift', 'reduce', 'pop']
    def __init__(self, pos, subject, cstack, itop, istack, vstack):
        self.pos    = pos
        self.subject = subject
        self.cstack = cstack
        self.itop   = itop
        self.istack = istack
        self.vstack = vstack
        self.shift  = _shift
        self.reduce = _reduce
        self.pop    = _pop
#----------------------------------------------------------------------------------------------------------------------
S = [] # search stack
_ = -1 # top level of search stack
_globals = None # global variables
#----------------------------------------------------------------------------------------------------------------------
def GLOBALS(g): global _globals; _globals = g
def MATCH     (string, P) -> bool: return SEARCH(string, POS(0) + P)
def FULLMATCH (string, P) -> bool: return SEARCH(string, POS(0) + P + RPOS(0))
def SEARCH    (string, P) -> bool:
    global _globals, S, _
    if _globals is None:
        _globals = globals()
    S.append(SNOBOL(0, string, [], -1, [], []))
    _ += 1
    try:
        m = next(P)
        logger.debug(f'SEARCH(): "{string}" ? "{m}"')
        for command in S[_].cstack:
            logger.debug(f'SEARCH(): {command}')
        for var, val in _globals.items():
            logger.debug(f'SEARCH(): var={var} val={val}')
        _globals['S'] = S
        _globals['_'] = _
        for command in S[_].cstack:
            exec(command, _globals)
        result = True
    except StopIteration:
        result = False
    _ -= 1
    S.pop()
    return result
#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if "SNOBOL4" in POS(0) + (SPAN("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "SNOBOL4" in POS(0) + (BREAK("0123456789") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "001_01C717AB.5C51AFDE" in φ(r"(?P<name>[0-9]{3}(_[0-9A-F]{4})?_[0-9A-F]{8}\.[0-9A-F]{8})"):
        print(name)

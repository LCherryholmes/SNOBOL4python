# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> python -m build
#> python -m pip install ./dist/snobol4python-0.1.0.tar.gz
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#> python tests/transl8r.py
#----------------------------------------------------------------------------------------------------------------------
import copy
from functools import wraps
from .SNOBOL4functions import PROTOTYPE
#----------------------------------------------------------------------------------------------------------------------
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
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
    def __contains__(self, other):  return MATCH(other, self)
#----------------------------------------------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    @wraps(func)
    def _PATTERN(*patterns, **features):
        return PATTERN(func, patterns, features)
    return _PATTERN
#----------------------------------------------------------------------------------------------------------------------
def FAIL(): raise StopIteration # return?
def ABORT(): raise Exception() # return?
def SUCCESS():
    while True: yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ε() -> PATTERN: yield "" # NULL, epsilon, zero-length string
#----------------------------------------------------------------------------------------------------------------------
_pos = None # internal position
_subject = None # internal subject
_globals = None # global variables
_cstack = None # command stack (conditional actions)
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
@pattern
def θ(V) -> PATTERN:
    global _pos, _globals
    if V == "OUTPUT": print("", _pos, end="")
    logger.debug("theta(%s) SUCCESS", V)
    _globals[V] = _pos
    yield ""
    logger.debug("theta(%s) backtracking...", V)
    del _globals[V]
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
@pattern
def Ω(P, V) -> PATTERN: # OMEGA, binary '/', SNOBOL4: P $ V
    global _globals
    logger.debug("OMEGA(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print('', _1, end="")
        logger.debug("%s = OMEGA(%s)", V, repr(_1))
        _globals[V] = _1
        yield _1
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (backtracking)
@pattern
def δ(P, V) -> PATTERN: # delta, binary '@', SNOBOL4: P $ V
    global _globals
    logger.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print('', _1, end="")
        logger.debug("%s = delta(%s)", V, repr(_1))
        _globals[V] = _1
        yield _1
        logger.debug("%s deleted", V)
        if V in _globals: del _globals[V]
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def λ(expression) -> PATTERN: # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
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
def Δ(P, V) -> PATTERN: # DELTA, binary '%', SNOBOL4: P . V
    global _pos, _cstack
    logger.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        logger.debug("%s = delta(%d, %d) SUCCESS", V, _pos - len(_1), _pos)
        _cstack.append(f"{V} = _subject[{_pos - len(_1)} : {_pos}]")
        yield _1
        logger.debug("%s = delta(%d, %d) backtracking...", V, _pos - len(_1), _pos)
        _cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
@pattern
def Λ(command) -> PATTERN: # LAMBDA, P . *exec(), P . tx . *func(tx)
    global _cstack
    logger.debug("LAMBDA(%s) compiling...", repr(command))
    if command:
        if compile(command, '<string>', 'exec'): # 'single', 'eval'
            logger.debug("LAMBDA(%s) SUCCESS", repr(command))
            _cstack.append(command)
            yield ""
            logger.debug("LAMBDA(%s) backtracking...", repr(command))
            _cstack.pop()
        else: logger.debug("LAMBDA(%s) Error compiling. FAIL", repr(command))
    else: yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def nPush() -> PATTERN:
    global _cstack
    logger.debug("nPush() SUCCESS")
    _cstack.append(f"itop += 1");
    _cstack.append(f"istack.append(0)");
    yield "";
    logger.debug("nPush() backtracking...")
    _cstack.pop()
    _cstack.pop()
@pattern
def nInc() -> PATTERN:
    global _cstack
    logger.debug("nInc() SUCCESS")
    _cstack.append(f"istack[itop] += 1");
    yield "";
    logger.debug("nInc() backtracking...")
    _cstack.pop()
@pattern
def nPop() -> PATTERN:
    global _cstack
    logger.debug("nPop() SUCCESS")
    _cstack.append(f"istack.pop()");
    _cstack.append(f"itop -= 1");
    yield "";
    logger.debug("nPop() backtracking...")
    _cstack.pop()
    _cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Shift(t, v='') -> PATTERN:
    global _cstack, _shift
    logger.debug("Shift(%s, %s) SUCCESS", repr(t), repr(v))
    if v is None:
        _cstack.append(f"_shift('{t}')")
    else: _cstack.append(f"_shift('{t}', {v})")
    yield ""
    logger.debug("Shift(%s, %s) backtracking...", repr(t), repr(v))
    _cstack.pop()
@pattern
def Reduce(t, n=None) -> PATTERN:
    global _cstack, _reduce
    logger.debug("Reduce(%s, %d) SUCCESS", repr(t), n)
    if n is None: n = "istack[itop]"
    _cstack.append(f"_reduce('{t}', {n})")
    yield ""
    logger.debug("Reduce(%s, %d) backtracking...", repr(t), n)
    _cstack.pop()
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
    global _pos
    if _pos == n:
        logger.debug("POS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logger.debug("POS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global _pos, _subject
    if _pos == len(_subject) - n:
        logger.debug("RPOS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logger.debug("RPOS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def α():
    global _pos, _subject
    if (_pos == 0) or \
       (_pos > 0 and _subject[_pos - 1 : _pos] == '\n'):
        yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ω():
    global _pos, _subject
    if (_pos == len(_subject)) or \
       (_pos < len(_subject) and _subject[_pos : _pos + 1] == '\n'):
       yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global _pos, _subject
    if _pos + n <= len(_subject):
        logger.debug("LEN(%d) SUCCESS(%d,%d)=%s", n, _pos, n, _subject[_pos:_pos + n])
        _pos += n
        yield _subject[_pos - n:_pos]
        _pos -= n
        logger.debug("LEN(%d) backtracking(%d)...", n, _pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def σ(s) -> PATTERN: # sigma, sequence of characters, literal string patttern
    global _pos, _subject
    logger.debug("sigma(%s) trying(%d)", repr(s), _pos)
    if _pos + len(s) <= len(_subject):
        if s == _subject[_pos:_pos + len(s)]:
            _pos += len(s)
            logger.debug("sigma(%s) SUCCESS(%d,%d)=", repr(s), _pos - len(s), len(s))
            yield s
            _pos -= len(s)
            logger.debug("sigma(%s) backtracking(%d)...", repr(s), _pos)
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching
import re
_rexs = dict()
@pattern
def φ(rex) -> PATTERN:
    global _pos, _subject, _rexs
    if rex not in _rexs:
        _rexs[rex] = re.compile(rex)
    if matches := _rexs[rex].match(_subject, pos = _pos, endpos = len(_subject)):
        if _pos == matches.start():
            pos0 = _pos
            if _pos < matches.end(): #must consume something
                _pos = matches.end()
                yield _subject[pos0 : _pos]
                _pos = pos0
            else: raise Exeption("Regular expression can not match epsilon.")
        else: raise Exeption("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Φ():
    print("Yikes! φ()")
    yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ψ(): print("Yikes! Φ()"); yield ""
@pattern
def Ψ(): print("Yikes! Ψ()"); yield ""
@pattern
def Ϙ(): print("Yikes! Ϙ()"); yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def TAB(n) -> PATTERN:
    global _pos, _subject
    if n <= len(_subject):
        if n >= _pos:
            pos0 = _pos
            _pos = n
            yield _subject[pos0:n]
            _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RTAB(n) -> PATTERN:
    global _pos, _subject
    if n <= len(_subject):
        n = len(_subject) - n
        if n >= _pos:
            pos0 = _pos
            _pos = n
            yield _subject[pos0:n]
            _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def REM() -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    _pos = len(_subject)
    yield _subject[pos0:]
    _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ANY(characters) -> PATTERN:
    global _pos, _subject
    logger.debug("ANY(%s) trying(%d)", repr(characters), _pos)
    if _pos < len(_subject):
        if _subject[_pos] in characters:
            logger.debug("ANY(%s) SUCCESS(%d,%d)=%s", repr(characters), _pos, 1, _subject[_pos])
            _pos += 1
            yield _subject[_pos - 1]
            _pos -= 1
            logger.debug("ANY(%s) backtracking(%d)...", repr(characters), _pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def NOTANY(characters) -> PATTERN:
    global _pos, _subject
    logger.debug("NOTANY(%s) trying(%d)", repr(characters), _pos)
    if _pos < len(_subject):
        if not _subject[_pos] in characters:
            logger.debug("NOTANY(%s) SUCCESS(%d,%d)=%s", repr(characters), _pos, 1, _subject[_pos])
            _pos += 1
            yield _subject[_pos - 1]
            _pos -= 1
            logger.debug("NOTANY(%s) backtracking(%d)...", repr(characters), _pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def SPAN(characters) -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    logger.debug("SPAN(%s) trying(%d)", repr(characters), pos0)
    while True:
        if _pos >= len(_subject): break
        if _subject[_pos] in characters:
            _pos += 1
        else: break
    if _pos > pos0:
        logger.debug("SPAN(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, _pos - pos0, _subject[pos0:_pos])
        yield _subject[pos0:_pos]
        _pos = pos0
        logger.debug("SPAN(%s) backtracking(%d)...", repr(characters), _pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAK(characters) -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    logger.debug("BREAK(%s) SUCCESS(%d)", repr(characters), pos0)
    while True:
        if _pos >= len(_subject): break
        if not _subject[_pos] in characters:
            _pos += 1
        else: break
    if _pos < len(_subject):
        logger.debug("BREAK(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, _pos - pos0, _subject[pos0:_pos])
        yield _subject[pos0:_pos]
        _pos = pos0
        logger.debug("BREAK(%s) backtracking(%d)...", repr(characters), _pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAKX(characters) -> PATTERN: yield from BREAK(characters)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ARB() -> PATTERN: # ARB
    global _pos, _subject
    pos0 = _pos
    while _pos <= len(_subject):
        yield _subject[pos0 : _pos]
        _pos += 1
    _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BAL() -> PATTERN: # BAL
    global _pos, _subject
    pos0 = _pos
    nest = 0
    _pos += 1
    while _pos <= len(_subject):
        ch = _subject[_pos - 1 : _pos]
        match ch:
            case '(': nest += 1
            case ')': nest -= 1
        if nest < 0: break
        elif nest > 0 and _pos >= len(_subject): break
        elif nest == 0: yield _subject[pos0 : _pos]
        _pos += 1
    _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ξ(P, Q) -> PATTERN: # PSI, AND, conjunction
    global _pos
    pos0 = _pos
    for _1 in P:
        pos1 = _pos
        try:
            _pos = pos0
            next(Q)
            if (_pos == pos1):
                yield _1
                _pos = pos0
        except StopIteration:
            _pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def π(P) -> PATTERN: # pi, optional, SNOBOL4: P | epsilon
    yield from P
    yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Π(*AP) -> PATTERN: # PI, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    global _pos
    logger.debug("PI([%s]) trying(%d)...",
        "|".join([PROTOTYPE(P) for P in AP]), _pos)
    for P in AP:
        yield from P
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
    global _pos, _subject
    pos0 = _pos
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
                logger.debug("SIGMA(*) SUCCESS(%d,%d)=%s", pos0, _pos - pos0, _subject[pos0:_pos])
                yield _subject[pos0:_pos]
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
    global _pos, _subject
    pos0 = _pos
    logger.debug("ARBNO(%s) SUCCESS(%d,%d)=%s", PROTOTYPE(P), pos0, _pos - pos0, _subject[pos0:_pos])
    yield ""
    logger.debug("ARBNO(*) backtracking(%d)...", pos0)
    AP = []
    cursor = 0
    highmark = 0
    while cursor >= 0:
        if cursor >= highmark:
            AP.append((_pos, copy.copy(P)))
            iter(AP[cursor][1])
            highmark += 1
        try:
            next(AP[cursor][1])
            cursor += 1
            logger.debug("ARBNO(*) SUCCESS(%d,%d)=%s", pos0, _pos - pos0, _subject[pos0:_pos])
            yield _subject[pos0:_pos]
            logger.debug("ARBNO(*) backtracking(%d)...", pos0)
        except StopIteration:
            cursor -= 1
            highmark -= 1
            AP.pop()
#----------------------------------------------------------------------------------------------------------------------
def _shift(t, v=None):
    global _globals
    if v is None:
        _globals['vstack'].append([t])
    else: _globals['vstack'].append([t, v])
#----------------------------------------------------------------------------------------------------------------------
def _reduce(t, n):
    global _globals
    if n == 0 and t == 'Σ':
        _globals['vstack'].append(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ξ'):
        x = [t]
        for i in range(n):
            x.insert(1, _globals['vstack'].pop())
        _globals['vstack'].append(x)
#----------------------------------------------------------------------------------------------------------------------
def GLOBALS(V): global _globals; _globals = V
def MATCH     (string, P) -> bool: return SEARCH(string, POS(0) + P)
def FULLMATCH (string, P) -> bool: return SEARCH(string, POS(0) + P + RPOS(0))
def SEARCH    (string, P) -> bool:
    global _pos, _subject, _cstack, _globals
    if _globals is None:
        _globals = globals()
    _pos = 0 # internal position
    _subject = string # internal subject
    _cstack = [] # insternal command stack (conditional actions)
    _globals['itop'] = -1
    _globals['istack'] = [] # counter stack (nPush, nInc, nPop, nTop)
    _globals['vstack'] = [] # value stack (Shift/Reduce values)
    _globals['_shift'] = _shift
    _globals['_reduce'] = _reduce
    try:
        m = next(P)
        logger.debug(f'SEARCH(): "{string}" ? "{m}"')
        for command in _cstack:
            logger.debug(f'SEARCH(): {command}')
        for var, val in _globals.items():
            logger.debug(f'SEARCH(): var={var} val={val}')
        _globals['_subject'] = string
        for command in _cstack:
            exec(command, _globals)
        return True
    except StopIteration:
        return False
#----------------------------------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python -m pip install --upgrade pip
#> python -m pip install build
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> python -m build
#> python -m pip install ./dist/snobol4python-0.3.4.tar.gz
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#> python ENG-685/transl8r_pop3.py > ENG-685/pop3.py
#----------------------------------------------------------------------------------------------------------------------
import copy
from pprint import pprint, pformat
from functools import wraps
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
    __slots__ = ['func', 'args', 'kwargs', 'generator']
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.__iter__()
    def __iter__(self):             # Constructor
                                    self.generator = self.func(*self.args, **self.kwargs)
                                    return self.generator
    def __next__(self):             return next(self.generator)
    def __deepcopy__(self, memo):   # Deep copy
                                    args = []
                                    for arg in self.args:
                                        if isinstance(arg, PATTERN):
                                            args.append(copy.deepcopy(arg, memo))
                                        else: args.append(arg)
                                    return PATTERN(self.func, args, self.kwargs)
    def __repr__(self):             #
                                    match self.func.__name__:
                                        case 'ε':       repr = f"ε()"
                                        case 'σ':       repr = f"σ({pformat(self.args[0])})"
                                        case 'π':       repr = f"π({pformat(self.args[0])})"
                                        case 'ANY':     repr = f"ANY({pformat(self.args[0])})"
                                        case 'BREAK':   repr = f"BREAK({pformat(self.args[0])})"
                                        case 'BREAKX':  repr = f"BREAKX({pformat(self.args[0])})"
                                        case 'NOTANY':  repr = f"NOTANY({pformat(self.args[0])})"
                                        case 'POS':     repr = f"POS({self.args[0]})"
                                        case 'REM':     repr = f"REM()"
                                        case 'RPOS':    repr = f"RPOS({self.args[0]})"
                                        case 'RTAB':    repr = f"RTAB({self.args[0]})"
                                        case 'SPAN':    repr = f"SPAN({pformat(self.args[0])})"
                                        case 'TAB':     repr = f"TAB({self.args[0]})"
                                        case _:         #
                                                        if len(self.args) > 0:
                                                            repr = f"{self.func.__name__}(*{len(self.args)})"
                                                        else: repr = f"{self.func.__name__}()"
                                    return repr
    def __invert__(self):           return π(self) # pi, unary '~', optional, zero or one
    def __add__(self, other):       # SIGMA, Σ, binary '+', subsequent, '+' is left associative
                                    if self.func.__name__ == "Σ": # ((P + Q) + R) + S, so flatten from the left
                                        return Σ(*self.args, other)
                                    else: return Σ(self, other)
    def __or__(self, other):        # PI, binary '|', alternate
                                    if self.func.__name__ == "Π": # ((P | Q) | R) | S, so flatten from the left
                                        return Π(*self.args, other)
                                    else: return Π(self, other)
    def __and__(self, other):       # PSI, binary '&', conjunction
                                    if self.func.__name__ == "ξ": # ((P & Q) & R) & S, so flatten from the left
                                        return ξ(*self.args, other)
                                    else: return ξ(self, other)
    def __matmul__(self, other):    return δ(self, other) # delta, binary '@', immediate assignment (permanent)
    def __mod__(self, other):       return Δ(self, other) # DELTA, binary '%', conditional assignment
    def __contains__(self, other):  return SEARCH(other, self)
#----------------------------------------------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    @wraps(func)
    def _PATTERN(*args, **kwargs):
        return PATTERN(func, args, kwargs)
    _PATTERN.__annotations__ = {'return': PATTERN}
    return _PATTERN
#----------------------------------------------------------------------------------------------------------------------
import re
re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    global re_repr_function
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
def ε(): yield "" # NULL, epsilon, zero-length string
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
@pattern
def Θ(N:str):
    global Ϣ, _globals
    if N == "OUTPUT":
        Ϣ[-1].nl = True
        print(Ϣ[-1].pos, end='·');
    logger.info("Θ(%s) SUCCESS", N)
    _globals[N] = Ϣ[-1].pos
    yield ""
    logger.warning("Θ(%s) backtracking...", N)
    del _globals[N]
#----------------------------------------------------------------------------------------------------------------------
# Conditional cursor assignment (after successful complete pattern match)
@pattern
def θ(N:str):
    global Ϣ; N = str(N)
    if N == "OUTPUT":
        Ϣ[-1].nl = True
        print(Ϣ[-1].pos, end='·')
    logger.info("θ(%s) SUCCESS", N)
    Ϣ[-1].cstack.append(f"{N} = {Ϣ[-1].pos}")
    yield ""
    logger.warning("θ(%s) backtracking...", N)
    Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
@pattern
def δ(P:PATTERN, N:str): # delta, binary '@', SNOBOL4: P $ N
    global _globals; N = str(N)
    logger.debug("δ(%s, %s)", PROTOTYPE(P), N)
    for _1 in P:
        if _1 == "": v = ""
        else: v = Ϣ[-1].subject[_1[0]:_1[1]]
        if N == "OUTPUT":
            Ϣ[-1].nl = True
            print(v, end='·')
        logger.debug("%s = δ(%r)", N, v)
        _globals[N] = v
        yield _1
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def Λ(expression:str|object): # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    global _globals
    match type(expression).__name__:
        case 'str':
            logger.debug("Λ(%r) evaluating...", expression)
            if eval(expression, _globals):
                logger.info("Λ(%r) SUCCESS", expression)
                yield ""
                logger.warning("Λ(%r) backtracking...", expression)
            else: logger.error("Λ(%r) Error evaluating. FAIL!", expression)
        case 'function':
            logger.debug("Λ(function) evaluating...")
            try:
                if expression():
                    logger.info("Λ(function) SUCCESS")
                    yield ""
                    logger.warning("Λ(function) backtracking...")
            except Exception as e:
                logger.error("Λ(function) EXCEPTION evaluating. (%r) FAIL!", e)
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
@pattern
def Δ(P:PATTERN, N:str): # DELTA, binary '%', SNOBOL4: P . N
    global Ϣ; N = str(N)
    logger.debug("Δ(%s, %s)", PROTOTYPE(P), N)
    for _1 in P:
        logger.info("%s = Δ(%r) SUCCESS", N, _1)
        if N == "OUTPUT":
            if _1 == "":
                Ϣ[-1].cstack.append(f"print('')")
            else: Ϣ[-1].cstack.append(f"print(Ϣ[-1].subject[{_1[0]}:{_1[1]}])")
        else:
            if _1 == "":
                Ϣ[-1].cstack.append(f"{N} = ''")
            else: Ϣ[-1].cstack.append(f"{N} = Ϣ[-1].subject[{_1[0]}:{_1[1]}]")
        yield _1
        logger.warning("%s = Δ(%r) backtracking...", N, _1)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
@pattern
def λ(command:str): # LAMBDA, P . *exec(), P . tx . *func(tx)
    global Ϣ
    logger.debug("λ(%r) compiling...", command)
    if command:
        if compile(command, '<string>', 'exec'): # 'single', 'eval'
            logger.info("λ(%r) SUCCESS", command)
            Ϣ[-1].cstack.append(command)
            yield ""
            logger.warning("λ(%r) backtracking...", command)
            Ϣ[-1].cstack.pop()
        else: logger.error("λ(%r) Error compiling. FAIL", command)
    else: yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def nPush():
    global Ϣ
    logger.info("nPush() SUCCESS")
    Ϣ[-1].cstack.append(f"Ϣ[-1].itop += 1");
    Ϣ[-1].cstack.append(f"Ϣ[-1].istack.append(0)");
    yield "";
    logger.warning("nPush() backtracking...")
    Ϣ[-1].cstack.pop()
    Ϣ[-1].cstack.pop()
@pattern
def nInc():
    global Ϣ
    logger.info("nInc() SUCCESS")
    Ϣ[-1].cstack.append(f"Ϣ[-1].istack[Ϣ[-1].itop] += 1");
    yield "";
    logger.warning("nInc() backtracking...")
    Ϣ[-1].cstack.pop()
@pattern
def nPop():
    global Ϣ
    logger.info("nPop() SUCCESS")
    Ϣ[-1].cstack.append(f"Ϣ[-1].istack.pop()");
    Ϣ[-1].cstack.append(f"Ϣ[-1].itop -= 1");
    yield "";
    logger.warning("nPop() backtracking...")
    Ϣ[-1].cstack.pop()
    Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Shift(t:str = None, v:str = None):
    global Ϣ
    logger.info("Shift(%r, %r) SUCCESS", t, v)
    if t is None:   Ϣ[-1].cstack.append(f"Ϣ[-1].shift()")
    elif v is None: Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{t}')")
    else:           Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{t}', {v})")
    yield ""
    logger.warning("Shift(%r, %r) backtracking...", t, v)
    Ϣ[-1].cstack.pop()
@pattern
def Reduce(t:str, n:int = -1):
    global Ϣ
    if type(t).__name__ == 'function': t = t()
    logger.info("Reduce(%r, %d) SUCCESS", t, n)
    if   n == -2: n = "Ϣ[-1].istack[Ϣ[-1].itop + 1]"
    elif n == -1: n = "Ϣ[-1].istack[Ϣ[-1].itop]"
    Ϣ[-1].cstack.append(f"Ϣ[-1].reduce('{t}', {n})")
    yield ""
    logger.warning("Reduce(%r, %d) backtracking...", t, n)
    Ϣ[-1].cstack.pop()
@pattern
def Pop(v:str):
    global Ϣ
    logger.info("Pop(%s) SUCCESS", v)
    Ϣ[-1].cstack.append(f"{v} = Ϣ[-1].pop()")
    yield ""
    logger.warning("Pop(%s) backtracking...", v)
    Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
@pattern
def FENCE(P:PATTERN = None): # FENCE and FENCE(P)
    if P:
        logger.info("FENCE(%s) SUCCESS", PROTOTYPE(P))
        yield from P
        logger.warning("FENCE(%s) backtracking...", PROTOTYPE(P))
    else:
        logger.info("FENCE() SUCCESS")
        yield ""
        logger.warning("FENCE() backtracking...")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def POS(n:int):
    global Ϣ; n = int(n)
    if Ϣ[-1].pos == n:
        logger.info("POS(%d) SUCCESS(%d,%d)=", n, Ϣ[-1].pos, 0)
        yield ""
        logger.warning("POS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RPOS(n:int):
    global Ϣ; n = int(n)
    if Ϣ[-1].pos == len(Ϣ[-1].subject) - n:
        logger.info("RPOS(%d) SUCCESS(%d,%d)=", n, Ϣ[-1].pos, 0)
        yield ""
        logger.warning("RPOS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def α():
    global Ϣ
    if (Ϣ[-1].pos == 0) or \
       (Ϣ[-1].pos > 0 and Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos] == '\n'):
        yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ω():
    global Ϣ
    if (Ϣ[-1].pos == len(Ϣ[-1].subject)) or \
       (Ϣ[-1].pos < len(Ϣ[-1].subject) and Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + 1] == '\n'):
       yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def LEN(n:int):
    global Ϣ; n = int(n)
    if Ϣ[-1].pos + n <= len(Ϣ[-1].subject):
        logger.info("LEN(%d) SUCCESS(%d,%d)=%s", n, Ϣ[-1].pos, n, Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + n])
        Ϣ[-1].pos += n
        yield (Ϣ[-1].pos - n, Ϣ[-1].pos)
        Ϣ[-1].pos -= n
        logger.warning("LEN(%d) backtracking(%d)...", n, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def σ(s:str): # sigma, σ, sequence of characters, literal string patttern
    global Ϣ; pos0 = Ϣ[-1].pos; s = str(s)
    logger.debug("σ(%r) trying(%d)", s, pos0)
    if pos0 + len(s) <= len(Ϣ[-1].subject):
        if s == Ϣ[-1].subject[pos0:pos0 + len(s)]:
            logger.info("σ(%r) SUCCESS(%d,%d)=", s, Ϣ[-1].pos, len(s))
            Ϣ[-1].pos += len(s)
            yield (pos0, Ϣ[-1].pos)
            Ϣ[-1].pos -= len(s)
            logger.warning("σ(%r) backtracking(%d)...", s, Ϣ[-1].pos)
    return None
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching
import re
_rexs = dict()
@pattern
def Φ(rex:str):
    global Ϣ, _rexs
    if rex not in _rexs:
        _rexs[rex] = re.compile(rex, re.MULTILINE)
    if matches := _rexs[rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
        pos0 = Ϣ[-1].pos
        if pos0 == matches.start():
            Ϣ[-1].pos = matches.end()
            for (N, V) in matches.groupdict().items():
                _globals[N] = V
            yield (pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
        else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def φ(rex:str):
    global Ϣ, _rexs
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
                    Ϣ[-1].cstack.append(f"{N} = Ϣ[-1].subject[{span[0]}:{span[1]}]")
            yield (pos0, Ϣ[-1].pos)
            for i in range(push_count):
                Ϣ[-1].cstack.pop()
            Ϣ[-1].pos = pos0
        else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ψ(): print("Yikes! ψ()"); yield ""
@pattern
def Ψ(): print("Yikes! Ψ()"); yield ""
@pattern
def Ϙ(): print("Yikes! Ϙ()"); yield ""
#----------------------------------------------------------------------------------------------------------------------
@pattern
def TAB(n:int):
    global Ϣ; n = int(n)
    if n <= len(Ϣ[-1].subject):
        if n >= Ϣ[-1].pos:
            pos0 = Ϣ[-1].pos
            Ϣ[-1].pos = n
            yield (pos0, n)
            Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RTAB(n:int):
    global Ϣ; n = int(n)
    if n <= len(Ϣ[-1].subject):
        n = len(Ϣ[-1].subject) - n
        if n >= Ϣ[-1].pos:
            pos0 = Ϣ[-1].pos
            Ϣ[-1].pos = n
            yield (pos0, n)
            Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def REM():
    global Ϣ; pos0 = Ϣ[-1].pos
    Ϣ[-1].pos = len(Ϣ[-1].subject)
    yield (pos0, Ϣ[-1].pos)
    Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ANY(characters:str):
    global Ϣ; assert type(characters) == str
    logger.debug("ANY(%r) trying(%d)", characters, Ϣ[-1].pos)
    if Ϣ[-1].pos < len(Ϣ[-1].subject):
        if Ϣ[-1].subject[Ϣ[-1].pos] in characters:
            logger.info("ANY(%r) SUCCESS(%d,%d)=%s", characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
            Ϣ[-1].pos += 1
            yield (Ϣ[-1].pos - 1, Ϣ[-1].pos)
            Ϣ[-1].pos -= 1
            logger.warning("ANY(%r) backtracking(%d)...", characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def NOTANY(characters:str):
    global Ϣ; assert type(characters) == str
    logger.debug("NOTANY(%r) trying(%d)", characters, Ϣ[-1].pos)
    if Ϣ[-1].pos < len(Ϣ[-1].subject):
        if not Ϣ[-1].subject[Ϣ[-1].pos] in characters:
            logger.info("NOTANY(%r) SUCCESS(%d,%d)=%s", characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
            Ϣ[-1].pos += 1
            yield (Ϣ[-1].pos - 1, Ϣ[-1].pos)
            Ϣ[-1].pos -= 1
            logger.warning("NOTANY(%r) backtracking(%d)...", characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def SPAN(characters:str):
    global Ϣ; pos0 = Ϣ[-1].pos; assert type(characters) == str
    logger.debug("SPAN(%r) trying(%d)", characters, pos0)
    while True:
        if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
        if Ϣ[-1].subject[Ϣ[-1].pos] in characters:
            Ϣ[-1].pos += 1
        else: break
    if Ϣ[-1].pos > pos0:
        logger.info("SPAN(%r) SUCCESS(%d,%d)=%s", characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
        yield (pos0, Ϣ[-1].pos)
        Ϣ[-1].pos = pos0
        logger.warning("SPAN(%r) backtracking(%d)...", characters, Ϣ[-1].pos)
    return None
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAK(characters:str):
    global Ϣ; pos0 = Ϣ[-1].pos; assert type(characters) == str
    logger.debug("BREAK(%r) SUCCESS(%d)", characters, pos0)
    while True:
        if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
        if not Ϣ[-1].subject[Ϣ[-1].pos] in characters:
            Ϣ[-1].pos += 1
        else: break
    if Ϣ[-1].pos < len(Ϣ[-1].subject):
        logger.info("BREAK(%r) SUCCESS(%d,%d)=%s", characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
        yield (pos0, Ϣ[-1].pos)
        Ϣ[-1].pos = pos0
        logger.warning("BREAK(%r) backtracking(%d)...", characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAKX(characters:str): yield from BREAK(characters)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ARB(): # ARB
    global Ϣ; pos0 = Ϣ[-1].pos
    while Ϣ[-1].pos <= len(Ϣ[-1].subject):
        yield (pos0, Ϣ[-1].pos)
        Ϣ[-1].pos += 1
    Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def MARB(): yield from ARB() # MARB
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BAL(): # BAL
    global Ϣ; pos0 = Ϣ[-1].pos; nest = 0
    Ϣ[-1].pos += 1
    while Ϣ[-1].pos <= len(Ϣ[-1].subject):
        ch = Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos]
        match ch:
            case '(': nest += 1
            case ')': nest -= 1
        if nest < 0: break
        elif nest > 0 and Ϣ[-1].pos >= len(Ϣ[-1].subject): break
        elif nest == 0: yield (pos0, Ϣ[-1].pos)
        Ϣ[-1].pos += 1
    Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ξ(P:PATTERN, Q:PATTERN): # PSI, AND, conjunction
    global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
    for _1 in P:
        pos1 = Ϣ[-1].pos
        try:
            Ϣ[-1].pos = pos0
            next(Q)
            if (Ϣ[-1].pos == pos1):
                yield _1
                Ϣ[-1].pos = pos0
        except StopIteration:
            Ϣ[-1].pos = pos0
    Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def π(P:PATTERN): # pi, optional, SNOBOL4: P | epsilon
    Ϣ[-1].depth += 1
    yield from P
    yield ""
    Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Π(*AP:PATTERN): # PI, Π, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    global Ϣ
    logger.debug("Π(%s) trying(%d)...", ", ".join([PROTOTYPE(P) for P in AP]), Ϣ[-1].pos)
    Ϣ[-1].depth += 1
    for P in AP: yield from P
    Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Σ(*AP:PATTERN): # SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
    global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
    logger.debug("Σ(%s) trying(%d)...", ", ".join([PROTOTYPE(P) for P in AP]), pos0)
    highmark = 0
    cursor = 0
    while cursor >= 0:
        if cursor >= len(AP):
            logger.info("Σ(*) SUCCESS(%d,%d)=%s", pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield (pos0, Ϣ[-1].pos)
            logger.warning("Σ(*) backtracking(%d)...", pos0)
            cursor -= 1
        if cursor >= highmark:
            iter(AP[cursor])
            highmark += 1
        try:
            next(AP[cursor])
            cursor += 1
        except StopIteration:
            highmark -= 1
            cursor -= 1
    Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def ARBNO(P:PATTERN):
    global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
    logger.debug("ARBNO(%s) trying(%d)...", PROTOTYPE(P), pos0)
    highmark = 0
    cursor = 0
    AP = []
    while cursor >= 0:
        if cursor >= len(AP):
            logger.info("ARBNO(%s) SUCCESS(%d,%d)=%s", PROTOTYPE(P), pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield (pos0, Ϣ[-1].pos)
            logger.warning("ARBNO(%s) backtracking(%d)...", PROTOTYPE(P), pos0)
        if cursor >= highmark:
            AP.append((Ϣ[-1].pos, copy.deepcopy(P)))
            iter(AP[cursor][1])
            highmark += 1
        try:
            next(AP[cursor][1])
            cursor += 1
        except StopIteration:
            highmark -= 1
            cursor -= 1
            AP.pop()
    Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
@pattern
def MARBNO(P:PATTERN): yield from ARBNO(P)
#----------------------------------------------------------------------------------------------------------------------
def _push(lyst:list): Ϣ[-1].vstack.append(lyst)
def _pop():           return Ϣ[-1].vstack.pop()
#----------------------------------------------------------------------------------------------------------------------
def _shift(t:str = '', v:str = None):
    global _globals
    if v is None:
        _push([t])
    else: _push([t, v])
#----------------------------------------------------------------------------------------------------------------------
def _reduce(t:str, n:int):
    global _globals
    if n == 0 and t == 'Σ':
        _push(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ξ', 'snoExprList', '|', '..'):
        x = [t]
        for i in range(n):
            x.insert(1, _pop())
        _push(x)
#----------------------------------------------------------------------------------------------------------------------
class SNOBOL:
    __slots__ = ['pos', 'subject', 'depth', 'cstack', 'itop', 'istack', 'vstack', 'nl' , 'shift', 'reduce', 'pop']
    def __repr__(self): return f"('SNOBOL', {self.depth}, {self.pos}, {len(self.subject)}, {pformat(self.subject)}, {pformat(self.cstack)})"
    def __init__(self, pos:int, subject:str, cstack:list, itop:int, istack:int, vstack:list):
        self.pos:int        = pos
        self.subject:str    = subject
        self.depth:int      = 0
        self.cstack:list    = cstack
        self.itop:int       = itop
        self.istack:list    = istack
        self.vstack:list    = vstack
        self.nl:bool        = False
        self.shift          = _shift
        self.reduce         = _reduce
        self.pop            = _pop
#----------------------------------------------------------------------------------------------------------------------
import logging
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
            formatted_message = "{0:s} {1:s}{2:s}".format(self.window(_window_size // 2), '  ' * Ϣ[-1].depth, original_message)
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
Ϣ = [] # SNOBOL stack
_globals = None # global variables
_window_size = 24
#----------------------------------------------------------------------------------------------------------------------
def GLOBALS(g:dict): global _globals; _globals = g
def WINDOW(size:int): global _window_size; _window_size = size
def TRACE(level:int):
    global handler
    if   level >  logging.CRITICAL: logger.setLevel(level);             handler.setLevel(level)
    elif level == logging.CRITICAL: logger.setLevel(logging.CRITICAL);  handler.setLevel(logging.CRITICAL)
    elif level >= logging.ERROR:    logger.setLevel(logging.ERROR);     handler.setLevel(logging.ERROR)
    elif level >= logging.WARNING:  logger.setLevel(logging.WARNING);   handler.setLevel(logging.WARNING)
    elif level >= logging.INFO:     logger.setLevel(logging.INFO);      handler.setLevel(logging.INFO)
    elif level >= logging.DEBUG:    logger.setLevel(logging.DEBUG);     handler.setLevel(logging.DEBUG)
#----------------------------------------------------------------------------------------------------------------------
def MATCH     (string:str, P:PATTERN) -> bool: return SEARCH(string, POS(0) + P)
def FULLMATCH (string:str, P:PATTERN) -> bool: return SEARCH(string, POS(0) + P + RPOS(0))
def SEARCH    (string:str, P:PATTERN) -> bool:
    global _globals, Ϣ
    if _globals is None:
        _globals = globals()
    Ϣ.append(SNOBOL(0, string, [], -1, [], []))
    command = None
    try:
        m = next(P)
        if Ϣ[-1].nl: print()
        logger.info(f'SEARCH(): "{string}" ? "{m}"')
        for command in Ϣ[-1].cstack:
            logger.debug(f'SEARCH(): {command}')
#       for var, val in _globals.items():
#           logger.debug(f'SEARCH(): var={var} val={val}')
        _globals['Ϣ'] = Ϣ
        for command in Ϣ[-1].cstack:
            exec(command, _globals)
        result = True
    except IndexError:
        logger.error("SEARCH(): IndexError: %s", command)
        result = False
    except StopIteration:
        result = False
    Ϣ.pop()
    return result
#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import ALPHABET, DIGITS, LCASE, UCASE
    TRACE(10)
    WINDOW(32)
    for N in range(1,3):
        for subject in ['FOX', 'WOLF']:
            matches = subject in (
                Λ(lambda: N == 1) + σ('FOX')
              | Λ(lambda: N == 2) + σ('WOLF')
            )
            pprint([N, subject, matches])
    exit(0)
    @pattern
    def word(): yield from (ANY(UCASE+LCASE) + (SPAN(LCASE) | ε())) # SPAN(UCASE+LCASE)
    @pattern
    def delimiter():
        yield from σ(', ')
        yield from σ(', and ')
        yield from σ(' and ')
        return None
    sentences = ["I went to X, and Y looking for Z."]
#                 000000000011111111112222222222333
#                 012345678901234567890123456789012
    for sentence in sentences:
        if sentence in \
              ( POS(0)
              + (σ('I') | σ('He') | σ('You'))
              + σ(' went to ')
              + word()
              + ARBNO((delimiter() + word()))
              + σ(' looking for ')
              + word()
              + ARBNO((delimiter() + word()))
              + σ('.')
              + RPOS(0)
              ):
              pprint(['Matched.', None, None, None, sentence])
        else: pprint(['Unmatched!', None, None, None, sentence])
    @pattern
    def As():
        yield from \
            (   POS(0)
            +   ARBNO(σ('a')) @ 'OUTPUT'
            +   RPOS(0)
            )
    assert True is ("" in As())
    assert True is ("a" in As())
    assert True is ("aa" in As())
    assert True is ("aaa" in As())
    assert True is ("aaaa" in As())
    if "SNOBOL4" in POS(0) + (SPAN("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "SNOBOL4" in POS(0) + (BREAK("0123456789") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "001_01C717AB.5C51AFDE ..." in φ(r"(?P<name>[0-9]{3}(_[0-9A-F]{4})?_[0-9A-F]{8}\.[0-9A-F]{8})"):
        print(name)
#----------------------------------------------------------------------------------------------------------------------

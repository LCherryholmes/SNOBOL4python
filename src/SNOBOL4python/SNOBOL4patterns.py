# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python -m pip install --upgrade pip
#> python -m pip install build
#> python src/SNOBOL4python/SNOBOL4patterns.py
#> python -m build
#> python -m pip install ./dist/snobol4python-0.4.0.tar.gz
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
    def __init__(self):             self.generator = self.γ()
    def __iter__(self):             self.generator = self.γ(); return self.generator
    def __next__(self):             return next(self.generator)
    def __call__(self):             return self
    def __deepcopy__(self, memo):   return type(self)()
    def __repr__(self):             #
                                    match type(self).__name__:
                                        case 'ε':       return f"ε()"
                                        case 'σ':       return f"σ({pformat(self.s)})"
                                        case 'π':       return f"π({pformat(self.P)})"
                                        case 'Σ':       return  "Σ(*{0})".format(len(self.AP))
                                        case 'Π':       return  "Π(*{0})".format(len(self.AP))
                                        case 'ξ':       return  "ξ(*{0})".format(len(self.AP))
                                        case 'Δ':       return f"Δ({pformat(self.P)}, {pformat(self.N)})"
                                        case 'δ':       return f"δ({pformat(self.P)}, {pformat(self.N)})"
                                        case 'Λ':       return f"Λ({pformat(self.expression)})"
                                        case 'λ':       return f"λ({pformat(self.command)})"
                                        case 'Θ':       return f"Θ({pformat(self.N)})"
                                        case 'ζ':       return f"ζ({pformat(self.N)})"
                                        case 'Φ':       return f"Φ({pformat(self.rex)})"
                                        case 'φ':       return f"φ({pformat(self.rex)})"
                                        case 'ANY':     return f"ANY({pformat(self.characters)})"
                                        case 'ARB':     return f"ARB()"
                                        case 'ARBNO':   return  "ARBNO({0})".format(pformat(self.P))
                                        case 'BAL':     return f"BAL()"
                                        case 'BREAK':   return f"BREAK({pformat(self.characters)})"
                                        case 'BREAKX':  return f"BREAKX({pformat(self.characters)})"
                                        case 'FENCE':   return f"FENCE({pformat(self.P)})"
                                        case 'NOTANY':  return f"NOTANY({pformat(self.characters)})"
                                        case 'LEN':     return f"LEN({pformat(self.n)})"
                                        case 'POS':     return f"POS({pformat(self.n)})"
                                        case 'REM':     return f"REM()"
                                        case 'RPOS':    return f"RPOS({pformat(self.n)})"
                                        case 'RTAB':    return f"RTAB({pformat(self.n)})"
                                        case 'SPAN':    return f"SPAN({pformat(self.characters)})"
                                        case 'TAB':     return f"TAB({pformat(self.n)})"
                                        case 'Shift':   return f"Shift()"
                                        case 'Reduce':  return f"Reduce()"
                                        case 'Pop':     return f"Pop()"
                                        case 'nPush':   return f"nPush"
                                        case 'nInc':    return f"nInc()"
                                        case 'nPop':    return f"nPop()"
                                        case _:         raise Exception(f"Yipper Skipper! {type(self).__name__}")
    def __invert__(self):           return π(self) # pi, unary '~', optional, zero or one
    def __add__(self, other):       # SIGMA, Σ, binary '+', subsequent, '+' is left associative
                                    if type(self).__name__ == "Σ": # ((P + Q) + R) + S, so flatten from the left
                                        return Σ(*self.AP, other)
                                    else: return Σ(self, other)
    def __or__(self, other):        # PI, binary '|', alternate
                                    if type(self).__name__ == "Π": # ((P | Q) | R) | S, so flatten from the left
                                        return Π(*self.AP, other)
                                    else: return Π(self, other)
    def __and__(self, other):       # PSI, binary '&', conjunction
                                    if type(self).__name__ == "ξ": # ((P & Q) & R) & S, so flatten from the left
                                        return ξ(*self.AP, other)
                                    else: return ξ(self, other)
    def __matmul__(self, other):    return δ(self, other) # delta, binary '@', immediate assignment (permanent)
    def __mod__(self, other):       return Δ(self, other) # DELTA, binary '%', conditional assignment
    def __contains__(self, other):  return SEARCH(other, self)
#----------------------------------------------------------------------------------------------------------------------
class ζ(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __deepcopy__(self, memo): return ζ(self.N)
    def γ(self):
        if not isinstance(self.N, str):
            if callable(self.N): self.N = self.N()
            else: self.N = _globals[str(self.N)]
        else: self.N = _globals[self.N]
        yield from self.N
#----------------------------------------------------------------------------------------------------------------------
class FAIL(PATTERN):
    def __init__(self): super().__init__()
    def γ(self): raise StopIteration # return?
#----------------------------------------------------------------------------------------------------------------------
class ABORT(PATTERN):
    def __init__(self): super().__init__()
    def γ(self): raise Exception() # return?
#----------------------------------------------------------------------------------------------------------------------
class SUCCESS(PATTERN):
    def __init__(self): super().__init__()
    def γ(self):
        while True: yield ""
#----------------------------------------------------------------------------------------------------------------------
class ε(PATTERN): # NULL, epsilon, zero-length string
    def __init__(self): super().__init__()
    def γ(self): yield ""
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
class Θ(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __deepcopy__(self, memo): return Θ(self.N)
    def γ(self):
        global Ϣ, _globals
        if self.N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·');
        logger.info("Θ(%s) SUCCESS", self.N)
        _globals[self.N] = Ϣ[-1].pos
        yield ""
        logger.warning("Θ(%s) backtracking...", self.N)
        del _globals[self.N]
#----------------------------------------------------------------------------------------------------------------------
# Conditional cursor assignment (after successful complete pattern match)
class θ(PATTERN):
    def __init__(self, N): super().__init__(); self.N = N
    def __deepcopy__(self, memo): return θ(self.N)
    def γ(self):
        global Ϣ; self.N = str(self.N)
        if self.N == "OUTPUT":
            Ϣ[-1].nl = True
            print(Ϣ[-1].pos, end='·')
        logger.info("θ(%s) SUCCESS", self.N)
        Ϣ[-1].cstack.append(f"{self.N} = {Ϣ[-1].pos}")
        yield ""
        logger.warning("θ(%s) backtracking...", self.N)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
class δ(PATTERN): # delta, binary '@', SNOBOL4: P $ N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __deepcopy__(self, memo): return δ(copy.deepcopy(self.P), self.N)
    def γ(self):
        global _globals; self.N = str(self.N)
        logger.debug("δ(%s, %s)", pformat(self.P), self.N)
        for _1 in self.P:
            if _1 == "": v = ""
            else: v = Ϣ[-1].subject[_1[0]:_1[1]]
            if self.N == "OUTPUT":
                Ϣ[-1].nl = True
                print(v, end='·')
            logger.debug("%s = δ(%r)", self.N, v)
            _globals[self.N] = v
            yield _1
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
class Λ(PATTERN): # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    def __init__(self, expression): super().__init__(); self.expression = expression
    def __deepcopy__(self, memo): return Λ(self.expression)
    def γ(self):
        global _globals
        match type(self.expression).__name__:
            case 'str':
                logger.debug("Λ(%r) evaluating...", self.expression)
                try:
                    if eval(self.expression, _globals):
                        logger.info("Λ(%r) SUCCESS", self.expression)
                        yield ""
                        logger.warning("Λ(%r) backtracking...", self.expression)
                    else: logger.warning("Λ(%r) FAIL!", self.expression)
                except Exception as e:
                    logger.error("Λ(%r) EXCEPTION evaluating. (%r) FAIL!", self.expression, e)
            case 'function':
                logger.debug("Λ(function) evaluating...")
                try:
                    if self.expression():
                        logger.info("Λ(function) SUCCESS")
                        yield ""
                        logger.warning("Λ(function) backtracking...")
                    else: logger.warning("Λ(function) FAIL!")
                except Exception as e:
                    logger.error("Λ(function) EXCEPTION evaluating. (%r) FAIL!", e)
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
class Δ(PATTERN): # DELTA, binary '%', SNOBOL4: P . N
    def __init__(self, P:PATTERN, N): super().__init__(); self.P:PATTERN = P; self.N = N
    def __deepcopy__(self, memo): return Δ(copy.deepcopy(self.P), self.N)
    def γ(self):
        global Ϣ; self.N = str(self.N)
        logger.debug("Δ(%s, %s)", pformat(self.P), self.N)
        for _1 in self.P:
            logger.info("%s = Δ(%r) SUCCESS", self.N, _1)
            if self.N == "OUTPUT":
                if _1 == "":
                    Ϣ[-1].cstack.append(f"print('')")
                else: Ϣ[-1].cstack.append(f"print(Ϣ[-1].subject[{_1[0]}:{_1[1]}])")
            else:
                if _1 == "":
                    Ϣ[-1].cstack.append(f"{self.N} = ''")
                else: Ϣ[-1].cstack.append(f"{self.N} = Ϣ[-1].subject[{_1[0]}:{_1[1]}]")
            yield _1
            logger.warning("%s = Δ(%r) backtracking...", self.N, _1)
            Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
class λ(PATTERN): # LAMBDA, P . *exec(), P . tx . *func(tx)
    def __init__(self, command): super().__init__(); self.command = command
    def __deepcopy__(self, memo): return λ(self.command)
    def γ(self):
        global Ϣ
        logger.debug("λ(%r) compiling...", self.command)
        if self.command:
            if compile(self.command, '<string>', 'exec'): # 'single', 'eval'
                logger.info("λ(%r) SUCCESS", self.command)
                Ϣ[-1].cstack.append(self.command)
                yield ""
                logger.warning("λ(%r) backtracking...", self.command)
                Ϣ[-1].cstack.pop()
            else: logger.error("λ(%r) Error compiling. FAIL", self.command)
        else: yield ""
#----------------------------------------------------------------------------------------------------------------------
class nPush(PATTERN):
    def __init__(self): super().__init__()
    def γ(self):
        global Ϣ
        logger.info("nPush() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop += 1");
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.append(0)");
        yield "";
        logger.warning("nPush() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nInc(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        global Ϣ
        logger.info("nInc() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack[Ϣ[-1].itop] += 1");
        yield "";
        logger.warning("nInc() backtracking...")
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class nPop(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        global Ϣ
        logger.info("nPop() SUCCESS")
        Ϣ[-1].cstack.append(f"Ϣ[-1].istack.pop()");
        Ϣ[-1].cstack.append(f"Ϣ[-1].itop -= 1");
        yield "";
        logger.warning("nPop() backtracking...")
        Ϣ[-1].cstack.pop()
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Shift(PATTERN):
    def __init__(self, t=None, v=None): super().__init__(); self.t = t; self.v = v
    def __deepcopy__(self, memo): return Shift(self.t, self.v)
    def γ(self):
        global Ϣ
        logger.info("Shift(%r, %r) SUCCESS", self.t, self.v)
        if self.t is None:   Ϣ[-1].cstack.append(f"Ϣ[-1].shift()")
        elif self.v is None: Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}')")
        else:                Ϣ[-1].cstack.append(f"Ϣ[-1].shift('{self.t}', {self.v})")
        yield ""
        logger.warning("Shift(%r, %r) backtracking...", self.t, self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Reduce(PATTERN):
    def __init__(self, t, n=-1): super().__init__(); self.t = t; self.n = n
    def __deepcopy__(self, memo): return Reduce(self.t, self.n)
    def γ(self):
        global Ϣ
        if type(self.t).__name__ == 'function': self.t = self.t()
        logger.info("Reduce(%r, %r) SUCCESS", self.t, self.n)
        if   self.n == -2: self.n = "Ϣ[-1].istack[Ϣ[-1].itop + 1]"
        elif self.n == -1: self.n = "Ϣ[-1].istack[Ϣ[-1].itop]"
        Ϣ[-1].cstack.append(f"Ϣ[-1].reduce('{self.t}', {self.n})")
        yield ""
        logger.warning("Reduce(%r, %r) backtracking...", self.t, self.n)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class Pop(PATTERN):
    def __init__(self, v): super().__init__(); self.v = v
    def __deepcopy__(self, memo): return Pop(self.v)
    def γ(self):
        global Ϣ
        logger.info("Pop(%s) SUCCESS", self.v)
        Ϣ[-1].cstack.append(f"{self.v} = Ϣ[-1].pop()")
        yield ""
        logger.warning("Pop(%s) backtracking...", self.v)
        Ϣ[-1].cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
class FENCE(PATTERN): # FENCE and FENCE(P)
    def __init__(self, P:PATTERN=None): super().__init__(); self.P:PATTERN = P
    def __deepcopy__(self, memo): return FENCE(copy.deepcopy(self.P))
    def γ(self):
        if self.P:
            logger.info("FENCE(%s) SUCCESS", pformat(self.P))
            yield from self.P
            logger.warning("FENCE(%s) backtracking...", pformat(self.P))
        else:
            logger.info("FENCE() SUCCESS")
            yield ""
            logger.warning("FENCE() backtracking...")
#----------------------------------------------------------------------------------------------------------------------
class POS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __deepcopy__(self, memo): return POS(self.n)
    def γ(self):
        global Ϣ
        if not isinstance(self.n, int):
            if callable(self.n): self.n = int(self.n())
            else: self.n = int(self.n)
        if Ϣ[-1].pos == self.n:
            logger.info("POS(%d) SUCCESS(%d,%d)=", self.n, Ϣ[-1].pos, 0)
            yield ""
            logger.warning("POS(%d) backtracking...", self.n)
#----------------------------------------------------------------------------------------------------------------------
class RPOS(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __deepcopy__(self, memo): return RPOS(self.n)
    def γ(self):
        global Ϣ
        if not isinstance(self.n, int):
            if callable(self.n): self.n = int(self.n())
            else: self.n = int(self.n)
        if Ϣ[-1].pos == len(Ϣ[-1].subject) - self.n:
            logger.info("RPOS(%d) SUCCESS(%d,%d)=", self.n, Ϣ[-1].pos, 0)
            yield ""
            logger.warning("RPOS(%d) backtracking...", self.n)
#----------------------------------------------------------------------------------------------------------------------
class α(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        global Ϣ
        if (Ϣ[-1].pos == 0) or \
           (Ϣ[-1].pos > 0 and Ϣ[-1].subject[Ϣ[-1].pos-1:Ϣ[-1].pos] == '\n'):
            yield ""
#----------------------------------------------------------------------------------------------------------------------
class ω(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        global Ϣ
        if (Ϣ[-1].pos == len(Ϣ[-1].subject)) or \
           (Ϣ[-1].pos < len(Ϣ[-1].subject) and Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + 1] == '\n'):
           yield ""
#----------------------------------------------------------------------------------------------------------------------
class LEN(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __deepcopy__(self, memo): return LEN(self.n)
    def γ(self):
        global Ϣ
        if not isinstance(self.n, int):
            if callable(self.n): self.n = int(self.n())
            else: self.n = int(self.n)
        if Ϣ[-1].pos + self.n <= len(Ϣ[-1].subject):
            logger.info("LEN(%d) SUCCESS(%d,%d)=%s", self.n, Ϣ[-1].pos, self.n, Ϣ[-1].subject[Ϣ[-1].pos:Ϣ[-1].pos + self.n])
            Ϣ[-1].pos += self.n
            yield (Ϣ[-1].pos - self.n, Ϣ[-1].pos)
            Ϣ[-1].pos -= self.n
            logger.warning("LEN(%d) backtracking(%d)...", self.n, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class σ(PATTERN): # sigma, σ, sequence of characters, literal string patttern
    def __init__(self, s): super().__init__(); self.s = s
    def __deepcopy__(self, memo): return σ(self.s)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        if not isinstance(self.s, str):
            if callable(self.s): self.s = str(self.s())
            else: self.s = str(self.s)
        logger.debug("σ(%r) trying(%d)", self.s, pos0)
        if pos0 + len(self.s) <= len(Ϣ[-1].subject):
            if self.s == Ϣ[-1].subject[pos0:pos0 + len(self.s)]:
                logger.info("σ(%r) SUCCESS(%d,%d)=", self.s, Ϣ[-1].pos, len(self.s))
                Ϣ[-1].pos += len(self.s)
                yield (pos0, Ϣ[-1].pos)
                Ϣ[-1].pos -= len(self.s)
                logger.warning("σ(%r) backtracking(%d)...", self.s, Ϣ[-1].pos)
        return None
#----------------------------------------------------------------------------------------------------------------------
# Regular Expression pattern matching
import re
_rexs = dict()
class Φ(PATTERN):
    def __init__(self, rex): super().__init__(); self.rex = rex
    def __deepcopy__(self, memo): return Φ(self.rex)
    def γ(self):
        global Ϣ, _rexs
        if not isinstance(self.rex, str):
            if callable(self.rex): self.rex = str(self.rex())
            else: self.rex = str(self.rex)
        if self.rex not in _rexs:
            _rexs[self.rex] = re.compile(self.rex, re.MULTILINE)
        if matches := _rexs[self.rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
            pos0 = Ϣ[-1].pos
            if pos0 == matches.start():
                Ϣ[-1].pos = matches.end()
                for (N, V) in matches.groupdict().items():
                    _globals[N] = V
                yield (pos0, Ϣ[-1].pos)
                Ϣ[-1].pos = pos0
            else: raise Exception("Yikes! Internal error.")
#----------------------------------------------------------------------------------------------------------------------
class φ(PATTERN):
    def __init__(self, rex): super().__init__(); self.rex = rex
    def __deepcopy__(self, memo): return φ(self.rex)
    def γ(self):
        global Ϣ, _rexs
        if not isinstance(self.rex, str):
            if callable(self.rex): self.rex = str(self.rex())
            else: self.rex = str(self.rex)
        if self.rex not in _rexs:
            _rexs[self.rex] = re.compile(self.rex, re.MULTILINE)
        if matches := _rexs[self.rex].match(Ϣ[-1].subject, pos = Ϣ[-1].pos, endpos = len(Ϣ[-1].subject)):
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
class ψ(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        print("Yikes! ψ()")
        yield ""
#----------------------------------------------------------------------------------------------------------------------
class Ψ(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        print("Yikes! Ψ()")
        yield ""
#----------------------------------------------------------------------------------------------------------------------
class Ϙ(PATTERN):
    def __init__(self): super().__init__();
    def γ(self):
        print("Yikes! Ϙ()")
        yield ""
#----------------------------------------------------------------------------------------------------------------------
class TAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __deepcopy__(self, memo): return TAB(self.n)
    def γ(self):
        global Ϣ
        if not isinstance(self.n, int):
            if callable(self.n): self.n = int(self.n())
            else: self.n = int(self.n)
        if self.n <= len(Ϣ[-1].subject):
            if self.n >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = self.n
                yield (pos0, self.n)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class RTAB(PATTERN):
    def __init__(self, n): super().__init__(); self.n = n
    def __deepcopy__(self, memo): return RTAB(self.n)
    def γ(self):
        global Ϣ
        if not isinstance(self.n, int):
            if callable(self.n): self.n = int(self.n())
            else: self.n = int(self.n)
        if self.n <= len(Ϣ[-1].subject):
            self.n = len(Ϣ[-1].subject) - self.n
            if n >= Ϣ[-1].pos:
                pos0 = Ϣ[-1].pos
                Ϣ[-1].pos = self.n
                yield (pos0, self.n)
                Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class REM(PATTERN):
    def __init__(self): super().__init__()
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        Ϣ[-1].pos = len(Ϣ[-1].subject)
        yield (pos0, Ϣ[-1].pos)
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class ANY(PATTERN):
    def __init__(self, characters): super().__init__(); self.characters = characters
    def __deepcopy__(self, memo): return ANY(self.characters)
    def γ(self):
        global Ϣ
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("ANY(%r) trying(%d)", self.characters, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                logger.info("ANY(%r) SUCCESS(%d,%d)=%s", self.characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield (Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
                logger.warning("ANY(%r) backtracking(%d)...", self.characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class NOTANY(PATTERN):
    def __init__(self, characters): super().__init__(); self.characters = characters
    def __deepcopy__(self, memo): return NOTANY(self.characters)
    def γ(self):
        global Ϣ
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("NOTANY(%r) trying(%d)", self.characters, Ϣ[-1].pos)
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            if not Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                logger.info("NOTANY(%r) SUCCESS(%d,%d)=%s", self.characters, Ϣ[-1].pos, 1, Ϣ[-1].subject[Ϣ[-1].pos])
                Ϣ[-1].pos += 1
                yield (Ϣ[-1].pos - 1, Ϣ[-1].pos)
                Ϣ[-1].pos -= 1
                logger.warning("NOTANY(%r) backtracking(%d)...", self.characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class SPAN(PATTERN):
    def __init__(self, characters): super().__init__(); self.characters:str = characters
    def __deepcopy__(self, memo): return SPAN(self.characters)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("SPAN(%r) trying(%d)", self.characters, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos > pos0:
            logger.info("SPAN(%r) SUCCESS(%d,%d)=%s", self.characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield (pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
            logger.warning("SPAN(%r) backtracking(%d)...", self.characters, Ϣ[-1].pos)
        return None
#----------------------------------------------------------------------------------------------------------------------
class BREAK(PATTERN):
    def __init__(self, characters): super().__init__(); self.characters:str = characters
    def __deepcopy__(self, memo): return BREAK(self.characters)
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        if not isinstance(self.characters, str):
            if not isinstance(self.characters, set):
                if callable(self.characters):
                    self.characters = self.characters()
                else: self.characters = str(self.characters)
        logger.debug("BREAK(%r) SUCCESS(%d)", self.characters, pos0)
        while True:
            if Ϣ[-1].pos >= len(Ϣ[-1].subject): break
            if not Ϣ[-1].subject[Ϣ[-1].pos] in self.characters:
                Ϣ[-1].pos += 1
            else: break
        if Ϣ[-1].pos < len(Ϣ[-1].subject):
            logger.info("BREAK(%r) SUCCESS(%d,%d)=%s", self.characters, pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
            yield (pos0, Ϣ[-1].pos)
            Ϣ[-1].pos = pos0
            logger.warning("BREAK(%r) backtracking(%d)...", self.characters, Ϣ[-1].pos)
#----------------------------------------------------------------------------------------------------------------------
class BREAKX(BREAK): pass
#----------------------------------------------------------------------------------------------------------------------
class ARB(PATTERN): # ARB
    def __init__(self): super().__init__()
    def γ(self):
        global Ϣ; pos0 = Ϣ[-1].pos
        while Ϣ[-1].pos <= len(Ϣ[-1].subject):
            yield (pos0, Ϣ[-1].pos)
            Ϣ[-1].pos += 1
        Ϣ[-1].pos = pos0
#----------------------------------------------------------------------------------------------------------------------
class MARB(ARB): pass
#----------------------------------------------------------------------------------------------------------------------
class BAL(PATTERN): # BAL
    def __init__(self): super().__init__()
    def γ(self):
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
class ξ(PATTERN): # PSI, AND, conjunction
    def __init__(self, P:PATTERN, Q:PATTERN): super().__init__(); self.P = P; self.Q = Q
    def __deepcopy__(self, memo): return ξ(copy.deepcopy(self.P), copy.deepcopy(self.Q))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        for _1 in self.P:
            pos1 = Ϣ[-1].pos
            try:
                Ϣ[-1].pos = pos0
                next(self.Q)
                if (Ϣ[-1].pos == pos1):
                    yield _1
                    Ϣ[-1].pos = pos0
            except StopIteration:
                Ϣ[-1].pos = pos0
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class π(PATTERN): # pi, optional, SNOBOL4: P | epsilon
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __deepcopy__(self, memo): return π(copy.deepcopy(self.P))
    def γ(self):
        Ϣ[-1].depth += 1
        yield from self.P
        yield ""
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class Π(PATTERN): # PI, Π, alternates, alternatives, SNOBOL4: P | Q | R | S | ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __deepcopy__(self, memo): return Π(*(copy.deepcopy(P) for P in self.AP))
    def γ(self):
        global Ϣ
        logger.debug("Π(%s) trying(%d)...", ", ".join([pformat(P) for P in self.AP]), Ϣ[-1].pos)
        Ϣ[-1].depth += 1
        for P in self.AP: yield from P
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class Σ(PATTERN): # SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
    def __init__(self, *AP:PATTERN): super().__init__(); self.AP = AP
    def __deepcopy__(self, memo): return Σ(*(copy.deepcopy(P) for P in self.AP))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        logger.debug("Σ(%s) trying(%d)...", ", ".join([pformat(P) for P in self.AP]), pos0)
        highmark = 0
        cursor = 0
        while cursor >= 0:
            if cursor >= len(self.AP):
                logger.info("Σ(*) SUCCESS(%d,%d)=%s", pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield (pos0, Ϣ[-1].pos)
                logger.warning("Σ(*) backtracking(%d)...", pos0)
                cursor -= 1
            if cursor >= highmark:
                iter(self.AP[cursor])
                highmark += 1
            try:
                next(self.AP[cursor])
                cursor += 1
            except StopIteration:
                highmark -= 1
                cursor -= 1
        Ϣ[-1].depth -= 1
#----------------------------------------------------------------------------------------------------------------------
class ARBNO(PATTERN):
    def __init__(self, P:PATTERN): super().__init__(); self.P = P
    def __deepcopy__(self, memo): return ARBNO(copy.deepcopy(self.P))
    def γ(self):
        global Ϣ; Ϣ[-1].depth += 1; pos0 = Ϣ[-1].pos
        logger.debug("ARBNO(%s) trying(%d)...", pformat(self.P), pos0)
        highmark = 0
        cursor = 0
        AP = []
        while cursor >= 0:
            if cursor >= len(AP):
                logger.info("ARBNO(%s) SUCCESS(%d,%d)=%s", pformat(self.P), pos0, Ϣ[-1].pos - pos0, Ϣ[-1].subject[pos0:Ϣ[-1].pos])
                yield (pos0, Ϣ[-1].pos)
                logger.warning("ARBNO(%s) backtracking(%d)...", pformat(self.P), pos0)
            if cursor >= highmark:
                AP.append((Ϣ[-1].pos, copy.deepcopy(self.P)))
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
class MARBNO(ARBNO): pass
#----------------------------------------------------------------------------------------------------------------------
def _push(lyst): Ϣ[-1].vstack.append(lyst)
def _pop(): return Ϣ[-1].vstack.pop()
#----------------------------------------------------------------------------------------------------------------------
def _shift(t='', v=None):
    global _globals
    if v is None:
        _push([t])
    else: _push([t, v])
#----------------------------------------------------------------------------------------------------------------------
def _reduce(t, n):
    global _globals
    if n == 0 and t == 'Σ':
        _push(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ξ', 'snoExprList', '|', '..'):
        x = [t]
        for i in range(n):
            x.insert(1, _pop())
        _push(x)
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
        global Ϣ, _window
        original_message = super().format(record)
        if len(Ϣ) > 0:
            formatted_message = "{0:s} {1:s}{2:s}".format(self.window(_window // 2), '  ' * Ϣ[-1].depth, original_message)
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
_window = 24
_globals = None # global variables
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
def GLOBALS(g:dict): global _globals; _globals = g; _globals['Ϣ'] = Ϣ
def TRACE(level:int=None, window:int=None):
    global _window, logger, handler
    if window is not None:
        _window = window
    if level is not None:
        logger.setLevel(level)
        handler.setLevel(level)
#----------------------------------------------------------------------------------------------------------------------
def MATCH     (string:str, P:PATTERN) -> bool: return SEARCH(string, POS(0) + P)
def FULLMATCH (string:str, P:PATTERN) -> bool: return SEARCH(string, POS(0) + P + RPOS(0))
def SEARCH    (string:str, P:PATTERN) -> bool:
    global _globals, Ϣ
    if _globals is None:
        _globals = globals()
    command = None
    result = None
    Ϣ.append(None)
    for cursor in range(0, 1+len(string)):
        TRY = copy.deepcopy(P)
        iter(TRY)
        try:
            Ϣ[-1] = SNOBOL(cursor, string)
            m = next(TRY)
            if Ϣ[-1].nl: print()
            logger.info(f'SEARCH(): "{string}" ? "{m}"')
            for command in Ϣ[-1].cstack:
                logger.debug('SEARCH(): %r', command)
            try:
                _globals['Ϣ'] = Ϣ
                for command in Ϣ[-1].cstack:
                    exec(command, _globals)
                result = True
            except Exception as e:
                logger.error("SEARCH(): Exception: %r, command: %r", e, command)
                result = False
            break
        except StopIteration:
            if Ϣ[-1].nl: print()
        except Exception as e:
            logger.critical("SEARCH(): Yikes: %r", e)
    Ϣ.pop()
    return result
#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import SNOBOL4functions
    from SNOBOL4functions import ALPHABET, DIGITS, LCASE, UCASE
    TRACE(level=50, window=32)
    if "SNOBOL4" in POS(0) + (SPAN("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "SNOBOL4" in POS(0) + (BREAK("0123456789") + σ('4')) % "name" + RPOS(0):
        print(name)
    if "001_01C717AB.5C51AFDE ..." in φ(r"(?P<name>[0-9]{3}(_[0-9A-F]{4})?_[0-9A-F]{8}\.[0-9A-F]{8})"):
        print(name)
#----------------------------------------------------------------------------------------------------------------------
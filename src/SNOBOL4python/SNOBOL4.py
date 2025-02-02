# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#>python3 src/SNOBOL4python/SNOBOL4.py
#>python3 -m build
#>python3 -m pip install .\dist\snobol4python-0.1.0.tar.gz
#>python3 tests/test_01.py
#------------------------------------------------------------------------------
# String pattern matching
import copy
class PATTERN(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = copy.copy(args)
        self.kwargs = copy.copy(kwargs)
        self.local_copy = self.func(*self.args, **self.kwargs)
    def __iter__(self):
        self.local_copy = self.func(*self.args, **self.kwargs)
        return self.local_copy
    def __next__(self): return next(self.local_copy)
    def __repr__(self): return f"{self.func}(*{len(self.args)})"
    def __add__(self, other):       return Σ(self, other) # SIGMA, binary '+', subsequent
    def __radd__(self, other):      return Σ(other, self) # SIGMA, binary '+', subsequent
    def __or__(self, other):        return Π(self, other) # PI, binary '|', alternate
    def __ror__(self, other):       return Π(other, self) # PI, binary '|', alternate
    def __and__(self, other):       return Ξ(self, other) # PSI, binary '&', conjunction
    def __rand__(self, other):      return Ξ(other, self) # PSI, binary '&', conjunction
    def __matmul__(self, other):    return δ(self, other) # delta, binary '@', immediate assignment
    def __xor__(self, other):       return Δ(self, other) # DELTA, binary '^', conditional assignment
    def __invert__(self):           return self # unary '~'
#------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    return lambda *args, **kwargs: PATTERN(func, args, kwargs)
#------------------------------------------------------------------------------
pos = 0 # internal position
subject = "" # internal subject
#------------------------------------------------------------------------------
_ALPHABET = "".join([chr(c) for c in range(256)])
_UCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LCASE = "abcdefghijklmnopqrstuvwxyz"
_digits = "0123456789"
def CHAR(n: int) -> str: return chr(n)
def ASCII(c: str) -> int: return ord(c)
def SIZE(o: object) -> int: return len(o)
def DUPL(s: str, n: int) -> str: return s * n
def LPAD(s: str, n: int) -> str: return ' ' * (n - len(s)) + s
def RPAD(s: str, n: int) -> str: return s + ' ' * (n - len(s))
def TRIM(s: str) -> str: return s.strip()
def REVERSE(s: str) -> str: return s.reverse() # s[::-1]
def DATATYPE(o: object) -> str: None
def REPLACE(s: str, old: str, new: str) -> str: return s.translate(str.maketrans(old, new))
#------------------------------------------------------------------------------
def FAIL() -> None: raise StopIteration # return?
def ABORT() -> None: raise StopIteration # return?
def SUCCESS():
    while True: yield ""
#------------------------------------------------------------------------------
@pattern
def ε() -> PATTERN: yield "" # NULL, epsilon, zero-length string
#------------------------------------------------------------------------------
itop = -1 # counter stack (nPush, nInc, nPop, nTop)
istack = []
vstack = [] # value stack (Shift/Reduce values)
cstack = [] # command stack (conditional actions)
#------------------------------------------------------------------------------
# Immediate actions during pattern matching
@pattern
def δ(P, V) -> PATTERN: # immediate assignment
    for _1 in P:
        if V == "OUTPUT": print(_1)
        globals()[V] = _1
        yield _1
        del globals()[V]

@pattern # immediate evaluation as test
def λ(expression) -> PATTERN: # P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    if eval(expression): yield ""
#------------------------------------------------------------------------------
# Conditional actions after successful pattern match
@pattern
def Δ(P, V) -> PATTERN: # conditional assignment
    for _1 in P:
        cstack.append(f"{V} = subject[{pos - len(_1)} : {pos}]\n")
        yield _1
        cstack.pop()

@pattern # conditional execution
def Λ(command) -> PATTERN: # P . *exec(), P . tx . *func(tx)
    if compile(command):
        cstack.append(command + '\n')
        yield ""
        cstack.pop()
#------------------------------------------------------------------------------
@pattern
def nPush() -> PATTERN:
    cstack.append(f"itop += 1\n");
    cstack.append(f"istack.append(0)\n");
    yield "";
    cstack.pop()
@pattern
def nInc() -> PATTERN:
    cstack.append(f"istack[itop] += 1\n");
    yield "";
    cstack.pop()
@pattern
def nPop() -> PATTERN:
    cstack.append(f"istack.pop()\n");
    cstack.append(f"itop -= 1\n");
    yield "";
    cstack.pop()
@pattern
def Shift(t, v) -> PATTERN:
    cstack.append(f"Shift('{t}', \"{v}\")\n")
    yield ""
    cstack.pop()
@pattern
def Reduce(t, n) -> PATTERN:
    if n is None: n = istack[itop]
    cstack.append(f"Reduce('{t}', {n})\n")
    yield ""
    cstack.pop()
#------------------------------------------------------------------------------
def IDENT(x, y) -> str:
    if x is y: return ""
def DIFFER(x, y) -> str:
    if not x is y: yield ""
def INTEGER(x) -> PATTERN: # *INTEGER()
    try:
        int(x)
        yield ""
    except ValueError:
        return
#------------------------------------------------------------------------------
@pattern
def FENCE(P=None) -> PATTERN: # FENCE and FENCE(P)
    if P: yield from P
    else: yield ""
#------------------------------------------------------------------------------
@pattern
def POS(n) -> PATTERN:
    global pos
    if pos == n:
#       print(f">>> POS({n})")
        yield ""
#       print(f"<<< POS({n})")
#------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global pos, subject
    if pos == len(subject) - n:
#       print(f">>> RPOS({n})")
        yield ""
#       print(f"<<< RPOS({n})")
#------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global pos, subject
    if pos + n <= len(subject):
        pos += n
        yield subject[pos - n:pos]
        pos -= n
#------------------------------------------------------------------------------
@pattern
def σ(s) -> PATTERN: # sigma, sequence of characters, literal string patttern
    global pos, subject
    if pos + len(s) <= len(subject):
        if s == subject[pos:pos + len(s)]:
            pos += len(s)
            print(f">>> σ({s}) = {pos - len(s)}, {len(s)}")
            yield s
            print(f"<<< σ({s})")
            pos -= len(s)
#------------------------------------------------------------------------------
@pattern
def TAB(n) -> PATTERN:
    global pos, subject
    if n <= len(subject):
        if n >= pos:
            pos0 = pos
            pos = n
            yield subject[pos0:n]
            pos = pos0
#------------------------------------------------------------------------------
@pattern
def RTAB(n) -> PATTERN:
    global pos, subject
    if n <= len(subject):
        n = len(subject) - n
        if n >= pos:
            pos0 = pos
            pos = n
            yield subject[pos0:n]
            pos = pos0
#------------------------------------------------------------------------------
@pattern
def REM() -> PATTERN:
    global pos, subject
    pos0 = pos
    pos = len(subject)
    yield subject[pos0:]
    pos = pos0
#------------------------------------------------------------------------------
@pattern
def ANY(characters) -> PATTERN:
    global pos, subject
    if pos < len(subject):
        if subject[pos] in characters:
            pos += 1
            yield subject[pos - 1]
            pos -= 1
#------------------------------------------------------------------------------
@pattern
def NOTANY(characters) -> PATTERN:
    global pos, subject
    if pos < len(subject):
        if not subject[pos] in characters:
            pos += 1
            yield subject[pos - 1]
            pos -= 1
#------------------------------------------------------------------------------
@pattern
def SPAN(characters) -> PATTERN:
    global pos, subject
    pos0 = pos
    while True:
        if pos >= len(subject): break
        if subject[pos] in characters:
            pos += 1
        else: break
    if pos > pos0:
        yield subject[pos0:pos]
        pos = pos0
#------------------------------------------------------------------------------
@pattern
def BREAK(characters) -> PATTERN:
    global pos, subject
    pos0 = pos
    while True:
        if pos >= len(subject): break
        if not subject[pos] in characters:
            pos += 1
        else: break
    if pos < len(subject):
        yield subject[pos0:pos]
        pos = pos0
#------------------------------------------------------------------------------
@pattern
def ARB() -> PATTERN: # ARB
    global pos, subject
    pos0 = pos
    while pos <= len(subject):
        yield subject[pos0 : pos]
        pos += 1
    pos = pos0
#------------------------------------------------------------------------------
@pattern
def BAL() -> PATTERN: # BAL
    global pos, subject
    pos0 = pos
    nest = 0
    pos += 1
    while pos <= len(subject):
        ch = subject[pos - 1 : pos]
        match ch:
            case '(': nest += 1
            case ')': nest -= 1
        if nest < 0: break
        elif nest > 0 and pos >= len(subject): break
        elif nest == 0: yield subject[pos0 : pos]
        pos += 1
    pos = pos0
#------------------------------------------------------------------------------
@pattern
def ARBNO(P) -> PATTERN:
    global pos, subject
    pos0 = pos
    yield ""
    while True:
        try:
            iter(P)
            next(P)
            yield subject[pos0:pos]
        except StopIteration:
            pos = pos0
            return
#------------------------------------------------------------------------------
@pattern
def Ξ(P, Q) -> PATTERN: # PSI, AND, conjunction
    global pos
    pos0 = pos
    for _1 in P:
        pos1 = pos
        try:
            pos = pos0
            next(Q)
            if (pos == pos1):
                yield _1
                pos = pos0
        except StopIteration:
            pos = pos0
#------------------------------------------------------------------------------
@pattern
def π(P) -> PATTERN: # (P | epsilon), pi, optional
    yield from P
    yield ""
#------------------------------------------------------------------------------
@pattern
def Π(*AP) -> PATTERN: # ALT, PI, alternates
    for P in AP:
        yield from P
#------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SEQ, SIGMA, subsequents
    pos0 = pos
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
                yield subject[pos0:pos]
                cursor -= 1
        except StopIteration:
            cursor -= 1
            highmark -= 1
#------------------------------------------------------------------------------
def SEARCH(S, P) -> bool: None
def MATCH(S, P) -> bool:
    global pos, subject
    pos = 0
    itop = -1
    istack = []
    cstack = []
    vstack = []
    subject = S
    try:
        m = next(P)
        print(f'"{S}" ? "{m}"')
        print(cstack)
        return True
    except StopIteration:
        print(f'"{S}" FAIL')
        return False
def FULLMATCH(S, P) -> bool: None
#------------------------------------------------------------------------------

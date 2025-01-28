# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#>python3 src/SNOBOL4python/SNOBOL4.py
#>python -m build
#>python -m pip install .\dist\snobol4python-0.1.0.tar.gz
#>python3 tests/test01.py
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
    def __add__(self, other):       return SEQ(self, other) # binary '+'
    def __radd__(self, other):      return SEQ(other, self) # binary '+'
    def __or__(self, other):        return ALT(self, other) # binary '|'
    def __ror__(self, other):       return ALT(other, self) # binary '|'
    def __and__(self, other):       return AND(self, other) # binary '&'
    def __rand__(self, other):      return AND(other, self) # binary '&'
    def __matmul__(self, other):    return assign(self, other) # binary '@'
    def __xor__(self, other):       return self # binary '^'
    def __invert__(self):           return self # unary '~'
#------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    return lambda *args, **kwargs: PATTERN(func, args, kwargs)
#------------------------------------------------------------------------------
# Built-in pattern matching
pos = 0
subject = ""

_ALPHABET = [c for c in range(256)]
_UCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LCASE = "abcdefghijklmnopqrstuvwxyz"
_digits = "0123456789"
#------------------------------------------------------------------------------
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
def FAIL() -> None: raise StopIteration
def ABORT() -> None: raise StopIteration
def SUCCESS():
    while True: yield ""
#------------------------------------------------------------------------------
def _(s) -> PATTERN: return LIT(s)
@pattern
def ε() -> PATTERN: yield "" # NULL, epsilon, zero-length string
@pattern
def FENCE(p) -> PATTERN:
    yield next(p)
@pattern
def IDENT(x, y) -> PATTERN: # *IDENT()
    if x is y: yield ""
@pattern
def DIFFER(x, y) -> PATTERN: # *DIFFER()
    if not x is y: yield ""
def INTEGER(x) -> PATTERN: # *INTEGER()
    try:
        int(x)
        yield ""
    except ValueError:
        return
#------------------------------------------------------------------------------
@pattern
def EQ(x, y) -> PATTERN: # *EQ()
    if int(x) == int(y): yield ""
    else: return
@pattern
def LT(x, y) -> PATTERN: # *LT()
    if int(x) < int(y): yield ""
    else: return
@pattern
def GT(x, y) -> PATTERN: # *GT()
    if int(x) > int(y): yield ""
    else: return
@pattern
def NE(x, y) -> PATTERN: # *NE()
    if int(x) != int(y): yield ""
    else: return
@pattern
def LE(x, y) -> PATTERN: # *LE()
    if int(x) <= int(y): yield ""
    else: return
@pattern
def GE(x, y) -> PATTERN: # *GE()
    if int(x) >= int(y): yield ""
    else: return
#------------------------------------------------------------------------------
@pattern
def LEQ(x, y) -> PATTERN: # *EQ()
    if str(x) == str(y): yield ""
    else: return
@pattern
def LLT(x, y) -> PATTERN: # *LT()
    if str(x) < str(y): yield ""
    else: return
@pattern
def LGT(x, y) -> PATTERN: # *GT()
    if str(x) > str(y): yield ""
    else: return
@pattern
def LNE(x, y) -> PATTERN: # *NE()
    if str(x) != str(y): yield ""
    else: return
@pattern
def LLE(x, y) -> PATTERN: # *LE()
    if str(x) <= str(y): yield ""
    else: return
@pattern
def LGE(x, y) -> PATTERN: # *GE()
    if str(x) >= str(y): yield ""
    else: return
#------------------------------------------------------------------------------
@pattern
def eq(x, y) -> PATTERN: # *(x == y)
    if x == y: yield ""
    else: return
@pattern
def lt(x, y) -> PATTERN: # *(x < y)
    if x < y: yield ""
    else: return
@pattern
def gt(x, y) -> PATTERN: # *(x > y)
    if x > y: yield ""
    else: return
@pattern
def ne(x, y) -> PATTERN: # *(x != y)
    if x != y: yield ""
    else: return
@pattern
def le(x, y) -> PATTERN: # *(x <= y)
    if x <= y: yield ""
    else: return
@pattern
def ge(x, y) -> PATTERN: # *(x >= y)
    if x >= y: yield ""
    else: return
#------------------------------------------------------------------------------
@pattern
def assign(P, V) -> PATTERN:
    for _1 in P:
        if V == "OUTPUT": print(_1)
        globals()[V] = _1
        yield _1
        del globals()[V]
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
def LIT(s) -> PATTERN:
    global pos, subject
    if pos + len(s) <= len(subject):
        if s == subject[pos:pos + len(s)]:
            pos += len(s)
#           print(f">>> LIT({lit}) = {pos - len(lit)}, {len(lit)}")
            yield s
#           print(f"<<< LIT({lit})")
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
def AND(P, Q) -> PATTERN:
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
def ALT(*AP) -> PATTERN:
    for P in AP:
        yield from P
#------------------------------------------------------------------------------
@pattern
def SEQ(*AP) -> PATTERN:
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
def MATCH(S, P) -> bool:
    global pos, subject
    pos = 0
    subject = S
    try:
        m = next(P)
        print(f'"{S}" ? "{m}"')
        return True
    except StopIteration:
        print(f'"{S}" FAIL')
        return False
#------------------------------------------------------------------------------
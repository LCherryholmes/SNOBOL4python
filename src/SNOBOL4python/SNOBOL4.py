# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#>python src/SNOBOL4python/SNOBOL4.py
#>python -m build
#>python -m pip install .\dist\snobol4python-0.1.0.tar.gz
#>python tests/test_01.py
#>python tests/test_json.py
#------------------------------------------------------------------------------
import logging
logging.basicConfig(level=logging.DEBUG)
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
    def __next__(self):             return next(self.local_copy)
    def __repr__(self):             return f"{self.func}(*{len(self.args)})"
    def __add__(self, other):       return Σ(self, other) # SIGMA, binary '+', subsequent
    def __radd__(self, other):      return Σ(other, self) # SIGMA, binary '+', subsequent
    def __or__(self, other):        return Π(self, other) # PI, binary '|', alternate
    def __ror__(self, other):       return Π(other, self) # PI, binary '|', alternate
    def __and__(self, other):       return Ξ(self, other) # PSI, binary '&', conjunction
    def __rand__(self, other):      return Ξ(other, self) # PSI, binary '&', conjunction
    def __matmul__(self, other):    return δ(self, other) # delta, binary '@', immediate assignment
    def __xor__(self, other):       return Δ(self, other) # DELTA, binary '^', conditional assignment
    def __floordiv__(self, other):  return Δ(self, other) # DELTA, binary '//', conditional assignment
    def __mod__(self, other):       return Δ(self, other) # DELTA, binary '%', conditional assignment
    def __invert__(self):           return self # unary '~'
#------------------------------------------------------------------------------
def pattern(func: callable) -> callable:
    return lambda *args, **kwargs: PATTERN(func, args, kwargs)
#------------------------------------------------------------------------------
pos = 0 # internal position
subject = "" # internal subject
#------------------------------------------------------------------------------
_digits = "0123456789"
_UCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LCASE = "abcdefghijklmnopqrstuvwxyz"
_ALPHABET = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F" \
            "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F" \
            "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F" \
            "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F" \
            "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F" \
            "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F" \
            "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F" \
            "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F" \
            "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F" \
            "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F" \
            "\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF" \
            "\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF" \
            "\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF" \
            "\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF" \
            "\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF" \
            "\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF"
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
def REPLACE(s: str, old: str, new: str) -> str:
    return s.translate(str.maketrans(old, new))
#------------------------------------------------------------------------------
import re
re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    global re_repr_function
    p = repr(P)
    r = re.fullmatch(re_repr_function, p)
    if r: return f"{r.group(1)}(*{r.group(3)})"
    else: return p
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
# Immediate assignment during pattern matching
@pattern
def δ(P, V) -> PATTERN:
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print(_1)
        logging.debug("%s = delta(%s)", V, repr(_1))
        globals()[V] = _1
        yield _1
        logging.debug("%s deleted", V)
        del globals()[V]
#------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def λ(expression) -> PATTERN: # P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    logging.debug("lambda(%s) evaluating...", repr(expression))
    if eval(expression):
        logging.debug("lambda(%s) SUCCESS", repr(expression))
        yield ""
        logging.debug("lambda(%s) backtracking...", repr(expression))
    else: logging.debug("lambda(%s) Error evaluating. FAIL", repr(expression))
#------------------------------------------------------------------------------
# Conditional assignment after totally completed pattern match
@pattern
def Δ(P, V) -> PATTERN:
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        logging.debug("%s = delta(%d, %d) SUCCESS", V, pos - len(_1), pos)
        cstack.append(f"{V} = subject[{pos - len(_1)} : {pos}]")
        yield _1
        logging.debug("%s = delta(%d, %d) backtracking...", V, pos - len(_1), pos)
        cstack.pop()
#------------------------------------------------------------------------------
# Conditional execution after totally completed pattern match
@pattern
def Λ(command) -> PATTERN: # P . *exec(), P . tx . *func(tx)
    logging.debug("LAMBDA(%s) compiling...", repr(command))
    if compile(command, '<string>', 'exec'): # 'single', 'eval'
        logging.debug("LAMBDA(%s) SUCCESS", repr(command))
        cstack.append(command)
        yield ""
        logging.debug("LAMBDA(%s) backtracking...", repr(command))
        cstack.pop()
    else: logging.debug("LAMBDA(%s) Error compiling. FAIL", repr(expression))
#------------------------------------------------------------------------------
@pattern
def nPush() -> PATTERN:
    logging.debug("nPush() SUCCESS")
    cstack.append(f"itop += 1");
    cstack.append(f"istack.append(0)");
    yield "";
    logging.debug("nPush() backtracking...")
    cstack.pop()
    cstack.pop()
@pattern
def nInc() -> PATTERN:
    logging.debug("nInc() SUCCESS")
    cstack.append(f"istack[itop] += 1");
    yield "";
    logging.debug("nInc() backtracking...")
    cstack.pop()
@pattern
def nPop() -> PATTERN:
    logging.debug("nPop() SUCCESS")
    cstack.append(f"istack.pop()");
    cstack.append(f"itop -= 1");
    yield "";
    logging.debug("nPop() backtracking...")
    cstack.pop()
    cstack.pop()
#------------------------------------------------------------------------------
@pattern
def Shift(t, v='') -> PATTERN:
    logging.debug("Shift(%s, %s) SUCCESS", repr(t), repr(v))
    cstack.append(f"shift('{t}', \"{v}\")")
    yield ""
    logging.debug("Shift(%s, %s) backtracking...", repr(t), repr(v))
    cstack.pop()
@pattern
def Reduce(t, n=None) -> PATTERN:
    logging.debug("Reduce(%s, %d) SUCCESS", repr(t), n)
    if n is None: n = "istack[itop]"
    cstack.append(f"reduce('{t}', {n})")
    yield ""
    logging.debug("Reduce(%s, %d) backtracking...", repr(t), n)
    cstack.pop()
#------------------------------------------------------------------------------
def shift(t, v):
    global vstack
    None
def reduce(t, n):
    global vstack
    None
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
    if P:
        logging.debug("FENCE(%s) SUCCESS", PROTOTYPE(P))
        yield from P
        logging.debug("FENCE(%s) backtracking...", PROTOTYPE(P))
    else:
        logging.debug("FENCE() SUCCESS")
        yield ""
        logging.debug("FENCE() backtracking...")
#------------------------------------------------------------------------------
@pattern
def POS(n) -> PATTERN:
    global pos
    if pos == n:
        logging.debug("POS(%d) SUCCESS(%d,%d)=", n, pos, 0)
        yield ""
        logging.debug("POS(%d) backtracking...", n)
#------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global pos, subject
    if pos == len(subject) - n:
        logging.debug("RPOS(%d) SUCCESS(%d,%d)=", n, pos, 0)
        yield ""
        logging.debug("RPOS(%d) backtracking...", n)
#------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global pos, subject
    if pos + n <= len(subject):
        logging.debug("LEN(%d) SUCCESS(%d,%d)=%s", n, pos, n, subject[pos:pos + n])
        pos += n
        yield subject[pos - n:pos]
        pos -= n
        logging.debug("LEN(%d) backtracking(%d)...", n, pos)
#------------------------------------------------------------------------------
@pattern
def σ(s) -> PATTERN: # sigma, sequence of characters, literal string patttern
    global pos, subject
    logging.debug("sigma(%s) trying(%d)", repr(s), pos)
    if pos + len(s) <= len(subject):
        if s == subject[pos:pos + len(s)]:
            pos += len(s)
            logging.debug("sigma(%s) SUCCESS(%d,%d)=", repr(s), pos - len(s), len(s))
            yield s
            pos -= len(s)
            logging.debug("sigma(%s) backtracking(%d)...", repr(s), pos)
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
    logging.debug("ANY(%s) trying(%d)", repr(characters), pos)
    if pos < len(subject):
        if subject[pos] in characters:
            logging.debug("ANY(%s) SUCCESS(%d,%d)=%s", repr(characters), pos, 1, subject[pos])
            pos += 1
            yield subject[pos - 1]
            pos -= 1
            logging.debug("ANY(%s) backtracking(%d)...", repr(characters), pos)
#------------------------------------------------------------------------------
@pattern
def NOTANY(characters) -> PATTERN:
    global pos, subject
    logging.debug("NOTANY(%s) trying(%d)", repr(characters), pos)
    if pos < len(subject):
        if not subject[pos] in characters:
            logging.debug("NOTANY(%s) SUCCESS(%d,%d)=%s", repr(characters), pos, 1, subject[pos])
            pos += 1
            yield subject[pos - 1]
            pos -= 1
            logging.debug("NOTANY(%s) backtracking(%d)...", repr(characters), pos)
#------------------------------------------------------------------------------
@pattern
def SPAN(characters) -> PATTERN:
    global pos, subject
    pos0 = pos
    logging.debug("SPAN(%s) trying(%d)", repr(characters), pos0)
    while True:
        if pos >= len(subject): break
        if subject[pos] in characters:
            pos += 1
        else: break
    if pos > pos0:
        logging.debug("SPAN(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, pos - pos0, subject[pos0:pos])
        yield subject[pos0:pos]
        pos = pos0
        logging.debug("SPAN(%s) backtracking(%d)...", repr(characters), pos)
#------------------------------------------------------------------------------
@pattern
def BREAK(characters) -> PATTERN:
    global pos, subject
    pos0 = pos
    logging.debug("BREAK(%s) SUCCESS(%d)", repr(characters), pos0)
    while True:
        if pos >= len(subject): break
        if not subject[pos] in characters:
            pos += 1
        else: break
    if pos < len(subject):
        logging.debug("BREAK(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, pos - pos0, subject[pos0:pos])
        yield subject[pos0:pos]
        pos = pos0
        logging.debug("BREAK(%s) backtracking(%d)...", repr(characters), pos)
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
    global pos
    logging.debug("PI([%s]) trying(%d)...",
        "|".join([PROTOTYPE(P) for P in AP]), pos)
    for P in AP:
        yield from P
#------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SEQ, SIGMA, sequence, subsequents
    global pos
    pos0 = pos
    logging.debug("SIGMA([%s]) trying(%d)...",
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
                logging.debug("SIGMA(*) SUCCESS(%d,%d)=%s", pos0, pos - pos0, subject[pos0:pos])
                yield subject[pos0:pos]
                logging.debug("SIGMA(*) bactracking(%d)...", pos0)
                cursor -= 1
        except StopIteration:
            cursor -= 1
            highmark -= 1
#------------------------------------------------------------------------------
@pattern
def ARBNO(P) -> PATTERN:
    global pos, subject
    pos0 = pos
    logging.debug("ARBNO(%s) SUCCESS(%d,%d)=%s", PROTOTYPE(P), pos0, pos - pos0, subject[pos0:pos])
    yield ""
    logging.debug("ARBNO(*) bactracking(%d)...", pos0)
    AP = []
    cursor = 0
    highmark = 0
    while cursor >= 0:
        if cursor >= highmark:
            AP.append((pos, copy.copy(P)))
            iter(AP[cursor][1])
            highmark += 1
        try:
            next(AP[cursor][1])
            cursor += 1
            logging.debug("ARBNO(*) SUCCESS(%d,%d)=%s", pos0, pos - pos0, subject[pos0:pos])
            yield subject[pos0:pos]
            logging.debug("ARBNO(*) bactracking(%d)...", pos0)
        except StopIteration:
            cursor -= 1
            highmark -= 1
            AP.pop()
#------------------------------------------------------------------------------
def SEARCH(S, P) -> bool: None
def MATCH(S, P) -> bool:
    global pos, subject
    global itop, istack, cstack, vstack
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

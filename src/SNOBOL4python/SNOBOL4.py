# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python src/SNOBOL4python/SNOBOL4.py
#> python -m build
#> python -m pip install .\dist\snobol4python-0.1.0.tar.gz
#> python tests/test_01.py
#> python tests/test_json.py
#------------------------------------------------------------------------------
import re
import copy
import logging
from pprint import pprint
from functools import wraps
logging.basicConfig(level=logging.INFO)
#------------------------------------------------------------------------------
_pos = None # internal position
_subject = None # internal subject
_variables = None # global variables
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
    @wraps(func)
    def _PATTERN(*args, **kwargs):
        return PATTERN(func, args, kwargs)
    return _PATTERN
#------------------------------------------------------------------------------
def GT(i1, i2):
    if int(i1) >  int(i2): return ""
    else:                  raise Exception()
def LT(i1, i2):
    if int(i1) <  int(i2): return ""
    else:                  raise Exception()
def EQ(i1, i2):
    if int(i1) == int(i2): return ""
    else:                  raise Exception()
def GE(i1, i2):
    if int(i1) >= int(i2): return ""
    else:                  raise Exception()
def LE(i1, i2):
    if int(i1) <= int(i2): return ""
    else:                  raise Exception()
def NE(i1, i2):
    if int(i1) != int(i2): return ""
    else:                  raise Exception()
#------------------------------------------------------------------------------
def LGT(s1, s2):
    if str(s1) >  str(s2): return ""
    else:                  raise Exception()
def LLT(s1, s2):
    if str(s1) <  str(s2): return ""
    else:                  raise Exception()
def LEQ(s1, s2):
    if str(s1) == str(s2): return ""
    else:                  raise Exception()
def LGE(s1, s2):
    if str(s1) >= str(s2): return ""
    else:                  raise Exception()
def LLE(s1, s2):
    if str(s1) <= str(s2): return ""
    else:                  raise Exception()
def LNE(s1, s2):
    if str(s1) != str(s2): return ""
    else:                  raise Exception()
#------------------------------------------------------------------------------
def IDENT(d1, d2):
    if d1 is d2:            return ""
    else:                   raise Exception()
def DIFFER(d1, d2):
    if not d1 is d2:        return ""
    else:                   raise Exception()
#------------------------------------------------------------------------------
def LPAD(s1, i, s2=None):   return (' ' * (i - len(s1))) + s1
def RPAD(s1, i, s2=None):   return s + (' ' * (i - len(s1)))
#------------------------------------------------------------------------------
def APPLY(n, *args):        return n(*args)
def ARG(n, i):              None
def ARRAY(s, d):            None
def ASCII(c):               return ord(c)
def CHAR(i):                return chr(i)
def CODE(s):                return compile(s, '<SNOBOL4>', 'exec')
def COLLECT(i):             None
def CONVERT(d, s):          None
def COPY(d):                return copy.copy(d)
def DATA(s):                None
def DATATYPE(d):            return type(d)
def DATE():                 None
def DEFINE(s, n):           None
def DETACH(n):              None
def DUMP(i):                print(_variables)
def DUPL(s, i):             return s * i
def ENDFILE(u):             None
def EVAL(s):                return eval(s, _variables)
def FIELD(s, i):            None
def INPUT(n, u, i, s):      None
def ITEM(a, *iN):           None # ITEM(t, d)
def LOCAL(n, i):            None
def OPSYN(s1, s2, i):       None
def OUTPUT(n, u, i, s):     None
def REMDR(i1, i2):          return i1 % i2
def REPLACE(s1, s2, s3):    return s.translate(str.maketrans(old, new))
def REVERSE(s):             return s.reverse() # s[::-1]
def SIZE(s):                return len(s)
def STOPTR(n, t):           None
def TABLE(i1, i2):          None
def TIME():                 None
def TRACE(n1, t, s, n2):    None
def TRIM(s):                return s.strip()
def UNLOAD(n):              None
def VALUE(n):               None
#------------------------------------------------------------------------------
def INTEGER(d):
    try:
        int(d)
        return ""
    except ValueError:
        return None
#------------------------------------------------------------------------------
re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    global re_repr_function
    re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
    p = repr(P)
    r = re.fullmatch(re_repr_function, p)
    if r: return f"{r.group(1)}(*{r.group(3)})"
    else: return p
#------------------------------------------------------------------------------
def FAIL(): raise StopIteration # return?
def ABORT(): raise StopIteration # return?
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
# Immediate cursor assignment during pattern matching
@pattern
def θ(V) -> PATTERN:
    global _pos, _variables
    logging.debug("theta(%s) SUCCESS", V)
    _variables[V] = _pos
    yield ""
    logging.debug("theta(%s) backtracking...", V)
    del _variables[V]
#------------------------------------------------------------------------------
# Immediate match assignment during pattern matching
@pattern
def δ(P, V) -> PATTERN:
    global _variables
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print(_1)
        logging.debug("%s = delta(%s)", V, repr(_1))
        _variables[V] = _1
        yield _1
        logging.debug("%s deleted", V)
        del _variables[V]
#------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def λ(expression) -> PATTERN: # P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    logging.debug("lambda(%s) evaluating...", repr(expression))
    if eval(expression, _variables):
        logging.debug("lambda(%s) SUCCESS", repr(expression))
        yield ""
        logging.debug("lambda(%s) backtracking...", repr(expression))
    else: logging.debug("lambda(%s) Error evaluating. FAIL", repr(expression))
#------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
@pattern
def Δ(P, V) -> PATTERN:
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        logging.debug("%s = delta(%d, %d) SUCCESS", V, _pos - len(_1), _pos)
        cstack.append(f"{V} = _subject[{_pos - len(_1)} : {_pos}]")
        yield _1
        logging.debug("%s = delta(%d, %d) backtracking...", V, _pos - len(_1), _pos)
        cstack.pop()
#------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
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
    cstack.append(f"_shift('{t}', {v})")
    yield ""
    logging.debug("Shift(%s, %s) backtracking...", repr(t), repr(v))
    cstack.pop()
@pattern
def Reduce(t, n=None) -> PATTERN:
    logging.debug("Reduce(%s, %d) SUCCESS", repr(t), n)
    if n is None: n = "istack[itop]"
    cstack.append(f"_reduce('{t}', {n})")
    yield ""
    logging.debug("Reduce(%s, %d) backtracking...", repr(t), n)
    cstack.pop()
#------------------------------------------------------------------------------
def _shift(t, v):
    _variables['vstack'].append([t, v])
def _reduce(t, n):
    x = []
    for i in range(n):
        x.insert(0, _variables['vstack'].pop())
    _variables['vstack'].append([t, x])
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
    global _pos
    if _pos == n:
        logging.debug("POS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logging.debug("POS(%d) backtracking...", n)
#------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global _pos, _subject
    if _pos == len(_subject) - n:
        logging.debug("RPOS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logging.debug("RPOS(%d) backtracking...", n)
#------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global _pos, _subject
    if _pos + n <= len(_subject):
        logging.debug("LEN(%d) SUCCESS(%d,%d)=%s", n, _pos, n, _subject[_pos:_pos + n])
        _pos += n
        yield _subject[_pos - n:_pos]
        _pos -= n
        logging.debug("LEN(%d) backtracking(%d)...", n, _pos)
#------------------------------------------------------------------------------
@pattern
def σ(s) -> PATTERN: # sigma, sequence of characters, literal string patttern
    global _pos, _subject
    logging.debug("sigma(%s) trying(%d)", repr(s), _pos)
    if _pos + len(s) <= len(_subject):
        if s == _subject[_pos:_pos + len(s)]:
            _pos += len(s)
            logging.debug("sigma(%s) SUCCESS(%d,%d)=", repr(s), _pos - len(s), len(s))
            yield s
            _pos -= len(s)
            logging.debug("sigma(%s) backtracking(%d)...", repr(s), _pos)
#------------------------------------------------------------------------------
@pattern
def TAB(n) -> PATTERN:
    global _pos, _subject
    if n <= len(_subject):
        if n >= _pos:
            pos0 = _pos
            _pos = n
            yield _subject[pos0:n]
            _pos = pos0
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
@pattern
def REM() -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    _pos = len(_subject)
    yield _subject[pos0:]
    _pos = pos0
#------------------------------------------------------------------------------
@pattern
def ANY(characters) -> PATTERN:
    global _pos, _subject
    logging.debug("ANY(%s) trying(%d)", repr(characters), _pos)
    if _pos < len(_subject):
        if _subject[_pos] in characters:
            logging.debug("ANY(%s) SUCCESS(%d,%d)=%s", repr(characters), _pos, 1, _subject[_pos])
            _pos += 1
            yield _subject[_pos - 1]
            _pos -= 1
            logging.debug("ANY(%s) backtracking(%d)...", repr(characters), _pos)
#------------------------------------------------------------------------------
@pattern
def NOTANY(characters) -> PATTERN:
    global _pos, _subject
    logging.debug("NOTANY(%s) trying(%d)", repr(characters), _pos)
    if _pos < len(_subject):
        if not _subject[_pos] in characters:
            logging.debug("NOTANY(%s) SUCCESS(%d,%d)=%s", repr(characters), _pos, 1, _subject[_pos])
            _pos += 1
            yield _subject[_pos - 1]
            _pos -= 1
            logging.debug("NOTANY(%s) backtracking(%d)...", repr(characters), _pos)
#------------------------------------------------------------------------------
@pattern
def SPAN(characters) -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    logging.debug("SPAN(%s) trying(%d)", repr(characters), pos0)
    while True:
        if _pos >= len(_subject): break
        if _subject[_pos] in characters:
            _pos += 1
        else: break
    if _pos > pos0:
        logging.debug("SPAN(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, _pos - pos0, _subject[pos0:_pos])
        yield _subject[pos0:_pos]
        _pos = pos0
        logging.debug("SPAN(%s) backtracking(%d)...", repr(characters), _pos)
#------------------------------------------------------------------------------
@pattern
def BREAK(characters) -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    logging.debug("BREAK(%s) SUCCESS(%d)", repr(characters), pos0)
    while True:
        if _pos >= len(_subject): break
        if not _subject[_pos] in characters:
            _pos += 1
        else: break
    if _pos < len(_subject):
        logging.debug("BREAK(%s) SUCCESS(%d,%d)=%s", repr(characters), pos0, _pos - pos0, _subject[pos0:_pos])
        yield _subject[pos0:_pos]
        _pos = pos0
        logging.debug("BREAK(%s) backtracking(%d)...", repr(characters), _pos)
#------------------------------------------------------------------------------
@pattern
def ARB() -> PATTERN: # ARB
    global _pos, _subject
    pos0 = _pos
    while _pos <= len(_subject):
        yield _subject[pos0 : _pos]
        _pos += 1
    _pos = pos0
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
@pattern
def Ξ(P, Q) -> PATTERN: # PSI, AND, conjunction
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
#------------------------------------------------------------------------------
@pattern
def π(P) -> PATTERN: # (P | epsilon), pi, optional
    yield from P
    yield ""
#------------------------------------------------------------------------------
@pattern
def Π(*AP) -> PATTERN: # ALT, PI, alternates
    global _pos
    logging.debug("PI([%s]) trying(%d)...",
        "|".join([PROTOTYPE(P) for P in AP]), _pos)
    for P in AP:
        yield from P
#------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SEQ, SIGMA, sequence, subsequents
    global _pos
    pos0 = _pos
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
                logging.debug("SIGMA(*) SUCCESS(%d,%d)=%s", pos0, _pos - pos0, _subject[pos0:_pos])
                yield _subject[pos0:_pos]
                logging.debug("SIGMA(*) backtracking(%d)...", pos0)
                cursor -= 1
        except StopIteration:
            cursor -= 1
            highmark -= 1
#------------------------------------------------------------------------------
@pattern
def ARBNO(P) -> PATTERN:
    global _pos, _subject
    pos0 = _pos
    logging.debug("ARBNO(%s) SUCCESS(%d,%d)=%s", PROTOTYPE(P), pos0, _pos - pos0, _subject[pos0:_pos])
    yield ""
    logging.debug("ARBNO(*) backtracking(%d)...", pos0)
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
            logging.debug("ARBNO(*) SUCCESS(%d,%d)=%s", pos0, _pos - pos0, _subject[pos0:_pos])
            yield _subject[pos0:_pos]
            logging.debug("ARBNO(*) backtracking(%d)...", pos0)
        except StopIteration:
            cursor -= 1
            highmark -= 1
            AP.pop()
#-----------------------------------------------------------------------------------------------------------------------
def JSONDecode(s) -> str: return s
#------------------------------------------------------------------------------
def SEARCH(S, P) -> bool: None
def MATCH(S, P, Vs=None) -> bool:
    global _pos, _subject, _variables
    global itop, istack, cstack, vstack
    _pos = 0
    itop = -1
    istack = []
    vstack = []
    cstack = []
    _subject = S
    if Vs: _variables = Vs
    else: _variables = dict()
    try:
        m = next(P)
        print(f'"{S}" ? "{m}"')
        for command in cstack:
            print(command)
        for var, val in _variables.items():
            print(var, val)
        print()
        _variables['itop'] = -1
        _variables['istack'] = []
        _variables['vstack'] = []
        _variables['_subject'] = _subject
        _variables['_shift'] = _shift
        _variables['_reduce'] = _reduce
        for command in cstack:
            exec(command, _variables)
        if len(_variables['vstack']) > 0:
            pprint(_variables['vstack'][0])
        return True
    except StopIteration:
        print(f'"{S}" FAIL')
        return False
def FULLMATCH(S, P) -> bool: None
#------------------------------------------------------------------------------

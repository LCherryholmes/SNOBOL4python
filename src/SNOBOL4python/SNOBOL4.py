# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
# SNOBOL4 string pattern matching
#> python src/SNOBOL4python/SNOBOL4.py
#> python -m build
#> python -m pip install .\dist\snobol4python-0.1.0.tar.gz
#> python tests/test_01.py
#> python tests/test_json.py
#> python tests/test_arbno.py
#> python tests/test_re_simple.py
#----------------------------------------------------------------------------------------------------------------------
import gc
import re
import sys
import copy
import time
import logging
import operator
from pprint import pprint
from datetime import date
from functools import wraps
logging.basicConfig(level=logging.INFO)
#----------------------------------------------------------------------------------------------------------------------
_pos = None # internal position
_subject = None # internal subject
_variables = None # global variables
_started = time.time_ns() // 1000
_units = dict() # file name associations and unit numbers
#----------------------------------------------------------------------------------------------------------------------
globals()['_DIGITS'] = "0123456789"
globals()['_UCASE'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
globals()['_LCASE'] = "abcdefghijklmnopqrstuvwxyz"
globals()['_ALPHABET'] = \
    "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F" \
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
#----------------------------------------------------------------------------------------------------------------------
class PATTERN(object):
    def __init__(self, func, patterns, features):
        self.func = func
        self.patterns = patterns
        self.features = features
        self.generator = self.func(*self.patterns, **self.features)
    def __iter__(self):           # Constructor
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
def GT(i1, i2):
    if int(i1) >  int(i2):  return ""
    else:                   raise Exception()
def LT(i1, i2):
    if int(i1) <  int(i2):  return ""
    else:                   raise Exception()
def EQ(i1, i2):
    if int(i1) == int(i2):  return ""
    else:                   raise Exception()
def GE(i1, i2):
    if int(i1) >= int(i2):  return ""
    else:                   raise Exception()
def LE(i1, i2):
    if int(i1) <= int(i2):  return ""
    else:                   raise Exception()
def NE(i1, i2):
    if int(i1) != int(i2):  return ""
    else:                   raise Exception()
#----------------------------------------------------------------------------------------------------------------------
def LGT(s1, s2):
    if str(s1) >  str(s2):  return ""
    else:                   raise Exception()
def LLT(s1, s2):
    if str(s1) <  str(s2):  return ""
    else:                   raise Exception()
def LEQ(s1, s2):
    if str(s1) == str(s2):  return ""
    else:                   raise Exception()
def LGE(s1, s2):
    if str(s1) >= str(s2):  return ""
    else:                   raise Exception()
def LLE(s1, s2):
    if str(s1) <= str(s2):  return ""
    else:                   raise Exception()
def LNE(s1, s2):
    if str(s1) != str(s2):  return ""
    else:                   raise Exception()
#----------------------------------------------------------------------------------------------------------------------
def IDENT(d1, d2):
    if d1 is d2:            return ""
    else:                   raise Exception()
def DIFFER(d1, d2):
    if not d1 is d2:        return ""
    else:                   raise Exception()
#----------------------------------------------------------------------------------------------------------------------
def LPAD(s1, i, s2=' '):    return (' ' * (i - len(s1))) + s1
def RPAD(s1, i, s2=' '):    return s1 + (' ' * (i - len(s1)))
#----------------------------------------------------------------------------------------------------------------------
def ARRAY(proto, d):      # An array is an indexed aggregate of variables, called elements.
                            limits = tuple(int(limit) for limit in proto.split(','))
                            dims = len(limits)
                            match dims:
                                case 1: return   [d] * limits[0]
                                case 2: return  [[d] * limits[1]] * limits[0]
                                case 3: return [[[d] * limits[2]] * limits[1]] * limits[0]
                                case _: raise Exception()
def ASCII(c):               return ord(c)
def CHAR(i):                return chr(i)
def CODE(s):                return compile(s, '<SNOBOL4>', 'exec')
def COLLECT(i):             return gc.collect()
def CONVERT(d, s):        # Conversion to a specified type
                            match s.upper():
                                case 'STRING':
                                    match type(d).__name__:
                                        case 'int':   return str(d)
                                        case 'float': return str(d)
                                        case 'str':   return d
                                        case 'list':  return 'ARRAY(' + PROTOTYPE(d) + ')'
                                        case 'dict':  return 'TABLE(' + len(d) + ')'
                                        case _:       return type(d).__name__
                                case 'INTEGER':       return int(d)
                                case 'REAL':          return float(d)
                                case 'PATTERN':       return σ(str(d))
                                case 'ARRAY':         return d # TODO
                                case 'TABLE':         return d # TODO
                                case 'NAME':          return d # NAME() objectt?
                                case 'EXPRESSION':    return compile(str(d), '<CONVERT>', 'single')
                                case 'CODE':          return compile(str(d), '<CONVERT>', 'exec')
                                case _:               return d
def COPY(d):                return copy.copy(d)
def DATATYPE(d):            return type(d).__name__
def DATE():                 return '{:%Y-%m-%d}'.format(date.today())
def DUMP(i):              # A listing of natural variables and their values
                            if int(i) != 0: print(_variables)
def DUPL(s, i):             return s * i
def EVAL(s):                return eval(s, _variables)
def EXEC(s):                return exec(s, _variables)
def INTEGER(d):           # Test for an integer, or a string convertabble to an integer
                            try:
                                int(d)
                                return ""
                            except ValueError:
                                return None
def ITEM(d, *args):       # Reference an array or table element
                            match len(args):
                                case 1: return d[args[0]]
                                case 2: return d[args[0]][args[1]]
                                case 3: return d[args[0]][args[1]][args[2]]
                                case _: raise Exception()
def REMDR(i1, i2):          return i1 % i2
def REPLACE(s1, s2, s3):    return str(s1).translate(str.maketrans(str(s2), str(s3)))
def REVERSE(s):             return s.reverse() # s[::-1]
def RSORT(d):               return d
def SIZE(s):                return len(s)
def SORT(d):                return d
def TABLE(i1, i2):          return dict()
def TIME():                 return (time.time_ns() // 1000) - _started
def TRIM(s):                return s.strip()
def VALUE(n):               return _variables[n]
#----------------------------------------------------------------------------------------------------------------------
def OPSYN(s1, s2, i):       None
def STOPTR(n, t):           None
def TRACE(n1, t, s, n2):    None
#----------------------------------------------------------------------------------------------------------------------
def INPUT(n, u, len=None, fname=None):
    global _units
    if not u: u = 0
    match u:
        case 0: _variables[n] = None; _units[u] = (n, sys.stdin) # .readline()
        case 1: raise Exception()
        case 2: raise Exception()
        case _: _variables[n] = None; _units[u] = (n, open(fname, "rt"))
    return ""
def OUTPUT(n, u, len=None, fname=None):
    global _units
    if not u: u = 1
    match u:
        case 0: raise Exception()
        case 1: _variables[n] = None; _units[u] = (n, sys.stdout) # .writeline()?
        case 2: _variables[n] = None; _units[u] = (n, sys.stderr)
        case _: _variables[n] = None; _units[u] = (n, open(fname, "wt"))
    return ""
def DETACH(n): del _variables[n] # removes input/output association with name
def ENDFILE(u): # writes an end of file on (closes) the data set
    global _units
    if not u: u = 0
    match u:
        case 0: del _variables[_units[u][0]]; del _units[u]
        case 1: del _variables[_units[u][0]]; del _units[u]
        case 2: del _variables[_units[u][0]]; del _units[u]
        case _: del _variables[_units[u][0]]; close(_units[u][1]); del _units[u]
    return ""
def BACKSPACE(u):           None # backspace one record
def REWIND():               None # repositions the data set associated with the number to the first file
#----------------------------------------------------------------------------------------------------------------------
rex_DEFINE_proto = re.compile(r"^(\w+)\((\w+(?:,\w+)*)\)(\w+(?:,\w+)*)$")
def DEFINE(proto, n=None):
    global re_DEFINE_proto
    matching = re.fullmatch(re_DEFINE_proto, proto)
    if matching:
        func_name = matching.group(1)
        func_params = matching.group(2)
        logging.debug("DEFINE: func_params=%s", func_params)
        func_params = tuple(f_param for f_param in func_params.split(','))
        func_locals = matching.group(3)
        logging.debug("DEFINE: func_locals=%s", func_locals)
        func_locals = tuple(f_local for f_local in func_locals.split(','))
        params = ', '.join(func_params)
        body = 'def ' + func_name + '(' + params + '):\n' \
               '    print(' + params + ')'
        code = compile(body, '<DEFINE>', 'exec')
        func = types.FunctionType(code.co_consts[0], globals(), func_name)
        func.__defaults__ = (None,) * len(func_params)
        _variables[func_name] = func
        return ""
def APPLY(n, *args):    return _variables[n](*args)
def ARG(n, i):          None
def LOCAL(n, i):        None
def LOAD(proto, lib):   None # Load external foreign library function
def UNLOAD(s):          None # function unloaded and consequently undefined
#----------------------------------------------------------------------------------------------------------------------
re_DATA_proto = re.compile(r"^(\w+)\((\w+(?:,\w+)*)\)$")
def FIELD(s, i): return s.__slots__[int(i)]
def DATA(s): # DATA('Node(value,link)')
    global re_DATA_proto
    matching = re.fullmatch(re_DATA_proto, s)
    if m:
        name = matching.group(1)
        fields = matching.group(2)
        fields = tuple(field for field in fields.split(','))
        namespace = dict()
        namespace['__slots__'] = fields
        def __init__(self, *args):
            for i, value in enumerate(args):
                setattr(self, self.__slots__[i], value)
        namespace['__init__'] = __init__
        _variables[name] = type(name, (object,), namespace)
        return ""
#----------------------------------------------------------------------------------------------------------------------
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
itop = -1 # counter stack (nPush, nInc, nPop, nTop)
istack = []
vstack = [] # value stack (Shift/Reduce values)
cstack = [] # command stack (conditional actions)
#----------------------------------------------------------------------------------------------------------------------
# Immediate cursor assignment during pattern matching
@pattern
def θ(V) -> PATTERN:
    global _pos, _variables
    logging.debug("theta(%s) SUCCESS", V)
    _variables[V] = _pos
    yield ""
    logging.debug("theta(%s) backtracking...", V)
    del _variables[V]
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (permanent)
@pattern
def Ω(P, V) -> PATTERN: # OMEGA, binary '/', SNOBOL4: P $ V
    global _variables
    logging.debug("OMEGA(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print(_1)
        logging.debug("%s = OMEGA(%s)", V, repr(_1))
        _variables[V] = _1
        yield _1
#----------------------------------------------------------------------------------------------------------------------
# Immediate match assignment during pattern matching (backtracking)
@pattern
def δ(P, V) -> PATTERN: # delta, binary '@', SNOBOL4: P $ V
    global _variables
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        if V == "OUTPUT": print(_1)
        logging.debug("%s = delta(%s)", V, repr(_1))
        _variables[V] = _1
        yield _1
        logging.debug("%s deleted", V)
        del _variables[V]
#----------------------------------------------------------------------------------------------------------------------
# Immediate evaluation as test during pattern matching
@pattern
def λ(expression) -> PATTERN: # lambda, P *eval(), *EQ(), *IDENT(), P $ tx $ *func(tx)
    logging.debug("lambda(%s) evaluating...", repr(expression))
    if eval(expression, _variables):
        logging.debug("lambda(%s) SUCCESS", repr(expression))
        yield ""
        logging.debug("lambda(%s) backtracking...", repr(expression))
    else: logging.debug("lambda(%s) Error evaluating. FAIL", repr(expression))
#----------------------------------------------------------------------------------------------------------------------
# Conditional match assignment (after successful complete pattern match)
@pattern
def Δ(P, V) -> PATTERN: # DELTA, binary '%', SNOBOL4: P . V
    logging.debug("delta(%s, %s)", PROTOTYPE(P), V)
    for _1 in P:
        logging.debug("%s = delta(%d, %d) SUCCESS", V, _pos - len(_1), _pos)
        cstack.append(f"{V} = _subject[{_pos - len(_1)} : {_pos}]")
        yield _1
        logging.debug("%s = delta(%d, %d) backtracking...", V, _pos - len(_1), _pos)
        cstack.pop()
#----------------------------------------------------------------------------------------------------------------------
# Conditional match execution (after successful complete pattern match)
@pattern
def Λ(command) -> PATTERN: # LAMBDA, P . *exec(), P . tx . *func(tx)
    logging.debug("LAMBDA(%s) compiling...", repr(command))
    if compile(command, '<string>', 'exec'): # 'single', 'eval'
        logging.debug("LAMBDA(%s) SUCCESS", repr(command))
        cstack.append(command)
        yield ""
        logging.debug("LAMBDA(%s) backtracking...", repr(command))
        cstack.pop()
    else: logging.debug("LAMBDA(%s) Error compiling. FAIL", repr(expression))
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Shift(t, v='') -> PATTERN:
    logging.debug("Shift(%s, %s) SUCCESS", repr(t), repr(v))
    if v is None:
        cstack.append(f"_shift('{t}')")
    else: cstack.append(f"_shift('{t}', {v})")
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
#----------------------------------------------------------------------------------------------------------------------
def _shift(t, v=None):
    if v is None:
        _variables['vstack'].append([t])
    else: _variables['vstack'].append([t, v])
def _reduce(t, n):
    if n == 0 and t == 'Σ':
        _variables['vstack'].append(['ε'])
    elif n != 1 or t not in ('Σ', 'Π', 'ξ'):
        x = [t]
        for i in range(n):
            x.insert(1, _variables['vstack'].pop())
        _variables['vstack'].append(x)
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
@pattern
def POS(n) -> PATTERN:
    global _pos
    if _pos == n:
        logging.debug("POS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logging.debug("POS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def RPOS(n) -> PATTERN:
    global _pos, _subject
    if _pos == len(_subject) - n:
        logging.debug("RPOS(%d) SUCCESS(%d,%d)=", n, _pos, 0)
        yield ""
        logging.debug("RPOS(%d) backtracking...", n)
#----------------------------------------------------------------------------------------------------------------------
@pattern
def LEN(n) -> PATTERN:
    global _pos, _subject
    if _pos + n <= len(_subject):
        logging.debug("LEN(%d) SUCCESS(%d,%d)=%s", n, _pos, n, _subject[_pos:_pos + n])
        _pos += n
        yield _subject[_pos - n:_pos]
        _pos -= n
        logging.debug("LEN(%d) backtracking(%d)...", n, _pos)
#----------------------------------------------------------------------------------------------------------------------
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
    logging.debug("ANY(%s) trying(%d)", repr(characters), _pos)
    if _pos < len(_subject):
        if _subject[_pos] in characters:
            logging.debug("ANY(%s) SUCCESS(%d,%d)=%s", repr(characters), _pos, 1, _subject[_pos])
            _pos += 1
            yield _subject[_pos - 1]
            _pos -= 1
            logging.debug("ANY(%s) backtracking(%d)...", repr(characters), _pos)
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
@pattern
def BREAKX(characters) -> PATTERN: pass
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
    logging.debug("PI([%s]) trying(%d)...",
        "|".join([PROTOTYPE(P) for P in AP]), _pos)
    for P in AP:
        yield from P
#----------------------------------------------------------------------------------------------------------------------
@pattern
def Σ(*AP) -> PATTERN: # SIGMA, sequence, subsequents, SNOBOL4: P Q R S T ...
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
#----------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------
def JSONDecode(s) -> str: return s
#----------------------------------------------------------------------------------------------------------------------
def _END(): None
def _RETURN(): None
def _FRETURN(): None
def _NRETURN(): None
#======================================================================================================================
def S(success):
    def S_decorator(stmt):
        @wraps(stmt)
        def S_wrapper():
            try:
                stmt()
                return success
            except: return None
        return S_wrapper
    return S_decorator
#----------------------------------------------------------------------------------------------------------------------
def F(failure):
    def F_decorator(stmt):
        @wraps(stmt)
        def F_wrapper():
            try:
                stmt()
                return None
            except: return failure
        return F_wrapper
    return F_decorator
#----------------------------------------------------------------------------------------------------------------------
def Ξ(success=None, failure=None):
    def Ξ_decorator(stmt):
        @wraps(stmt)
        def Ξ_wrapper():
            try:
                stmt()
                return success
            except: return failure
        return Ξ_wrapper
    return Ξ_decorator
#----------------------------------------------------------------------------------------------------------------------
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
    if not Vs is None:
        _variables = Vs
    else: _variables = dict()
    try:
        m = next(P)
        logging.debug(f'MATCH(): "{S}" ? "{m}"')
        for command in cstack:
            logging.debug(f'MATCH(): {command}')
        for var, val in _variables.items():
            logging.debug(f'MATCH(): var={var} val={val}')
        _variables['itop'] = -1
        _variables['istack'] = []
        _variables['vstack'] = []
        _variables['_subject'] = _subject
        if '_shift' not in _variables:  _variables['_shift'] = _shift
        if '_reduce' not in _variables: _variables['_reduce'] = _reduce
        for command in cstack:
            exec(command, _variables)
        return True
    except StopIteration:
        logging.info(f'"{S}" FAIL')
        return False
def FULLMATCH(S, P) -> bool: None
#----------------------------------------------------------------------------------------------------------------------
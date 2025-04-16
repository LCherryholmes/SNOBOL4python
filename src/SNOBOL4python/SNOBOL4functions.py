# -*- coding: utf-8 -*-
import gc
import re
import sys
import time
import logging
import operator
from pprint import pprint
from datetime import date
from functools import wraps
logger = logging.getLogger(__name__)
#----------------------------------------------------------------------------------------------------------------------
_globals = None # WARNING: dummy, global variables
_started = time.time_ns() // 1000
_units = dict() # file name associations and unit numbers
#----------------------------------------------------------------------------------------------------------------------
globals()['NULL'] = ""
globals()['UCASE'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
globals()['LCASE'] = "abcdefghijklmnopqrstuvwxyz"
globals()['DIGITS'] = "0123456789"
globals()['ALPHABET'] = (
    "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"
    "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F"
    "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F"
    "\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F"
    "\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F"
    "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F"
    "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F"
    "\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F"
    "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F"
    "\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F"
    "\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF"
    "\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF"
    "\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF"
    "\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF"
    "\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF"
    "\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF"
)
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
                            if int(i) != 0: print(_globals)
def DUPL(s, i):             return s * i
def EVAL(s):                return eval(s, _globals)
def EXEC(s):                return exec(s, _globals)
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
def VALUE(n):               return _globals[n]
#----------------------------------------------------------------------------------------------------------------------
def OPSYN(s1, s2, i):       None
def STOPTR(n, t):           None
def TRACE(n1, t, s, n2):    None
#----------------------------------------------------------------------------------------------------------------------
def INPUT(n, u, len=None, fname=None):
    global _units
    if not u: u = 0
    match u:
        case 0: _globals[n] = None; _units[u] = (n, sys.stdin) # .readline()
        case 1: raise Exception()
        case 2: raise Exception()
        case _: _globals[n] = None; _units[u] = (n, open(fname, "rt"))
    return ""
def OUTPUT(n, u, len=None, fname=None):
    global _units
    if not u: u = 1
    match u:
        case 0: raise Exception()
        case 1: _globals[n] = None; _units[u] = (n, sys.stdout) # .writeline()?
        case 2: _globals[n] = None; _units[u] = (n, sys.stderr)
        case _: _globals[n] = None; _units[u] = (n, open(fname, "wt"))
    return ""
def DETACH(n): del _globals[n] # removes input/output association with name
def ENDFILE(u): # writes an end of file on (closes) the data set
    global _units
    if not u: u = 0
    match u:
        case 0: del _globals[_units[u][0]]; del _units[u]
        case 1: del _globals[_units[u][0]]; del _units[u]
        case 2: del _globals[_units[u][0]]; del _units[u]
        case _: del _globals[_units[u][0]]; close(_units[u][1]); del _units[u]
    return ""
def BACKSPACE(u):           None # backspace one record
def REWIND():               None # repositions the data set associated with the number to the first file
#----------------------------------------------------------------------------------------------------------------------
re_repr_function = re.compile(r"\<function\ ([^\s]+)\ at\ 0x([0-9A-F]{16})\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    global re_repr_function
    p = repr(P)
    r = re.fullmatch(re_repr_function, p)
    if r: return f"{r.group(1)}(*{r.group(3)})"
    else: return p
#----------------------------------------------------------------------------------------------------------------------
rex_DEFINE_proto = re.compile(r"^(\w+)\((\w+(?:,\w+)*)\)(\w+(?:,\w+)*)$")
def DEFINE(proto, n=None):
    global re_DEFINE_proto
    matching = re.fullmatch(re_DEFINE_proto, proto)
    if matching:
        func_name = matching.group(1)
        func_params = matching.group(2)
        logger.debug("DEFINE: func_params=%s", func_params)
        func_params = tuple(f_param for f_param in func_params.split(','))
        func_locals = matching.group(3)
        logger.debug("DEFINE: func_locals=%s", func_locals)
        func_locals = tuple(f_local for f_local in func_locals.split(','))
        params = ', '.join(func_params)
        body = 'def ' + func_name + '(' + params + '):\n' \
               '    print(' + params + ')'
        code = compile(body, '<DEFINE>', 'exec')
        func = types.FunctionType(code.co_consts[0], globals(), func_name)
        func.__defaults__ = (None,) * len(func_params)
        _globals[func_name] = func
        return ""
def APPLY(n, *args):    return _globals[n](*args)
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
        _globals[name] = type(name, (object,), namespace)
        return ""
#----------------------------------------------------------------------------------------------------------------------
def END(): pass
def RETURN(): pass
def FRETURN(): pass
def NRETURN(): pass
#======================================================================================================================
def S(success):
    def S_decorator(statement):
        @wraps(statement)
        def S_wrapper():
            try:
                statement()
                return success
            except: return None
        return S_wrapper
    return S_decorator
#----------------------------------------------------------------------------------------------------------------------
def F(failure):
    def F_decorator(statement):
        @wraps(statement)
        def F_wrapper():
            try:
                statement()
                return None
            except: return failure
        return F_wrapper
    return F_decorator
#----------------------------------------------------------------------------------------------------------------------
def Ξ(success=None, failure=None):
    def Ξ_decorator(statement):
        @wraps(statement)
        def Ξ_wrapper():
            try:
                statement()
                return success
            except: return failure
        return Ξ_wrapper
    return Ξ_decorator
#----------------------------------------------------------------------------------------------------------------------
def JSONDecode(s) -> str: return s
#----------------------------------------------------------------------------------------------------------------------

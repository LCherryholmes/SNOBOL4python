# -*- coding: utf-8 -*-
# SNOBOL4functions.py — SNOBOL4 built-in functions
#
# All functions that need the SNOBOL environment dict read it from _env._g.
# This module does NOT define GLOBALS() — that lives in _env.py and is
# re-exported via __init__.py.
# ─────────────────────────────────────────────────────────────────────────────
import gc
import re
import sys
import time
import types
import logging
from datetime import date
from . import _env

logger = logging.getLogger(__name__)

# ── I/O unit table ────────────────────────────────────────────────────────────
_started = time.time_ns() // 1000
_units: dict = {}           # unit-number → (varname, file-object)

# ── SNOBOL4 standard string constants ─────────────────────────────────────────
UCASE    = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LCASE    = "abcdefghijklmnopqrstuvwxyz"
DIGITS   = "0123456789"
ALPHABET = (
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

# ── Integer comparison functions ───────────────────────────────────────────────
def GT(i1, i2):
    if int(i1) >  int(i2): return ""
    raise Exception()
def LT(i1, i2):
    if int(i1) <  int(i2): return ""
    raise Exception()
def EQ(i1, i2):
    if int(i1) == int(i2): return ""
    raise Exception()
def GE(i1, i2):
    if int(i1) >= int(i2): return ""
    raise Exception()
def LE(i1, i2):
    if int(i1) <= int(i2): return ""
    raise Exception()
def NE(i1, i2):
    if int(i1) != int(i2): return ""
    raise Exception()

# ── String comparison functions ────────────────────────────────────────────────
def LGT(s1, s2):
    if str(s1) >  str(s2): return ""
    raise Exception()
def LLT(s1, s2):
    if str(s1) <  str(s2): return ""
    raise Exception()
def LEQ(s1, s2):
    if str(s1) == str(s2): return ""
    raise Exception()
def LGE(s1, s2):
    if str(s1) >= str(s2): return ""
    raise Exception()
def LLE(s1, s2):
    if str(s1) <= str(s2): return ""
    raise Exception()
def LNE(s1, s2):
    if str(s1) != str(s2): return ""
    raise Exception()

# ── Identity / difference ──────────────────────────────────────────────────────
def IDENT(d1, d2):
    if d1 is d2:     return ""
    raise Exception()
def DIFFER(d1, d2):
    if d1 is not d2: return ""
    raise Exception()

# ── String utilities ───────────────────────────────────────────────────────────
def LPAD(s1, i, s2=' '): return (' ' * (i - len(s1))) + s1
def RPAD(s1, i, s2=' '): return s1 + (' ' * (i - len(s1)))
def DUPL(s, i):          return s * i
def REPLACE(s1, s2, s3): return str(s1).translate(str.maketrans(str(s2), str(s3)))
def REVERSE(s):          return s[::-1]
def SIZE(s):             return len(s)
def TRIM(s):             return s.strip()

def SUBSTITUTE(subject, slyce, replacement):
    subject = str(subject)
    return f"{subject[:slyce.start]}{replacement}{subject[slyce.stop:]}"

# ── Type / conversion functions ────────────────────────────────────────────────
def ASCII(c):   return ord(c)
def CHAR(i):    return chr(i)
def CODE(s):    return compile(s, '<SNOBOL4>', 'exec')
def COLLECT(i): return gc.collect()
def COPY(d):
    import copy
    return copy.copy(d)
def DATATYPE(d): return type(d).__name__
def DATE():      return '{:%Y-%m-%d}'.format(date.today())
def TIME():      return (time.time_ns() // 1000) - _started

def INTEGER(d):
    try:    int(d); return ""
    except (ValueError, TypeError): return None

def ITEM(d, *args):
    match len(args):
        case 1: return d[args[0]]
        case 2: return d[args[0]][args[1]]
        case 3: return d[args[0]][args[1]][args[2]]
        case _: raise Exception()

def REMDR(i1, i2): return i1 % i2
def SORT(d):       return d
def RSORT(d):      return d
def TABLE(i1, i2): return dict()

def ARRAY(proto, d):
    limits = tuple(int(x) for x in proto.split(','))
    match len(limits):
        case 1: return [d] * limits[0]
        case 2: return [[d] * limits[1]] * limits[0]
        case 3: return [[[d] * limits[2]] * limits[1]] * limits[0]
        case _: raise Exception()

def CONVERT(d, s):
    match s.upper():
        case 'STRING':
            match type(d).__name__:
                case 'int'  | 'float': return str(d)
                case 'str'            : return d
                case 'list'           : return 'ARRAY(' + PROTOTYPE(d) + ')'
                case 'dict'           : return 'TABLE(' + str(len(d)) + ')'
                case _                : return type(d).__name__
        case 'INTEGER':    return int(d)
        case 'REAL':       return float(d)
        case 'EXPRESSION': return compile(str(d), '<CONVERT>', 'single')
        case 'CODE':       return compile(str(d), '<CONVERT>', 'exec')
        case _:            return d

_re_proto = re.compile(r"\<function\ ([^\s]+)\ at\ 0x[0-9a-fA-F]+\>\(\*([0-9]+)\)")
def PROTOTYPE(P):
    p = repr(P)
    r = _re_proto.fullmatch(p)
    if r: return f"{r.group(1)}(*{r.group(2)})"
    return p

# ── Environment-dependent functions ───────────────────────────────────────────
# All of these read _env._g — the single shared SNOBOL environment dict.

def DUMP(i):
    if int(i) != 0: print(_env._g)

def EVAL(s):
    return eval(s, _env._g)

def EXEC(s):
    return exec(s, _env._g)

def VALUE(n):
    return _env._g[n]

# ── I/O association ───────────────────────────────────────────────────────────
def INPUT(n, u, len=None, fname=None):
    if not u: u = 0
    match u:
        case 0: _env._g[n] = None; _units[u] = (n, sys.stdin)
        case 1 | 2: raise Exception()
        case _: _env._g[n] = None; _units[u] = (n, open(fname, "rt"))
    return ""

def OUTPUT(n, u, len=None, fname=None):
    if not u: u = 1
    match u:
        case 0: raise Exception()
        case 1: _env._g[n] = None; _units[u] = (n, sys.stdout)
        case 2: _env._g[n] = None; _units[u] = (n, sys.stderr)
        case _: _env._g[n] = None; _units[u] = (n, open(fname, "wt"))
    return ""

def DETACH(n):
    del _env._g[n]

def ENDFILE(u):
    if not u: u = 0
    match u:
        case 0 | 1 | 2:
            del _env._g[_units[u][0]]; del _units[u]
        case _:
            del _env._g[_units[u][0]]; _units[u][1].close(); del _units[u]
    return ""

def BACKSPACE(u): pass      # backspace one record
def REWIND():     pass      # reposition to first file

# ── DEFINE / APPLY ────────────────────────────────────────────────────────────
_rex_define = re.compile(r"^(\w+)\((\w+(?:,\w+)*)\)(\w+(?:,\w+)*)$")

def DEFINE(proto, n=None):
    m = _rex_define.fullmatch(proto)
    if not m:
        return None
    func_name   = m.group(1)
    func_params = tuple(p for p in m.group(2).split(','))
    # func_locals = m.group(3)  — reserved for future use
    params = ', '.join(func_params)
    body   = f'def {func_name}({params}):\n    print({params})'
    code   = compile(body, '<DEFINE>', 'exec')
    func   = types.FunctionType(code.co_consts[0], _env._g, func_name)
    func.__defaults__ = (None,) * len(func_params)
    _env._g[func_name] = func
    return ""

def APPLY(n, *args): return _env._g[n](*args)
def ARG(n, i):       pass
def LOCAL(n, i):     pass
def LOAD(proto, lib): pass
def UNLOAD(s):        pass

# ── DATA / FIELD ──────────────────────────────────────────────────────────────
_rex_data = re.compile(r"^(\w+)\((\w+(?:,\w+)*)\)$")

def FIELD(s, i): return s.__slots__[int(i)]

def DATA(s):
    m = _rex_data.fullmatch(s)
    if not m:
        return None
    name   = m.group(1)
    fields = tuple(f for f in m.group(2).split(','))
    def __init__(self, *args):
        for i, value in enumerate(args):
            setattr(self, self.__slots__[i], value)
    _env._g[name] = type(name, (object,), {'__slots__': fields, '__init__': __init__})
    return ""

# ── Control-flow stubs (meaningful only in a full SNOBOL4 runtime) ────────────
def END():     pass
def RETURN():  pass
def FRETURN(): pass
def NRETURN(): pass

# ── Stubs for unimplemented features ──────────────────────────────────────────
def OPSYN(s1, s2, i): pass
def STOPTR(n, t):     pass

# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import copy
class PATTERN(object):
    def __init__(self, func, args, kwargs):
#       print(f"__init__({func})")
        self.func = func
        self.args = copy.copy(args)
        self.kwargs = copy.copy(kwargs)
        self.local_copy = self.func(*self.args, **self.kwargs)

    def __iter__(self):
        self.local_copy = self.func(*self.args, **self.kwargs)
#       print(f"__iter__({self})")
#       print(f"__iter__({self}) = {self.local_copy}")
        return self.local_copy

    def __next__(self):
#       print(f"__next__({self})")
        return next(self.local_copy)

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

#from functools import wraps
def pattern(func: callable) -> callable:
#   @wraps(func)
#   def _PATTERN_(*args, **kwargs):
#       return PATTERN(func, args, kwargs)
#   return _PATTERN_
    return lambda *args, **kwargs: PATTERN(func, args, kwargs)

#------------------------------------------------------------------------------
# Built-in pattern matching
#
pos = 0
subject = ""
results = None

_UCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LCASE = "abcdefghijklmnopqrstuvwxyz"
_digits = "0123456789"

def _(S):
    return LIT(S)

def FAIL():
    raise StopIteration

def SUCCESS():
    while True:
        yield ""    

@pattern
def ε(): yield ""    

@pattern
def assign(P, V):
    global results
    for _1 in P:
        results[V] = _1
#       print(f"{V} = {_1}")
        yield _1
#       print(f"{V} deleted")
        del results[V]

@pattern
def FENCE(p):
    yield next(p)

@pattern
def POS(n):
    global pos
    if pos == n:
#       print(f">>> POS({n})")
        yield ""
#       print(f"<<< POS({n})")
   
@pattern
def RPOS(n):
    global pos, subject
    if pos == len(subject) - n:
#       print(f">>> RPOS({n})")
        yield ""
#       print(f"<<< RPOS({n})")

@pattern
def REM():
    global pos, subject
    pos0 = pos
    pos = len(subject)
    yield subject[pos0:]
    pos = pos0
    
@pattern
def LEN(n):
    global pos, subject
    if pos + n <= len(subject):
        pos += n
        yield subject[pos - n:pos]
        pos -= n
        
@pattern
def LIT(lit):
    global pos, subject
    if pos + len(lit) <= len(subject):
        if lit == subject[pos:pos + len(lit)]:
            pos += len(lit)
#           print(f">>> LIT({lit}) = {pos - len(lit)}, {len(lit)}")
            yield lit
#           print(f"<<< LIT({lit})")
            pos -= len(lit)

@pattern
def TAB(n):
    global pos, subject
    if n <= len(subject):
        if n >= pos:
            pos0 = pos
            pos = n
            yield subject[pos0:n]
            pos = pos0
        
@pattern
def RTAB(n):
    global pos, subject
    if n <= len(subject):
        n = len(subject) - n
        if n >= pos:
            pos0 = pos
            pos = n
            yield subject[pos0:n]
            pos = pos0
    
@pattern
def ANY(characters):
    global pos, subject
    if pos < len(subject):
        if subject[pos] in characters:
            pos += 1
            yield subject[pos - 1]
            pos -= 1

@pattern 
def NOTANY(characters):
    global pos, subject
    if pos < len(subject):
        if not subject[pos] in characters:
            pos += 1
            yield subject[pos - 1]
            pos -= 1
    
@pattern 
def SPAN(characters):
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

@pattern 
def BREAK(characters):
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

@pattern
def ARBNO(P):
    global pos
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

@pattern
def AND(P, Q):
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

@pattern
def ALT(*AP):
    for P in AP:
        yield from P

@pattern
def SEQ(*AP):
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

def MATCH(S, P):
    global pos, subject, results
    pos = 0
    subject = S
    results = dict()
    try:
        m = next(P)
        print(f'"{S}" ? "{m}" {results}')
        return True
    except StopIteration:
        print(f'"{S}" FAIL')
        return False

 # -*- coding: utf-8 -*-
import SNOBOL4python as S4p
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, Σ, Π, ANY, ARB, ARBNO, BAL, FENCE, POS, RPOS, SPAN
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
@pattern
def RegEx():        yield from POS(0) + Expression() + RPOS(0)
@pattern
def Expression():   yield from Term() + ARBNO(σ('|') + Term())
@pattern
def Term():         yield from ARBNO(Factor())
@pattern
def Factor():       yield from Item() + Quantifier()
@pattern
def Item():         yield from \
                             ( σ('.')
                             | σ('\\') + ANY('.\\(|*+?)')
                             | ANY(_UCASE + _LCASE + _digits)
                             | σ('(') + Expression() + σ(')')
                             )
@pattern
def Quantifier():   yield from σ('*') | σ('+') | σ('?') | ε()
#------------------------------------------------------------------------------
assert True  is MATCH("", RegEx())
assert True  is MATCH("a", RegEx())
assert True  is MATCH("aa", RegEx())
assert True  is MATCH("a*", RegEx())
assert True  is MATCH("a+", RegEx())
assert True  is MATCH("a?", RegEx())
assert True  is MATCH("aaa", RegEx())
assert False is MATCH("a|b", RegEx())
assert False is MATCH("a|bc", RegEx())
assert False  is MATCH("ab|c", RegEx())
assert True  is MATCH("(a|b)*", RegEx())
assert True  is MATCH("(a|b)+", RegEx())
assert True  is MATCH("(a|b)?", RegEx())
assert True  is MATCH("(a|b)c", RegEx())
assert True  is MATCH("a|(bc)", RegEx())
assert False is MATCH("(ab|cd)", RegEx())
assert False is MATCH("(ab*|cd*)", RegEx())
assert True  is MATCH("((ab)*|(cd)*)", RegEx())
assert True  is MATCH("(a|(bc))", RegEx())
assert True  is MATCH("((ab)|c)", RegEx())
assert True  is MATCH("a(a|b)*b", RegEx())
assert True  is MATCH("(ab|(cd))", RegEx())
#------------------------------------------------------------------------------

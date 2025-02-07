 # -*- coding: utf-8 -*-
import SNOBOL4python as S4p
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, Σ, Π
from SNOBOL4python import ANY, ARB, ARBNO, BAL, FENCE, POS, RPOS, SPAN
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
@pattern
def re_RegEx():      yield from POS(0) + re_Expression() + RPOS(0)
@pattern
def re_Expression(): yield from re_Term() + ARBNO(σ('|') + re_Term())
@pattern
def re_Term():       yield from ARBNO(re_Factor())
@pattern
def re_Factor():     yield from re_Item() + re_Quantifier()
@pattern
def re_Item():       yield from ( σ('.')
                                | σ('\\') + ANY('.\\(|*+?)')
                                | ANY(_UCASE + _LCASE + _digits)
                                | σ('(') + re_Expression() + σ(')')
                                )
@pattern
def re_Quantifier(): yield from σ('*') | σ('+') | σ('?') | ε()
#------------------------------------------------------------------------------
assert True  is MATCH("", re_RegEx())
assert True  is MATCH("a", re_RegEx())
assert True  is MATCH("aa", re_RegEx())
assert True  is MATCH("a*", re_RegEx())
assert True  is MATCH("a+", re_RegEx())
assert True  is MATCH("a?", re_RegEx())
assert True  is MATCH("aaa", re_RegEx())
assert True  is MATCH("a|b", re_RegEx())
assert True  is MATCH("a|bc", re_RegEx())
assert True  is MATCH("ab|c", re_RegEx())
assert True  is MATCH("(a|b)*", re_RegEx())
assert True  is MATCH("(a|b)+", re_RegEx())
assert True  is MATCH("(a|b)?", re_RegEx())
assert True  is MATCH("(a|b)c", re_RegEx())
assert True  is MATCH("a|(bc)", re_RegEx())
assert True  is MATCH("(ab|cd)", re_RegEx())
assert True  is MATCH("(ab*|cd*)", re_RegEx())
assert True  is MATCH("((ab)*|(cd)*)", re_RegEx())
assert True  is MATCH("(a|(bc))", re_RegEx())
assert True  is MATCH("((ab)|c)", re_RegEx())
assert True  is MATCH("a(a|b)*b", re_RegEx())
assert True  is MATCH("(ab|(cd))", re_RegEx())
#------------------------------------------------------------------------------

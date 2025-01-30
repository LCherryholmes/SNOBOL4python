 # -*- coding: utf-8 -*-
import SNOBOL4python as S4p
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, Σ, Π, ANY, ARB, ARBNO, BAL, FENCE, POS, RPOS, SPAN
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
@pattern
def RegEx():        yield from POS(0) + Expr() + RPOS(0)
@pattern
def Expr():         yield from Term() + ARBNO(σ('|') + Term())
@pattern
def Term():         yield from Factor() + ARBNO(Factor())
@pattern
def Factor():       yield from Match() + Quantifier()
@pattern
def Quantifier():   yield from σ('*')  | σ('+')  | σ('?') | ε()
@pattern
def Match():        yield from \
                             ( σ('.')
                             | σ('\\.')
                             | σ('\\(')
                             | σ('\\|')
                             | σ('\\*')
                             | σ('\\+')
                             | σ('\\?')
                             | σ('\\)')
                             | σ('\\\\')
                             | ANY(_UCASE + _LCASE + _digits)
                             | σ('(') + Expr() + σ(')')
                             )
#------------------------------------------------------------------------------
assert False is MATCH("", RegEx())
assert True  is MATCH("a", RegEx())
assert True  is MATCH("aa", RegEx())
assert True  is MATCH("a*", RegEx())
assert True  is MATCH("a+", RegEx())
assert True  is MATCH("a?", RegEx())
assert True  is MATCH("aaa", RegEx())
assert True  is MATCH("a|b", RegEx())
assert False is MATCH("a|bc", RegEx())
assert True  is MATCH("ab|c", RegEx())
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

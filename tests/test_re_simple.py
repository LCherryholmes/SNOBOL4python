# -*- coding: utf-8 -*-
import SNOBOL4python as S4p
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, π, Λ, λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, FENCE, POS, RPOS, SPAN
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
@pattern
def re_RegEx():      yield from POS(0) + re_Expression() + Pop('RE_tree') + RPOS(0)
@pattern
def re_Expression(): yield from ( nPush()
                                + re_Term() + nInc()
                                + ARBNO(σ('|') + re_Term() + nInc())
                                + Reduce('Π')
                                + nPop()
                                )
@pattern
def re_Term():       yield from nPush() + ARBNO(re_Factor() + nInc()) + Reduce('Σ') + nPop()
@pattern
def re_Factor():     yield from re_Item() + (re_Quantifier() + Reduce('ς', 2) | ε())
@pattern
def re_Item():       yield from ( σ('.') + Shift('.')
                                | σ('\\') + ANY('.\\(|*+?)') % 'tx' + Shift('σ', "tx")
                                | ANY(UCASE + LCASE + DIGITS) % 'tx' + Shift('σ', "tx")
                                | σ('(') + re_Expression() + σ(')')
                                )
@pattern
def re_Quantifier(): yield from ( σ('*') + Shift('*')
                                | σ('+') + Shift('+')
                                | σ('?') + Shift('?')
                                )
#------------------------------------------------------------------------------
rexs = {
    "",
    "A",
    "AA",
    "A*",
    "A+",
    "A?",
    "AAA",
    "A|B",
    "A|BC",
    "AB|C",
    "(A|)",
    "(A|)*",
    "(A|B)*",
    "(A|B)+",
    "(A|B)?",
    "(A|B)C",
    "A|(BC)",
    "(AB|CD)",
    "(AB*|CD*)",
    "((AB)*|(CD)*)",
    "(A|(BC))",
    "((AB)|C)",
    "A(A|B)*B",
    "(Ab|(CD))"
}
#------------------------------------------------------------------------------
results = dict()
from pprint import pprint
for rex in rexs:
    print(rex)
    results.clear()
    GLOBALS(results)
    if rex in re_RegEx():
#       pprint(results)
        pprint(results['RE_tree'], indent=3, width=36)
        print()
#------------------------------------------------------------------------------

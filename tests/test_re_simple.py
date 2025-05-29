# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import SNOBOL4python
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from SNOBOL4python import PATTERN, STRING
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
re_Quantifier   =   ( σ('*') + Shift('*')
                    | σ('+') + Shift('+')
                    | σ('?') + Shift('?')
                    )
re_Item         =   ( σ('.') + Shift('.')
                    | σ('\\') + ANY('.\\(|*+?)') % 'tx' + Shift('σ', "tx")
                    | ANY(UCASE + LCASE + DIGITS) % 'tx' + Shift('σ', "tx")
                    | σ('(') + ζ(lambda: re_Expression) + σ(')')
                    )
re_Factor       =   re_Item + (re_Quantifier + Reduce('ς', 2) | ε())
re_Term         =   nPush() + ARBNO(re_Factor + nInc()) + Reduce('Σ') + nPop()
re_Expression   =   ( nPush()
                    + re_Term + nInc()
                    + ARBNO(σ('|') + re_Term + nInc())
                    + Reduce('Π')
                    + nPop()
                    )
re_RegEx        =   POS(0) + re_Expression + Pop('RE_tree') + RPOS(0)
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
from pprint import pprint
results = dict()
TRACE(40)
GLOBALS(results)
for rex in rexs:
    print(rex)
    results.clear()
    if rex in re_RegEx:
        pprint(results['RE_tree'], indent=3, width=36)
        print()
#------------------------------------------------------------------------------

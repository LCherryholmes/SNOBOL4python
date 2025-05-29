# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import PATTERN, STRING, NULL
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, pformat
GLOBALS(globals())
TRACE(40)
#------------------------------------------------------------------------------
icon_source = "every write(5 > ((1 to 2) * (3 to 4)));"
#------------------------------------------------------------------------------
η           =   SPAN(" \t\r\n") | ε()
def ς(s):       return η + σ(s) @ "text"
integer     =   η + SPAN(DIGITS) @ "text" % "value"
word        =   η + SPAN(LCASE) @ "text" % "word"
to          =   word + Λ(lambda: text == "to")
every       =   word + Λ(lambda: text == "every")
write       =   word + Λ(lambda: text == "write")
variable    =   word + Λ(lambda: text not in ["every", "to"])
function    =   word + Λ(lambda: text in ["write"])
#------------------------------------------------------------------------------
expression6 =   ( ς('(') + ζ("expression1") + ς(')')
                | write + ς('(') + ζ("expression1") + ς(')') + Reduce("WRITE", 1)
                | variable + Shift("V", "word")
                | integer + Shift("I", "value")
                )
#------------------------------------------------------------------------------
expression5 =   ( ς('+') + ζ("expression5") + Reduce('+', 1)
                | ς('-') + ζ("expression5") + Reduce('-', 1)
                | expression6
                )
#------------------------------------------------------------------------------
expression4 =   ( expression5
                + ( ς('*') + ζ("expression4") + Reduce('*', 2)
                  | ς('/') + ζ("expression4") + Reduce('/', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
expression3  =  ( expression4
                + ( ς('+') + ζ("expression3") + Reduce('+', 2)
                  | ς('-') + ζ("expression3") + Reduce('-', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
expression2  =  ( expression3 + to + expression3 + Reduce('TO', 2)
                | expression3
                )
#------------------------------------------------------------------------------
expression1 =   ( expression2
                + ( ς('<')  + expression2 + Reduce('<', 2)
                  | ς('>')  + expression2 + Reduce('>', 2)
                  | ς('==') + expression2 + Reduce('==', 2)
                  | ς('<=') + expression2 + Reduce('<=', 2)
                  | ς('>=') + expression2 + Reduce('<=', 2)
                  | ς('!=') + expression2 + Reduce('!=', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
statement   =   ( every + expression1 + Reduce('EVERY', 1)
                | expression1
                )
#------------------------------------------------------------------------------
program     =   ( POS(0)
                + nPush()
                + ARBNO(statement + nInc() + ς(';'))
                + Reduce("ICON")
                + nPop()
                + Pop('icon')
                + RPOS(0)
                )
#------------------------------------------------------------------------------
if icon_source in program:
    pprint(icon)
else: print("Boo!")
#------------------------------------------------------------------------------

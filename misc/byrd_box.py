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
η         =   SPAN(" \t\r\n") | ε()
def ς(s):     return η + σ(s) @ "text"
integer   =   η + SPAN(DIGITS) @ "text" % "value"
word      =   η + SPAN(LCASE) @ "text" % "word"
to        =   word + Λ(lambda: text == "to")
every     =   word + Λ(lambda: text == "every")
write     =   word + Λ(lambda: text == "write")
variable  =   word + Λ(lambda: text not in ["every", "to"])
function  =   word + Λ(lambda: text in ["write"])
#------------------------------------------------------------------------------
expr6     =   ( ς('(') + ζ("expr1") + ς(')')
              | write + ς('(') + ζ("expr1") + ς(')') + Reduce("WRITE", 1)
              | variable + Shift("V", "word")
              | integer + Shift("I", "value")
              )
#------------------------------------------------------------------------------
expr5     =   ( ς('+') + ζ("expr5") + Reduce('+', 1)
              | ς('-') + ζ("expr5") + Reduce('-', 1)
              | expr6
              )
#------------------------------------------------------------------------------
expr4     =   ( expr5
              + ( ς('*') + ζ("expr4") + Reduce('*', 2)
                | ς('/') + ζ("expr4") + Reduce('/', 2)
                | ε()
                )
              )
#------------------------------------------------------------------------------
expr3     =   ( expr4
              + ( ς('+') + ζ("expr3") + Reduce('+', 2)
                | ς('-') + ζ("expr3") + Reduce('-', 2)
                | ε()
                )
              )
#------------------------------------------------------------------------------
expr2     =   ( expr3 + to + expr3 + Reduce('TO', 2)
              | expr3
              )
#------------------------------------------------------------------------------
expr1     =   ( expr2
              + ( ς('<')  + expr2 + Reduce('<', 2)
                | ς('>')  + expr2 + Reduce('>', 2)
                | ς('==') + expr2 + Reduce('==', 2)
                | ς('<=') + expr2 + Reduce('<=', 2)
                | ς('>=') + expr2 + Reduce('<=', 2)
                | ς('!=') + expr2 + Reduce('!=', 2)
                | ε()
                )
              )
#------------------------------------------------------------------------------
stmt        =   every + expr1 + Reduce('EVERY', 1) | expr1
#------------------------------------------------------------------------------
program     =   ( POS(0)
              + nPush()
              + ARBNO(stmt + nInc() + ς(';'))
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

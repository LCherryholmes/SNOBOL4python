# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import PATTERN, STRING, NULL
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, pformat
#-----------------------------------------------------------------------------------------------------------------------
import ctypes
#print(ctypes.CDLL("/mnt/c/SNOBOL4python/misc/_bootstrap.so"))
from _bootstrap import _bootstrap # import the C extension function
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
TRACE(40)
"""
#-----------------------------------------------------------------------------------------------------------------------
BEAD = POS(0) + (σ('B') | σ('R')) + (σ('E') | σ('EA')) + (σ('D') | σ('DS')) + RPOS(0)
_bootstrap("READS", BEAD, "BEAD")
print()
#-----------------------------------------------------------------------------------------------------------------------
P = σ('BE') | σ('BEA') | σ('BEAR')
Q = σ('RO') | σ('ROO') | σ('ROOS')
R = σ('DS') | σ('D')
S = σ('TS') | σ('T')
BEARDS = POS(0) + (P + R | Q + S) + RPOS(0)
_bootstrap("ROOSTS", BEARDS, "BEARDS")
print()
#-----------------------------------------------------------------------------------------------------------------------
V = ANY(LCASE) % "N"      + λ("S.append(int(globals()[N]))")
I = SPAN(DIGITS) % "N"    + λ("S.append(int(N))")
E = ( V | I | σ('(') + ζ("X") + σ(')'))
X = ( E + σ('+') + ζ("X") + λ("S.append(S.pop() + S.pop())")
    | E + σ('-') + ζ("X") + λ("S.append(S.pop() - S.pop())")
    | E + σ('*') + ζ("X") + λ("S.append(S.pop() * S.pop())")
    | E + σ('/') + ζ("X") + λ("S.append(S.pop() // S.pop())")
    | σ('+') + ζ("X")
    | σ('-') + ζ("X")     + λ("S.append(-S.pop())")
    | E
    )
C = POS(0) + λ("S = []") + X + λ("print(S.pop())") + RPOS(0)
_bootstrap("x+y*z", C, "C")
print()
#-----------------------------------------------------------------------------------------------------------------------
RE_Quantifier   =   ( σ('*') + Shift('*')
                    | σ('+') + Shift('+')
                    | σ('?') + Shift('?')
                    )
RE_Item         =   ( σ('.') + Shift('.')
                    | σ('\\') + ANY('.\\(|*+?)') % 'tx' + Shift('σ', "tx")
                    | ANY(UCASE + LCASE + DIGITS) % 'tx' + Shift('σ', "tx")
                    | σ('(') + ζ("RE_Expression") + σ(')')
                    )
RE_Factor       =   ζ("RE_Item") + (ζ("RE_Quantifier") + Reduce('ς', 2) | ε())
RE_Term         =   nPush() + ARBNO(ζ("RE_Factor") + nInc()) + Reduce('Σ') + nPop()
RE_Expression   =   ( nPush()
                    + ζ("RE_Term") + nInc()
                    + ARBNO(σ('|') + ζ("RE_Term") + nInc())
                    + Reduce('Π')
                    + nPop()
                    )
RE_RegEx        =   POS(0) + ζ("RE_Expression") + Pop('RE_tree') + RPOS(0)
_bootstrap("", RE_Quantifier, "RE_Quantifier")
_bootstrap("", RE_Item, "RE_Item")
_bootstrap("", RE_Factor, "RE_Factor")
_bootstrap("", RE_Term, "RE_Term")
_bootstrap("", RE_Expression, "RE_Expression")
_bootstrap("", RE_RegEx, "RE_RegEx")
print()
"""
#-----------------------------------------------------------------------------------------------------------------------
P = FENCE(TAB(lambda: N + 1) + Θ("OUTPUT") + Θ("N") | ABORT())
S = POS(0) + Θ("N") + SUCCEED() + ζ("P") + FAIL()
_bootstrap("", P, "P")
_bootstrap("", S, "S")
print()
#-----------------------------------------------------------------------------------------------------------------------

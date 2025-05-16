# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import PATTERN, STRING, NULL
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, pformat
#-----------------------------------------------------------------------------------------------------------------------
import ctypes
print(ctypes.CDLL("/mnt/c/SNOBOL4python/misc/_bootstrap.so"))
from _bootstrap import _bootstrap # import the C extension function
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
TRACE(40)
#   --------------------------------------------------------------------------------------------------------------------
V = ANY(LCASE) % "N"      + λ(lambda: S.append(int(globals()[N])))
I = SPAN(DIGITS) % "N"    + λ(lambda: S.append(int(N)))
E = ( V | I | σ('(') + ζ("X") + σ(')'))
X = ( E + σ('+') + ζ("X") + λ(lambda: S.append(S.pop() + S.pop()))
    | E + σ('-') + ζ("X") + λ(lambda: S.append(S.pop() - S.pop()))
    | E + σ('*') + ζ("X") + λ(lambda: S.append(S.pop() * S.pop()))
    | E + σ('/') + ζ("X") + λ(lambda: S.append(S.pop() // S.pop()))
    | σ('+') + ζ("X")
    | σ('-') + ζ("X")     + λ(lambda: S.append(-S.pop()))
    | E
    )
C = POS(0) + λ("S = []") + X + λ(lambda: print(S.pop())) + RPOS(0)

x = 1; y = 2; z = 3
for s in ["x+y*z", "x+(y*z)", "(x+y)*z"]:
    if not s in C:
        print("Boo!")

_bootstrap("x+y*z", C)
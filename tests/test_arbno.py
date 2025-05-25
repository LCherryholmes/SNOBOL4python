# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#------------------------------------------------------------------------------
TRACE(50)
GLOBALS(globals())
#------------------------------------------------------------------------------
As = (POS(0) + ARBNO(σ('a')) @ 'sequence' + RPOS(0))
assert True  is ("" in As)
assert True  is ("a" in As)
assert True  is ("aa" in As)
assert True  is ("aaa" in As)
assert True  is ("aaaa" in As)
#------------------------------------------------------------------------------
Alist = ( POS(0)
        + (σ('a') | σ('b'))
        + ARBNO(σ(',') + (σ('a') | σ('b')))
        + RPOS(0)
        )
assert False is ("" in Alist)
assert True  is ("a" in Alist)
assert True  is ("a,a" in Alist)
assert True  is ("a,a,a" in Alist)
assert True  is ("a,a,a,a" in Alist)
#------------------------------------------------------------------------------
Pairs = POS(0) + ARBNO(σ('AA') | LEN(2) | σ('XX')) + RPOS(0)
assert False is ('CCXXAA$' in Pairs)
#------------------------------------------------------------------------------
PAIRS = \
    ( Θ('pos') + Λ(lambda: print('POS try', pos))
    + POS(0)
    + Λ(lambda: print('POS got'))
    + ARBNO(
          (Θ('pos') + Λ(lambda: print('AA try', pos))     + σ('AA') @ 'tx' + Λ(lambda: print(tx, 'got')))
        | (Θ('pos') + Λ(lambda: print('LEN(2) try', pos)) + LEN(2)  @ 'tx' + Λ(lambda: print(tx, 'got')))
        | (Θ('pos') + Λ(lambda: print('XX try', pos))     + σ('XX') @ 'tx' + Λ(lambda: print(tx, 'got')))
      )
    + Θ('pos') + Λ(lambda: print('RPOS try', pos))
    + RPOS(0)
    + Λ(lambda: print('RPOS got'))
    )
# assert False is ('CCXXAA$' in PAIRS)
#------------------------------------------------------------------------------

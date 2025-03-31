# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, Σ, Π, Λ, λ, θ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, FENCE, LEN, POS, RPOS, SPAN
#------------------------------------------------------------------------------
GLOBALS(globals())
#------------------------------------------------------------------------------
@pattern
def As():
    yield from \
        (   POS(0)
        +   ARBNO(σ('a')) @ 'sequence'
        +   RPOS(0)
        )
assert True  is ("" in As())
assert True  is ("a" in As())
assert True  is ("aa" in As())
assert True  is ("aaa" in As())
assert True  is ("aaaa" in As())
#------------------------------------------------------------------------------
@pattern
def Alist():
    yield from \
        (   POS(0)
        +   (σ('a') | σ('b'))
        +   ARBNO(σ(',') + (σ('a') | σ('b')))
        +   RPOS(0)
        )
assert False is ("" in Alist())
assert True  is ("a" in Alist())
assert True  is ("a,a" in Alist())
assert True  is ("a,a,a" in Alist())
assert True  is ("a,a,a,a" in Alist())
#------------------------------------------------------------------------------
@pattern
def Pairs(): yield from POS(0) + ARBNO(σ('AA') | LEN(2) | σ('XX')) + RPOS(0)
assert False is ('CCXXAA$' in Pairs())
#------------------------------------------------------------------------------
@pattern
def PAIRS(): yield from \
    (
        θ('pos') + Λ(lambda: print('POS try', pos))
    +   POS(0)
    +   Λ(lambda: print('POS got'))
    +   ARBNO(
          (θ('pos') + Λ(lambda: print('AA try', pos))     + σ('AA') @ 'tx' + Λ(lambda: print(tx, 'got')))
        | (θ('pos') + Λ(lambda: print('LEN(2) try', pos)) + LEN(2)  @ 'tx' + Λ(lambda: print(tx, 'got')))
        | (θ('pos') + Λ(lambda: print('XX try', pos))     + σ('XX') @ 'tx' + Λ(lambda: print(tx, 'got')))
        )
    +   θ('pos') + Λ(lambda: print('RPOS try', pos))
    +   RPOS(0)
    +   Λ(lambda: print('RPOS got'))
    )
# assert False is ('CCXXAA$' in PAIRS())
#------------------------------------------------------------------------------

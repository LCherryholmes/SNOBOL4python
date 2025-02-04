# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, Σ, Π, λ, Λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, FENCE, LEN, POS, RPOS, SPAN
#------------------------------------------------------------------------------
@pattern
def As():
    yield from \
        (   POS(0)
        +   ARBNO(σ('a')) @ 'sequence'
        +   RPOS(0)
        )
assert True  is MATCH("", As())
assert True  is MATCH("a", As())
assert True  is MATCH("aa", As())
assert True  is MATCH("aaa", As())
assert True  is MATCH("aaaa", As())
#------------------------------------------------------------------------------
@pattern
def Alist():
    yield from \
        (   POS(0)
        +   (σ('a') | σ('b'))
        +   ARBNO(σ(',') + (σ('a') | σ('b')))
        +   RPOS(0)
        )
assert False is MATCH("", Alist())
assert True  is MATCH("a", Alist())
assert True  is MATCH("a,a", Alist())
assert True  is MATCH("a,a,a", Alist())
assert True  is MATCH("a,a,a,a", Alist())
#------------------------------------------------------------------------------
@pattern
def Pairs(): yield from POS(0) + ARBNO(σ('AA') | LEN(2) | σ('XX')) + RPOS(0)
assert False is MATCH('CCXXAA$', Pairs())
#------------------------------------------------------------------------------
@pattern
def PAIRS(): yield from \
    (
        AT('pos') + λ(lambda: print('POS try', pos))
    +   POS(0)
    +   λ(lambda: print('POS got'))
    +   ARBNO(
          (AT('pos') + λ(lambda: print('AA try', pos))     + σ('AA') @ 'tx' + λ(lambda: print(tx, 'got')))
        | (AT('pos') + λ(lambda: print('LEN(2) try', pos)) + LEN(2)  @ 'tx' + λ(lambda: print(tx, 'got')))
        | (AT('pos') + λ(lambda: print('XX try', pos))     + σ('XX') @ 'tx' + λ(lambda: print(tx, 'got')))
        )
    +   AT('pos') + λ(lambda: print('RPOS try', pos))
    +   RPOS(0)
    +   λ(lambda: print('RPOS got'))
    )
# assert False is MATCH('CCXXAA$', PAIRS())
#------------------------------------------------------------------------------

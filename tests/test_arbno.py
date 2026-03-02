# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import pytest
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
#------------------------------------------------------------------------------
Alist = ( POS(0)
        + (σ('a') | σ('b'))
        + ARBNO(σ(',') + (σ('a') | σ('b')))
        + RPOS(0)
        )
#------------------------------------------------------------------------------
Pairs = POS(0) + ARBNO(σ('AA') | LEN(2) | σ('XX')) + RPOS(0)
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
#------------------------------------------------------------------------------
# ── As: ARBNO(σ('a')) ──────────────────────────────────────────────────────

@pytest.mark.parametrize("s", ["", "a", "aa", "aaa", "aaaa"])
def test_as_matches(s):
    assert s in As

@pytest.mark.parametrize("s", ["b", "ab", "ba", "aab", "aaab"])
def test_as_no_match(s):
    assert s not in As

#------------------------------------------------------------------------------
# ── Alist: comma-separated a/b tokens ──────────────────────────────────────

@pytest.mark.parametrize("s", [
    "a", "b",
    "a,a", "a,b", "b,a", "b,b",
    "a,a,a", "b,b,b",
    "a,a,a,a",
])
def test_alist_matches(s):
    assert s in Alist

@pytest.mark.parametrize("s", [
    "",       # empty — at least one element required
    ",a",     # leading comma
    "a,",     # trailing comma
    "a,,a",   # double comma
    "a,c",    # invalid token 'c'
    "c",      # completely invalid
])
def test_alist_no_match(s):
    assert s not in Alist

#------------------------------------------------------------------------------
# ── Pairs: ARBNO of even-length chunks ─────────────────────────────────────

@pytest.mark.parametrize("s", [
    "",         # zero iterations is valid
    "AA",
    "XX",
    "AB",       # any 2-char chunk via LEN(2)
    "AAXX",
    "AABB",
    "XXAA",
    "AABBCC",
])
def test_pairs_matches(s):
    assert s in Pairs

@pytest.mark.parametrize("s", [
    "CCXXAA$",  # odd-length tail '$' cannot be consumed
    "A",        # single char — LEN(2) requires two
    "AAA",      # three chars — not evenly divisible into pairs
])
def test_pairs_no_match(s):
    assert s not in Pairs

#------------------------------------------------------------------------------
# assert False is ('CCXXAA$' in PAIRS)
#------------------------------------------------------------------------------

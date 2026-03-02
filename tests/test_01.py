# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import pytest
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from SNOBOL4python import Σ, Π
#------------------------------------------------------------------------------
GLOBALS(globals())
#------------------------------------------------------------------------------
identifier = \
        (   POS(0)
        +   ANY(UCASE + LCASE)
        +   FENCE(SPAN("." + DIGITS + UCASE + "_" + LCASE) | ε())
        +   RPOS(0)
        )
#------------------------------------------------------------------------------
real_number = \
        (   POS(0)
        +   (   (   SPAN(DIGITS) @ 'whole'
                +   (σ('.') + FENCE(SPAN(DIGITS) | ε()) @ 'fract' | ε())
                +   (σ('E') | σ('e'))
                +   (σ('+') | σ('-') | ε())
                +   SPAN(DIGITS) @ 'exp'
                )
            |   (   SPAN(DIGITS) @ 'whole'
                +   σ('.')
                +   FENCE(SPAN(DIGITS) | ε()) @ 'fract'
                )
            )
        +   RPOS(0)
        )
#------------------------------------------------------------------------------
test_one = Σ( POS(0) @ 'OUTPUT'
           ,  Π(σ('B') , σ('F') , σ('L') , σ('R')) @ 'OUTPUT'
           ,  Π(σ('E') , σ('EA')) @ 'OUTPUT'
           ,  Π(σ('D') , σ('DS')) @ 'OUTPUT'
           ,  RPOS(0) @ 'OUTPUT'
           )
#------------------------------------------------------------------------------
# units = None
# romanXlat = '0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,'
# def Roman(n):
#     global units
#     if not MATCH_REPLACE(n, RPOS(1) + LEN(1) @ 'units', ''):
#         return ""
#     if not units, BREAK(',') @ 'units', globals()):
#         return None
#     return REPLACE(Roman(n),'IVXLCDM','XLCDM**') + units
# print(Roman(1))
# print(Roman(4))
# print(Roman(5))
# print(Roman(9))
# print(Roman(10))
#------------------------------------------------------------------------------
# BALEXP = NOTANY(' ( ) , ) I ' (' ARBNO( *BALEXP) ')')
# BAL BALEXP ARBNO(BALEXP)
# ALLBAL = BAL S OUTPUT FAIL
#------------------------------------------------------------------------------
Bal = POS(0) + BAL() @ 'OUTPUT' + RPOS(0)
#------------------------------------------------------------------------------
Arb = POS(0) + ARB() @ 'OUTPUT' + RPOS(0)
#------------------------------------------------------------------------------
# ── identifier ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("s", [
    "Id_99", "A", "Z", "abc", "X1", "a.b", "A_B_C",
])
def test_identifier_matches(s):
    assert s in identifier

@pytest.mark.parametrize("s", [
    "",        # empty
    "9abc",    # starts with digit
    "_abc",    # starts with underscore
    "a b",     # contains space
])
def test_identifier_no_match(s):
    assert s not in identifier

#------------------------------------------------------------------------------
# ── real_number ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("s", [
    "12.99E+3",   # canonical example
    "1.0E0",      # minimal scientific
    "0.5E-10",    # negative exponent
    "99.E+1",     # empty fractional part
    "3.14",       # simple decimal
    "0.0",        # zero
    "100.001",    # longer decimal
])
def test_real_number_matches(s):
    assert s in real_number

@pytest.mark.parametrize("s", [
    "",        # empty
    "abc",     # no digits
    "1",       # integer only — no decimal or exponent
    ".5",      # starts with decimal point
    "1.2.3",   # two decimal points
])
def test_real_number_no_match(s):
    assert s not in real_number

#------------------------------------------------------------------------------
# ── test_one (BEAD pattern) ────────────────────────────────────────────────

@pytest.mark.parametrize("word", [
    "BED",   "FED",   "LED",   "RED",
    "BEAD",  "FEAD",  "LEAD",  "READ",
    "BEDS",  "FEDS",  "LEDS",  "REDS",
    "BEADS", "FEADS", "LEADS", "READS",
])
def test_one_matches(word):
    assert word in test_one

@pytest.mark.parametrize("word", [
    "BID",    # wrong vowel
    "BREAD",  # extra consonant
    "ED",     # missing initial consonant
    "BEDSS",  # double suffix
    "",       # empty
])
def test_one_no_match(word):
    assert word not in test_one

#------------------------------------------------------------------------------
# ── BAL ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("expr", [
    "(A+B)",
    "A+B()",
    "A()+B",
    "X",
    "XYZ",
    "A(B*C) (E/F)G+H",
    "( (A+ ( B*C) ) +D)",
    "(0+(1*9))",
    "((A+(B*C))+D)",
])
def test_bal_matches(expr):
    assert expr in Bal

@pytest.mark.parametrize("expr", [
    "",          # empty — no balanced content
    ")A+B(",     # reversed parens
    "A+B)",      # unmatched close
    "(A+B",      # unmatched open
    "A+B())",    # extra close
    "((A+B)",    # extra open
])
def test_bal_no_match(expr):
    assert expr not in Bal

#------------------------------------------------------------------------------
# ── ARB ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("s", ["", "$", "$$", "$$$", "hello", "1 2 3"])
def test_arb_matches(s):
    assert s in Arb

#------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import pytest
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

@pytest.mark.parametrize("rex", [
    # empty and single characters
    "",
    "A",
    "AA",
    "AAA",
    # quantifiers
    "A*",
    "A+",
    "A?",
    # alternation
    "A|B",
    "A|BC",
    "AB|C",
    # grouping with alternation
    "(A|)",
    "(A|B)*",
    "(A|B)+",
    "(A|B)?",
    "(A|B)C",
    "(A|)*",
    # nested grouping
    "A|(BC)",
    "(AB|CD)",
    "(AB*|CD*)",
    "((AB)*|(CD)*)",
    "(A|(BC))",
    "((AB)|C)",
    "(Ab|(CD))",
    # complex
    "A(A|B)*B",
])
def test_re_parses(rex):
    results = dict()
    TRACE(40)
    GLOBALS(results)
    assert rex in re_RegEx

#------------------------------------------------------------------------------

def test_re_tree_is_tuple(rex='A|B'):
    results = dict()
    TRACE(40)
    GLOBALS(results)
    assert 'A|B' in re_RegEx
    assert isinstance(results['RE_tree'], tuple)
    assert len(results['RE_tree']) >= 1

#------------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "(",    # unmatched open paren
    ")",    # unmatched close paren
    "*",    # quantifier with no preceding item
    "+",    # quantifier with no preceding item
])
def test_re_no_parse(bad):
    results = dict()
    TRACE(40)
    GLOBALS(results)
    assert bad not in re_RegEx

#------------------------------------------------------------------------------

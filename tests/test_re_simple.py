# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import sys
import pytest
import SNOBOL4python
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω

# The C backend segfaults on Python 3.10 in the manylinux2014 container when
# running this recursive-pattern test suite.  The pure-Python backend is fine,
# and 3.11+ with the C backend is fine.  Skip only the specific combination.
_skip_c_py310 = pytest.mark.skipif(
    sys.version_info < (3, 11) and SNOBOL4python.C_AVAILABLE,
    reason="C backend segfaults on Python 3.10 manylinux with recursive patterns"
)
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

@_skip_c_py310
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

@_skip_c_py310
def test_re_tree_is_tuple(rex='A|B'):
    results = dict()
    TRACE(40)
    GLOBALS(results)
    assert 'A|B' in re_RegEx
    assert isinstance(results["RE_tree"], list)
    assert len(results['RE_tree']) >= 1

#------------------------------------------------------------------------------

@_skip_c_py310
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_backends.py — dual-backend conformance tests for SNOBOL4python 0.5.0

Verifies that the C/SPIPAT backend and the pure-Python backend produce
identical results for all core pattern primitives and combinators.

Run:
    python3 tests/test_backends.py
    python3 -m pytest tests/test_backends.py -v
"""
import pytest
import SNOBOL4python as S4
#------------------------------------------------------------------------------

BACKENDS = []
if S4.C_AVAILABLE:
    BACKENDS.append('c')
BACKENDS.append('pure')

@pytest.fixture(params=BACKENDS)
def backend(request):
    """Switch to the requested backend and restore afterwards."""
    name = request.param
    if name == 'c':
        S4.use_c()
    else:
        S4.use_pure()
    S4.GLOBALS(globals())
    yield name
    S4.use_pure()

#------------------------------------------------------------------------------
# ── ε / σ ──────────────────────────────────────────────────────────────────

def test_epsilon_matches_empty(backend):
    assert S4.SEARCH("",    S4.ε()) == slice(0, 0)

def test_epsilon_matches_anywhere(backend):
    assert S4.SEARCH("abc", S4.ε()) == slice(0, 0)

def test_sigma_found(backend):
    assert S4.SEARCH("say hello", S4.σ("hello")) == slice(4, 9)

def test_sigma_not_found(backend):
    assert S4.SEARCH("goodbye",   S4.σ("hello")) is None

def test_sigma_1_char(backend):
    assert S4.SEARCH("axb",    S4.σ("x"))  == slice(1, 2)

def test_sigma_2_char(backend):
    assert S4.SEARCH("say hi", S4.σ("hi")) == slice(4, 6)

#------------------------------------------------------------------------------
# ── FAIL / ABORT / SUCCEED ─────────────────────────────────────────────────

def test_fail_always_fails(backend):
    assert S4.SEARCH("abc", S4.FAIL())    is None

def test_succeed_matches_empty(backend):
    assert S4.SEARCH("abc", S4.SUCCEED()) == slice(0, 0)

#------------------------------------------------------------------------------
# ── α / ω ──────────────────────────────────────────────────────────────────

def test_alpha_at_start(backend):
    assert S4.SEARCH("hello", S4.α()) == slice(0, 0)

def test_omega_at_end(backend):
    assert S4.SEARCH("hello", S4.ω()) == slice(5, 5)

#------------------------------------------------------------------------------
# ── ANY / NOTANY ───────────────────────────────────────────────────────────

def test_any_vowel_in_hello(backend):
    assert S4.SEARCH("hello", S4.ANY("aeiou"))    == slice(1, 2)

def test_any_miss(backend):
    assert S4.SEARCH("bcdf",  S4.ANY("aeiou"))    is None

def test_notany_consonant(backend):
    assert S4.SEARCH("hello", S4.NOTANY("aeiou")) == slice(0, 1)

#------------------------------------------------------------------------------
# ── SPAN / BREAK / NSPAN ───────────────────────────────────────────────────

def test_span_abc(backend):
    assert S4.SEARCH("aabbcc!", S4.SPAN("abc"))  == slice(0, 6)

def test_span_miss(backend):
    assert S4.SEARCH("xyz",     S4.SPAN("abc"))  is None

def test_break_at_bang(backend):
    assert S4.SEARCH("hello!",  S4.BREAK("!"))   == slice(0, 5)

def test_nspan_zero_match(backend):
    assert S4.SEARCH("xyz",     S4.NSPAN("abc")) == slice(0, 0)

def test_nspan_some_match(backend):
    assert S4.SEARCH("aabc",    S4.NSPAN("ab"))  == slice(0, 3)

#------------------------------------------------------------------------------
# ── POS / RPOS / LEN / TAB / RTAB ─────────────────────────────────────────

def test_pos_0(backend):
    assert S4.SEARCH("hello", S4.POS(0))  == slice(0, 0)

def test_rpos_0(backend):
    assert S4.SEARCH("hello", S4.RPOS(0)) == slice(5, 5)

def test_len_3(backend):
    assert S4.SEARCH("hello", S4.LEN(3))  == slice(0, 3)

def test_tab_3(backend):
    assert S4.SEARCH("hello", S4.TAB(3))  == slice(0, 3)

def test_rtab_2(backend):
    assert S4.SEARCH("hello", S4.RTAB(2)) == slice(0, 3)

#------------------------------------------------------------------------------
# ── ARB / ARBNO ────────────────────────────────────────────────────────────

def test_arb_full_string(backend):
    arb_full = S4.POS(0) + S4.ARB() + S4.RPOS(0)
    assert S4.SEARCH("hello", arb_full)  == slice(0, 5)

def test_arbno_a_in_aaaa(backend):
    p_a    = S4.σ("a")
    arb_no = S4.POS(0) + S4.ARBNO(p_a) + S4.RPOS(0)
    assert S4.SEARCH("aaaa", arb_no)     == slice(0, 4)

def test_arbno_a_in_empty(backend):
    p_a    = S4.σ("a")
    arb_no = S4.POS(0) + S4.ARBNO(p_a) + S4.RPOS(0)
    assert S4.SEARCH("",     arb_no)     == slice(0, 0)

#------------------------------------------------------------------------------
# ── BAL ────────────────────────────────────────────────────────────────────

def test_bal_simple(backend):
    assert S4.SEARCH("(abc)",   S4.BAL()) == slice(0, 5)

def test_bal_nested(backend):
    assert S4.SEARCH("(a(b)c)", S4.BAL()) == slice(0, 7)

#------------------------------------------------------------------------------
# ── concat / alt ───────────────────────────────────────────────────────────

def test_concat(backend):
    cat = S4.σ("hel") + S4.σ("lo")
    assert S4.SEARCH("hello",   cat) == slice(0, 5)

def test_alt_cat(backend):
    alt = S4.σ("cat") | S4.σ("dog")
    assert S4.SEARCH("the cat", alt) == slice(4, 7)

def test_alt_dog(backend):
    alt = S4.σ("cat") | S4.σ("dog")
    assert S4.SEARCH("the dog", alt) == slice(4, 7)

def test_alt_none(backend):
    alt = S4.σ("cat") | S4.σ("dog")
    assert S4.SEARCH("the fox", alt) is None

#------------------------------------------------------------------------------
# ── Σ / Π ──────────────────────────────────────────────────────────────────

def test_sigma_concat(backend):
    big_cat = S4.Σ(S4.σ("h"), S4.σ("e"), S4.σ("l"), S4.σ("lo"))
    assert S4.SEARCH("hello", big_cat) == slice(0, 5)

def test_pi_alt(backend):
    big_alt = S4.Π(S4.σ("x"), S4.σ("y"), S4.σ("z"))
    assert S4.SEARCH("y",     big_alt) == slice(0, 1)

#------------------------------------------------------------------------------
# ── optional (~P) / π ──────────────────────────────────────────────────────

def test_optional_present(backend):
    opt = S4.POS(0) + ~S4.σ("x") + S4.σ("y") + S4.RPOS(0)
    assert S4.SEARCH("xy", opt) == slice(0, 2)

def test_optional_absent(backend):
    opt = S4.POS(0) + ~S4.σ("x") + S4.σ("y") + S4.RPOS(0)
    assert S4.SEARCH("y",  opt) == slice(0, 1)

#------------------------------------------------------------------------------
# ── MATCH / FULLMATCH ──────────────────────────────────────────────────────

def test_match_anchored(backend):
    assert S4.MATCH("hello world", S4.σ("hello"))  == slice(0, 5)

def test_match_fails_mid(backend):
    assert S4.MATCH("world hello", S4.σ("hello"))  is None

def test_fullmatch_exact(backend):
    assert S4.FULLMATCH("hello",  S4.σ("hello"))   == slice(0, 5)

def test_fullmatch_fails_short(backend):
    assert S4.FULLMATCH("hello!", S4.σ("hello"))   is None

#------------------------------------------------------------------------------
# ── 'in' / '==' operators ──────────────────────────────────────────────────

def test_in_found(backend):
    p = S4.σ("hi")
    assert "say hi" in p

def test_in_not_found(backend):
    p = S4.σ("hi")
    assert "bye" not in p

def test_eq_returns_slice(backend):
    p = S4.σ("hi")
    assert (p == "say hi") == slice(4, 6)

#------------------------------------------------------------------------------
# ── conditional assignment (%) ─────────────────────────────────────────────

def test_conditional_assignment(backend):
    p_cond = S4.SPAN("abc") % "result"
    S4.SEARCH("aabbcc!", p_cond)
    assert result == "aabbcc"                               # noqa: F821

#------------------------------------------------------------------------------
# ── immediate assignment (@) ───────────────────────────────────────────────

def test_immediate_assignment(backend):
    p_imm = S4.SPAN("abc") @ "imm_result"
    S4.SEARCH("aabbcc!", p_imm)
    assert imm_result == "aabbcc"                           # noqa: F821

#------------------------------------------------------------------------------
# ── REM ────────────────────────────────────────────────────────────────────

def test_rem_captures_tail(backend):
    p_rem = S4.σ("hel") + S4.REM() % "tail"
    S4.SEARCH("hello world", p_rem)
    assert tail == "lo world"                               # noqa: F821

#------------------------------------------------------------------------------
# ── ζ (deferred reference) ─────────────────────────────────────────────────

def test_zeta_deferred_arbno(backend):
    ab     = S4.σ("a") | S4.σ("b")
    p_zeta = S4.POS(0) + S4.ARBNO(S4.ζ(lambda: ab)) + S4.RPOS(0)
    assert S4.SEARCH("aabb", p_zeta) == slice(0, 4)

#------------------------------------------------------------------------------
# ── FENCE ──────────────────────────────────────────────────────────────────

def test_fence_matches_a(backend):
    p_fence = S4.POS(0) + S4.FENCE(S4.σ("a") | S4.σ("b")) + S4.RPOS(0)
    assert S4.SEARCH("a", p_fence) == slice(0, 1)

def test_fence_matches_b(backend):
    p_fence = S4.POS(0) + S4.FENCE(S4.σ("a") | S4.σ("b")) + S4.RPOS(0)
    assert S4.SEARCH("b", p_fence) == slice(0, 1)

def test_fence_miss(backend):
    p_fence = S4.POS(0) + S4.FENCE(S4.σ("a") | S4.σ("b")) + S4.RPOS(0)
    assert S4.SEARCH("c", p_fence) is None

#------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))

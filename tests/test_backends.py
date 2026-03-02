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
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import SNOBOL4python as S4

PASS = FAIL = 0


def check(label, result, expected):
    global PASS, FAIL
    ok = result == expected
    mark = "✓" if ok else "✗"
    print(f"  {mark}  {label}")
    if not ok:
        print(f"       got      {result!r}")
        print(f"       expected {expected!r}")
        FAIL += 1
    else:
        PASS += 1


def run_suite(backend_name: str):
    """Run the full conformance suite against whichever backend is active."""
    print(f"\n{'='*60}")
    print(f"  Backend: {backend_name}")
    print(f"{'='*60}")

    # GLOBALS must be called after switching backends
    S4.GLOBALS(globals())

    # ── ε / sigma ──────────────────────────────────────────────────────────
    print("\n── ε / σ ──")
    check("ε matches empty",       S4.SEARCH("",    S4.ε()),          slice(0,0))
    check("ε matches anywhere",    S4.SEARCH("abc", S4.ε()),          slice(0,0))
    check("σ found",               S4.SEARCH("say hello", S4.σ("hello")), slice(4,9))
    check("σ not found",           S4.SEARCH("goodbye",   S4.σ("hello")), None)
    check("σ 1-char",              S4.SEARCH("axb", S4.σ("x")),       slice(1,2))
    check("σ 2-char",              S4.SEARCH("say hi", S4.σ("hi")),   slice(4,6))

    # ── FAIL / ABORT / SUCCEED ─────────────────────────────────────────────
    print("\n── FAIL / ABORT / SUCCEED ──")
    check("FAIL always fails",     S4.SEARCH("abc", S4.FAIL()),        None)
    check("SUCCEED matches empty", S4.SEARCH("abc", S4.SUCCEED()),     slice(0,0))

    # ── α / ω anchors ──────────────────────────────────────────────────────
    print("\n── α / ω ──")
    check("α at start",            S4.SEARCH("hello", S4.α()),         slice(0,0))
    check("ω at end",              S4.SEARCH("hello", S4.ω()),         slice(5,5))

    # ── ANY / NOTANY ───────────────────────────────────────────────────────
    print("\n── ANY / NOTANY ──")
    check("ANY vowel in 'hello'",  S4.SEARCH("hello", S4.ANY("aeiou")),   slice(1,2))
    check("ANY miss",              S4.SEARCH("bcdf",  S4.ANY("aeiou")),   None)
    check("NOTANY consonant",      S4.SEARCH("hello", S4.NOTANY("aeiou")), slice(0,1))

    # ── SPAN / BREAK / NSPAN ───────────────────────────────────────────────
    print("\n── SPAN / BREAK / NSPAN ──")
    check("SPAN 'abc'",            S4.SEARCH("aabbcc!", S4.SPAN("abc")),   slice(0,6))
    check("SPAN miss",             S4.SEARCH("xyz",     S4.SPAN("abc")),   None)
    check("BREAK at '!'",          S4.SEARCH("hello!",  S4.BREAK("!")),    slice(0,5))
    check("NSPAN zero match",      S4.SEARCH("xyz",     S4.NSPAN("abc")),  slice(0,0))
    check("NSPAN some match",      S4.SEARCH("aabc",    S4.NSPAN("ab")),   slice(0,3))

    # ── POS / RPOS / LEN / TAB / RTAB ─────────────────────────────────────
    print("\n── POS / RPOS / LEN / TAB / RTAB ──")
    check("POS(0)",                S4.SEARCH("hello", S4.POS(0)),          slice(0,0))
    check("RPOS(0)",               S4.SEARCH("hello", S4.RPOS(0)),         slice(5,5))
    check("LEN(3)",                S4.SEARCH("hello", S4.LEN(3)),          slice(0,3))
    check("TAB(3)",                S4.SEARCH("hello", S4.TAB(3)),          slice(0,3))
    check("RTAB(2)",               S4.SEARCH("hello", S4.RTAB(2)),         slice(0,3))

    # ── ARB / ARBNO ────────────────────────────────────────────────────────
    print("\n── ARB / ARBNO ──")
    arb_full = S4.POS(0) + S4.ARB() + S4.RPOS(0)
    check("ARB full string",       S4.SEARCH("hello",  arb_full),          slice(0,5))
    p_a  = S4.σ("a")
    arb_no = S4.POS(0) + S4.ARBNO(p_a) + S4.RPOS(0)
    check("ARBNO(a) in 'aaaa'",    S4.SEARCH("aaaa", arb_no),              slice(0,4))
    check("ARBNO(a) in ''",        S4.SEARCH("",     arb_no),              slice(0,0))

    # ── BAL ────────────────────────────────────────────────────────────────
    print("\n── BAL ──")
    check("BAL simple",            S4.SEARCH("(abc)",   S4.BAL()),          slice(0,5))
    check("BAL nested",            S4.SEARCH("(a(b)c)", S4.BAL()),          slice(0,7))

    # ── concat / alt ───────────────────────────────────────────────────────
    print("\n── concat / alt ──")
    cat = S4.σ("hel") + S4.σ("lo")
    check("concat",                S4.SEARCH("hello", cat),                 slice(0,5))
    alt = S4.σ("cat") | S4.σ("dog")
    check("alt → cat",             S4.SEARCH("the cat", alt),               slice(4,7))
    check("alt → dog",             S4.SEARCH("the dog", alt),               slice(4,7))
    check("alt → none",            S4.SEARCH("the fox", alt),               None)

    # ── Σ / Π ──────────────────────────────────────────────────────────────
    print("\n── Σ / Π ──")
    big_cat = S4.Σ(S4.σ("h"), S4.σ("e"), S4.σ("l"), S4.σ("lo"))
    check("Σ concat",              S4.SEARCH("hello",  big_cat),            slice(0,5))
    big_alt = S4.Π(S4.σ("x"), S4.σ("y"), S4.σ("z"))
    check("Π alt → y",             S4.SEARCH("y",       big_alt),           slice(0,1))

    # ── optional (~) ───────────────────────────────────────────────────────
    print("\n── optional (~P) / π ──")
    opt = S4.POS(0) + ~S4.σ("x") + S4.σ("y") + S4.RPOS(0)
    check("~σ('x') optional present", S4.SEARCH("xy", opt),                slice(0,2))
    check("~σ('x') optional absent",  S4.SEARCH("y",  opt),                slice(0,1))

    # ── MATCH / FULLMATCH ──────────────────────────────────────────────────
    print("\n── MATCH / FULLMATCH ──")
    check("MATCH anchored",        S4.MATCH("hello world", S4.σ("hello")),  slice(0,5))
    check("MATCH fails mid",       S4.MATCH("world hello", S4.σ("hello")),  None)
    check("FULLMATCH exact",       S4.FULLMATCH("hello", S4.σ("hello")),    slice(0,5))
    check("FULLMATCH fails short", S4.FULLMATCH("hello!", S4.σ("hello")),   None)

    # ── in / == operators ──────────────────────────────────────────────────
    print("\n── 'in' / '==' operators ──")
    p = S4.σ("hi")
    check("'hi' in pattern",       "say hi" in p,                           True)
    check("'bye' not in pattern",  "bye"    in p,                           False)

    # ── conditional assignment % ───────────────────────────────────────────
    print("\n── conditional assignment (%) ──")
    S4.GLOBALS(globals())
    p_cond = S4.SPAN("abc") % "result"
    S4.SEARCH("aabbcc!", p_cond)
    check("% sets result",         result,                                   "aabbcc")

    # ── immediate assignment @ ─────────────────────────────────────────────
    print("\n── immediate assignment (@) ──")
    S4.GLOBALS(globals())
    p_imm = S4.SPAN("abc") @ "imm_result"
    S4.SEARCH("aabbcc!", p_imm)
    check("@ sets imm_result",     imm_result,                               "aabbcc")

    # ── REM ────────────────────────────────────────────────────────────────
    print("\n── REM ──")
    p_rem = S4.σ("hel") + S4.REM() % "tail"
    S4.GLOBALS(globals())
    S4.SEARCH("hello world", p_rem)
    check("REM captures tail",     tail,                                      "lo world")

    # ── ζ (deferred reference) ─────────────────────────────────────────────
    print("\n── ζ (deferred reference) ──")
    S4.GLOBALS(globals())
    ab = S4.σ("a") | S4.σ("b")
    # Use callable form for reliable cross-backend behaviour
    p_zeta = S4.POS(0) + S4.ARBNO(S4.ζ(lambda: ab)) + S4.RPOS(0)
    check("ζ deferred ARBNO",      S4.SEARCH("aabb", p_zeta),               slice(0,4))

    # ── FENCE ──────────────────────────────────────────────────────────────
    print("\n── FENCE ──")
    p_fence = S4.POS(0) + S4.FENCE(S4.σ("a") | S4.σ("b")) + S4.RPOS(0)
    check("FENCE(a|b) → a",        S4.SEARCH("a", p_fence),                 slice(0,1))
    check("FENCE(a|b) → b",        S4.SEARCH("b", p_fence),                 slice(0,1))
    check("FENCE(a|b) miss",       S4.SEARCH("c", p_fence),                 None)

    return PASS, FAIL


def main():
    global PASS, FAIL

    backends_to_test = []
    if S4.C_AVAILABLE:
        backends_to_test.append(('c',    S4.use_c))
    backends_to_test.append(('pure', S4.use_pure))

    total_pass = total_fail = 0
    results_per_backend = {}

    for name, switcher in backends_to_test:
        PASS = FAIL = 0
        switcher()
        p, f = run_suite(name)
        results_per_backend[name] = (p, f)
        total_pass += p
        total_fail += f

    # cross-backend comparison summary
    print(f"\n{'='*60}")
    print("  Summary")
    print(f"{'='*60}")
    for name, (p, f) in results_per_backend.items():
        status = "✓ all pass" if f == 0 else f"✗ {f} failed"
        print(f"  {name:6s}  {p} passed, {f} failed  — {status}")

    if S4.C_AVAILABLE:
        print("\n  Both backends produce identical results ✓" if total_fail == 0
              else "\n  ✗ Backend divergence detected — see failures above.")

    print(f"\n── Total: {total_pass} passed, {total_fail} failed ──\n")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())

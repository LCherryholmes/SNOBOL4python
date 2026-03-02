#!/usr/bin/env python3
"""
tests/test_basic.py — smoke tests for the sno4py C engine

Run:  make test
 or:  python3 tests/test_basic.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import sno4py

PASS = 0
FAIL = 0

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

def match(subject, pat, anchored=0):
    """Return (start,stop) tuple or None."""
    return sno4py.sno_match(subject, pat, globals(), anchored)

# ── ε (epsilon / null) ────────────────────────────────────────────────────
print("\n── ε (epsilon) ──")
p = sno4py.epsilon()
check("epsilon matches empty",    match("",    p, anchored=1), (0, 0))
check("epsilon matches anywhere", match("abc", p),             (0, 0))

# ── σ (literal string) ────────────────────────────────────────────────────
print("\n── σ (literal string) ──")
p1 = sno4py.string("hello")
check("'hello' found",            match("say hello world", p1), (4, 9))
check("'hello' not found",        match("goodbye",         p1), None)

p2 = sno4py.string("hi")      # 2-char fast path
check("2-char found",             match("say hi", p2), (4, 6))

p3 = sno4py.string("x")       # single char path
check("single char found",        match("axb", p3), (1, 2))

p_long = sno4py.string("SNOBOL4")   # > 6 chars
check("long string found",        match("this is SNOBOL4 pattern", p_long), (8, 15))

# ── ANY(chars) ────────────────────────────────────────────────────────────
print("\n── ANY(chars) ──")
p_any = sno4py.any("aeiou")
check("ANY vowel in 'hello'",     match("hello", p_any), (1, 2))
check("ANY vowel not in 'bcdf'",  match("bcdf",  p_any), None)

# ── α (BOL anchor) ────────────────────────────────────────────────────────
print("\n── α (BOL anchor) ──")
p_bol = sno4py.alpha()
check("α at start of string",     match("hello", p_bol, anchored=1), (0, 0))
check("α finds pos 0 unanchored", match("hello", p_bol, anchored=0), (0, 0))

# ── ω (EOL anchor) ────────────────────────────────────────────────────────
print("\n── ω (EOL anchor) ──")
p_eol = sno4py.omega()
check("ω at end",                 match("hello", p_eol), (5, 5))

# ── POS / RPOS ────────────────────────────────────────────────────────────
print("\n── POS / RPOS ──")
p_pos = sno4py.pos(0)
check("POS(0) at start",          match("hello", p_pos), (0, 0))
p_rpos = sno4py.rpos(0)
check("RPOS(0) at end",           match("hello", p_rpos), (5, 5))

# ── SPAN ──────────────────────────────────────────────────────────────────
print("\n── SPAN ──")
p_span = sno4py.span("abc")
check("SPAN 'abc' in 'aabbcc!'",  match("aabbcc!", p_span), (0, 6))
check("SPAN 'abc' not in 'xyz'",  match("xyz",     p_span), None)

# ── concat + alt ──────────────────────────────────────────────────────────
print("\n── concat / alt ──")
p_cat = sno4py.concat(sno4py.string("hel"), sno4py.string("lo"))
check("concat 'hel'+'lo'",        match("hello", p_cat), (0, 5))

p_alt = sno4py.alt(sno4py.string("cat"), sno4py.string("dog"))
check("alt 'cat'|'dog' → cat",    match("the cat", p_alt), (4, 7))
check("alt 'cat'|'dog' → dog",    match("the dog", p_alt), (4, 7))
check("alt 'cat'|'dog' none",     match("the fox", p_alt), None)

# ── ARB ───────────────────────────────────────────────────────────────────
print("\n── ARB ──")
p_arb = sno4py.concat(sno4py.pos(0), sno4py.concat(sno4py.arb(), sno4py.rpos(0)))
check("ARB matches full string",  match("hello", p_arb), (0, 5))

# ── ARBNO ─────────────────────────────────────────────────────────────────
print("\n── ARBNO ──")
p_a  = sno4py.string("a")
p_no = sno4py.concat(sno4py.pos(0), sno4py.concat(sno4py.arbno(p_a), sno4py.rpos(0)))
check("ARBNO(a) in 'aaaa'",       match("aaaa", p_no), (0, 4))
check("ARBNO(a) in ''",           match("",     p_no), (0, 0))

# ── assignment (immediate) ────────────────────────────────────────────────
print("\n── assign_imm ──")
class STRING(str): pass
g = {"STRING": STRING}
p_imm = sno4py.assign_imm(sno4py.span("abc"), "result")
sno4py.sno_match("aabbcc!", p_imm, g)
check("assign_imm sets 'result'", g.get("result"), "aabbcc")

# ── summary ───────────────────────────────────────────────────────────────
print(f"\n── Results: {PASS} passed, {FAIL} failed ──\n")
if __name__ == "__main__":
    sys.exit(1 if FAIL else 0)

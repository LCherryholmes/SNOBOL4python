#!/usr/bin/env python3
"""
test_bead.py — BEAD pattern test for the sno4py C engine

From BEAD_PATTERN.h:
    BEAD_0 = Σ( POS(0), Π(B,R), Π(E,EA), Π(D,DS), RPOS(0) )

Directly constructs the pattern in C, no Python wrapper layer.
Run:  make test_bead
 or:  python3 tests/test_bead.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import sno4py

PASS = FAIL = 0

def check(label, got, expected):
    global PASS, FAIL
    ok = (got is None) == (expected is None)
    if ok and got is not None:
        ok = (got[0] == expected[0] and got[1] == expected[1])
    mark = "✓" if ok else "✗"
    print(f"  {mark}  {label}")
    if not ok:
        print(f"       got      {got!r}")
        print(f"       expected {expected!r}")
        FAIL += 1
    else:
        PASS += 1

# ── Build BEAD pattern using raw C constructors ──────────────────────────
#
#  POS(0)
#  + (σ('B') | σ('R'))
#  + (σ('E') | σ('EA'))
#  + (σ('D') | σ('DS'))
#  + RPOS(0)
#
g = {}   # globals dict (unused by this pattern, but required by sno_match)

def build_bead():
    pos0  = sno4py.pos(0)              # POS(0)
    B     = sno4py.string("B")
    R     = sno4py.string("R")
    BR    = sno4py.alt(B, R)            # B | R
    E     = sno4py.string("E")
    EA    = sno4py.string("EA")
    E_EA  = sno4py.alt(E, EA)          # E | EA
    D     = sno4py.string("D")
    DS    = sno4py.string("DS")
    D_DS  = sno4py.alt(D, DS)          # D | DS
    rpos0 = sno4py.rpos(0)            # RPOS(0)

    # Concatenate: POS(0) + BR + E_EA + D_DS + RPOS(0)
    p = sno4py.concat(pos0, BR)
    p = sno4py.concat(p,    E_EA)
    p = sno4py.concat(p,    D_DS)
    p = sno4py.concat(p,    rpos0)
    return p

def match(subject, pat):
    return sno4py.sno_match(subject, pat, g)

bead = build_bead()

print("\n── BEAD pattern: POS(0)+(B|R)+(E|EA)+(D|DS)+RPOS(0) ──")

# Should MATCH (fullmatch)
check("BED   matches", match("BED",   bead), (0, 3))
check("RED   matches", match("RED",   bead), (0, 3))
check("BEAD  matches", match("BEAD",  bead), (0, 4))
check("READ  matches", match("READ",  bead), (0, 4))
check("BEDS  matches", match("BEDS",  bead), (0, 4))
check("READS matches", match("READS", bead), (0, 5))

# Should NOT match
check("CAT   no match", match("CAT",   bead), None)
check("BE    no match", match("BE",    bead), None)
check("BREAD no match", match("BREAD", bead), None)  # not anchored at 0

print(f"\n── Results: {PASS} passed, {FAIL} failed ──\n")
sys.exit(1 if FAIL else 0)

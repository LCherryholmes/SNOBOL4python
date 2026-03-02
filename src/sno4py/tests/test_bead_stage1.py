#!/usr/bin/env python3
"""
test_bead_stage1.py — BEAD pattern test using Stage 1 sno4py directly.

Mirrors the test_one block from test_01.py:
    Σ( POS(0), Π(B,F,L,R), Π(E,EA), Π(D,DS), RPOS(0) )
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import sno4py

PASS = FAIL = 0

def check(label, got, expected):
    global PASS, FAIL
    ok = got == expected
    print(f"  {'✓' if ok else '✗'}  {label}")
    if not ok:
        print(f"       got      {got!r}")
        print(f"       expected {expected!r}")
        FAIL += 1
    else:
        PASS += 1

g = {}

def build_bead():
    # Π(σ('B'), σ('F'), σ('L'), σ('R'))
    B   = sno4py.string("B")
    F   = sno4py.string("F")
    L   = sno4py.string("L")
    R   = sno4py.string("R")
    BFR = sno4py.alt(sno4py.alt(sno4py.alt(B, F), L), R)

    # Π(σ('E'), σ('EA'))
    E   = sno4py.string("E")
    EA  = sno4py.string("EA")
    EEA = sno4py.alt(E, EA)

    # Π(σ('D'), σ('DS'))
    D   = sno4py.string("D")
    DS  = sno4py.string("DS")
    DDS = sno4py.alt(D, DS)

    # POS(0) + BFR + EEA + DDS + RPOS(0)
    p = sno4py.concat(sno4py.pos(0), BFR)
    p = sno4py.concat(p, EEA)
    p = sno4py.concat(p, DDS)
    p = sno4py.concat(p, sno4py.rpos(0))
    return p

bead = build_bead()

print("\n── BEAD: POS(0)+(B|F|L|R)+(E|EA)+(D|DS)+RPOS(0) ──")

# Should match (fullmatch)
for s in ["BED","FED","LED","RED","BEAD","FEAD","LEAD","READ",
          "BEDS","FEDS","LEDS","REDS","BEADS","FEADS","LEADS","READS"]:
    r = sno4py.sno_match(s, bead, g)
    check(f"{s:8} matches", r is not None and r == (0, len(s)), True)

# Should NOT match
for s in ["CAT","BE","BREAD","XED"]:
    r = sno4py.sno_match(s, bead, g)
    check(f"{s:8} no match", r, None)

print(f"\n── Results: {PASS} passed, {FAIL} failed ──\n")
sys.exit(1 if FAIL else 0)

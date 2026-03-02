#!/usr/bin/env python3
"""
test_speed.py — Speed benchmarks for the CLAWS and treebank patterns.

Compares SNOBOL4python 0.5.0 (SPIPAT C engine) against the 0.4.5
pure-Python baseline, using the same patterns and data from assignment3.py.

Tests both a small representative subset (repeated timing) and the full
dataset (single-run throughput).

Run:  python3 tests/test_speed.py [data_dir]

data_dir defaults to the project root alongside this repo.
Pass an explicit path if CLAWS5inTASA.dat / VBGinTASA.dat live elsewhere.

Baseline timings measured from SNOBOL4python==0.4.5 (pure Python):
  CLAWS  small (20 sentences, 2.6 KB) :   94.2 ms/run   (  27 kchar/s)
  CLAWS  full  (244 sentences, 66 KB) : 2466.5 ms        (  27 kchar/s)
  Treebank small (20 trees,  6.8 KB)  :  420.0 ms/run   (  16 kchar/s)
  Treebank full  (249 trees, 100 KB)  : 6953.2 ms        (  14 kchar/s)
"""
import sys, os, re, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from SNOBOL4python import (
    GLOBALS, λ, ζ, σ, SPAN, BREAK, NOTANY, ANY, ARBNO, POS, RPOS,
    DIGITS, UCASE,
)

GLOBALS(globals())

# ── locate data files ─────────────────────────────────────────────────────────

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '..', 'project'
)

CLAWS_FILE    = os.path.join(DATA_DIR, 'CLAWS5inTASA.dat')
TREEBANK_FILE = os.path.join(DATA_DIR, 'VBGinTASA.dat')

# ── 0.4.5 baseline (measured, not re-run) ─────────────────────────────────────
#
# Recorded from SNOBOL4python==0.4.5 (pure-Python generator engine)
# on the same machine and same data files.

BASELINE = {
    'claws_small_ms':     94.2,
    'claws_full_ms':    2466.5,
    'treebank_small_ms': 420.0,
    'treebank_full_ms': 6953.2,
}

# ── helpers ───────────────────────────────────────────────────────────────────

PASS = FAIL = 0

def check(label, ok, detail=''):
    global PASS, FAIL
    mark = '✓' if ok else '✗'
    print(f'  {mark}  {label}' + (f'  ({detail})' if detail else ''))
    if ok:
        PASS += 1
    else:
        FAIL += 1

def throughput(chars, ms):
    return f'{chars / ms:.0f} kchar/s'

def speedup(baseline_ms, current_ms):
    return f'{baseline_ms / current_ms:.1f}×'

# ── CLAWS pattern ─────────────────────────────────────────────────────────────

def make_claws_pattern():
    return (
        POS(0)
        + λ("mem = dict()")
        + ARBNO(
            ( SPAN(DIGITS) % "num" + σ('_CRD :_PUN')
            + λ("num = int(num)")
            + λ("mem[num] = dict()")
            | (NOTANY("_") + BREAK("_")) % "wrd"
            + σ('_')
            + (ANY(UCASE) + SPAN(DIGITS+UCASE)) % "tag"
            + λ("if wrd not in mem[num]:      mem[num][wrd] = dict()")
            + λ("if tag not in mem[num][wrd]: mem[num][wrd][tag] = 0")
            + λ("mem[num][wrd][tag] += 1")
            )
          + σ(' ')
          )
        + RPOS(0)
    )

# ── treebank pattern ──────────────────────────────────────────────────────────

def count_tag(tag):
    if tag not in tags:
        tags[tag] = 1
    else:
        tags[tag] += 1

def init_list(v): return λ(f"{v} = None") + λ(f"tags = dict()") + λ(f"stack = []")
def push_list(v): return λ(f"count_tag({v})") + λ(f"stack.append(list())") + λ(f"stack[-1].append({v})")
def push_item(v): return λ(f"stack[-1].append({v})")
def pop_list():   return λ(f"stack[-2].append(tuple(stack.pop()))")
def pop_final(v): return λ(f"{v} = tuple(stack.pop())")

def make_treebank_pattern():
    delim = SPAN(" \n")
    word  = NOTANY("( )\n") + BREAK("( )\n")
    group = ( σ('(')
            + word % "tag"
            + push_list("tag")
            + ARBNO(
                delim
              + ( ζ(lambda: group)
                | word % "wrd" + push_item("wrd")
                )
              )
            + pop_list()
            + σ(')')
            )
    return (
        POS(0)
        + init_list("bank")
        + push_list("'BANK'")
        + ARBNO(
            push_list("'ROOT'")
          + ARBNO(group)
          + pop_list()
          + delim
          )
        + pop_final("bank")
        + RPOS(0)
    )

# ── load / split data ─────────────────────────────────────────────────────────

def load_claws(path):
    with open(path) as f:
        lines = []
        while line := f.readline():
            lines.append(line[:-1])   # strip trailing newline (as assignment3.py does)
    return ''.join(lines)

def load_treebank(path):
    with open(path) as f:
        return f.read()

def split_claws(data, n):
    """Return the first n CLAWS sentences as a single string."""
    sentences = [s for s in re.split(r'(?=\d+_CRD)', data) if s.strip()]
    return ''.join(sentences[:n])

def split_treebank(data, n):
    """Return the first n complete (balanced) treebank trees as a single string."""
    result = []
    i = 0
    while i < len(data) and len(result) < n:
        while i < len(data) and data[i] in ' \n\t':
            i += 1
        if i >= len(data) or data[i] != '(':
            break
        depth, start = 0, i
        while i < len(data):
            if   data[i] == '(': depth += 1
            elif data[i] == ')': depth -= 1
            i += 1
            if depth == 0:
                break
        result.append(data[start:i])
    return '\n'.join(result) + '\n'

# ── benchmark runners ─────────────────────────────────────────────────────────

def run_claws(data_path, small_n=20, small_reps=10):
    print(f'\n── CLAWS (POS-tagged sentences) ─────────────────────────────')

    global mem
    full_data  = load_claws(data_path)
    small_data = split_claws(full_data, small_n)
    pat = make_claws_pattern()

    # small subset
    mem = None
    ok  = small_data in pat
    sentences_small = len(mem) if mem else 0
    check(f'small ({small_n} sentences) matches',
          ok and sentences_small > 0,
          f'{sentences_small} sentences, {len(small_data)} chars')

    t0 = time.perf_counter()
    for _ in range(small_reps):
        mem = None
        small_data in pat
    t1 = time.perf_counter()
    small_ms = (t1 - t0) / small_reps * 1000
    print(f'       {small_reps}× average : {small_ms:7.1f} ms'
          f'  ({throughput(len(small_data), small_ms)})'
          f'  |  0.4.5: {BASELINE["claws_small_ms"]:7.1f} ms'
          f'  →  {speedup(BASELINE["claws_small_ms"], small_ms)} faster')

    # full dataset
    mem = None
    t0 = time.perf_counter()
    ok = full_data in pat
    t1 = time.perf_counter()
    full_ms = (t1 - t0) * 1000
    sentences_full = len(mem) if mem else 0
    check(f'full dataset matches',
          ok and sentences_full > 0,
          f'{sentences_full} sentences, {len(full_data)} chars')
    print(f'       single run  : {full_ms:7.1f} ms'
          f'  ({throughput(len(full_data), full_ms)})'
          f'  |  0.4.5: {BASELINE["claws_full_ms"]:7.1f} ms'
          f'  →  {speedup(BASELINE["claws_full_ms"], full_ms)} faster')


def run_treebank(data_path, small_n=20, small_reps=10):
    print(f'\n── Treebank (Penn-style parse trees) ────────────────────────')

    global bank, tags
    full_data  = load_treebank(data_path)
    small_data = split_treebank(full_data, small_n)
    pat = make_treebank_pattern()

    # small subset
    bank = None
    ok   = small_data in pat
    trees_small = len(bank) - 1 if bank else 0
    check(f'small ({small_n} trees) matches',
          ok and trees_small == small_n,
          f'{trees_small} trees, {len(small_data)} chars')

    t0 = time.perf_counter()
    for _ in range(small_reps):
        bank = None
        small_data in pat
    t1 = time.perf_counter()
    small_ms = (t1 - t0) / small_reps * 1000
    print(f'       {small_reps}× average : {small_ms:7.1f} ms'
          f'  ({throughput(len(small_data), small_ms)})'
          f'  |  0.4.5: {BASELINE["treebank_small_ms"]:7.1f} ms'
          f'  →  {speedup(BASELINE["treebank_small_ms"], small_ms)} faster')

    # full dataset
    bank = None
    t0 = time.perf_counter()
    ok = full_data in pat
    t1 = time.perf_counter()
    full_ms = (t1 - t0) * 1000
    trees_full = len(bank) - 1 if bank else 0
    check(f'full dataset matches',
          ok and trees_full > 0,
          f'{trees_full} trees, {len(full_data)} chars')
    print(f'       single run  : {full_ms:7.1f} ms'
          f'  ({throughput(len(full_data), full_ms)})'
          f'  |  0.4.5: {BASELINE["treebank_full_ms"]:7.1f} ms'
          f'  →  {speedup(BASELINE["treebank_full_ms"], full_ms)} faster')


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    missing = [p for p in (CLAWS_FILE, TREEBANK_FILE) if not os.path.exists(p)]
    if missing:
        print(f'ERROR: data file(s) not found: {missing}')
        print(f'Pass data directory as first argument: python3 test_speed.py /path/to/data')
        sys.exit(1)

    print('SNOBOL4python 0.5.0 (SPIPAT C engine) vs 0.4.5 (pure Python)')
    print('=' * 62)

    run_claws(CLAWS_FILE)
    run_treebank(TREEBANK_FILE)

    print(f'\n── Results: {PASS} passed, {FAIL} failed ──\n')
    sys.exit(1 if FAIL else 0)

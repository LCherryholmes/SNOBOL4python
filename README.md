# SNOBOL4python 0.5.0

SNOBOL4-style string pattern matching for Python — with a dual backend:

| Backend | Speed | Availability |
|---------|-------|--------------|
| **C / SPIPAT** (default) | 7–11× faster than 0.4.x | CPython 3.10+ with GCC |
| **Pure Python** | 100 % portable | Any Python ≥ 3.10 |

The C backend is powered by [Phil Budne's SPIPAT](https://github.com/pbudne/spipat) pattern engine, wrapped as a CPython extension (`sno4py`).

---

## Quick Start

```python
from SNOBOL4python import *

GLOBALS(globals())

p = σ("hello") | σ("world")
if "say hello" in p:
    print("matched")

result = SEARCH("say hello", σ("hello"))   # → slice(4, 9)
```

---

## Backend Selection

### Automatic (default)

On import, SNOBOL4python checks whether the `sno4py` C extension is
importable.  If it is, the C/SPIPAT backend is used; otherwise the
pure-Python backend is used transparently — no code changes required.

### Environment variable

```bash
# Force pure-Python (always available, useful for debugging):
SNOBOL4_BACKEND=pure python3 my_script.py

# Force C backend (ImportError if sno4py not installed):
SNOBOL4_BACKEND=c python3 my_script.py
```

### Runtime switching

```python
import SNOBOL4python as S4

print(S4.current_backend())   # 'c' or 'pure'
print(S4.C_AVAILABLE)         # True if sno4py extension is present

S4.use_pure()                 # switch to pure-Python
S4.use_c()                    # switch back to C (raises ImportError if unavailable)

# After switching, call GLOBALS() again so the new backend
# sees the caller's variable namespace:
S4.GLOBALS(globals())
```

> **Note:** Patterns are compiled at construction time by whichever backend
> is active.  Do not mix pattern objects from different backends in the same
> expression; rebuild patterns after switching.

---

## Installing the C/SPIPAT Backend

The `sno4py` extension is built from source alongside the `sno4py_stage8`
directory that is distributed separately (or built from the repository).

```bash
cd sno4py
make                    # produces sno4py.<platform>.so
# then place or symlink it somewhere on sys.path, or into site-packages
```

Requirements: Python 3.10+, GCC (or compatible C compiler), `python3-dev`.

---

## Pattern Reference

| Constructor | SNOBOL4 equivalent | Description |
|-------------|-------------------|-------------|
| `ε()` | null | Matches empty string |
| `σ(s)` | `'s'` | Literal string |
| `FAIL()` | `FAIL` | Always fails |
| `ABORT()` | `ABORT` | Aborts entire match |
| `SUCCEED()` | `SUCCEED` | Always succeeds (infinite) |
| `P + Q` | `P Q` | Concatenation |
| `P \| Q` | `P \| Q` | Alternation |
| `~P` / `π(P)` | `P \| ''` | Optional |
| `P @ 'name'` | `P $ N` | Immediate assignment |
| `P % 'name'` | `P . N` | Conditional assignment |
| `Σ(P, Q, …)` | `P Q …` | Multi-way concatenation |
| `Π(P, Q, …)` | `P \| Q \| …` | Multi-way alternation |
| `P & Q` / `ρ(P, Q)` | — | Conjunction (same span) |
| `ANY(chars)` | `ANY(s)` | One char from set |
| `NOTANY(chars)` | `NOTANY(s)` | One char not in set |
| `SPAN(chars)` | `SPAN(s)` | One or more chars from set |
| `BREAK(chars)` | `BREAK(s)` | Up to (not incl.) char in set |
| `BREAKX(chars)` | `BREAKX(s)` | Like BREAK, resumes after break char |
| `NSPAN(chars)` | — | Zero or more chars (possessive) |
| `ARB()` | `ARB` | Any string (shortest first) |
| `ARBNO(P)` | `ARBNO(P)` | Zero or more repetitions of P |
| `BAL()` | `BAL` | Balanced parentheses |
| `REM()` | `REM` | Remainder of subject |
| `FENCE()` | `FENCE` | Commit point (abort on backtrack) |
| `FENCE(P)` | `FENCE(P)` | Protected region |
| `POS(n)` | `POS(n)` | Cursor at position n from left |
| `RPOS(n)` | `RPOS(n)` | Cursor at position n from right |
| `LEN(n)` | `LEN(n)` | Match exactly n chars |
| `TAB(n)` | `TAB(n)` | Advance cursor to position n |
| `RTAB(n)` | `RTAB(n)` | Advance cursor to position n from right |
| `ζ(name_or_callable)` | `*name` | Deferred pattern reference |
| `Λ(expr_or_fn)` | `*expr` | Immediate predicate / eval |
| `λ(stmt_or_fn)` | — | Conditional action |
| `Θ(name)` | — | Immediate cursor assignment |
| `θ(name)` | — | Conditional cursor assignment |
| `Φ(regex)` | — | Regex match (immediate group capture) |
| `φ(regex)` | — | Regex match (conditional group capture) |
| `α()` | — | BOL anchor |
| `ω()` | — | EOL anchor |

### Shift-reduce parser stack (Stage 8)

| Constructor | Description |
|-------------|-------------|
| `nPush()` | Push 0 onto integer counter stack |
| `nInc()` | Increment top of integer counter stack |
| `nPop()` | Pop integer counter stack |
| `Shift(tag[, expr])` | Push node onto parse-tree value stack |
| `Reduce(tag[, n])` | Pop n nodes, wrap as [tag, …], push back |
| `Pop(var)` | Pop top of value stack into globals[var] |

---

## Match Functions

```python
SEARCH(S, P)        # → slice or None   (search anywhere in S)
MATCH(S, P)         # → slice or None   (anchored at start)
FULLMATCH(S, P)     # → slice or None   (anchored at both ends)

# Operators:
subject in pattern          # → bool
pattern == subject          # → slice (raises F on failure)
```

---

## Version History

| Version | Notes |
|---------|-------|
| **0.5.0** | Dual backend: C/SPIPAT (default, 7–11× faster) + pure-Python. `NSPAN` added. `use_c()` / `use_pure()` / `current_backend()` / `C_AVAILABLE`. |
| 0.4.x | Pure-Python generator engine. Stage 8: shift-reduce parser stack. |

---

## Credits

- **SNOBOL4python** — Lon Jones Cherryholmes
- **SPIPAT / sno4py C engine** — Phil Budne
- Pattern semantics based on *The SNOBOL4 Programming Language* (Griswold, Poage, Polonsky) and the SPITBOL manual.

## License

GPL-3.0-or-later

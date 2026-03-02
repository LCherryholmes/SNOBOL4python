# SNOBOL4python

SNOBOL4-style string pattern matching for Python — with a dual backend:

| Backend | Speed | Availability |
|---------|-------|--------------|
| **C / SPIPAT** (default) | 7–11× faster | CPython 3.10+ |
| **Pure Python** | 100% portable | Any Python ≥ 3.10 |

## Quick Start

```python
from SNOBOL4python import *

GLOBALS(globals())

p = σ("hello") | σ("world")
if "say hello" in p:
    print("matched")
```

## Installation

```bash
pip install SNOBOL4python
```

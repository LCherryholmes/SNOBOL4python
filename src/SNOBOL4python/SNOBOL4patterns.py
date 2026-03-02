# -*- coding: utf-8 -*-
# SNOBOL4patterns.py — public shim for SNOBOL4python 0.5.0
#
# This file no longer contains the engine itself.  It re-exports everything
# from whichever backend is currently active (_backend_c or _backend_pure),
# as determined by SNOBOL4python._backend at import time.
#
# To inspect or switch backends at runtime:
#
#   import SNOBOL4python
#   print(SNOBOL4python.current_backend())   # 'c' or 'pure'
#   SNOBOL4python.use_pure()                 # switch to pure-Python
#   SNOBOL4python.use_c()                    # switch back to C (if available)
#
# ─────────────────────────────────────────────────────────────────────────────
from ._backend import *          # noqa: F401, F403
from ._backend import (          # noqa: F401  (explicit for IDEs & type checkers)
    F, PATTERN, STRING, NULL, Ϩ, Γ,
    ε, σ, FAIL, ABORT, SUCCEED,
    α, ω, ARB, MARB, BAL, REM, FENCE,
    ANY, NOTANY, SPAN, BREAK, BREAKX, NSPAN,
    POS, RPOS, LEN, TAB, RTAB,
    ARBNO, MARBNO, π,
    Σ, Π, ρ,
    δ, Δ, Θ, θ, Λ, λ, ζ, Φ, φ,
    nPush, nInc, nPop, Shift, Reduce, Pop,
    GLOBALS, TRACE, SEARCH, MATCH, FULLMATCH,
    # backend meta
    C_AVAILABLE, use_c, use_pure, current_backend,
)

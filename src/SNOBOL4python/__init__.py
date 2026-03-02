# -*- coding: utf-8 -*-
# SNOBOL4python 0.5.0
#
# The SNOBOL4 environment (variable namespace) is a single flat dict kept in
# _env._g.  Set it once with GLOBALS(globals()); all pattern assignments,
# built-in functions, and deferred evaluations share that one reference.
# No module in this package keeps its own copy.
#
# ─────────────────────────────────────────────────────────────────────────────

# ── pattern engine (backend-agnostic shim) ────────────────────────────────────
from .SNOBOL4patterns import (
    GLOBALS, TRACE,
    F, PATTERN, STRING, NULL, Ϩ, Γ,
    ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω,
    ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL,
    FENCE, LEN, MARB, MARBNO, NOTANY, NSPAN, POS, REM, RPOS,
    RTAB, SPAN, SUCCEED, TAB,
    nPush, nInc, nPop, Shift, Reduce, Pop,
    Σ, Π, ρ, Δ, δ,
    SEARCH, MATCH, FULLMATCH,
    # backend control
    C_AVAILABLE, use_c, use_pure, current_backend,
)

# ── built-in functions ────────────────────────────────────────────────────────
from .SNOBOL4functions import (
    ALPHABET, DIGITS, UCASE, LCASE,
    DEFINE, APPLY, REPLACE, SUBSTITUTE,
    CHAR, DIFFER, IDENT, INTEGER,
    END, RETURN, FRETURN, NRETURN,
)

__version__ = '0.5.0'
__author__  = 'Lon Jones Cherryholmes'

__all__ = [
    # backend control
    'C_AVAILABLE', 'use_c', 'use_pure', 'current_backend',
    # environment
    'GLOBALS', 'TRACE',
    # core types
    'F', 'PATTERN', 'STRING', 'NULL', 'Ϩ', 'Γ',
    # Greek-letter pattern constructors
    'ε', 'σ', 'π', 'λ', 'Λ', 'ζ', 'θ', 'Θ', 'φ', 'Φ', 'α', 'ω',
    'Σ', 'Π', 'ρ', 'Δ', 'δ',
    # named pattern constructors
    'ABORT', 'ANY', 'ARB', 'ARBNO', 'BAL', 'BREAK', 'BREAKX', 'FAIL',
    'FENCE', 'LEN', 'MARB', 'MARBNO', 'NOTANY', 'NSPAN', 'POS', 'REM', 'RPOS',
    'RTAB', 'SPAN', 'SUCCEED', 'TAB',
    # shift-reduce parser stack
    'nPush', 'nInc', 'nPop', 'Shift', 'Reduce', 'Pop',
    # match API
    'SEARCH', 'MATCH', 'FULLMATCH',
    # built-in string constants
    'ALPHABET', 'DIGITS', 'UCASE', 'LCASE', 'NULL',
    # built-in functions
    'DEFINE', 'APPLY', 'REPLACE', 'SUBSTITUTE',
    'CHAR', 'DIFFER', 'IDENT', 'INTEGER',
    'END', 'RETURN', 'FRETURN', 'NRETURN',
]

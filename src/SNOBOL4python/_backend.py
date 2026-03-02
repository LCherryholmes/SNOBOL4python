# -*- coding: utf-8 -*-
# SNOBOL4python — backend selector
#
# This module decides which pattern-matching engine is loaded and provides
# use_c() / use_pure() / current_backend() for runtime switching.
#
# Resolution order for the initial backend:
#   1. Environment variable  SNOBOL4_BACKEND = 'c' | 'pure'
#   2. If unset: try the C/SPIPAT extension; fall back to pure-Python.
#
# The selected backend is exposed as the module-level name `backend`
# ('c' or 'pure'), and all public symbols are re-exported from here so
# that SNOBOL4patterns.py can do a single "from ._backend import *".
#
# ─────────────────────────────────────────────────────────────────────────────
import os as _os
import sys as _sys
import importlib as _importlib
from . import _env

# ── env and backend state ────────────────────────────────────────────────────

_C_MODULE_NAME    = 'sno4py'          # the compiled extension
_BACKEND_C_PKG    = 'SNOBOL4python._backend_c'
_BACKEND_PURE_PKG = 'SNOBOL4python._backend_pure'

_current: str = ''          # 'c' or 'pure'
_mod            = None      # currently active backend module

# ── public names exported from whichever backend is loaded ────────────────────

__all__ = [
    # meta
    'backend', 'C_AVAILABLE', 'use_c', 'use_pure', 'current_backend',
    # patterns & types
    'F', 'PATTERN', 'STRING', 'NULL', 'Ϩ', 'Γ',
    'ε', 'σ', 'FAIL', 'ABORT', 'SUCCEED',
    'α', 'ω', 'ARB', 'MARB', 'BAL', 'REM', 'FENCE',
    'ANY', 'NOTANY', 'SPAN', 'BREAK', 'BREAKX', 'NSPAN',
    'POS', 'RPOS', 'LEN', 'TAB', 'RTAB',
    'ARBNO', 'MARBNO', 'π',
    'Σ', 'Π', 'ρ',
    'δ', 'Δ', 'Θ', 'θ', 'Λ', 'λ', 'ζ', 'Φ', 'φ',
    'nPush', 'nInc', 'nPop', 'Shift', 'Reduce', 'Pop',
    # API
    'GLOBALS', 'TRACE', 'SEARCH', 'MATCH', 'FULLMATCH',
]


def _c_available() -> bool:
    """True if the sno4py C extension can be imported."""
    try:
        _importlib.import_module(_C_MODULE_NAME)
        return True
    except ImportError:
        return False


C_AVAILABLE: bool = _c_available()


def _load_backend(name: str):
    """Import and activate one backend module ('c' or 'pure')."""
    global _current, _mod

    if name == 'c':
        if not C_AVAILABLE:
            raise ImportError(
                "The sno4py C extension is not available on this system. "
                "Use use_pure() or install sno4py."
            )
        pkg = _BACKEND_C_PKG
    elif name == 'pure':
        pkg = _BACKEND_PURE_PKG
    else:
        raise ValueError(f"Unknown backend {name!r}: choose 'c' or 'pure'.")

    mod = _importlib.import_module(pkg)
    _current = name
    _mod     = mod
    return mod


def _inject(mod):
    """
    Copy every public symbol from *mod* into this module's namespace so that
    callers who did `from ._backend import *` earlier pick up the new ones.
    We also update the SNOBOL4python package namespace if it's already loaded.
    """
    g = _sys.modules[__name__].__dict__
    for name in __all__:
        if name in ('backend', 'C_AVAILABLE', 'use_c', 'use_pure', 'current_backend'):
            continue
        obj = getattr(mod, name, None)
        if obj is not None:
            g[name] = obj

    # propagate into the parent package if already initialised
    pkg_mod = _sys.modules.get('SNOBOL4python')
    if pkg_mod is not None:
        for name in __all__:
            if name in ('backend', 'C_AVAILABLE', 'use_c', 'use_pure', 'current_backend'):
                continue
            obj = getattr(mod, name, None)
            if obj is not None:
                setattr(pkg_mod, name, obj)



# ── GLOBALS — defined here once, not per-backend ─────────────────────────────
# Both _backend_pure and _backend_c also define GLOBALS(g) as thin wrappers
# to _env.set(g), but this definition is the canonical one injected into the
# package namespace.  Switching backends never changes what GLOBALS does.

def GLOBALS(g: dict) -> None:
    """
    Register *g* as the SNOBOL environment — the single flat variable space
    shared by all pattern operations, assignments, and built-in functions.

    Call once at the top of your script/module:

        from SNOBOL4python import *
        GLOBALS(globals())

    If you switch backends with use_c() / use_pure(), call GLOBALS(globals())
    again so the new backend's SEARCH sees the correct namespace.
    """
    _env.set(g)


# ── public API ────────────────────────────────────────────────────────────────

def use_c() -> None:
    """
    Switch to the C/SPIPAT backend.

    Raises ImportError if sno4py is not installed.
    All subsequently constructed patterns will use the C engine.
    Patterns built with the previous backend remain valid for the duration of
    any in-progress match but should not be mixed with new ones.
    """
    mod = _load_backend('c')
    _inject(mod)


def use_pure() -> None:
    """
    Switch to the pure-Python backend.

    Useful for debugging, testing, or deployment on platforms without a C
    compiler.  All subsequently constructed patterns will use the generator
    engine from SNOBOL4python ≤ 0.4.x.
    """
    mod = _load_backend('pure')
    _inject(mod)


def current_backend() -> str:
    """Return 'c' or 'pure'."""
    return _current


# ── property-style shim so ``backend`` reads the live value ──────────────────

class _BackendDescriptor:
    """Makes ``from SNOBOL4python._backend import backend`` always current."""
    def __get__(self, obj, objtype=None):
        return _current


class _BackendModule(_sys.modules[__name__].__class__):
    """Module subclass so `SNOBOL4python._backend.backend` is always live."""
    @property
    def backend(self):
        return _current


_sys.modules[__name__].__class__ = _BackendModule


# ── initial backend selection ────────────────────────────────────────────────

def _resolve_initial() -> str:
    env = _os.environ.get('SNOBOL4_BACKEND', '').strip().lower()
    if env == 'pure':
        return 'pure'
    if env == 'c':
        if not C_AVAILABLE:
            import warnings
            warnings.warn(
                "SNOBOL4_BACKEND=c requested but sno4py is not available; "
                "falling back to pure-Python backend.",
                RuntimeWarning,
                stacklevel=2,
            )
            return 'pure'
        return 'c'
    # auto: prefer C if available
    return 'c' if C_AVAILABLE else 'pure'


_load_backend(_resolve_initial())
_inject(_mod)

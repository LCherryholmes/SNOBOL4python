# -*- coding: utf-8 -*-
# SNOBOL4python._env — shared SNOBOL environment
#
# SNOBOL4 has one flat global variable space.  In Python that maps to the
# caller's module dict, passed in once via GLOBALS(globals()).
#
# This module holds the single shared reference to that dict.  Every other
# module in the package (both backends, SNOBOL4functions) imports _g from
# here rather than keeping its own private copy.
#
# Nothing else lives here.  No logic.  No classes.  One name.
# ─────────────────────────────────────────────────────────────────────────────

_g: dict | None = None          # the live SNOBOL environment dict


def set(g: dict) -> None:
    """Point the shared environment at a new dict.  Called only by GLOBALS()."""
    global _g
    _g = g


def get() -> dict | None:
    """Return the current environment dict (may be None before GLOBALS())."""
    return _g

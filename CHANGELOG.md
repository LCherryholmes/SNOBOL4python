# Changelog

All notable changes to SNOBOL4python are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.5.0] — unreleased

### Added
- Dual-backend architecture: C/SPIPAT (7–11× faster) and pure-Python fallback
- `_backend.py` backend selector with runtime switching via `use_c()` / `use_pure()`
- `SNOBOL4_BACKEND` environment variable for forcing a backend
- `sno4py` C extension wrapping SPIPAT with heap-allocated stack (Stack_Size 2,000,000)
- Full conformance test suite comparing both backends (`tests/test_backends.py`)
- `MARB`, `MARBNO` extensions beyond standard SPIPAT
- Greek-letter constructors: `ε`, `σ`, `π`, `λ`, `Λ`, `ζ`, `θ`, `Θ`, `φ`, `Φ`, `α`, `ω`, `Σ`, `Π`
- `SEARCH`, `MATCH`, `FULLMATCH` match functions
- Conditional assignment `%` and immediate assignment `@` operators
- Optional pattern `~P` shorthand

### Changed
- SPIPAT `Stack_Size` raised from 2,000 → 2,000,000; stack moved to heap

---

## [0.4.x] — prior releases

- Initial pure-Python implementation of SNOBOL4 pattern primitives

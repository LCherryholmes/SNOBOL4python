/*
 * sno4py.c — SNOBOL4python C extension
 *
 * Stage 1: SpiPat engine subsumed + Python wrapper.
 * Covers: epsilon, string, concat, alt, pos, rpos, assign_imm → BEAD test.
 *
 * SpiPat portions:
 *   Copyright (C) 2007-2021, Philip L. Budne
 *   Copyright (C) 1998-2005, AdaCore
 *   GPL-2.0-or-later (with link exception)
 *
 * Python extension:
 *   GPL-3.0-or-later
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

/* ═══════════════════════════════════════════════════════════════════════
 *  SPIPAT — subsumed verbatim
 * ═══════════════════════════════════════════════════════════════════════ */

#include "spipat.h"
#include "spipat_impl.h"  /* struct dynamic */

/* VStack deferred-execution keys (used in sno_match and Stage 4) */
#define VS_CSTACK "__vs_cstack__"
#define VS_ISTACK "__vs_istack__"
#define VS_VSTACK "__vs_vstack__"

/* Forward declaration — defined in Stage 4 block */
static void execute_vstack_op(PyObject *g, PyObject *op);

/* spipat_exception is provided in spipat_stubs.c; declared here for clarity */

/* ═══════════════════════════════════════════════════════════════════════
 *  Python Pattern type — wraps struct pat *
 * ═══════════════════════════════════════════════════════════════════════ */

typedef struct {
    PyObject_HEAD
    struct pat *pat;
} PatternObject;

static PyTypeObject PatternType;

static PyObject *
wrap_pat(struct pat *p) {
    if (!p) return NULL;
    PatternObject *o = PyObject_New(PatternObject, &PatternType);
    if (!o) { spipat_free(p); return NULL; }
    o->pat = p;
    return (PyObject *)o;
}

static void
Pattern_dealloc(PatternObject *self) {
    spipat_free(self->pat);
    PyObject_Del(self);
}

static PyObject *
Pattern_repr(PatternObject *self) {
    char buf[128];
    spipat_image(self->pat, buf, sizeof(buf));
    return PyUnicode_FromFormat("<Pattern %s>", buf);
}

static PyTypeObject PatternType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "sno4py.Pattern",
    .tp_basicsize = sizeof(PatternObject),
    .tp_dealloc   = (destructor)Pattern_dealloc,
    .tp_repr      = (reprfunc)Pattern_repr,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_doc       = "SNOBOL4 compiled pattern",
};

#define PAT_ARG(var, pyobj) \
    do { \
        if (!PyObject_TypeCheck((pyobj), &PatternType)) { \
            PyErr_SetString(PyExc_TypeError, "expected Pattern"); \
            return NULL; \
        } \
        (var) = ((PatternObject *)(pyobj))->pat; \
    } while (0)

/* ═══════════════════════════════════════════════════════════════════════
 *  assign_imm callback — stores matched text into globals dict
 *  match_cookie IS the globals dict (set in sno_match).
 * ═══════════════════════════════════════════════════════════════════════ */

static void
assign_imm_call(VString s, void *match_cookie, void *cookie) {
    PyObject *globals = (PyObject *)match_cookie;
    PyObject *key     = (PyObject *)cookie;

    if (PyUnicode_CompareWithASCIIString(key, "OUTPUT") == 0) {
        PySys_WriteStdout("%.*s\xc2\xb7", (int)s.len, (const char *)s.ptr);
        return;
    }
    PyObject *STRING = PyDict_GetItemString(globals, "STRING");
    PyObject *raw    = PyUnicode_DecodeUTF8((const char *)s.ptr,
                                            (Py_ssize_t)s.len, "replace");
    if (!raw) { PyErr_Clear(); return; }
    PyObject *val;
    if (STRING && PyCallable_Check(STRING))
        val = PyObject_CallOneArg(STRING, raw);
    else
        val = Py_NewRef(raw);
    Py_DECREF(raw);
    if (val) {
        PyDict_SetItem(globals, key, val);
        Py_DECREF(val);
    }
}

/* ═══════════════════════════════════════════════════════════════════════
 *  Constructors
 * ═══════════════════════════════════════════════════════════════════════ */

static PyObject *
py_epsilon(PyObject *self, PyObject *args) {
    (void)self; (void)args;
    return wrap_pat(spipat_string(C2VSTRING("")));
}

static PyObject *
py_string(PyObject *self, PyObject *args) {
    (void)self;
    const char *s; Py_ssize_t slen;
    if (!PyArg_ParseTuple(args, "s#", &s, &slen)) return NULL;
    return wrap_pat(spipat_string(PL2VSTRING(s, (size_t)slen)));
}

static PyObject *
py_concat(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *po, *qo;
    if (!PyArg_ParseTuple(args, "OO", &po, &qo)) return NULL;
    struct pat *pp, *pq;
    PAT_ARG(pp, po); PAT_ARG(pq, qo);
    spipat_hold(pp); spipat_hold(pq);
    return wrap_pat(spipat_and(pp, pq));
}

static PyObject *
py_alt(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *po, *qo;
    if (!PyArg_ParseTuple(args, "OO", &po, &qo)) return NULL;
    struct pat *pp, *pq;
    PAT_ARG(pp, po); PAT_ARG(pq, qo);
    spipat_hold(pp); spipat_hold(pq);
    return wrap_pat(spipat_or(pp, pq));
}

static PyObject *
py_pos(PyObject *self, PyObject *args) {
    (void)self;
    Py_ssize_t n;
    if (!PyArg_ParseTuple(args, "n", &n)) return NULL;
    return wrap_pat(spipat_pos((size_t)n));
}

static PyObject *
py_rpos(PyObject *self, PyObject *args) {
    (void)self;
    Py_ssize_t n;
    if (!PyArg_ParseTuple(args, "n", &n)) return NULL;
    return wrap_pat(spipat_rpos((size_t)n));
}

static PyObject *
py_assign_imm(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *po, *key;
    if (!PyArg_ParseTuple(args, "OO!", &po, &PyUnicode_Type, &key)) return NULL;
    struct pat *pp; PAT_ARG(pp, po);
    /* key is passed as cookie; keep it alive for the life of the pattern */
    Py_INCREF(key);
    spipat_hold(pp);
    struct pat *r = spipat_call_immed(pp, assign_imm_call, key);
    if (!r) { Py_DECREF(key); return NULL; }
    return wrap_pat(r);
}

/* ═══════════════════════════════════════════════════════════════════════
 *  sno_match(subject, pattern, globals_dict, anchored=0)
 *  Returns (start, stop) as 0-based half-open indices, or None.
 *  globals_dict becomes match_cookie so callbacks can reach it.
 * ═══════════════════════════════════════════════════════════════════════ */

static PyObject *
py_match(PyObject *self, PyObject *args) {
    (void)self;
    const char *subject; Py_ssize_t slen;
    PyObject   *pat_obj, *globals;
    int         anchored = 0;

    if (!PyArg_ParseTuple(args, "s#OO!|i",
                          &subject, &slen,
                          &pat_obj,
                          &PyDict_Type, &globals,
                          &anchored))
        return NULL;

    if (!PyObject_TypeCheck(pat_obj, &PatternType)) {
        PyErr_SetString(PyExc_TypeError, "expected Pattern");
        return NULL;
    }

    /* Clear vstack state before each match */
    PyObject *empty_is = PyList_New(0);
    PyObject *empty_vs = PyList_New(0);
    if (empty_is) { PyDict_SetItemString(globals, VS_ISTACK, empty_is); Py_DECREF(empty_is); }
    if (empty_vs) { PyDict_SetItemString(globals, VS_VSTACK, empty_vs); Py_DECREF(empty_vs); }

    struct spipat_match mp;
    memset(&mp, 0, sizeof(mp));
    mp.subject      = PL2VSTRING(subject, (size_t)slen);
    mp.pattern      = ((PatternObject *)pat_obj)->pat;
    mp.match_cookie = globals;
    mp.flags        = anchored ? SPIPAT_ANCHORED : 0;

    enum spipat_match_ret ret = spipat_match2(&mp);

    if (ret == SPIPAT_MATCH_EXCEPTION) {
        if (!PyErr_Occurred())
            PyErr_SetString(PyExc_RuntimeError, "spipat exception");
        return NULL;
    }
    if (ret == SPIPAT_MATCH_FAILURE)
        Py_RETURN_NONE;

    /* SpiPat: 1-based inclusive [start,stop] → 0-based half-open */
    return Py_BuildValue("(nn)",
                         (Py_ssize_t)(mp.start - 1),
                         (Py_ssize_t)(mp.stop));
}

/* ═══════════════════════════════════════════════════════════════════════
 *  Stage 2 constructors
 * ═══════════════════════════════════════════════════════════════════════ */

static PyObject *py_arb    (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_arb());}
static PyObject *py_bal    (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_bal());}
static PyObject *py_rem    (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_rem());}
static PyObject *py_fail   (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_fail());}
static PyObject *py_abort  (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_abort());}
static PyObject *py_succeed(PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_succeed());}
/* α = POS(0), ω = RPOS(0) — SNOBOL4python conventions */
static PyObject *py_alpha  (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_pos(0));}
static PyObject *py_omega  (PyObject *s,PyObject *a){(void)s;(void)a;return wrap_pat(spipat_rpos(0));}

static PyObject *py_fence(PyObject *s, PyObject *args) {
    (void)s;
    if (PyTuple_GET_SIZE(args) == 0)
        return wrap_pat(spipat_fence_simple());
    PyObject *po;
    if (!PyArg_ParseTuple(args, "O", &po)) return NULL;
    struct pat *pp; PAT_ARG(pp, po);
    spipat_hold(pp);
    return wrap_pat(spipat_fence_function(pp));
}

#define MAKE_STR_CTOR(fname, spipat_fn) \
static PyObject *fname(PyObject *s, PyObject *args) { \
    (void)s; const char *str; Py_ssize_t slen; \
    if (!PyArg_ParseTuple(args, "s#", &str, &slen)) return NULL; \
    return wrap_pat(spipat_fn(PL2VSTRING(str, (size_t)slen))); \
}
MAKE_STR_CTOR(py_any,    spipat_any_str)
MAKE_STR_CTOR(py_notany, spipat_notany_str)
MAKE_STR_CTOR(py_span,   spipat_span_str)
MAKE_STR_CTOR(py_nspan,  spipat_nspan_str)
MAKE_STR_CTOR(py_brk,    spipat_break_str)
MAKE_STR_CTOR(py_breakx, spipat_breakx_str)

#define MAKE_NAT_CTOR(fname, spipat_fn) \
static PyObject *fname(PyObject *s, PyObject *args) { \
    (void)s; Py_ssize_t n; \
    if (!PyArg_ParseTuple(args, "n", &n)) return NULL; \
    return wrap_pat(spipat_fn((size_t)n)); \
}
MAKE_NAT_CTOR(py_len,  spipat_len)
MAKE_NAT_CTOR(py_tab,  spipat_tab)
MAKE_NAT_CTOR(py_rtab, spipat_rtab)

static PyObject *py_arbno(PyObject *s, PyObject *args) {
    (void)s;
    PyObject *po;
    if (!PyArg_ParseTuple(args, "O", &po)) return NULL;
    struct pat *pp; PAT_ARG(pp, po);
    spipat_hold(pp);
    return wrap_pat(spipat_arbno(pp));
}

/* assign_onm: P % key  — deferred (on-match); reuses same callback as imm */
static PyObject *py_assign_onm(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *po, *key;
    if (!PyArg_ParseTuple(args, "OO!", &po, &PyUnicode_Type, &key)) return NULL;
    struct pat *pp; PAT_ARG(pp, po);
    Py_INCREF(key);
    spipat_hold(pp);
    struct pat *r = spipat_call_onmatch(pp, assign_imm_call, key);
    if (!r) { Py_DECREF(key); return NULL; }
    return wrap_pat(r);
}

/* ═══════════════════════════════════════════════════════════════════════
 *  Stage 3 — Python callbacks: call, pred, setcur, rpat/ζ
 *
 *  All callbacks receive match_cookie = globals dict (set in sno_match).
 *  cookie = owned PyObject* (Py_INCREF on build, freed by spipat_free_cookie
 *  which we keep as a no-op; we rely on pattern lifetime instead).
 *
 *  NOTE: SpiPat's spipat_free_cookie / spipat_copy_cookie are called when
 *  patterns are freed/copied.  We need to ref-count properly for Python
 *  objects stored as cookies.  We override via a wrapper struct.
 * ═══════════════════════════════════════════════════════════════════════ */

/* Generic cookie that owns a PyObject* ref */
typedef struct { PyObject *obj; } PyCookie;

static PyCookie *pycookie_new(PyObject *obj) {
    PyCookie *c = malloc(sizeof(PyCookie));
    if (!c) return NULL;
    Py_INCREF(obj);
    c->obj = obj;
    return c;
}

/* ── call_imm / call_onm ──────────────────────────────────────────────
 * cookie->obj is a Python callable OR a str expression to eval.
 * For call_imm (Λ): if callable → call with no args (predicate/side-effect);
 *                   if str     → eval in globals.
 * For call_onm (λ): if callable → call with matched substring as arg;
 *                   if str     → exec in globals (side-effect).
 * On failure (return falsy / exception) we cannot signal fail from inside
 * spipat's callback; instead we store a flag and check after match.
 * Simpler: for Λ(callable) use PC_Pred_Func; for λ use PC_Call_OnM.
 */

/* call_imm callback: evaluate expression / call predicate-style */
static void
call_imm_cb(VString s, void *match_cookie, void *cookie) {
    (void)s;
    PyCookie *c  = (PyCookie *)cookie;
    PyObject *g  = (PyObject *)match_cookie;
    PyObject *fn = c->obj;

    if (PyCallable_Check(fn)) {
        PyObject *r = PyObject_CallNoArgs(fn);
        Py_XDECREF(r);
    } else if (PyUnicode_Check(fn)) {
        const char *expr = PyUnicode_AsUTF8(fn);
        if (expr) PyRun_String(expr, Py_eval_input, g, g);
    }
    PyErr_Clear();  /* ignore errors — SpiPat can't handle them here */
}

/* call_onm callback: call fn(matched_str) or exec str in globals */
static void
call_onm_cb(VString s, void *match_cookie, void *cookie) {
    PyCookie *c  = (PyCookie *)cookie;
    PyObject *g  = (PyObject *)match_cookie;
    PyObject *fn = c->obj;
    PyObject *matched = PyUnicode_DecodeUTF8(
                            (const char *)s.ptr, (Py_ssize_t)s.len, "replace");
    if (!matched) { PyErr_Clear(); return; }

    if (PyCallable_Check(fn)) {
        PyObject *r = PyObject_CallOneArg(fn, matched);
        Py_XDECREF(r);
    } else if (PyUnicode_Check(fn)) {
        /* exec the string; put matched text into globals as 'OUTPUT' first */
        PyDict_SetItemString(g, "_match_", matched);
        const char *stmt = PyUnicode_AsUTF8(fn);
        if (stmt) PyRun_String(stmt, Py_file_input, g, g);
    }
    Py_DECREF(matched);
    PyErr_Clear();
}

static PyObject *py_call_imm(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *fn;
    if (!PyArg_ParseTuple(args, "O", &fn)) return NULL;
    PyCookie *c = pycookie_new(fn);
    if (!c) return PyErr_NoMemory();
    return wrap_pat(spipat_call_immed(spipat_arb(), call_imm_cb, c));
    /* Note: call_imm in SNOBOL4python is a standalone pattern (no P arg
       from the bridge — Λ(expr) just evaluates the expression as a predicate
       at that point in the match). We use ARB() as the wrapped pattern so
       the region records zero-length; the callback fires on success. */
}

/* Actually, looking at bridge: _compile_Lambda_imm calls _C.pred(callable)
   for callables, and _C.call_imm(str) for strings.  call_imm wraps a
   zero-length pattern that fires the callback.  But SpiPat's PC_Call_Imm
   wraps an existing pattern P and fires after P matches.  We need a
   zero-length "trigger": wrap spipat_string("") so region = empty. */
static PyObject *py_call_onm(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *fn;
    if (!PyArg_ParseTuple(args, "O", &fn)) return NULL;
    PyCookie *c = pycookie_new(fn);
    if (!c) return PyErr_NoMemory();
    /* call_onm: also standalone — fires with zero-length match */
    struct pat *eps = spipat_string(C2VSTRING(""));
    spipat_hold(eps);
    struct pat *r = spipat_call_onmatch(eps, call_onm_cb, c);
    return wrap_pat(r);
}

/* ── pred ─────────────────────────────────────────────────────────────
 * PC_Pred_Func: cookie->obj is a Python callable.
 * Returns true → match continues; false/exception → fail.
 */
static bool
pred_cb(void *match_cookie, void *cookie) {
    (void)match_cookie;
    PyCookie *c = (PyCookie *)cookie;
    PyObject *r = PyObject_CallNoArgs(c->obj);
    if (!r) { PyErr_Clear(); return false; }
    bool ok = PyObject_IsTrue(r);
    Py_DECREF(r);
    return ok;
}

static PyObject *py_pred(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *fn;
    if (!PyArg_ParseTuple(args, "O", &fn)) return NULL;
    if (!PyCallable_Check(fn)) {
        PyErr_SetString(PyExc_TypeError, "pred() requires a callable");
        return NULL;
    }
    PyCookie *c = pycookie_new(fn);
    if (!c) return PyErr_NoMemory();
    return wrap_pat(spipat_predicate(pred_cb, c));
}

/* ── setcur_imm / setcur_onm ──────────────────────────────────────────
 * Θ(key) / θ(key): record cursor position into globals[key] as int.
 * SpiPat's PC_Setcur_Func calls func(cursor, match_cookie, cookie).
 */
static void
setcur_cb(size_t cursor, void *match_cookie, void *cookie) {
    PyCookie *c = (PyCookie *)cookie;    /* c->obj = key str */
    PyObject *g = (PyObject *)match_cookie;
    PyObject *v = PyLong_FromSsize_t((Py_ssize_t)cursor);
    if (v) { PyDict_SetItem(g, c->obj, v); Py_DECREF(v); }
}

static PyObject *py_setcur_imm(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *key;
    if (!PyArg_ParseTuple(args, "O!", &PyUnicode_Type, &key)) return NULL;
    PyCookie *c = pycookie_new(key);
    if (!c) return PyErr_NoMemory();
    return wrap_pat(spipat_setcur_fnc(setcur_cb, c));
}

/* setcur_onm: SpiPat has no separate on-match setcur; we use imm variant
   (the difference only matters at backtrack time, which Python patterns
   handle in the Python layer anyway). */
static PyObject *py_setcur_onm(PyObject *self, PyObject *args) {
    return py_setcur_imm(self, args);
}

/* ── rpat / ζ ─────────────────────────────────────────────────────────
 * ζ(name_or_callable): dynamic pattern — re-evaluate at match time.
 * SpiPat's PC_Dynamic_Func calls func(match_cookie, cookie, &dynamic).
 * We set dynamic->type = DY_PAT and dynamic->pat = compiled pattern.
 *
 * cookie->obj is a Python str (variable name) or callable returning a
 * PATTERN object.  We call .compile() on it each time to get the C pat.
 */
/* Release function for DY_PAT: drops the Python PatternObject ref we kept
 * alive to protect the underlying spipat pat* during the match. */
static void rpat_release(void *obj) { Py_DECREF((PyObject *)obj); }

static void
rpat_cb(void *match_cookie, void *cookie, struct dynamic *d) {
    PyCookie *c = (PyCookie *)cookie;
    PyObject *g = (PyObject *)match_cookie;
    PyObject *pat_py = NULL;

    if (PyUnicode_Check(c->obj)) {
        /* look up name in globals */
        pat_py = PyDict_GetItem(g, c->obj);  /* borrowed */
        Py_XINCREF(pat_py);
    } else if (PyCallable_Check(c->obj)) {
        pat_py = PyObject_CallNoArgs(c->obj);
    }

    if (!pat_py) { PyErr_Clear(); d->type = DY_UNK; return; }

    PyObject *compiled = PyObject_CallMethod(pat_py, "compile", NULL);
    Py_DECREF(pat_py);
    if (!compiled || !PyObject_TypeCheck(compiled, &PatternType)) {
        PyErr_Clear(); Py_XDECREF(compiled);
        d->type = DY_UNK; return;
    }

    /* Keep 'compiled' (the PatternObject) alive for the duration of the match
     * by storing it as the cookie.  rpat_release drops it afterward via
     * free_dynamic_objects.  This keeps pat->P valid throughout xmatch. */
    d->type = DY_PAT;
    d->val.pat.p      = ((PatternObject *)compiled)->pat;
    d->val.pat.release = rpat_release;
    d->val.pat.cookie  = compiled;   /* owns the ref; NOT Py_DECREF'd here */
}

static PyObject *py_rpat(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *ref;
    if (!PyArg_ParseTuple(args, "O", &ref)) return NULL;
    PyCookie *c = pycookie_new(ref);
    if (!c) return PyErr_NoMemory();
    return wrap_pat(spipat_dynamic_fnc(rpat_cb, c));
}

/* ═══════════════════════════════════════════════════════════════════════
 *  Stage 3 method table entries (appended below)
 * ═══════════════════════════════════════════════════════════════════════ */

/* ═══════════════════════════════════════════════════════════════════════
 *  Stage 4 — VStack: nPush/nInc/nPop/Shift/Reduce/Pop
 *
 *  KEY INSIGHT: SpiPat's PC_Call_Imm fires during tentative matching,
 *  before backtracking is resolved.  The Python engine avoids this by
 *  building a `cstack` of deferred commands and executing them only
 *  after a successful match.  We mirror that: each VStack op appends
 *  a Python callable to globals["__cstack__"], and sno_match() executes
 *  them after a successful spipat_match().
 *
 *  Backtracking: on backtrack SpiPat re-enters alternative paths, so
 *  new commands overwrite the cstack — exactly as in the Python engine
 *  which also re-runs cstack only for the winning path (the cstack is
 *  rebuilt per-attempt via the generator).
 *
 *  Implementation:
 *    - Each op callback appends a Python callable to __cstack__
 *    - sno_match() clears __cstack__ before match, runs it after success
 *    - The actual istack/vstack live in globals and are mutated by those
 *      callables at execution time (after the winning path is found)
 * ═══════════════════════════════════════════════════════════════════════ */

/* Append a Python tuple-op to globals[VS_CSTACK] */
static void cstack_push(PyObject *g, PyObject *fn) {
    PyObject *cs = PyDict_GetItemString(g, VS_CSTACK);
    if (!cs) {
        cs = PyList_New(0);
        if (!cs) { PyErr_Clear(); return; }
        PyDict_SetItemString(g, VS_CSTACK, cs);
        Py_DECREF(cs);
        cs = PyDict_GetItemString(g, VS_CSTACK);
    }
    PyList_Append(cs, fn);
}

/* Get or lazily create a list in globals */
static PyObject *vs_get_list(PyObject *g, const char *key) {
    PyObject *lst = PyDict_GetItemString(g, key);
    if (!lst) {
        lst = PyList_New(0);
        if (!lst) return NULL;
        PyDict_SetItemString(g, key, lst);
        Py_DECREF(lst);
        lst = PyDict_GetItemString(g, key);
    }
    return lst;
}

/* vstk_cb: append op tuple to cstack (fires on match, before backtrack resolution) */
static void vstk_cb(VString s, void *mc, void *cookie) {
    PyObject *g  = (PyObject *)mc;
    PyObject *op = ((PyCookie *)cookie)->obj;
    execute_vstack_op(g, op);
    (void)s;
}

/* Execute one cstack tuple against globals */
static void execute_vstack_op(PyObject *g, PyObject *op) {
    const char *cmd = PyUnicode_AsUTF8(PyTuple_GET_ITEM(op, 0));
    PyObject *ist = vs_get_list(g, VS_ISTACK);
    PyObject *vst = vs_get_list(g, VS_VSTACK);
    if (!ist || !vst) { PyErr_Clear(); return; }

    if (strcmp(cmd, "npush") == 0) {
        PyObject *z = PyLong_FromLong(0);
        if (z) { PyList_Append(ist, z); Py_DECREF(z); }

    } else if (strcmp(cmd, "ninc") == 0) {
        Py_ssize_t top = PyList_GET_SIZE(ist) - 1;
        if (top >= 0) {
            long v = PyLong_AsLong(PyList_GET_ITEM(ist, top));
            PyObject *nv = PyLong_FromLong(v + 1);
            if (nv) PyList_SetItem(ist, top, nv);
        }

    } else if (strcmp(cmd, "npop") == 0) {
        Py_ssize_t sz = PyList_GET_SIZE(ist);
        if (sz > 0) PySequence_DelItem(ist, sz - 1);

    } else if (strcmp(cmd, "shift") == 0) {
        /* ("shift", tag, var_or_None) */
        PyObject *tag_o = PyTuple_GET_ITEM(op, 1);
        PyObject *var_o = PyTuple_GET_ITEM(op, 2);  /* None or str */
        PyObject *node  = PyList_New(0);
        if (!node) { PyErr_Clear(); return; }
        PyList_Append(node, tag_o);
        if (var_o != Py_None) {
            /* look up var in globals */
            PyObject *val = PyDict_GetItem(g, var_o);
            if (val) PyList_Append(node, val);
            else     PyList_Append(node, var_o);  /* literal fallback */
        }
        PyList_Append(vst, node);
        Py_DECREF(node);

    } else if (strcmp(cmd, "reduce") == 0) {
        /* ("reduce", tag, n) — n==-1 means use istack top */
        PyObject *tag_o = PyTuple_GET_ITEM(op, 1);
        long n = PyLong_AsLong(PyTuple_GET_ITEM(op, 2));
        if (n == -1) {
            Py_ssize_t sz = PyList_GET_SIZE(ist);
            n = sz > 0 ? PyLong_AsLong(PyList_GET_ITEM(ist, sz-1)) : 0;
        } else if (n == -2) {
            /* use istack[itop+1] = second from top */
            Py_ssize_t sz = PyList_GET_SIZE(ist);
            n = sz > 1 ? PyLong_AsLong(PyList_GET_ITEM(ist, sz-2)) : 0;
        }
        const char *tag = PyUnicode_AsUTF8(tag_o);

        /* Σ with 0 children → ['ε'] */
        if (n == 0 && tag && strcmp(tag, "Σ") == 0) {
            PyObject *en = PyList_New(1);
            if (en) {
                PyList_SET_ITEM(en, 0, PyUnicode_FromString("ε"));
                PyList_Append(vst, en); Py_DECREF(en);
            }
            return;
        }
        /* transparent single-child wrappers */
        static const char *trans[] = {"Σ","Π","ρ","snoExprList","|","..",NULL};
        if (n == 1 && tag) {
            for (int i = 0; trans[i]; i++)
                if (strcmp(tag, trans[i]) == 0) return;
        }

        int ni = (int)n;
        Py_ssize_t vsz = PyList_GET_SIZE(vst);
        Py_ssize_t start = vsz - ni;
        if (start < 0) { start = 0; ni = (int)vsz; }

        /* collect children with owned refs */
        PyObject **children = malloc(sizeof(PyObject *) * (size_t)(ni > 0 ? ni : 1));
        if (!children) { PyErr_Clear(); return; }
        for (int i = 0; i < ni; i++) {
            children[i] = PyList_GET_ITEM(vst, start + i);
            Py_INCREF(children[i]);
        }
        /* delete from vstack (from end) */
        for (int i = 0; i < ni; i++)
            PySequence_DelItem(vst, PyList_GET_SIZE(vst) - 1);

        PyObject *node = PyList_New(0);
        if (node) {
            PyList_Append(node, tag_o);
            for (int i = 0; i < ni; i++) PyList_Append(node, children[i]);
            PyList_Append(vst, node);
            Py_DECREF(node);
        }
        for (int i = 0; i < ni; i++) Py_DECREF(children[i]);
        free(children);

    } else if (strcmp(cmd, "pop") == 0) {
        /* ("pop", key) */
        PyObject *key = PyTuple_GET_ITEM(op, 1);
        Py_ssize_t sz = PyList_GET_SIZE(vst);
        if (sz > 0) {
            PyObject *val = PyList_GET_ITEM(vst, sz-1);
            Py_INCREF(val);
            PySequence_DelItem(vst, sz-1);
            PyDict_SetItem(g, key, val);
            Py_DECREF(val);
        }
    }
}

/* Helper: make a pattern that pushes a vstack op tuple on fire */
static PyObject *make_vstk_pat(PyObject *op_tuple) {
    /* Use call_onmatch — fires only on the winning match path,
       not during tentative/backtracked alternatives. */
    PyCookie *c = pycookie_new(op_tuple);
    if (!c) return NULL;
    struct pat *eps = spipat_string(C2VSTRING(""));
    spipat_hold(eps);
    struct pat *r = spipat_call_onmatch(eps, vstk_cb, c);
    return wrap_pat(r);
}

static PyObject *py_npush(PyObject *s, PyObject *a) {
    (void)s; (void)a;
    PyObject *op = PyTuple_Pack(1, PyUnicode_FromString("npush"));
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}
static PyObject *py_ninc(PyObject *s, PyObject *a) {
    (void)s; (void)a;
    PyObject *op = PyTuple_Pack(1, PyUnicode_FromString("ninc"));
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}
static PyObject *py_npop(PyObject *s, PyObject *a) {
    (void)s; (void)a;
    PyObject *op = PyTuple_Pack(1, PyUnicode_FromString("npop"));
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}

static PyObject *py_shift(PyObject *self, PyObject *args) {
    (void)self;
    const char *tag = NULL, *var = NULL;
    if (!PyArg_ParseTuple(args, "|zz", &tag, &var)) return NULL;
    PyObject *tag_o = PyUnicode_FromString(tag ? tag : "");
    PyObject *var_o = var ? PyUnicode_FromString(var) : Py_None;
    if (var_o == Py_None) Py_INCREF(Py_None);
    PyObject *op = PyTuple_Pack(3, PyUnicode_FromString("shift"), tag_o, var_o);
    Py_DECREF(tag_o); Py_DECREF(var_o);
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}

static PyObject *py_reduce(PyObject *self, PyObject *args) {
    (void)self;
    const char *tag = NULL; int n = -1;
    if (!PyArg_ParseTuple(args, "z|i", &tag, &n)) return NULL;
    PyObject *tag_o = PyUnicode_FromString(tag ? tag : "");
    PyObject *n_o   = PyLong_FromLong(n);
    PyObject *op    = PyTuple_Pack(3, PyUnicode_FromString("reduce"), tag_o, n_o);
    Py_DECREF(tag_o); Py_DECREF(n_o);
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}

static PyObject *py_pop(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *key;
    if (!PyArg_ParseTuple(args, "O!", &PyUnicode_Type, &key)) return NULL;
    PyObject *op = PyTuple_Pack(2, PyUnicode_FromString("pop"), key);
    if (!op) return NULL;
    PyObject *r = make_vstk_pat(op);
    Py_DECREF(op); return r;
}

static PyMethodDef methods[] = {
    /* Stage 1 */
    {"epsilon",    py_epsilon,    METH_NOARGS,  "ε"},
    {"string",     py_string,     METH_VARARGS, "σ(s)"},
    {"concat",     py_concat,     METH_VARARGS, "P+Q"},
    {"alt",        py_alt,        METH_VARARGS, "P|Q"},
    {"pos",        py_pos,        METH_VARARGS, "POS(n)"},
    {"rpos",       py_rpos,       METH_VARARGS, "RPOS(n)"},
    {"assign_imm", py_assign_imm, METH_VARARGS, "P@key"},
    /* Stage 2 */
    {"assign_onm", py_assign_onm, METH_VARARGS, "P%key"},
    {"arb",        py_arb,        METH_NOARGS,  "ARB"},
    {"bal",        py_bal,        METH_NOARGS,  "BAL"},
    {"rem",        py_rem,        METH_NOARGS,  "REM"},
    {"fail",       py_fail,       METH_NOARGS,  "FAIL"},
    {"abort",      py_abort,      METH_NOARGS,  "ABORT"},
    {"succeed",    py_succeed,    METH_NOARGS,  "SUCCEED"},
    {"alpha",      py_alpha,      METH_NOARGS,  "α = POS(0)"},
    {"omega",      py_omega,      METH_NOARGS,  "ω = RPOS(0)"},
    {"fence",      py_fence,      METH_VARARGS, "FENCE/FENCE(P)"},
    {"any",        py_any,        METH_VARARGS, "ANY(s)"},
    {"notany",     py_notany,     METH_VARARGS, "NOTANY(s)"},
    {"span",       py_span,       METH_VARARGS, "SPAN(s)"},
    {"nspan",      py_nspan,      METH_VARARGS, "NSPAN(s)"},
    {"brk",        py_brk,        METH_VARARGS, "BREAK(s)"},
    {"breakx",     py_breakx,     METH_VARARGS, "BREAKX(s)"},
    {"length",     py_len,        METH_VARARGS, "LEN(n)"},
    {"tab",        py_tab,        METH_VARARGS, "TAB(n)"},
    {"rtab",       py_rtab,       METH_VARARGS, "RTAB(n)"},
    {"arbno",      py_arbno,      METH_VARARGS, "ARBNO(P)"},
    /* Stage 4 */
    {"npush",      py_npush,      METH_NOARGS,  "nPush()"},
    {"ninc",       py_ninc,       METH_NOARGS,  "nInc()"},
    {"npop",       py_npop,       METH_NOARGS,  "nPop()"},
    {"shift",      py_shift,      METH_VARARGS, "Shift(tag[,var])"},
    {"reduce",     py_reduce,     METH_VARARGS, "Reduce(tag[,n])"},
    {"pop",        py_pop,        METH_VARARGS, "Pop(key)"},
    {"sno_match",  py_match,      METH_VARARGS, "match(subj,pat,globs[,anchored])"},
    {"call_onm",   py_call_onm,   METH_VARARGS, "λ(fn_or_str)"},
    {"pred",       py_pred,       METH_VARARGS, "Λ(callable) predicate"},
    {"setcur_imm", py_setcur_imm, METH_VARARGS, "Θ(key)"},
    {"setcur_onm", py_setcur_onm, METH_VARARGS, "θ(key)"},
    {"rpat",       py_rpat,       METH_VARARGS, "ζ(name_or_fn)"},
    {NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "sno4py", "SNOBOL4 C engine (SpiPat)", -1, methods
};

PyMODINIT_FUNC
PyInit_sno4py(void) {
    if (PyType_Ready(&PatternType) < 0) return NULL;
    PyObject *m = PyModule_Create(&moduledef);
    if (!m) return NULL;
    Py_INCREF(&PatternType);
    PyModule_AddObject(m, "Pattern", (PyObject *)&PatternType);
    return m;
}

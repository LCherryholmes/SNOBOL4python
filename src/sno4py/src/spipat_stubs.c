/*
 * spipat_stubs.c — SpiPat support functions for sno4py
 *
 * Replaces malloc.c, free_cookie.c, copy_cookie.c, exception.c.
 * spipat_exception raises a Python RuntimeError then calls Py_FatalError
 * (the latter only fires if somehow called outside of a Python context).
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include "spipat.h"

void *spipat_malloc(size_t size)        { return malloc(size); }
void  spipat_free_cookie(void *cookie)  { (void)cookie; }
void  spipat_copy_cookie(void *cookie)  { (void)cookie; }

#ifdef _MSC_VER
__declspec(noreturn)
#else
__attribute__((noreturn))
#endif
void
spipat_exception(const char *msg) {
    PyErr_SetString(PyExc_RuntimeError, msg);
    Py_FatalError(msg);
}

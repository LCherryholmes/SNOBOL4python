/* gcc -g -shared -o _bootstrap.so -fPIC $(python-config --cflags --ldflags) _bootstrap.c */
#include <Python.h>
#include <stdio.h>
#include <string.h>
//----------------------------------------------------------------------------------------------------------------------
static int pos = 0;
static char * subject = NULL;
static int counter = 0;
const char * attrs[] = {"N", "n", "chars", "rex", "s", "t", "v", "expression", "command", NULL};
//----------------------------------------------------------------------------------------------------------------------
static int dump_pattern(PyObject * pattern, int depth) {
    const char * type = Py_TYPE(pattern)->tp_name;
    int count = counter++;
    if  (  !strcmp(type, "Σ")
        || !strcmp(type, "Π")
        || !strcmp(type, "ρ")
        ) {
        int refs[32];
        memset(&refs, 0, sizeof(refs));
        if (PyObject_HasAttrString(pattern, "AP")) {
            PyObject * attr = PyObject_GetAttrString(pattern, "AP");
            Py_ssize_t list_size = 0;
            if (PyTuple_Check(attr)) {
                list_size = PyTuple_Size(attr);
                for (Py_ssize_t j = 0; j < list_size; j++)
                    refs[j] = dump_pattern(PyTuple_GetItem(attr, j), depth + 2);
            }
            PySys_WriteStdout("static PATTERN P%d = {\"%s\", NULL, {", count, type);
            for (Py_ssize_t j = 0; j < list_size; j++) {
                if (j > 0) PySys_WriteStdout(", ");
                PySys_WriteStdout("&P%d", refs[j]);
            }
            PySys_WriteStdout(", NULL}};\n");
            Py_DECREF(attr);
        }
    } else if (  !strcmp(type, "ARBNO")
              || !strcmp(type, "FENCE")
              || !strcmp(type, "π")
              ) {
        int ref = -1;
        if (PyObject_HasAttrString(pattern, "P")) {
            PyObject * attr = PyObject_GetAttrString(pattern, "P");
            ref = dump_pattern(attr, depth + 2);
            Py_DECREF(attr);
        }
        PySys_WriteStdout("static PATTERN P%d = {\"%s\", NULL, &P%d};\n", count, type, ref);
    } else if (  !strcmp(type, "Δ")
              || !strcmp(type, "δ")
              ) {
        int ref = -1;
        if (PyObject_HasAttrString(pattern, "P")) {
            PyObject * attr = PyObject_GetAttrString(pattern, "P");
            ref = dump_pattern(attr, depth + 2);
            Py_DECREF(attr);
        }
        const char * N = NULL;
        if (PyObject_HasAttrString(pattern, "N")) {
            PyObject * attr = PyObject_GetAttrString(pattern, "N");
            if (PyUnicode_Check(attr)) N = PyUnicode_AsUTF8(attr);
            Py_DECREF(attr);
        }
        PySys_WriteStdout("static PATTERN P%d = {\"%s\", .s=\"%s\", &P%d};\n", count, type, N, ref);
    } else {
//  --------------------------------------------------------------------------------------------------------------------
        PySys_WriteStdout("static PATTERN P%d = {\"%s\"", count, type);
        for (int i = 0; attrs[i]; i++) {
            if (PyObject_HasAttrString(pattern, attrs[i])) {
                PyObject * attr = PyObject_GetAttrString(pattern, attrs[i]);
                if (PyLong_Check(attr)) {
                    long value = PyLong_AsLong(attr);
                    PySys_WriteStdout(", .%s=%ld", attrs[i], value);
                } else if (PyUnicode_Check(attr)) {
                    PySys_WriteStdout(", .%s=\"%s\"", attrs[i], PyUnicode_AsUTF8(attr));
                } else if (PyObject * repr = PyObject_Repr(attr)) {
                    PySys_WriteStdout(", .%s=\"%s\"", attrs[i], PyUnicode_AsUTF8(repr));
                    Py_DECREF(repr);
                }
                Py_DECREF(attr);
            }
        }
        PySys_WriteStdout("};\n");
    }
//  --------------------------------------------------------------------------------------------------------------------
    return count;
}
//----------------------------------------------------------------------------------------------------------------------
static PyObject * bootstrap(PyObject *self, PyObject *args) {
    const char * subject;
    PyObject * pattern;
    if (!PyArg_ParseTuple(args, "sO", &subject, &pattern))
        return NULL;
    PySys_WriteStdout("Subject: %s\n", subject);
    dump_pattern(pattern, 0);
    Py_RETURN_NONE;
}
//----------------------------------------------------------------------------------------------------------------------
static PyMethodDef bootstrap_methods[] = {
    {"_bootstrap", bootstrap, METH_VARARGS, "Dump the hierarchical PATTERN structure recursively."},
    {NULL, NULL, 0, NULL}
};
//----------------------------------------------------------------------------------------------------------------------
static struct PyModuleDef bootstrap_module = {
    PyModuleDef_HEAD_INIT,
    "_bootstrap",
    "Module for dumping hierarchical PATTERN structure.",
    -1,
    bootstrap_methods
};
//----------------------------------------------------------------------------------------------------------------------
PyMODINIT_FUNC PyInit__bootstrap(void) {
    return PyModule_Create(&bootstrap_module);
}
//----------------------------------------------------------------------------------------------------------------------

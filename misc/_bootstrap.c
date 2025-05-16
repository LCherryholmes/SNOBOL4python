/* gcc -g -shared -o _bootstrap.so -fPIC $(python-config --cflags --ldflags) _bootstrap.c */
#include <Python.h>
#include <stdio.h>
#include <string.h>

static void dump_pattern(PyObject * pattern, int depth) {
    const char * type_name = Py_TYPE(pattern)->tp_name;
    PySys_WriteStdout("%*s%s", depth * 2, "", type_name);
    const char * attrs[] = {
        "N", "n", "chars", "rex", "s", "t", "v", "expression", "command", NULL
    };
//  ----------------------------------------------------------------------------
    for (int i = 0; attrs[i]; i++) {
        if (PyObject_HasAttrString(pattern, attrs[i])) {
            PyObject * attr = PyObject_GetAttrString(pattern, attrs[i]);
            if (PyLong_Check(attr)) {
                long value = PyLong_AsLong(attr);
                PySys_WriteStdout(" %ld", value);
            } else if (PyUnicode_Check(attr)) {
                PySys_WriteStdout(" %s", PyUnicode_AsUTF8(attr));
            } else if (PyObject * repr = PyObject_Repr(attr)) {
                PySys_WriteStdout(" %s", PyUnicode_AsUTF8(repr));
                Py_DECREF(repr);
            }
            Py_DECREF(attr);
        }
    }
    PySys_WriteStdout("\n");
//  ----------------------------------------------------------------------------
    if (PyObject_HasAttrString(pattern, "P")) {
        PyObject * attr = PyObject_GetAttrString(pattern, "P");
        dump_pattern(attr, depth + 2);
        Py_DECREF(attr);
    }
    if (PyObject_HasAttrString(pattern, "Q")) {
        PyObject * attr = PyObject_GetAttrString(pattern, "Q");
        dump_pattern(attr, depth + 2);
        Py_DECREF(attr);
    }
    if (PyObject_HasAttrString(pattern, "AP")) {
        PyObject * attr = PyObject_GetAttrString(pattern, "AP");
        if (PyTuple_Check(attr)) {
            Py_ssize_t list_size = PyTuple_Size(attr);
            for (Py_ssize_t j = 0; j < list_size; j++)
                dump_pattern(PyTuple_GetItem(attr, j), depth + 2);
        }
        Py_DECREF(attr);
    }
//  ----------------------------------------------------------------------------
}
//------------------------------------------------------------------------------
static PyObject* bootstrap(PyObject *self, PyObject *args) {
    const char * subject;
    PyObject * pattern;
    if (!PyArg_ParseTuple(args, "sO", &subject, &pattern))
        return NULL;
    PySys_WriteStdout("Subject: %s\n", subject);
    dump_pattern(pattern, 0);
    Py_RETURN_NONE;
}
//------------------------------------------------------------------------------
static PyMethodDef BootstrapMethods[] = {
    {"_bootstrap", bootstrap, METH_VARARGS, "Dump the hierarchical PATTERN structure recursively."},
    {NULL, NULL, 0, NULL}   // Sentinel
};
//------------------------------------------------------------------------------
static struct PyModuleDef bootstrap_module = {
    PyModuleDef_HEAD_INIT,
    "_bootstrap",
    "Module for dumping hierarchical PATTERN structure.",
    -1,
    BootstrapMethods
};
//------------------------------------------------------------------------------
PyMODINIT_FUNC PyInit__bootstrap(void) {
    return PyModule_Create(&bootstrap_module);
}
//------------------------------------------------------------------------------

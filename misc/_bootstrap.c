/* gcc -shared -o _bootstrap.so -fPIC $(python-config --cflags --ldflags) _bootstrap.c */
#include <Python.h>
#include <stdlib.h>
#include <string.h>

static PyObject* _bootstrap(PyObject* self, PyObject* args) {
    PyObject *py_subject = NULL;
    PyObject *py_pattern = NULL;

    if (!PyArg_ParseTuple(args, "OO", &py_subject, &py_pattern))
        return NULL;

    if (!PyUnicode_Check(py_subject)) {
        PyErr_SetString(PyExc_TypeError, "subject must be a string");
        return NULL;
    }

    const char* subject_c = PyUnicode_AsUTF8(py_subject);
    if (!subject_c)
        return NULL;

    size_t subject_len = strlen(subject_c);
    char* subject_buffer = (char*) malloc(subject_len + 1);
    if (!subject_buffer) {
        PyErr_NoMemory();
        return NULL;
    }
    strcpy(subject_buffer, subject_c);

    PyObject* py_N = PyObject_GetAttrString(py_pattern, "N");
    if (!py_N || !PyUnicode_Check(py_N)) {
        free(subject_buffer);
        Py_XDECREF(py_N);
        PyErr_SetString(PyExc_AttributeError, "pattern must have a Unicode attribute 'N'");
        return NULL;
    }
    const char* pattern_N = PyUnicode_AsUTF8(py_N);
    if (!pattern_N) {
        free(subject_buffer);
        Py_DECREF(py_N);
        return NULL;
    }

    PyObject* py_n = PyObject_GetAttrString(py_pattern, "n");
    if (!py_n) {
        free(subject_buffer);
        Py_DECREF(py_N);
        PyErr_SetString(PyExc_AttributeError, "pattern must have an attribute 'n'");
        return NULL;
    }
    long pattern_n = PyLong_AsLong(py_n);

    PyObject* py_AP = PyObject_GetAttrString(py_pattern, "AP");
    if (!py_AP || !PyList_Check(py_AP)) {
        free(subject_buffer);
        Py_DECREF(py_N);
        Py_DECREF(py_n);
        Py_XDECREF(py_AP);
        PyErr_SetString(PyExc_AttributeError, "pattern must have a list attribute 'AP'");
        return NULL;
    }
    Py_ssize_t ap_len = PyList_Size(py_AP);

    PySys_WriteStdout("Subject: %s\n", subject_buffer);
    PySys_WriteStdout("Pattern.N: %s\n", pattern_N);
    PySys_WriteStdout("Pattern.n: %ld\n", pattern_n);
    PySys_WriteStdout("Pattern.AP contents:\n");

    for (Py_ssize_t i = 0; i < ap_len; i++) {
        PyObject *item = PyList_GetItem(py_AP, i); // Borrowed reference.
        if (!item) continue;
        PyObject *item_N = PyObject_GetAttrString(item, "N");
        if (item_N && PyUnicode_Check(item_N)) {
            const char* item_N_str = PyUnicode_AsUTF8(item_N);
            if (item_N_str) PySys_WriteStdout("  AP[%zd].N: %s\n", i, item_N_str);
            Py_DECREF(item_N);
        } else {
            Py_XDECREF(item_N);
            PySys_WriteStdout("  AP[%zd].N: <not found or not a string>\n", i);
        }
    }

    free(subject_buffer);
    Py_DECREF(py_N);
    Py_DECREF(py_n);
    Py_DECREF(py_AP);

    Py_RETURN_NONE;
}

static PyMethodDef SearchMethods[] = {
    {"_bootstrap", (PyCFunction)_bootstrap, METH_VARARGS, "C function to display subject and pattern parameters."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _bootstrap_module = {
    PyModuleDef_HEAD_INIT,
    "_bootstrap",
    "Module that implements the _bootstrap function using CPython API with passed arguments.",
    -1,
    SearchMethods
};

PyMODINIT_FUNC PyInit__bootstrap(void) {
    return PyModule_Create(&_bootstrap_module);
}

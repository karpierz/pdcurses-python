
// Like PyUnicode_AsUTF8(), but check for embedded null characters.
// Export for '_sqlite3' shared extension, and for Argument Clinic code.
PyAPI_FUNC(const char *) _PyUnicode_AsUTF8NoNUL(PyObject *);


/* This function declaration was moved from pycore_structseq.h file to adapt
it for windows-curses package */
// Export for '_curses' shared extension
PyAPI_FUNC(PyTypeObject*) _PyStructSequence_NewType(
    PyStructSequence_Desc *desc,
    unsigned long tp_flags);

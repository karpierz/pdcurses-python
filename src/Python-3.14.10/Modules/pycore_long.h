#pragma once

#define _PyLong_GetZero() PyLong_FromLong(0)

// Export for '_testclinic' shared extension (Argument Clinic code)
PyAPI_FUNC(int) _PyLong_UnsignedInt_Converter(PyObject *, void *);

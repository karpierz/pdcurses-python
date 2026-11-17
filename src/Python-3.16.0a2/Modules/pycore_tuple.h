#pragma once

// Export for '_socket' shared extension
PyAPI_FUNC(int) _Py_dup(int fd);

//From "pycore_tuple.h"
#if SIZEOF_PY_UHASH_T > 4
#define _PyTuple_HASH_XXPRIME_1 ((Py_uhash_t)11400714785074694791ULL)
#define _PyTuple_HASH_XXPRIME_2 ((Py_uhash_t)14029467366897019727ULL)
#define _PyTuple_HASH_XXPRIME_5 ((Py_uhash_t)2870177450012600261ULL)
#define _PyTuple_HASH_XXROTATE(x) ((x << 31) | (x >> 33))  /* Rotate left 31 bits */
#else
#define _PyTuple_HASH_XXPRIME_1 ((Py_uhash_t)2654435761UL)
#define _PyTuple_HASH_XXPRIME_2 ((Py_uhash_t)2246822519UL)
#define _PyTuple_HASH_XXPRIME_5 ((Py_uhash_t)374761393UL)
#define _PyTuple_HASH_XXROTATE(x) ((x << 13) | (x >> 19))  /* Rotate left 13 bits */
#endif

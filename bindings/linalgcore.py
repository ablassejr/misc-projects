"""Python ctypes bridge to liblinalgcore.dylib."""

import ctypes
import ctypes.util
import os

_lib_path = os.path.join(os.path.dirname(__file__), '..', 'engine', 'build', 'liblinalgcore.dylib')
_lib = ctypes.CDLL(_lib_path)


class _LAMatrix(ctypes.Structure):
    _fields_ = [
        ('data', ctypes.POINTER(ctypes.c_double)),
        ('rows', ctypes.c_int),
        ('cols', ctypes.c_int),
    ]


# la_matrix_new
_lib.la_matrix_new.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.la_matrix_new.restype = ctypes.POINTER(_LAMatrix)

# la_matrix_free
_lib.la_matrix_free.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_free.restype = None

# la_matrix_from_array
_lib.la_matrix_from_array.argtypes = [
    ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)
]
_lib.la_matrix_from_array.restype = ctypes.POINTER(_LAMatrix)

# la_matrix_get / la_matrix_set
_lib.la_matrix_get.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.c_int, ctypes.c_int]
_lib.la_matrix_get.restype = ctypes.c_double
_lib.la_matrix_set.argtypes = [ctypes.POINTER(_LAMatrix), ctypes.c_int, ctypes.c_int, ctypes.c_double]
_lib.la_matrix_set.restype = None

# la_matrix_data_ptr
_lib.la_matrix_data_ptr.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_data_ptr.restype = ctypes.POINTER(ctypes.c_double)

# la_matrix_rows / la_matrix_cols
_lib.la_matrix_rows.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_rows.restype = ctypes.c_int
_lib.la_matrix_cols.argtypes = [ctypes.POINTER(_LAMatrix)]
_lib.la_matrix_cols.restype = ctypes.c_int


class CMatrix:
    """Python wrapper around a C LAMatrix pointer."""

    def __init__(self, rows, cols, data=None):
        if data is not None:
            arr = (ctypes.c_double * len(data))(*data)
            self._ptr = _lib.la_matrix_from_array(rows, cols, arr)
        else:
            self._ptr = _lib.la_matrix_new(rows, cols)
        if not self._ptr:
            raise MemoryError("Failed to allocate LAMatrix")

    def __del__(self):
        if hasattr(self, '_ptr') and self._ptr:
            _lib.la_matrix_free(self._ptr)

    @property
    def rows(self):
        return _lib.la_matrix_rows(self._ptr)

    @property
    def cols(self):
        return _lib.la_matrix_cols(self._ptr)

    def __getitem__(self, key):
        i, j = key
        return _lib.la_matrix_get(self._ptr, i, j)

    def __setitem__(self, key, value):
        i, j = key
        _lib.la_matrix_set(self._ptr, i, j, value)

    def to_list(self):
        return [[self[i, j] for j in range(self.cols)] for i in range(self.rows)]

    @property
    def ptr(self):
        return self._ptr

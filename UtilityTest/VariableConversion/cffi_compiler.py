from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
                double * FloatArrayManaging (int VecLen, float *Array);
                double ** FloatMatrixManaging (int dim1, int dim2, float **Matrix);
                """)

ffibuilder.set_source("_test",  # name of the output C extension
"""
    #include "test.h"
""",
    sources=['test.c'],   # includes pi.c as additional sources
    libraries=['m'])    # on Unix, link with the math library

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
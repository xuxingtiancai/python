cdef extern from "math.h":
    float sinf(float theta)

def run():
    cdef float x
    cdef int i
    x = 0
    i = 0
    while i < 3000000:
        x = sinf(x + 1)
        i += 1
    print x

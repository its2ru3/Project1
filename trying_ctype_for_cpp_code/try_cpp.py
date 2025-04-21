import ctypes

# Load the shared library
lib = ctypes.CDLL('./libtry.so')

# Call hello()
lib.hello()

# Setup argument and return types
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

# Call add()
result = lib.add(10, 20)
print("Result from C++ add:", result)

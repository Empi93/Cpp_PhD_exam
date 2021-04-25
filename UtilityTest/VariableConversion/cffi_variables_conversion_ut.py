"""
Test Unit to find a way to exchange data between the python script and the
C lib.

Apparently the conversion from ndarray to Ctype does not work, 
while .tolist() works just fine.

On the other hand the conversion from Ctype to numpy ndarray works very well.
The only problem is that one needs to know the dimension of the array in 
advance. In this scenario it would be better to make ndarray->Ctype conversion
works and then return the dimension of the array at the end of the C method
and convert back our array.
"""

import numpy as np 
import os
from cffi import FFI
 
ffi = FFI()

# Compile
os.system('python compiler.py')
from _test.lib import VariablesManaging

# Define variables
VecLen = 10
dim1, dim2 = 3, 4
InputArray = np.full(VecLen, 2., dtype=np.float32)
InputMatrix = np.full((dim1, dim2), 2., dtype=np.float32)
OutputArray = np.full(VecLen, 3.)
OutputMatrix = np.full((dim1, dim2), 3.)

# Print before function
print("BEFORE test function excecution")
print("InputArray: ", InputArray)
print("OutputArray: ", OutputArray)
print("\n\n");

# Convert ndarray to cdata
InputArray_cffi = ffi.cast('float*', InputArray.ctypes.data)

# Convert InputArray back to python
buffer_size = InputArray.size*InputArray.dtype.itemsize
c_buffer = ffi.buffer(InputArray_cffi,buffer_size)
InputArray = np.frombuffer(c_buffer, dtype=InputArray.dtype)

print("InputArray: ", InputArray)

# Test function
OutputArray_cffi = VariablesManaging(VecLen, InputArray_cffi)
#OutputArray_cffi = VariablesManaging(VecLen, InputArray.tolist())

# Convert OutputArray back to python
# This procedure must be implemented only for float *->np.float32 conversion
# int * returns an array ready to use
buffer_size = OutputArray.size*OutputArray.dtype.itemsize
c_buffer = ffi.buffer(OutputArray_cffi,buffer_size)
OutputArray = np.frombuffer(c_buffer, dtype=OutputArray.dtype)

# Convert InputArray back to python
buffer_size = InputArray.size*InputArray.dtype.itemsize
c_buffer = ffi.buffer(InputArray_cffi,buffer_size)
InputArray = np.frombuffer(c_buffer, dtype=InputArray.dtype)

# Print after function
print("AFTER test function excecution")
print("InputArray: ", InputArray)
print("OutputArray: ", OutputArray)
print("\n\n");


 


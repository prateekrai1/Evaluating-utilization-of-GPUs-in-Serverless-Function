import numpy as np
import cupy as cp
import time
array_side = 625
total_array_size = array_side * array_side * array_side
print('Total Array to be Benchmarked: '+str(total_array_size))
### Numpy and CPU
s = time.time()
x_cpu = np.ones((array_side,array_side,array_side))
e = time.time()
print('Numpy & CPU operation to create array took '+str(e - s))
### CuPy and GPU
s = time.time()
x_gpu = cp.ones((array_side,array_side,array_side))
cp.cuda.Stream.null.synchronize()
e = time.time()
print('CuPy & GPU operation to create array took '+str(e - s))

### Numpy and CPU
s = time.time()
x_cpu *= 5
x_cpu *= x_cpu
x_cpu += x_cpu
e = time.time()
print('Numpy & CPU operation to multiple the array by 5, multiple the array by itself and add the array to itself took '+str(e - s))
### CuPy and GPU
s = time.time()
x_gpu *= 5
x_gpu *= x_gpu
x_gpu += x_gpu
cp.cuda.Stream.null.synchronize()
e = time.time()
print('CuPy & GPU operation to multiple the array by 5, multiple the array by itself and add the array to itself took '+str(e - s))

print('Finished\n\n')
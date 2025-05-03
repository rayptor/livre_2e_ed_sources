import pyopencl as cl
import numpy as np
import time as ti

import os
os.environ['PYOPENCL_CTX'] = '0'
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

n = 3000
rng = np.random.default_rng(seed=9081725364)
a = rng.random(size=(n,n), dtype = np.float32)
b = rng.random(size=(n,n), dtype = np.float32)
c = np.zeros((n,n), dtype = np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

device = queue.get_info(cl.command_queue_info.DEVICE).get_info(cl.device_info.NAME)
print(f"CPU : {device}")
globalmem = queue.get_info(cl.command_queue_info.DEVICE).get_info(cl.device_info.GLOBAL_MEM_SIZE)
print(f"RAM : {globalmem / 1024**2} Mo")

mf = cl.mem_flags
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

prg = cl.Program(ctx, """
    __kernel void multiply(ushort n, __global float *a, __global float *b, __global float *c)
    {
      int gid = get_global_id(0);
      c[gid] = 0.0f;
      int row = gid / n;
      int col = gid % n;
      __global float *ptra = &a[row * n];
      __global float *ptrb = &b[col];
                 
      barrier(CLK_LOCAL_MEM_FENCE);
      for(int i = 0; i < n; i++) {
         ptrb = &b[col + i * n];
         c[gid] += (*(ptra++)) * (*ptrb);
      }
      barrier(CLK_LOCAL_MEM_FENCE);
    }
    """).build()

t = 10
temps = np.zeros(t)
for k in range(t):
  debut = ti.perf_counter()
  prg.multiply(queue, c.shape, None, np.uint16(n), a_buf, b_buf, c_buf)
  queue.finish()
  temps[k] = ti.perf_counter() - debut
  moyenne = np.mean(temps)
print(f"OPENCL : Temps moyen écoulé pour n=%s : %s s" % (n, moyenne))
cl.enqueue_copy(queue, c, c_buf)
# print(f"OpenCL : {c}")

temps = np.zeros(t)
for k in range(t):
  debut = ti.perf_counter()
  c = a @ b
  temps[k] = ti.perf_counter() - debut
  moyenne = np.mean(temps)
print(f"NUMPY : Temps moyen écoulé pour n=%s : %s s" % (n, moyenne))
# print(f"Numpy : {c}")
import timeit
import pyopencl as cl
import numpy as np
#------------------------------------------------------------------------------
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
input_text = "\0" * 1024
input_array = np.frombuffer(input_text.encode('ascii'), dtype=np.uint8)
mf = cl.mem_flags
input_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_array)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, input_array.nbytes)
#------------------------------------------------------------------------------
c_name = "C:/SNOBOL4python/tests/test_icon.c"
with open(c_name, "r") as c_file:
    kernel_source = c_file.read()
    program = cl.Program(ctx, kernel_source).build()
    global_size = (1,) # (input_array.size,)
    if True:
        time = timeit.timeit(
                 lambda: program.icon(queue, global_size, None, input_buf, output_buf, np.uint32(input_array.size))
               , number = 100_000, globals = globals());
        print(time)
    else: program.icon(queue, global_size, None, input_buf, output_buf, np.uint32(input_array.size))
    output_array = np.empty_like(input_array)
    cl.enqueue_copy(queue, output_array, output_buf)
    queue.finish()
    output_text = output_array.tobytes().decode('ascii')
    print(output_text)
#------------------------------------------------------------------------------

import pyopencl as cl
import numpy as np

ctx = cl.create_some_context() # Create an OpenCL context (this selects a device, e.g., a GPU) and command queue.
queue = cl.CommandQueue(ctx)
input_text = "Hello, OpenCL!" # Define the input text.
input_array = np.frombuffer(input_text.encode('ascii'), dtype=np.uint8) # Convert the string to a NumPy array of type uint8 (each element is an ASCII code).
mf = cl.mem_flags # Allocate device memory buffers.
input_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_array)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, input_array.nbytes)
# OpenCL kernel: Converts lowercase letters to uppercase.
# It reads each uchar (character code) and if it is between 'a' (97) and 'z' (122),
# it subtracts 32 to convert it to the corresponding uppercase letter.
kernel_source = """
__kernel void to_upper(__global const uchar *input,
                       __global uchar *output) {
    int i = get_global_id(0);
    uchar c = input[i];
    // Convert lowercase letter to uppercase (if in range 'a' - 'z').
    if (c >= 'a' && c <= 'z') {
        c = c - 32;
    }
    output[i] = c;
}
"""
program = cl.Program(ctx, kernel_source).build() # Build the OpenCL program.
global_size = (input_array.size,) # Set the global work size to the length of the input (each work-item handles one character).
program.to_upper(queue, global_size, None, input_buf, output_buf) # Execute the kernel.
output_array = np.empty_like(input_array) # Create an empty NumPy array to hold the output.
cl.enqueue_copy(queue, output_array, output_buf) # Copy the output buffer from the device back into the host array.
queue.finish()
output_text = output_array.tobytes().decode('ascii') # Convert the NumPy array back into a string.
print("Original text:", input_text)
print("Transformed text:", output_text)

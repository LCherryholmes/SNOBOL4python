# File: fun_with_loops.py
import numpy as np
import timeit
#------------------------------------------------------------------------------
def zip_it_good():
    result = np.empty(len(flags), int)
    for i, (c, s1, s2) in enumerate(zip(flags, ones, zeroes)):
        if c: result[i] = s1
        else: result[i] = s2
    return result
#------------------------------------------------------------------------------
def two_to_tango():
    result = zeroes.copy()
    result[flags] = ones[flags]
    return result
#------------------------------------------------------------------------------
n = 1000000
for length in (10, 50, 100, 200):
    ones  = np.ones(length)
    zeroes = np.zeros(length)
    flags = [(False, True)[np.random.randint(0, 1+1)] for i in range(length)]
    print(f"len={length}")    
    zipit = timeit.timeit("zip_it_good()", number=n, globals=globals());
    print(f"zip_it_good:  {zipit}")
    tango = timeit.timeit("two_to_tango()", number=n, globals=globals());
    print(f"two_to_tango: {tango}")
    print(f"ratio(z/t):  {zipit / tango: 2.2f}", )
    print()
#------------------------------------------------------------------------------

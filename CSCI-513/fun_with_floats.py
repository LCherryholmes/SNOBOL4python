import numpy as np
#------------------------------------------------------------------------------
count = 0
total = 10000000
ppt = 1000000.0
for i in range(total):
    r = np.random.uniform(99.99999999, 100.0)
    if (r >= 100.0):
        count += 1
        print(r)
print()        
print(count, 'do include 100.0 due to rounding errors.')
print(count * ppt / total)
print()        
#------------------------------------------------------------------------------
count = 0
total = 10000000
for i in range(total):
    r = np.random.uniform(0.0, 101.0)
    if (r > 100.0):
        count += 1
print(count, 'wrong answers')        
print(count * ppt / total)
print()        
#------------------------------------------------------------------------------
count = 0
total = 10000000
print(100.00000000000001) # fine
print(100.000000000000009) # round-error
print(100.000000000000008) # round-error
print(100.000000000000007) # under-flow
print()        
for i in range(total):
    r = np.random.uniform(99.99999999, 100.000000000000008)
    if (r >= 100.0):
        count += 1
print(count, 'to be absolutely accurate and precise ...')
print(count * ppt / total)
print()        
#------------------------------------------------------------------------------

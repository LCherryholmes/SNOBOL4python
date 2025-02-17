# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# CSCI 513.01W – Python Programming for AI
# Assignment 4 - NumPy
# CWID: 50417840
# Name: Lon Jones Cherryholmes
import numpy as np
#------------------------------------------------------------------------------
print("Exercise I")
# Create an array called prices of 50 random float numbers between 0 and 100
# (inclusive).
prices = np.random.uniform(0, 100, (50,))
print(prices, end="\n\n")
#------------------------------------------------------------------------------
print("Exercise II")
# Create a NumPy array called ages. This array should have 15 random ages
# between 5 and 25 (inclusive).  Create a NumPy array called ages2. The values
# in ages2 should be double the ones in ages.
ages = np.random.randint(5, 25 + 1, 15)
print(ages, end="\n\n")
ages2 = ages * 2
print(ages2, end="\n\n")
#------------------------------------------------------------------------------
print("Exercise III")
# To make ages2 a little bit more realistic, insert a little random noise into
# each element of the array you created.  To be more precise, modify each value
# assigned to ages2 by adding a different random floating-point value between
# -2 and +2.
ages2 = np.array(ages2, float)
for i in range(len(ages2)):
    ages2[i] += np.random.random_sample() * 4.0 - 2.0
print(ages2, end="\n\n")
ages2 = ages * 2
ages2 = ages2 + np.random.uniform(-2.0, +2.0, (15,))
print(ages2, end="\n\n")
#------------------------------------------------------------------------------
print("Exercise IV")
# Suppose we have two numpy arrays that represent the price of the same items
# from different stores: Create a new array where we take the value from store1
# whenever the corresponding value in cond is True, otherwise we take the value
# from store2.
store1 = np.array([29, 4, 2, 30, 15, 48, 63, 32, 53, 70, 47, 19, 24])
store2 = np.array([23, 2, 12, 32, 25, 47, 53, 39, 63, 71, 47, 18, 21])
cond = np.array([False, True, False, False, False, True, False, False, True,
                 True, False, False, True])
result = np.empty(len(cond), int)
for i, (c, s1, s2) in enumerate(zip(cond, store1, store2)):
    if c: result[i] = s1
    else: result[i] = s2
print(result, end="\n\n")
#------------------------------------------------------------------------------
print("Exercise V")
# Solve Exercise IV using numpy where function.
result = np.where(cond, store1, store2)
print(result, end="\n\n")
#------------------------------------------------------------------------------
print("Exercise VI")
# Suppose we have the scores from players playing an arcade game:
# 1. Retrieve the scores that are greater than 20.
# 2. Retrieve the scores that are not 30.
# 3. Retrieve the average score.
# 4. Retrieve the minimum score.
# 5. Retrieve the maximum score.
scores = np.random.randint(low=0, high=70, size=[2000])
print(scores[scores > 20])
print(scores[scores != 30])
print(np.mean(scores))
print(np.min(scores))
print(np.max(scores))
#------------------------------------------------------------------------------

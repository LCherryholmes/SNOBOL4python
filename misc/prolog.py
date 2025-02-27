# -*- coding: utf-8 -*-
from pyDatalog import pyDatalog as prolog
from math import sqrt

prolog.create_terms("squares, X, Y, sqrt")
squares(X, Y) <= ((X._in(range(10)) & (Y == sqrt(X)) & (Y < 3)))
print(squares(X, Y)); print()
print(squares(3, Y)); print()
print(squares(X, 2)); print()

prolog.create_terms("factorial, N, F")
factorial[N] = N * factorial[N - 1]
factorial[1] = 1
print(factorial[4] == N)


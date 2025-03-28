# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ, φ, Φ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ANY, ARB, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from pprint import pprint
#-------------------------------------------------------------------------------
import os
import sys
import pstats
import cProfile
sys.path.append(os.getcwd())
#from transl8r_y import *
#from transl8r_yaml import *
from transl8r_pop3 import *
#from transl8r_english import *
#-------------------------------------------------------------------------------
def main():
    pass
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------

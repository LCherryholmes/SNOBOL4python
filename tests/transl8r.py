# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
#-------------------------------------------------------------------------------
import os
import sys
sys.path.append(os.getcwd())
#from transl8r_y import *
from transl8r_yaml import *
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    yamlInput_nm = r"""C:\Users\lcher\.conda\pkgs\python-3.12.3-h2628c8c_0_cpython\info\recipe\meta.yaml"""
    pyOutput_nm = r""".\meta-yaml.py"""
    GLOBALS(globals())
    with open(yamlInput_nm, "r") as yamlInput:
        yaml = yamlInput.read()
        if MATCH(yaml, yamlTokens()):
            with open(pyOutput_nm, "w", encoding="utf-8") as pyOutput:
                pyOutput.write(P[:-3])
#-------------------------------------------------------------------------------

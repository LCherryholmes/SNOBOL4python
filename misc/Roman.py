# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# 31 flavors of patterns to choose from ...
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, LCASE, UCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from SNOBOL4python import DEFINE, REPLACE, SUBSTITUTE
from SNOBOL4python import F, END, RETURN, FRETURN, NRETURN
from SNOBOL4python import PATTERN, Ϩ, STRING, NULL
from pprint import pprint
#-----------------------------------------------------------------------------------------------------------------------
"""\
         DEFINE('Roman(n)units')
         romanXlat   =     '0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,'   :(RomanEnd)
Roman    n           RPOS(1) LEN(1) . units =                           :F(RETURN)
         romanXlat   units BREAK(',') . units                           :F(FRETURN)
         Roman       =     REPLACE(Roman(n),'IVXLCDM','XLCDM**') units  :S(RETURN)F(FRETURN)
RomanEnd
         OUTPUT      =     "1961 = " + Roman(1961)
         OUTPUT      =     "2025 = " + Roman(2025)                      :(END)
END
"""
#-----------------------------------------------------------------------------------------------------------------------
def Ξ1():
                    try:      DEFINE('Roman(n)units')
                    except F: pass
def Ξ2():
                    try:
                    global    romanXlat
                              romanXlat = Ϩ('0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,')
                              return ΞRomanEnd
                    except F: return ΞRomanEnd

def ΞRoman():
                    try:
                    global    n
                              n = SUBSTITUTE(n, n == RPOS(1) + LEN(1) % "units", NULL)
                    except F: return RETURN
def Ξ4():
                    try:      romanXlat == units + BREAK(',') % "units"
                    except F: return FRETURN
def Ξ5():
                    try:
                    global    Roman
                              Roman = REPLACE(ϘRoman(n), 'IVXLCDM', 'XLCDM**') + units
                              return RETURN
                    except F: return FRETURN
def ΞRomanEnd():    pass
def Ξ7():
                    try:
                              print('1961 = ' + ϘRoman(1961))
                              print('2025 = ' + ϘRoman(2025))
                              return END
                    except F: return END
#-----------------------------------------------------------------------------------------------------------------------
ξ = {3: ΞRoman, 6: ΞRomanEnd}
Ξ = {ΞRoman: 3, ΞRomanEnd: 6}
#-----------------------------------------------------------------------------------------------------------------------
def ϘRoman(ϙn):
    global Roman, n, units
    _Roman = Roman if 'Roman' in globals() else None; Roman = NULL
    _n = n if 'n' in globals() else None; n = ϙn
    _units = units if 'units' in globals() else None; units = NULL
    Xi = RUN(Ξ[ΞRoman])
    ϙ = Roman
    units = _units
    n = _n
    Roman = _Roman
    return ϙ
#-----------------------------------------------------------------------------------------------------------------------
STNO = None
def RUN(at):
    global STNO
    STNO = at
    while True:
        if STNO in ξ:                 invocation = ξ[STNO]
        elif f'Ξ{STNO}' in globals(): invocation = globals()[f'Ξ{STNO}']
        else:                         raise Exception("It's the end of the world.")
        goto = invocation()
        if   goto is None:    STNO += 1
        elif goto == RETURN:  return goto
        elif goto == FRETURN: return goto
        elif goto == NRETURN: return goto
        elif goto == END:     return goto
        else:                 STNO = Ξ[goto]
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
RUN(1)
#-----------------------------------------------------------------------------------------------------------------------
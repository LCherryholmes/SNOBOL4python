# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH
from SNOBOL4python import ε, σ, Σ, Π, λ, Λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, FENCE, LEN, POS, RPOS, SPAN
#------------------------------------------------------------------------------
@pattern
def identifier():
    yield from \
        (   POS(0)
        +   ANY(_UCASE + _LCASE)
        +   FENCE(SPAN("." + _digits + _UCASE + "_" + _LCASE) | ε())
        +   RPOS(0)
        )
assert True is MATCH("Id_99", identifier())
#------------------------------------------------------------------------------
@pattern
def real_number():
    yield from \
        (   POS(0)
        +   (   (   SPAN(_digits) @ 'whole'
                +   (σ('.') + FENCE(SPAN(_digits) | ε()) @ 'fract' | ε())
                +   (σ('E') | σ('e'))
                +   (σ('+') | σ('-') | ε())
                +   SPAN(_digits) @ 'exp'
                )
            |   (   SPAN(_digits) @ 'whole'
                +   σ('.')
                +   FENCE(SPAN(_digits) | ε()) @ 'fract'
                )
            )
        +   RPOS(0)
        )
assert True is MATCH("12.99E+3", real_number());
#variable = None
#for variable in globals().items():
#    print(variable)
#print(f"whole={whole} fract={fract} exp={exp}")
#------------------------------------------------------------------------------
@pattern
def test_one():
    yield from Σ( POS(0) @ 'OUTPUT'
               ,  Π(σ('B') , σ('F') , σ('L') , σ('R')) @ 'OUTPUT'
               ,  Π(σ('E') , σ('EA')) @ 'OUTPUT'
               ,  Π(σ('D') , σ('DS')) @ 'OUTPUT'
               ,  RPOS(0) @ 'OUTPUT'
               )
assert True is MATCH("BED", test_one())
assert True is MATCH("FED", test_one())
assert True is MATCH("LED", test_one())
assert True is MATCH("RED", test_one())
assert True is MATCH("BEAD", test_one())
assert True is MATCH("FEAD", test_one())
assert True is MATCH("LEAD", test_one())
assert True is MATCH("READ", test_one())
assert True is MATCH("BEDS", test_one())
assert True is MATCH("FEDS", test_one())
assert True is MATCH("LEDS", test_one())
assert True is MATCH("REDS", test_one())
assert True is MATCH("BEADS", test_one())
assert True is MATCH("FEADS", test_one())
assert True is MATCH("LEADS", test_one())
assert True is MATCH("READS", test_one())
#------------------------------------------------------------------------------
@pattern
def As():
    yield from \
        (   POS(0)
        +   ARBNO(σ('a')) @ 'sequence'
        +   RPOS(0)
        )
assert True is MATCH("", As())
assert True is MATCH("a", As())
assert False is MATCH("aa", As())
assert False is MATCH("aaa", As())
assert False is MATCH("aaaa", As())
#------------------------------------------------------------------------------
@pattern
def Alist():
    yield from \
        (   POS(0)
        +   (σ('a') | σ('b'))
        +   ARBNO(σ(',') + (σ('a') | σ('b')))
        +   RPOS(0)
        )
assert False is MATCH("", Alist())
assert True is MATCH("a", Alist())
assert True is MATCH("a,a", Alist())
assert False is MATCH("a,a,a", Alist())
assert False is MATCH("a,a,a,a", Alist())
#------------------------------------------------------------------------------
if False:
    global units
    romanXlat = '0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,'
    def Roman(n):
        if not REPLACE(n, RPOS(1) + LEN(1) @ 'units', ''):
            return ""
        if not MATCH(units, BREAK(',') @ 'units'):
            return None
        Roman = REPLACE(Roman(n),'IVXLCDM','XLCDM**') + units
    print(Roman(1))
    print(Roman(4))
    print(Roman(5))
    print(Roman(9))
    print(Roman(10))
#------------------------------------------------------------------------------
# BALEXP = NOTANY(' ( ) , ) I ' (' ARBNO( *BALEXP) ')'
# BAL BALEXP ARBNO(BALEXP)
# ALLBAL = BAL S OUTPUT FAIL
#------------------------------------------------------------------------------
@pattern
def Bal(): yield from POS(0) + BAL() @ 'OUTPUT' + RPOS(0)
assert False is MATCH("", Bal())
assert False is MATCH(")A+B(", Bal())
assert False is MATCH("A+B)", Bal())
assert False is MATCH("(A+B", Bal())
assert True  is MATCH("(A+B)", Bal())
assert True  is MATCH("A+B()", Bal())
assert True  is MATCH("A()+B", Bal())
assert False is MATCH("A+B())", Bal())
assert False is MATCH("((A+B)", Bal())
assert True  is MATCH("X", Bal())
assert True  is MATCH("XYZ", Bal())
assert True  is MATCH("(A+B)", Bal())
assert True  is MATCH("A(B*C) (E/F)G+H", Bal())
assert True  is MATCH("( (A+ ( B*C) ) +D)", Bal())
assert True  is MATCH("(0+(1*9))", Bal())
assert True  is MATCH("((A+(B*C))+D)", Bal())
#------------------------------------------------------------------------------
@pattern
def Arb(): yield from POS(0) + ARB() @ 'OUTPUT' + RPOS(0)
assert True is MATCH("", Arb())
assert True is MATCH("$", Arb())
assert True is MATCH("$$", Arb())
assert True is MATCH("$$$", Arb())
#------------------------------------------------------------------------------
@pattern
def Pairs(): yield from POS(0) + ARBNO('AA' | LEN(2) | 'XX') + RPOS(0)
assert False is MATCH('CCXXAA$', Pairs())
#------------------------------------------------------------------------------
@pattern
def PAIRS(): yield from \
    (
        AT('pos') + λ(lambda: write('POS try', pos))
    +   POS(0)
    +   λ(lambda: write('POS got'))
    +   ARBNO(
          (AT('pos') + λ(lambda: write('AA try', pos))     + σ('AA') @ 'tx' + λ(lambda: write(tx, 'got')))
        | (AT('pos') + λ(lambda: write('LEN(2) try', pos)) + LEN(2)  @ 'tx' + λ(lambda: write(tx, 'got')))
        | (AT('pos') + λ(lambda: write('XX try', pos))     + σ('XX') @ 'tx' + λ(lambda: write(tx, 'got')))
        )
    +   AT('pos') + λ(lambda: wrrite('RPOS try', pos))
    +   RPOS(0)
    +   λ(lambda: write('RPOS got'))
    )
# assert False is MATCH('CCXXAA$', PAIRS())
#------------------------------------------------------------------------------

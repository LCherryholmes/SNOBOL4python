# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, _UCASE, _LCASE, _digits, MATCH, SEQ, ALT
from SNOBOL4python import ε, _, ANY, ARBNO, FENCE, POS, RPOS, SPAN
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
def real_number():
    yield from \
        (   POS(0)
        +   (   (   SPAN(_digits) @ 'whole'
                +   (_('.') + FENCE(SPAN(_digits) | ε()) @ 'fract' | ε())
                +   (_('E') | _('e'))
                +   (_('+') | _('-') | ε())
                +   SPAN(_digits) @ 'exp'
                )
            |   (   SPAN(_digits) @ 'whole'
                +   _('.')
                +   FENCE(SPAN(_digits) | ε()) @ 'fract'
                )
            )
        +   RPOS(0)
        )
assert True is MATCH("12.99E+3", real_number());
variable = None
for variable in globals().items():
    print(variable)
#print(f"whole={whole} fract={fract} exp={exp}")
#------------------------------------------------------------------------------
def test_one():
    yield from \
     SEQ(   POS(0)
        ,ALT(_('B') , _('F') , _('L') , _('R')) @ '1'
        ,ALT(_('E') , _('EA')) @ '2'
        ,ALT(_('D') , _('DS')) @ '3'
        ,   RPOS(0)
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
def As():
    yield from \
        (   POS(0)
        +   ARBNO(_('a')) @ 'sequence'
        +   RPOS(0)
        )
assert True is MATCH("", As())
assert True is MATCH("a", As())
assert True is MATCH("aa", As())
assert True is MATCH("aaa", As())
assert True is MATCH("aaaa", As())
#------------------------------------------------------------------------------
def Alist():
    yield from \
        (   POS(0)
        +   (_('a') | _('b'))
        +   ARBNO(_(',') + (_('a') | _('b')))
        +   RPOS(0)
        )
assert False is MATCH("", Alist())
assert True is MATCH("a", Alist())
assert True is MATCH("a,a", Alist())
assert True is MATCH("a,a,a", Alist())
assert True is MATCH("a,a,a,a", Alist())
#------------------------------------------------------------------------------
if False:
    units = None
    romanXlat = '0,1I,2II,3III,4IV,5V,6VI,7VII,8VIII,9IX,'
    def Roman(n):
        # Get rightmost digit to units and remove it from n
        # Return null result if argument is null
        if True is REPLACE(n, RPOS(1) + LEN(1) @ 'units', ''):
            units = results['units']
        else: return ""
        # Search for digit, replace with its Roman form.
        # Return failing if not a digit.
        if True is MATCH(units, BREAK(',') @ 'units'):
            units = results['units']
        else: return None
        # Convert rest of n and multiply by 10.
        # Propagate a failure return from recursive call back to caller
        Roman = REPLACE(Roman(n),'IVXLCDM','XLCDM**') + units
        print(Roman(1))
        print(Roman(4))
        print(Roman(5))
        print(Roman(9))
        print(Roman(10))
#------------------------------------------------------------------------------
# BAL
# "X"
# "XYZ"
# "(A+B)"
# "A(B*C) (E/F)G+H"
# BALEXP = NOTANY(' ( ) , ) I ' (' ARBNO( *BALEXP) ')'
# BAL BALEXP ARBNO(BALEXP)
# ALLBAL = BAL S OUTPUT FAIL
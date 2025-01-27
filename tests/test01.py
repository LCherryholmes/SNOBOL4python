# -*- coding: utf-8 -*-
import SNOBOL4python
#------------------------------------------------------------------------------
@pattern
def identifier():
    yield from \
        (   POS(0)
        +   ANY(_UCASE + _LCASE)
        +   FENCE(SPAN("." + digits + _UCASE + "_" + _LCASE) | ε())
        +   RPOS(0)
        )
#------------------------------------------------------------------------------
def real_number():
    yield from \
        (   POS(0)
        +   (   (   SPAN(digits) @ 'whole'
                +   (_('.') + FENCE(SPAN(digits) | ε()) @ 'fract' | ε())
                +   (_('E') | _('e'))
                +   (_('+') | _('-') | ε())
                +   SPAN(digits) @ 'exp'
                )
            |   (   SPAN(digits) @ 'whole'
                +   _('.')
                +   FENCE(SPAN(digits) | ε()) @ 'fract'
                )
            )
        +   RPOS(0)
        )
#------------------------------------------------------------------------------
def test_one():
    yield from \
     SEQ(   POS(0)
        ,ALT(_('B') , _('F') , _('L') , _('R')) @ '1'
        ,ALT(_('E') , _('EA')) @ '2'
        ,ALT(_('D') , _('DS')) @ '3'
        ,   RPOS(0)
        )
#------------------------------------------------------------------------------
assert True is MATCH("Id_99", identifier())
assert True is MATCH("12.99E+3", real_number())
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

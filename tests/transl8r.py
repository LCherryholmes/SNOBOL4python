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
#from transl8r_yaml import *
#-------------------------------------------------------------------------------
@pattern
def μ():                yield from  FENCE(SPAN(" \t\r\f") | ε())
@pattern
def ς(s):               yield from  μ() + σ(s)
@pattern
def inboxDOW():         yield from \
                        ( ς('Mon') | ς('Tue') | ς('Wed') | ς('Thu')
                        | ς('Fri') | ς('Sat') | ς('Sun')
                        )
@pattern
def inboxMonth():       yield from \
                        ( ς('Jan') | ς('Feb') | ς('Mar') | ς('Apr')
                        | ς('May') | ς('Jun') | ς('Jul') | ς('Aug')
                        | ς('Sep') | ς('Oct') | ς('Nov') | ς('Dec')
                        )
@pattern
def inboxDOM():         yield from SPAN(_DIGITS)
@pattern
def inboxTime():        yield from \
                        ( ANY(_DIGITS) + ANY(_DIGITS) + σ(':') 
                        + ANY(_DIGITS) + ANY(_DIGITS) + σ(':')
                        + ANY(_DIGITS) + ANY(_DIGITS) 
                        )
@pattern
def inboxYear():        yield from \
                        ANY(_DIGITS) + ANY(_DIGITS) + ANY(_DIGITS) + ANY(_DIGITS)
@pattern
def inboxFrom():        yield from \
                        ( ς('From - ') + inboxDOW() 
                        + ς(' ') + inboxMonth()
                        + ς(' ') + inboxDOM()
                        + ς(' ') + inboxTime()
                        + ς(' ') + inboxYear()
                        )
#-------------------------------------------------------------------------------
@pattern
def inboxLine():
    yield from  \
    ( POS(0)                        + Λ("""P = "yield from (\\n\"""")
    + ARBNO(
        θ("OUTPUT") +
        ( σ('\\\n')                 + Λ("""P += "σ('\\\n') + \"""")
        | σ('\n')                   + Λ("""P += "η() +\\n\"""") 
        | SPAN(" ") % "tx"          + Λ("""P += "ς('" + tx + "') + \"""")
        | SPAN("\t\r\f")            + Λ("""P += "μ() + \"""")
        | inboxFrom()               + Λ("""P += "inboxFrom() + \"""")
        | ( NOTANY(" \t\r\f\n")
          + BREAK(" \t\r\f\n")
          ) % "tx"                  + Λ("""P += "ς('" + tx + "') + \"""")
        | SPAN(_DIGITS)             + Λ("""P += "SPAN(_DIGITS) + \"""")
        | SPAN(_UCASE)              + Λ("""P += "SPAN(_UCASE) + \"""")
        | SPAN(_LCASE)              + Λ("""P += "SPAN(_LCASE) + \"""")
        | NOTANY(_DIGITS+_UCASE+_LCASE) % "tx"
                                    + Λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) # @ "OUTPUT"
      )
    + RPOS(0)                       + Λ("""P += "'')\\n\"""")
    )
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    yamlInput_nm = r"""C:/Users/lcher/.conda/pkgs/python-3.12.3-h2628c8c_0_cpython/info/recipe/meta.yaml"""
    inbox_nm = "C:/Users/lcher/AppData/Local/Packages/MozillaThunderbird.MZLA_h5892qc0xkpca" \
                "/LocalCache/Roaming/Thunderbird/Profiles/nsn6odxd.default-esr" \
               "/Mail/pop.mail.yahoo.com/Inbox"
    pyOutput_nm = r"""./inbox-pop3.py"""
    GLOBALS(globals())
    inbox = ""
    lineno = 0
    with open(inbox_nm, "r") as inboxInput:
        while line := inboxInput.readline():
            if lineno < 100:
                inbox += line
                lineno += 1
            else: break
    if MATCH(inbox, inboxLine()):
        with open(pyOutput_nm, "w", encoding="utf-8") as pyOutput:
            pyOutput.write(P)
#-------------------------------------------------------------------------------

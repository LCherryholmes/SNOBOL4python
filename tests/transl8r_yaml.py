# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
#-------------------------------------------------------------------------------
@pattern
def blanks():           yield from  σ('\\\n') | SPAN(" \t\r\f")
@pattern
def white():            yield from  σ('\\\n') | SPAN(" \t\r\f\n")
@pattern
def hashStyleComment(): yield from  σ('#') + BREAK("\n") + σ('\n')
@pattern
def space():            yield from  (   blanks()
                                    |   hashStyleComment()
                                    ) + FENCE(space() | ε())
@pattern
def whitespace():       yield from  (   white()
                                    |   hashStyleComment()
                                    ) + FENCE(whitespace() | ε())
#-------------------------------------------------------------------------------
@pattern
def μ():                yield from  FENCE(space() | ε())
@pattern
def η():                yield from  FENCE(whitespace() | ε())
@pattern
def ς(s):               yield from  η() + σ(s)
#-------------------------------------------------------------------------------
@pattern
def operator():         yield from  ( σ(':') | σ('-')
                                    )
#-------------------------------------------------------------------------------
@pattern
def identifier():       yield from  ( ANY(_UCASE + '_' + _LCASE) 
                                    + FENCE(SPAN(_DIGITS + _UCASE + '_' + _LCASE) | ε())
                                    ) % "tx"
#-------------------------------------------------------------------------------
@pattern
def escapedCharacter(): yield from  ( σ('\\')
                                    + (  ANY('"\\abfnrtv\n' + "'")
                                      |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                                      |  ANY('0123') + ANY('01234567') + ANY('01234567')
                                      |  ANY('Xx') + SPAN('0123456789ABCDEFabcdef')
                                      )
                                    )
@pattern
def stringLiteral():    yield from  σ("'") + BREAK("'") + σ('"')
#-------------------------------------------------------------------------------
@pattern
def yamlTokens():
    yield from  ( POS(0)                    + Λ("""P = "yield from (\\n\"""")
                                            + Λ("""Q = set()""")
                + ARBNO(
                    θ("OUTPUT") +
                    ( σ('\\\n')             + Λ("""P += "σ('\\\n') + \"""")
                    | σ('\n')               + Λ("""P += "η() +\\n\"""") 
                    | SPAN(" \t\r\f\n")     + Λ("""P += "η() +\\n\"""")
                    | SPAN(" \t\r\f")       + Λ("""P += "μ() + \"""") # currently unreachable
                    | hashStyleComment()    + Λ("""P += "hashStyleComment() + \"""")
                    | stringLiteral()       + Λ("""P += "stringLiteral() + \"""")
                    | identifier() + σ(':') + Λ("""P += "ς('" + tx + "') + σ(':') + \"""")
                                            + Λ("""Q.add(tx)""")
                    | identifier()          + Λ("""P += "identifier() + \"""")
                    | operator() % "tx"     + Λ("""P += "ς('" + tx + "') + \"""")
                    | SPAN(_DIGITS)         + Λ("""P += "SPAN(_DIGITS) + \"""")
                    | SPAN(_UCASE)          + Λ("""P += "SPAN(_UCASE) + \"""")
                    | SPAN(_LCASE)          + Λ("""P += "SPAN(_LCASE) + \"""")
                    | ANY(_ALPHABET) % "tx" + Λ("""P += "ς('" + tx + "') + \"""")
                    ) @ "OUTPUT"
                  )
                + RPOS(0)                   + Λ("""P += ")\\n\"""")
                )
#-------------------------------------------------------------------------------

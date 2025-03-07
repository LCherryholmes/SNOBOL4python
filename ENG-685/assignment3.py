# -*- coding: utf-8 -*-
# ENG 685, Lon Jones Cherryholmes, VBG Exercise
from SNOBOL4python import GLOBALS, REPLACE, pattern
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, Σ, Π, λ, Λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, BREAK
from SNOBOL4python import FENCE, LEN, POS, RPOS, SPAN
#------------------------------------------------------------------------------
@pattern
def delim():    yield from  SPAN(" \n")
#------------------------------------------------------------------------------
@pattern
def word():     yield from  BREAK('( )')
#------------------------------------------------------------------------------
@pattern
def tag():      yield from  BREAK('( )') @ "OUTPUT" % "tag"
#------------------------------------------------------------------------------
@pattern
def group():    yield from  ( σ('(') @ "OUTPUT"
                            + tag() @ "OUTPUT"
                            + ARBNO(
                                delim() @ "OUTPUT"
                              + ( group() @ "OUTPUT"
                                | word() @ "OUTPUT"
                                )
                              )
                            + σ(')') @ "OUTPUT"
                            )
#------------------------------------------------------------------------------
GLOBALS(globals())
with open("VBGinTASA.txt", "r") as trees_file:
    trees_source = trees_file.read()
    if trees_source in (POS(0) + BAL() + RPOS(0)):
        print("Balanced!")
    if trees_source in (POS(0) + σ('(') + BAL() % "sentence_source"  + σ(')')):
        sentence_source = "(" + sentence_source + ")"
        print(sentence_source)
        if sentence_source in (POS(0) + group()):
            print("\nYeah!")

# -*- coding: utf-8 -*-
# ENG 685, Lon Cherryholmes Sr., VBG Exercise
from pprint import pprint
from SNOBOL4python import GLOBALS, REPLACE, pattern
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, Σ, Π, λ, Λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, BREAK
from SNOBOL4python import FENCE, LEN, POS, RPOS, SPAN
from SNOBOL4python import nPush, nPop, nInc, Shift, Reduce
#------------------------------------------------------------------------------
@pattern
def delim():    yield from  SPAN(" \n")
#------------------------------------------------------------------------------
@pattern
def word():     yield from  BREAK('( )\n')
#------------------------------------------------------------------------------
@pattern
def group():    yield from  ( σ('(')
                            + nPush()
                            + word() % "tx" + Shift("tag", "tx") + nInc()
                            + Λ("count_tag(tx)")
                            + ARBNO(
                                delim() 
                              + ( group()
                                | word() % "tx" + Shift("word", "tx")
                                ) + nInc()
                              )
                            + Reduce('Part')
                            + nPop()
                            + σ(')')
                            )
#------------------------------------------------------------------------------
@pattern
def groups():   yield from  ( POS(0)
                            + Λ("tags = dict()")
                            + nPush()
                            + ARBNO(
                                nPush()
                              + ARBNO(group() + nInc())
                              + delim()
                              + Reduce('Sentence')
                              + nPop()
                              + nInc()
                              )
                            + Reduce('Sentences')
                            + nPop()
                            + RPOS(0)
                            )
#------------------------------------------------------------------------------
def count_tag(tag):
    if tag not in tags:
        tags[tag] = 0
    else: tags[tag] += 1
#------------------------------------------------------------------------------
GLOBALS(globals())
with open("VBGinTASA.txt", "r") as trees_file:
    trees_source = trees_file.read()
    if trees_source in (POS(0) + BAL() + RPOS(0)):
        print("Balanced!")
    if trees_source in groups():
        print("Yeah!")
        print(tags)
        sentences_tree = vstack.pop()
        pprint(sentences_tree)
    else: print("Boo!")

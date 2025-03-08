# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
from pprint import pprint
from SNOBOL4python import GLOBALS, REPLACE, pattern
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, Σ, Π, λ, Λ
from SNOBOL4python import ANY, ARB, ARBNO, BAL, BREAK
from SNOBOL4python import FENCE, LEN, NOTANY, POS, RPOS, SPAN
#------------------------------------------------------------------------------
@pattern
def delim(): yield from SPAN(" \n")
#------------------------------------------------------------------------------
@pattern
def word(): yield from NOTANY("( )\n") + BREAK("( )\n")
#------------------------------------------------------------------------------
@pattern
def group():
    yield from  ( σ('(')
                + word() % "tag"
                + Λ("count_tag(tag)")
                + Λ("stack.append(list())")
                + Λ("stack[-1].append(tag)")
                + ARBNO(
                    delim() 
                  + ( group()
                    | word() % "word" + Λ("stack[-1].append(word)")
                    )
                  )
                + Λ("top = stack.pop()")
                + Λ("if len(stack) == 0: bank = top")
                + Λ("if len(stack) > 0: stack[-1].append(top)")
                + σ(')')
                )
#------------------------------------------------------------------------------
@pattern
def groups():
    yield from  ( POS(0)
                + Λ("tags = dict()")
                + Λ("bank = None")
                + Λ("stack = []")
                + ARBNO(ARBNO(group()) + delim())
                + RPOS(0)
                )
#------------------------------------------------------------------------------
def count_tag(tag):
    if tag not in tags:
        tags[tag] = 1
    else: tags[tag] += 1
#------------------------------------------------------------------------------
GLOBALS(globals())
"""(S (S (NP (NN none)) (ADVP (RB ever)) (VP (VBN penned) (NP (DT a) (NN
manifesto)) (PP (IN as) (S (VP (VBG stirring) (PP (IN as) (NP (NP (DT the)
(NN one)) (SBAR (WHNP (WDT that)) (S (VP (VBD appeared) (PP (IN in) (NP (NP
(DT the) (JJ first) (NN issue)) (PP (IN of) (NP (DT the) (NN
liberator))))))))))))))) (, ,) (CC and) (S (NP (DT no) (JJ other) (NN
abolitionist) (NN document)) (VP (VBZ is) (ADVP (RB so) (RB well)) (VP (VBN
remembered)))) (.  .))
""" in groups()
pprint(bank, indent=2)
print()
pprint(tags, indent=2)
exit()
#------------------------------------------------------------------------------
with open("VBGinTASA.txt", "r") as trees_file:
    trees_source = trees_file.read()
    if trees_source in (POS(0) + BAL() + RPOS(0)):
        print("Balanced!")
    if trees_source in groups():
        print("Yeah!")
        print(tags)
        print(bank)
    else: print("Boo!")
#------------------------------------------------------------------------------

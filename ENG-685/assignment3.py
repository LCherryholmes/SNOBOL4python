# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, λ, Λ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
#------------------------------------------------------------------------------
@pattern
def init_list(v):
    yield from Λ(f"{v} = None") \
             + Λ(f"tags = dict()") \
             + Λ(f"stack = []")
@pattern
def push_list(v):
    yield from Λ(f"count_tag({v})") \
             + Λ(f"stack.append(list())") \
             + Λ(f"stack[-1].append({v})")
@pattern
def push_item(v):
    yield from Λ(f"stack[-1].append({v})")
@pattern
def pop_list():
    yield from Λ(f"stack[-2].append(stack.pop())")
@pattern
def pop_final(v):
    yield from Λ(f"{v} = stack.pop()")
#------------------------------------------------------------------------------
@pattern
def delim(): yield from SPAN(" \n")
@pattern
def word(): yield from NOTANY("( )\n") + BREAK("( )\n")
#------------------------------------------------------------------------------
@pattern
def group():
    yield from  ( σ('(')
                + word() % "tag"
                + push_list("tag")
                + ARBNO(
                    delim()
                  + (group() | word() % "word" + push_item("word"))
                  )
                + pop_list()
                + σ(')')
                )
#------------------------------------------------------------------------------
@pattern
def groups(): yield from push_list("'ROOT'") + ARBNO(group()) + pop_list()
#------------------------------------------------------------------------------
@pattern
def treebank():
    yield from  ( POS(0)
                + init_list("bank")
                + push_list("'BANK'")
                + ARBNO(groups() + delim())
                + pop_final("bank")
                + RPOS(0)
                )
#------------------------------------------------------------------------------
def count_tag(tag):
    if tag not in tags:
        tags[tag] = 1
    else: tags[tag] += 1
#------------------------------------------------------------------------------
GLOBALS(globals())
#------------------------------------------------------------------------------
sentence = """She was hiking."""            # progressive participles
sentence = """She loves hiking."""          # deverbal nouns (aka gerunds)
sentence = """This homework is exciting.""" # deverbal adjectives
sentence = """These are hiking boots."""    # deverbal undecidables
#------------------------------------------------------------------------------
with open("VBGinTASA.txt", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
        print("Balanced!")
        if bank_source in treebank():
            print("Yeah!")
            print(); pprint(tags, indent=2, width=80)
            print(); pprint(bank, indent=2, width=80)
    else: print("Boo!")
#------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, λ, Λ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
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
@pattern
def init_list(v):   yield from Λ(f"{v} = None") \
                             + Λ(f"tags = dict()") \
                             + Λ(f"stack = []")
@pattern
def push_list(v):   yield from Λ(f"count_tag({v})") \
                             + Λ(f"stack.append(list())") \
                             + Λ(f"stack[-1].append({v})")
@pattern
def push_item(v):   yield from Λ(f"stack[-1].append({v})")
@pattern
def pop_list():     yield from Λ(f"stack[-2].append(stack.pop())")
@pattern
def pop_final(v):   yield from Λ(f"{v} = stack.pop()")
#------------------------------------------------------------------------------
def count_tag(tag):
    if tag not in tags:
        tags[tag] = 1
    else: tags[tag] += 1
#------------------------------------------------------------------------------
GLOBALS(globals())
#------------------------------------------------------------------------------
roots = list()
def traverse(t, root=None):
    root = t if not root else root
    match t:
        case ['VBG', word]: roots.append(root)
        case _:
            for c in t:
                if type(c) == list: traverse(c, root) 
#------------------------------------------------------------------------------
def sentence(t):
    t, *children = t
    t = ""
    for c in children:
        if type(c) == str: t += ' ' + c
        if type(c) == list: t += sentence(c) 
    return t
#------------------------------------------------------------------------------
# Progressive
# Expresses ongoing action. Always with an auxiliary (e.g., am, is, are).
# Part of the predicate. Typically adverbs.
# Uses auxiliary (helping) verbs like "be" (am, is, are, was, were, been, being).
"She was hiking." # progressive participles
"I am writing a report." # present progressive: am/is/are + writing
"I was writing a report when the phone rang." # past progressive: was/were + writing
"I will be writing a report at 9 PM." # future progressive: will be + writing
"I have been writing reports all day." # present perfect progressive: have/has been + writing
"I had been writing a report before the meeting started." # past perfect progressive: had been + writing
"By next week, I will have been writing my thesis for three months." # future perfect progressive: will have been + writing
#------------------------------------------------------------------------------
def classify(t, parent=None):
    if type(t) == list:
        match t:
            case ['VBP', 'am']:         None
            case ['VBZ', 'is']:         None
            case ['VBP', 'are']:        None
            case ['VBD', 'was'|'were']: None
            case ['VB',  'be']:         None
            case ['VBN', 'been']:       None
            case _:
                for c in t:
                    classify(c, t) 
#------------------------------------------------------------------------------
# Gerund, deverbal nouns
# Acts as a noun. Stand-alone; no auxiliaries. Subject, object, complement.
# Modified by adjectives;
# may take determiners in nominalized compound noun phrases
"Writing is fun."
"She loves hiking."
#------------------------------------------------------------------------------
# Adjectival Participle, deverbal adjectives
# Qualifies/modifies a noun. Stand-alone; directly attached to a noun.
# Attributive (before/after a noun).
# Functions like adjectives and can sometimes be preceded by intensifiers.
"The writing style is unique."
"This homework is exciting."
#------------------------------------------------------------------------------
# Undecidable Participle, deverbal undecidables
# Ambiguous—shares features of both. No auxiliary; ambiguity in usage.
# Varies by context. Relies on broader syntactic context.
"I like reading."
"These are hiking boots."
#------------------------------------------------------------------------------
with open("VBGinTASA.txt", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
        if bank_source in treebank():
            print('#', tags['VBG'])
            for root in bank:
                traverse(root)
            print('#', len(roots))
            for root in roots:
#               print('#' + '-' * 79)
#               print('#', sentence(root)[1:])
#               pprint(root)
                classify(root)
    else: print("Boo!")
#------------------------------------------------------------------------------

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
        case ('VBG', word): roots.append(root)
        case _:
            for c in t:
                if type(c) == tuple:
                    traverse(c, root) 
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
def classify(t, phrase, parent=None):
    if type(t) == str: print([phrase, t])
    elif type(t) == tuple:
        match t:
            case ():                                    return
            case ('S', *rest) if phrase == None:        classify(tuple(rest), 'S', t)
            case ('NP', *rest) if phrase == None:       classify(tuple(rest), 'NP', t)
            case ('VP', *rest) if phrase == None:       classify(tuple(rest), 'VP', t)
            case ('VBG', w):                            pprint([phrase, t])
            case ('VB',  'be'):                         pprint([phrase, t])
            case ('VBZ', 'is'):                         pprint([phrase, t])
            case ('VBP', 'am'|'are'):                   pprint([phrase, t])
            case ('VBD', 'was'|'were'):                 pprint([phrase, t])
            case ('VBN', 'been'):                       pprint([phrase, t])
            case (('VBZ', 'is'), ('VP', ('VBG', w)), *rest):
                                                        print("<<<YIPPER>>>>")
                                                        pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (('VBP', 'am'|'are'), ('VP', ('VBG', w)), *rest):
                                                        print("<<<YIPPER>>>>")
                                                        pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (('VBD', 'was'|'were'), ('VP', ('VBG', w)), *rest):
                                                        print("<<<YIPPER>>>>")
                                                        pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (tag, w) if type(tag) == str \
                          and type(w) == str:           None # pprint([phrase, t])
            case ((tag, q), ('VBN', 'been'), ('VBG', w), *rest):
                                                        pprint((phrase, tag, q, 'been', w))
                                                        classify(tuple(rest), phrase, parent)
            case (('VB',  'be'), ('VBG', w), *rest):    pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (('VBD', 'was'), ('VBG', w), *rest):   pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (('VBD', 'were'), ('VBG', w), *rest):  pprint([phrase, t]); classify(tuple(rest), phrase, parent)
            case (tag, *rest) if type(tag) == str:      classify(tuple(rest), phrase, parent)
            case (top, *rest):                          classify(top, phrase, parent); \
                                                        classify(tuple(rest), phrase, parent)
    elif type(t) == list: raise Exception(f"What's going on! {type(t)} {t}")
    else: raise Exception(f"Yikes! {type(t)} {t}")
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
def list_to_tuple(t):
    if type(t) == list:
        return tuple(list_to_tuple(c) for c in t)
    else: return t
#------------------------------------------------------------------------------
with open("VBGinTASA.txt", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
        print("Parsing...")
        if bank_source in treebank():
            bank = list_to_tuple(bank)
            print('#', tags['VBG'])
            print("Searching...")
            for root in bank:
                traverse(root)
            roots = list_to_tuple(roots)
            print('#', len(roots))
            print("Clasifying...")
            for root in roots:
                print('#' + '-' * 79)
#               print('#', sentence(root)[1:])
#               pprint(root)
                classify(tuple(root), None)
    else: print("Boo!")
#------------------------------------------------------------------------------

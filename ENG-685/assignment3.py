# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, pattern, ε, σ, λ, Λ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
#------------------------------------------------------------------------------
from pprint import pprint
from pprint import PrettyPrinter
ppr = PrettyPrinter(indent=2, width=80)
#------------------------------------------------------------------------------
@pattern
def delim(): yield from SPAN(" \n")
@pattern
def word(): yield from NOTANY("( )\n") + BREAK("( )\n")
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
@pattern
def groups(): yield from push_list("'ROOT'") + ARBNO(group()) + pop_list()
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
roots = dict()
def traverse(t, root=None):
    root = t if not root else root
    match t:
        case ('VBG', word):
            if root not in roots:
                roots[root] = 1
            else: roots[root] += 1
        case _:
            for c in t:
                if type(c) == tuple:
                    traverse(c, root) 
#------------------------------------------------------------------------------
display = ""
def sentence(t):
    global display
    t, *children = t
    for c in children:
        if type(c) == str:
            if display == "":
                if c == "``":        display += "`"
                else:                display += c.capitalize()
            elif c == "``":          display += " `"
            elif c == "''":          display += "'"
            elif c == "'s":          display += "'s"
            elif c in ".;!?,":       display += c
            elif display[-1] == "`": display += c
            else:                    display += ' ' + c
        if type(c) == tuple: sentence(c) 
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
    global pp
    if type(t) == str: print([phrase, type(t), t])
    elif type(t) == tuple:
        match t:
            case ():                                    return
#           --------------------------------------------------------------------
            case ('S', *rem) if phrase == None: classify(tuple(rem), 'S', t)
            case ('NP', *rem) if phrase in (None, 'S', 'VP'): classify(tuple(rem), 'NP', t)
            case ('VP', *rem) if phrase in (None, 'S', 'NP'): classify(tuple(rem), 'VP', t)
            case ('VBG', 'being'):              ppr.pprint([phrase, t]); ppr.pprint(parent)
            case ('VBG',  w):                   ppr.pprint([phrase, t]); ppr.pprint(parent)
#           --------------------------------------------------------------------
            case ('NP', ('DT', dt), ('VBG', vbg), *np) if len(np) == 0:
                 ppr.pprint([phrase, dt, vbg, len(np)])
#           --------------------------------------------------------------------
            case ('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('NP', *np), *vp):
                 ppr.pprint([phrase, vbg1, cc, vbg2, len(np), len(vp)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('PP', *pp), *vp):
                 ppr.pprint([phrase, vbg1, cc, vbg2, len(pp), len(vp)])
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('NP', *np), *vp):
                 ppr.pprint([phrase, vbg, len(np), len(vp)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('PP', *pp), *vp):
                 ppr.pprint([phrase, vbg, len(pp), len(vp)])
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('``', '``'), ('VBG', vbg), ("''", "''"), ('PP', *pp), *vp):
                 ppr.pprint([phrase, vbg, len(pp), len(vp)])
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('VP', *vp1), *vp2):
                 ppr.pprint([phrase, vbg, len(vp1), len(vp2)])
                 classify(tuple(vp1), phrase, parent)
                 classify(tuple(vp2), phrase, parent)
            case ('VP', ('VBG', vbg), *vp) if len(vp) == 0:
                 ppr.pprint([phrase, vbg, len(vp)])
            case ('VP', ('VBG', vbg), ('ADJP', *adjp), *vp):
                 ppr.pprint([phrase, vbg, len(adjp), len(vp)])
                 classify(tuple(adjp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('ADVP', *advp), *vp):
                 ppr.pprint([phrase, vbg, len(advp), len(vp)])
                 classify(tuple(advp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
#           --------------------------------------------------------------------
            case ('PP', ('VBG', vbg), ('NP', *np), *pp):
                 ppr.pprint([phrase, vbg, len(np), len(pp)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(pp), phrase, parent)
            case ('ADJP', *adjp, ('VBG', vbg)):
                 ppr.pprint([phrase, len(adjp), vbg])
                 classify(tuple(adjp), phrase, parent)
#           --------------------------------------------------------------------
            case ('VP', ('ADVP', *advp), ('VBG', vbg), *vp) if len(vp) == 0:
                 ppr.pprint([phrase, advp, vbg, len(vp)])
                 classify(tuple(advp), phrase, parent)
            case ('PP', ('IN', _in), ('NP', ('VBG', vbg), *np), *pp) \
              if len(np) == 0 and len(pp) == 0:
                 ppr.pprint([phrase, _in, vbg, len(np), len(pp)])
            case ('VP', ('VBG', vbg), ('PRT', *prt), *vp):
                 ppr.pprint([phrase, vbg, len(prt), len(vp)])
                 classify(tuple(prt), phrase, parent)
                 classify(tuple(vp), phrase, parent)
#           --------------------------------------------------------------------
            case (('VB',  'be'),   ('VBG', vbg), *rem): ppr.pprint([phrase, t]); classify(tuple(rem), phrase, parent)
            case (('VBD', 'was'),  ('VBG', vbg), *rem): ppr.pprint([phrase, t]); classify(tuple(rem), phrase, parent)
            case (('VBD', 'were'), ('VBG', vbg), *rem): ppr.pprint([phrase, t]); classify(tuple(rem), phrase, parent)
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), *vp), *rem):
                 ppr.pprint([phrase, vbg, len(vp), len(rem)])
                 print("<<<1. progressive participle>>>") # 9 matches, 1 questionable ('ranching')
                 ppr.pprint(parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBP', 'am'|'are'), ('VP', ('VBG', vbg), *vp), *rem):
                 ppr.pprint([phrase, vbg, len(vp), len(rem)])
                 print("<<<1. progressive participle>>>") # 14 matches
                 ppr.pprint(parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBD', 'was'|'were'), ('VP', ('VBG', vbg), *vp), *rem):
                 ppr.pprint([phrase, vbg, len(vp), len(rem)])
                 print("<<<1. progressive participle>>>") # 11 matches
                 ppr.pprint(parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case ( ('VBZ'|'VB'|'VBP'|'VBD', 'has'|'have'|'had')
                 , ('VP'
                   , ('VBN', 'been')
                   , ('VP', ('VBG', vbg), *rem1)
                   , *rem2
                   )
                 , *rem3
                 ):
                 ppr.pprint([phrase, vbg, len(rem1), len(rem2), len(rem3)])
                 print("<<<1. progressive participle>>>") # 5 matches
                 ppr.pprint(parent)
                 classify(tuple(rem1), phrase, parent)
                 classify(tuple(rem2), phrase, parent)
                 classify(tuple(rem3), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('NN'|'NNS', nn), *rem):
                 ppr.pprint([phrase, vbg, nn, len(rem)])
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('CD', cd), ('NN'|'NNS', nn), *rem):
                 ppr.pprint([phrase, vbg, cd, nn, len(rem)])
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('PRT', *prt), *rem):
                 ppr.pprint([phrase, vbg, len(prt), len(rem)])
                 classify(tuple(prt), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('NP', ('DT', dt), *np), *rem):
                 ppr.pprint([phrase, vbg, dt, len(np), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('PRP$', prp), *np), *rem):
                 ppr.pprint([phrase, vbg, prp, len(np), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *rem):
                 ppr.pprint([phrase, vbg, nn, len(np1), len(np2), len(rem)])
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('NP', ('DT', dt), *np1), *np2), *rem):
                 ppr.pprint([phrase, vbg, dt, len(np1), len(np2), len(rem)])
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', *np), *rem):
                 ppr.pprint([phrase, vbg, len(np), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ("''", "''"), ('NP', ('NN'|'NNS', nn), *np), *rem):
                 ppr.pprint([phrase, vbg, nn, len(np), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('``', '``'), ('VBG', vbg), ("''", "''"), ('NP', *np), *rem):
                 ppr.pprint([phrase, vbg, len(np), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('PP', ('IN'|'TO', ppx), *pp), *rem):
                 ppr.pprint([phrase, vbg, ppx, len(pp), len(rem)])
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('JJ', jj), ('NN'|'NNS', nn), *rem):
                 ppr.pprint([phrase, vbg, jj, nn, len(rem)])
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('S', ('NP', *np), *s), *rem):
                 ppr.pprint([phrase, vbg, len(np), len(s), len(rem)])
                 classify(tuple(np), phrase, parent)
                 classify(tuple(s), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('S', ('VP', ('TO', *to), *vp), *s), *rem):
                 ppr.pprint([phrase, vbg, to, len(vp), len(s), len(rem)])
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(s), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('SBAR', *sbar), *rem):
                 ppr.pprint([phrase, vbg, len(sbar), len(rem)])
                 classify(tuple(sbar), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (tag, w) \
              if type(tag) == str and type(w) == str:   None # ppr.pprint([phrase, t])
            case (tag, *rem) if type(tag) == str:       classify(tuple(rem), phrase, parent)
            case (top, *rem):                           classify(top, phrase, parent); \
                                                        classify(tuple(rem), phrase, parent)
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
GLOBALS(globals())
with open("VBGinTASA.dat", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
#       print("Parsing...")
        if bank_source in treebank():
            bank = list_to_tuple(bank)
#           print("# all tags"); ppr.pprint(tags)
#           print('# tree banks=', len(bank))
#           print('# VBG tags=', tags['VBG'])
#           print("Searching...")
            for root in bank:
                traverse(root)
#           print('# roots=', len(roots))
#           print("Clasifying...")
            n = 0
            for root in roots:
#               print('#' + '=' * 79)
#               print()
                n += 1
                display = ""
                sentence(root)
                print(str(n) + ":", display)
#               print('#' + '-' * 79)
#               ppr.pprint(root, width=80)
#               print('#' + '-' * 79)
#               classify(tuple(root), None)
    else: print("Boo!")
#------------------------------------------------------------------------------

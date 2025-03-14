# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, pattern, ε, σ, λ, Λ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ANY, ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
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
                  + (group() | word() % "wrd" + push_item("wrd"))
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
def pop_list():     yield from Λ(f"stack[-2].append(tuple(stack.pop()))")
@pattern
def pop_final(v):   yield from Λ(f"{v} = tuple(stack.pop())")
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
        case ('VBG', wrd):
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
versus = dict()
def register(ruleno, vbg, *args):
    if rootno in mem:
        if vbg in mem[rootno]:
            keys = list(mem[rootno][vbg].keys())
            assert(len(keys) == 1)
            tag = keys[0]
            if ruleno not in versus:                versus[ruleno] = dict()
            if tag    not in versus[ruleno]:        versus[ruleno][tag] = dict()
            if vbg    not in versus[ruleno][tag]:   versus[ruleno][tag][vbg] = set()
            versus[ruleno][tag][vbg].add(rootno)
            ppr.pprint([ruleno, vbg, tag, *args])
        else: ppr.pprint([ruleno, vbg, None, *args])
#------------------------------------------------------------------------------
def classify(t, phrase, parent=None):
    if type(t) == str: print([phrase, type(t), t])
    elif type(t) == tuple:
        match t:
            case (): return
#           --------------------------------------------------------------------
            case ('S', *rem)  if phrase == None:              classify(tuple(rem), 'S', t)
            case ('NP', *rem) if phrase in (None, 'S', 'VP'): classify(tuple(rem), 'NP', t)
            case ('VP', *rem) if phrase in (None, 'S', 'NP'): classify(tuple(rem), 'VP', t)
            case ('VBG', 'being'):  register(1, 'being', phrase, t); ppr.pprint(root)
            case ('VBG',  vbg):     register(2, vbg, phrase, t);     ppr.pprint(root)
#           --------------------------------------------------------------------
            case ('NP', ('DT', dt), ('VBG', vbg), *np) if len(np) == 0:
                 register(3, vbg, phrase, dt, vbg, len(np)) # NN1
#           --------------------------------------------------------------------
            case (('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('NP', *np), *vp), *rem):
                 register(4, vbg1, phrase, cc, len(np), len(vp)) # NN1
                 register(4, vbg2, phrase, cc, len(np), len(vp)) # NN1
                 classify(tuple(np), phrase, parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('PP', *pp), *vp), *rem):
                 register(5, vbg1, phrase, cc, len(pp), len(vp)) # NN1
                 register(5, vbg2, phrase, cc, len(pp), len(vp)) # NN1
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *np3), *vp):
                 register(6.3, vbg, phrase, nn, len(np1), len(np2), len(np3), len(vp))
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(np3), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *vp):
                 register(6.2, vbg, phrase, nn, len(np1), len(np2), len(vp))
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('NP', ('NN'|'NNS', nn), *np), *vp):
                 register(6.1, vbg, phrase, nn, np, len(vp))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('NP', *np), *vp):
                 register(6, vbg, phrase, np, len(vp))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('PP', *pp), *vp):
                 register(7, vbg, phrase, len(pp), len(vp))
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('VP', *vp1), *vp2):
                 register(8, vbg, phrase, len(vp1), len(vp2))
                 classify(tuple(vp1), phrase, parent)
                 classify(tuple(vp2), phrase, parent)
            case ('VP', ('VBG', vbg), *vp) if len(vp) == 0:
                 register(9, vbg, phrase, len(vp))
            case ('VP', ('VBG', vbg), ('ADJP', *adjp), *vp):
                 register(10, vbg, phrase, len(adjp), len(vp))
                 classify(tuple(adjp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
            case ('VP', ('VBG', vbg), ('ADVP', *advp), *vp):
                 register(11, vbg, phrase, len(advp), len(vp))
                 classify(tuple(advp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
#           --------------------------------------------------------------------
            case ('PP', ('VBG', vbg), ('NP', *np), *pp):
                 register(12, vbg, phrase, len(np), len(pp))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(pp), phrase, parent)
            case ('ADJP', *adjp, ('VBG', vbg)):
                 register(13, vbg, phrase, len(adjp), vbg)
                 classify(tuple(adjp), phrase, parent)
#           --------------------------------------------------------------------
            case ('VP', ('ADVP', *advp), ('VBG', vbg), *vp) if len(vp) == 0:
                 register(14, vbg, phrase, advp, len(vp))
                 classify(tuple(advp), phrase, parent)
            case ('PP', ('IN', _in), ('NP', ('VBG', vbg), *np), *pp) \
              if len(np) == 0 and len(pp) == 0:
                 register(15, vbg, phrase, _in, len(np), len(pp))
            case ('VP', ('VBG', vbg), ('PRT', *prt), *vp):
                 register(16, vbg, phrase, len(prt), len(vp))
                 classify(tuple(prt), phrase, parent)
                 classify(tuple(vp), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), *vp), *rem):
                 register(17, vbg, phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBP', 'am'|'are'), ('VP', ('VBG', vbg), *vp), *rem):
                 register(18, vbg, phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBD', 'was'|'were'), ('VP', ('VBG', vbg), *vp), *rem):
                 register(19, vbg, phrase, len(vp), len(rem))
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
                 register(20, vbg, phrase, len(rem1), len(rem2), len(rem3))
                 classify(tuple(rem1), phrase, parent)
                 classify(tuple(rem2), phrase, parent)
                 classify(tuple(rem3), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('NN'|'NNS', nn), *rem):
                 register(21, vbg, phrase, nn, len(rem))
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('CD', cd), ('NN'|'NNS', nn), *rem):
                 register(22, vbg, phrase, cd, nn, len(rem))
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('PRT', *prt), *rem):
                 register(23, vbg, phrase, len(prt), len(rem))
                 classify(tuple(prt), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('NP', ('DT', dt), *np), *rem):
                 register(24, vbg, phrase, dt, len(np), len(rem))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('PRP$', prp), *np), *rem):
                 register(25, vbg, phrase, prp, len(np), len(rem))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *rem):
                 register(26, vbg, phrase, nn, len(np1), len(np2), len(rem))
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', ('NP', ('DT', dt), *np1), *np2), *rem):
                 register(27, vbg, phrase, dt, len(np1), len(np2), len(rem))
                 classify(tuple(np1), phrase, parent)
                 classify(tuple(np2), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('NP', *np), *rem):
                 register(28, vbg, phrase, len(np), len(rem))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('PP', ('IN'|'TO', ppx), *pp), *rem):
                 register(29, vbg, phrase, ppx, len(pp), len(rem))
                 classify(tuple(pp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('JJ', jj), ('NN'|'NNS', nn), *rem):
                 register(30, vbg, phrase, jj, nn, len(rem))
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('S', ('NP', *np), *s), *rem):
                 register(31, vbg, phrase, len(np), len(s), len(rem))
                 classify(tuple(np), phrase, parent)
                 classify(tuple(s), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('S', ('VP', ('TO', *to), *vp), *s), *rem):
                 register(32, vbg, phrase, to, len(vp), len(s), len(rem))
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(s), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VBG', vbg), ('SBAR', *sbar), *rem):
                 register(33, vbg, phrase, len(sbar), len(rem))
                 classify(tuple(sbar), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VP', ('VBG', vbg), ('ADVP', *advp), *vp), *rem):
                 register(34, vbg, phrase, len(advp), len(vp), len(rem))
                 classify(tuple(advp), phrase, parent)
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
            case (('VP', ('VBG', 'doing'), *vp), *rem) \
              if len(vp) == 0: # VDG
                 register(35, 'doing', phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase, parent)
                 classify(tuple(rem), phrase, parent)
#           --------------------------------------------------------------------
            case (tag, w) \
              if type(tag) == str and type(w) == str:   None # register(w, phrase, t)
            case (tag, *rem) if type(tag) == str:       classify(tuple(rem), phrase, parent)
            case (top, *rem):                           classify(top, phrase, parent); \
                                                        classify(tuple(rem), phrase, parent)
    elif type(t) == list: raise Exception(f"What's going on! {type(t)} {t}")
    else: raise Exception(f"Yikes! {type(t)} {t}")
#------------------------------------------------------------------------------
def list_to_tuple(t):
    if type(t) == list:
        return tuple(list_to_tuple(c) for c in t)
    else: return t
#------------------------------------------------------------------------------
# VBG, -ing form of the verb "BE", i.e. BEING
# VDG, -ing form of the verb "DO", i.e. DOING
# VHG, -ing form of the verb "HAVE", i.e. HAVING
# VVG, -ing form of lexical verb (e.g. TAKING, LIVING)
# AJ0, adjective (unmarked) (e.g. GOOD, OLD)
# NN1, singular noun (e.g. PENCIL, GOOSE) beginning, grouping
# VVB, base form of lexical verb (except the infinitive)(e.g. TAKE, LIVE) flooding
# PRP, preposition (except for OF) (e.g. FOR, ABOVE, TO) including
#------------------------------------------------------------------------------
@pattern
def claws_info():
    yield from  ( POS(0)
                + Λ("mem = dict()")
                + ARBNO(
                    ( SPAN(_DIGITS) % "num" + σ('_CRD :_PUN')
                    + Λ("num = int(num)")
                    + Λ("mem[num] = dict()")
                    | (NOTANY("_\n") + BREAK("_\n")) % "wrd"
                    + σ('_')
                    + (ANY(_UCASE) + SPAN(_DIGITS+_UCASE)) % "tag"
                    + Λ("if wrd not in mem[num]:      mem[num][wrd] = dict()")
                    + Λ("if tag not in mem[num][wrd]: mem[num][wrd][tag] = 0")
                    + Λ("mem[num][wrd][tag] += 1")
                    )
                  + σ(' ')
                  )
                + RPOS(0)
                )
#------------------------------------------------------------------------------
GLOBALS(globals())
with open("CLAWS5inTASA.dat", "r") as claws_file:
    lines = []
    while line := claws_file.readline():
        lines.append(line[0:-1])
    claws_data = ''.join(lines)
    if not claws_data in claws_info():
        print("Yikes")
#------------------------------------------------------------------------------
with open("VBGinTASA.dat", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
        if bank_source in treebank():
#           bank = list_to_tuple(bank)
            for root in bank:
                traverse(root)
            rootno = 0
            for root in roots:
                rootno += 1
                print('#', '=' * 79)
                display = ""
                sentence(root)
                print(f"# {str(rootno)}:")
                ppr.pprint(display)
                print('#', '-' * 79)
                classify(root, None)
    else: print("Boo!")
#------------------------------------------------------------------------------
pprint(versus, width=56)
# -*- coding: utf-8 -*-
# ENG 685, VBG Exercise, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, PrettyPrinter
ppr = PrettyPrinter(indent=2, width=80)
#------------------------------------------------------------------------------
def init_list(v): return λ(f"{v} = None") + λ(f"tags = dict()") + λ(f"stack = []")
def push_list(v): return λ(f"count_tag({v})") + λ(f"stack.append(list())") + λ(f"stack[-1].append({v})")
def push_item(v): return λ(f"stack[-1].append({v})")
def pop_list():   return λ(f"stack[-2].append(tuple(stack.pop()))")
def pop_final(v): return λ(f"{v} = tuple(stack.pop())")
#------------------------------------------------------------------------------
delim       =   SPAN(" \n")
word        =   NOTANY("( )\n") + BREAK("( )\n")
group       =   ( σ('(')
                + word % "tag"
                + push_list("tag")
                + ARBNO(
                    delim
                  + ( ζ('group')
                    | word % "wrd" + push_item("wrd")
                    )
                  )
                + pop_list()
                + σ(')')
                )
treebank    =   ( POS(0)
                + init_list("bank")
                + push_list("'BANK'")
                + ARBNO(
                    push_list("'ROOT'")
                  + ARBNO(ζ('group'))
                  + pop_list()
                  + delim
                  )
                + pop_final("bank")
                + RPOS(0)
                )
#------------------------------------------------------------------------------
def count_tag(tag):
    if tag not in tags:
        tags[tag] = 1
    else: tags[tag] += 1
#------------------------------------------------------------------------------
roots = dict()
def traverse(t, root=None):
    global roots
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
def register(ruleno, subtree, vbg, *args):
    global versus
    if rootno in mem:
        if vbg in mem[rootno]:
            keys = list(mem[rootno][vbg].keys())
            assert(len(keys) == 1)
            tag = keys[0]
            if ruleno not in versus:                versus[ruleno] = dict()
            if tag    not in versus[ruleno]:        versus[ruleno][tag] = dict()
            if vbg    not in versus[ruleno][tag]:   versus[ruleno][tag][vbg] = set()
            versus[ruleno][tag][vbg].add(rootno)
            ppr.pprint([ruleno, vbg, tag, *args, subtree])
        else: ppr.pprint([ruleno, vbg, None, *args, subtree])
#------------------------------------------------------------------------------
def classify(t, phrase):
    global root
    if type(t) == str: print([phrase, type(t), t])
    elif type(t) == tuple:
        match t:
            case (): return
#           --------------------------------------------------------------------
            case ('S', *rem)  if phrase == None:              classify(tuple(rem), 'S')
            case ('NP', *rem) if phrase in (None, 'S', 'VP'): classify(tuple(rem), 'NP')
            case ('VP', *rem) if phrase in (None, 'S', 'NP'): classify(tuple(rem), 'VP')
            case ('VBG', 'being'):  pass # register(1, t, 'being', phrase, t); ppr.pprint(root)
            case ('VBG',  vbg):     pass # register(2, t, vbg, phrase, t);     ppr.pprint(root)
#           --------------------------------------------------------------------
            case ('NP', ('DT', dt), ('VBG', vbg), *np) if len(np) == 0:
                 register(3, t, vbg, phrase, dt, vbg, len(np)) # NN1
#           --------------------------------------------------------------------
            case (('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('NP', *np), *vp), *rem):
                 register(4, t, vbg1, phrase, cc, len(np), len(vp)) # VVG
                 register(4, t, vbg2, phrase, cc, len(np), len(vp)) # VVG
                 classify(tuple(np), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case (('VP', ('VBG', vbg1), ('CC', cc), ('VBG', vbg2), ('PP', *pp), *vp), *rem):
                 register(5, t, vbg1, phrase, cc, len(pp), len(vp)) # VVG
                 register(5, t, vbg2, phrase, cc, len(pp), len(vp)) # VVG
                 classify(tuple(pp), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *np3), *vp):
                 register(6.2, t, vbg, phrase, nn, len(np1), len(np2), len(np3), len(vp))
                 classify(tuple(np1), phrase)
                 classify(tuple(np2), phrase)
                 classify(tuple(np3), phrase)
                 classify(tuple(vp), phrase)
                 # ('VP', ('VBG', 'cutting'), ('NP', ('NP', ('NNS', 'workers'), ('POS', "'"))))
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), ('POS', "'"), *np1), *np2), *vp):
                 register(6.13, t, vbg, phrase, nn, len(np1), len(np2), len(vp))
                 classify(tuple(np1), phrase)
                 classify(tuple(np2), phrase)
                 classify(tuple(vp), phrase)
                 # ('S', ('VP', ('VBG', 'determining'), ('NP', ('NP', ('NNS', 'patterns')), ('PP', *))))
                 #       ('VP', ('VBG', 'determining'), ('NP', ('NP', ('NNS', 'patterns'))))
                 # ('S', ('VP', ('VBG', 'studying'),    ('NP', ('NP', ('NNS', 'people')), ('VP', *))))
                 #       ('VP', ('VBG', 'studying'),    ('NP', ('NP', ('NNS', 'people'))))
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), ('PP', *pp)), *vp):
                 register(6.12, t, vbg, phrase, nn, len(np1), len(pp), len(vp))
                 classify(tuple(np1), phrase)
                 classify(tuple(pp), phrase)
                 classify(tuple(vp), phrase)
            case ('VP', ('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), ('VP', *vp1)), *vp2):
                 register(6.11, t, vbg, phrase, nn, len(np1), len(vp1), len(vp2))
                 classify(tuple(np1), phrase)
                 classify(tuple(vp1), phrase)
                 classify(tuple(vp2), phrase)
            case ('VP', ('VBG', vbg), ('NP', ('NN'|'NNS', nn), *np), *vp):
                 register(6.0, t, vbg, phrase, nn, len(np), len(vp))
                 classify(tuple(np), phrase)
                 classify(tuple(vp), phrase)
            case ('VP', ('VBG', vbg), ('NP', *np), *vp):
                 if vbg == "having":
                    register(7.2, t, vbg, phrase, len(np), len(vp))
                 elif vbg == "including":
                    register(7.1, t, vbg, phrase, len(np), len(vp))
                 else: register(7.0, t, vbg, phrase, len(np), len(vp))
                 classify(tuple(np), phrase)
                 classify(tuple(vp), phrase)
            case ('VP', ('VBG', vbg), ('VP', *vp1), *vp2):
                 register(8, t, vbg, phrase, len(vp1), len(vp2))
                 classify(tuple(vp1), phrase)
                 classify(tuple(vp2), phrase)
            case ('VP', ('VBG', vbg), ('ADJP', *adjp), *vp):
                 if vbg == "being":
                    register(9.2, t, vbg, phrase, len(adjp), len(vp))
                 else: register(9.1, t, vbg, phrase, len(adjp), len(vp))
                 classify(tuple(adjp), phrase)
                 classify(tuple(vp), phrase)
#           --------------------------------------------------------------------
            case ('PP', ('VBG', vbg), ('NP', *np), *pp):
                 register(10, t, vbg, phrase, len(np), len(pp))
                 classify(tuple(np), phrase)
                 classify(tuple(pp), phrase)
            case ('ADJP', *adjp, ('VBG', vbg)):
                 register(11, t, vbg, phrase, len(adjp), vbg)
                 classify(tuple(adjp), phrase)
#           --------------------------------------------------------------------
            case ('VP', ('ADVP', *advp), ('VBG', vbg), *vp) if len(vp) == 0:
                 register(12, t, vbg, phrase, advp, len(vp))
                 classify(tuple(advp), phrase)
            case ('PP', ('IN', _in), ('NP', ('VBG', vbg), *np), *pp) \
              if len(np) == 0 and len(pp) == 0:
                 register(13, t, vbg, phrase, _in, len(np), len(pp))
            case ('VP', ('VBG', vbg), ('PRT', *prt), *vp):
                 register(14, t, vbg, phrase, len(prt), len(vp))
                 classify(tuple(prt), phrase)
                 classify(tuple(vp), phrase)
#           --------------------------------------------------------------------
            # ('S', ('NP', *np), ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'gaining'), ('NP'))))
            # ('S', ('NP', *np), ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'suffering'), ('PP'))))
            # ('S', ('NP', *np), ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'drowning')
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), ('NP', *np), *vp), *rem):
                 register(15.3, t, vbg, phrase, len(np), len(vp), len(rem))
                 classify(tuple(np), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), ('PP', *pp), *vp), *rem):
                 register(15.2, t, vbg, phrase, len(pp), len(vp), len(rem))
                 classify(tuple(pp), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            # ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'helping'), ('S', *s)))
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), ('S', *s), *vp), *rem):
                 register(15.12, t, vbg, phrase, len(s), len(vp), len(rem))
                 classify(tuple(s), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            # ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'gaining'),
            # ('VP', ('VBZ', 'is'), ('VP', ('VBG', 'drowning')))
            case (('VBZ', 'is'), ('VP', ('VBG', vbg), *vp), *rem):
                 register(15.11, t, vbg, phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
#           --------------------------------------------------------------------
            case (('VBP', 'am'|'are'), ('VP', ('VBG', vbg), *vp), *rem):
                 register(16, t, vbg, phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case (('VBD', 'was'|'were'), ('VP', ('VBG', vbg), *vp), *rem):
                 if vbg == "doing":
                    register(17.2, t, vbg, phrase, len(vp), len(rem))
                 else: register(17.1, t, vbg, phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case ( ('VBZ'|'VB'|'VBP'|'VBD', 'has'|'have'|'had')
                 , ('VP'
                   , ('VBN', 'been')
                   , ('VP', ('VBG', vbg), *rem1)
                   , *rem2
                   )
                 , *rem3
                 ):
                 register(18, t, vbg, phrase, len(rem1), len(rem2), len(rem3))
                 classify(tuple(rem1), phrase)
                 classify(tuple(rem2), phrase)
                 classify(tuple(rem3), phrase)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('CD', cd), ('NN'|'NNS', nn), *rem):
                 register(19, t, vbg, phrase, cd, nn, len(rem))
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('PRT', *prt), *rem):
                 register(20, t, vbg, phrase, len(prt), len(rem))
                 classify(tuple(prt), phrase)
                 classify(tuple(rem), phrase)
#           --------------------------------------------------------------------
            case (('VBG', vbg), ('NP', ('DT', dt), *np), *rem):
                 if vbg == "having":
                    register(21.2, t, vbg, phrase, dt, len(np), len(rem))
                 else: register(21.1, t, vbg, phrase, dt, len(np), len(rem))
                 classify(tuple(np), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('NP', ('PRP$', prp), *np), *rem):
                 register(22, t, vbg, phrase, prp, len(np), len(rem))
                 classify(tuple(np), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('NP', ('NP', ('NN'|'NNS', nn), *np1), *np2), *rem):
                 register(23, t, vbg, phrase, nn, len(np1), len(np2), len(rem))
                 classify(tuple(np1), phrase)
                 classify(tuple(np2), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('NP', ('NP', ('DT', dt), *np1), *np2), *rem):
                 if vbg == "being":
                    register(24.2, t, vbg, phrase, dt, len(np1), len(np2), len(rem))
                 else: register(24.1, t, vbg, phrase, dt, len(np1), len(np2), len(rem))
                 classify(tuple(np1), phrase)
                 classify(tuple(np2), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('NP', *np), *rem):
                 if vbg == "having":
                    register(25.2, t, vbg, phrase, len(np), len(rem))
                 else: register(25.1, t, vbg, phrase, len(np), len(rem))
                 classify(tuple(np), phrase)
                 classify(tuple(rem), phrase)
#           --------------------------------------------------------------------
            case ('NP', ('VBG', vbg), ('JJ', jj), ('NN'|'NNS', nn), *np):
                 register(26.1, t, vbg, phrase, jj, nn, len(np))
                 classify(tuple(np), phrase)
            case (('VBG', vbg), ('JJ', jj), ('NN'|'NNS', nn), *rem):
                 register(26.0, t, vbg, phrase, jj, nn, len(rem))
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('S', ('NP', *np), *s), *rem):
                 if vbg == "having":
                    register(27.1, t, vbg, phrase, len(np), len(s), len(rem))
                 else: register(27.0, t, vbg, phrase, len(np), len(s), len(rem))
                 classify(tuple(np), phrase)
                 classify(tuple(s), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('S', ('VP', ('TO', *to), *vp), *s), *rem):
                 if vbg == "having":
                    register(28.1, t, vbg, phrase, to, len(vp), len(s), len(rem))
                 else: register(28.0, t, vbg, phrase, to, len(vp), len(s), len(rem))
                 classify(tuple(vp), phrase)
                 classify(tuple(s), phrase)
                 classify(tuple(rem), phrase)
            case (('VBG', vbg), ('SBAR', *sbar), *rem):
                 register(29, t, vbg, phrase, len(sbar), len(rem))
                 classify(tuple(sbar), phrase)
                 classify(tuple(rem), phrase)
            case (('VP', ('VBG', vbg), ('ADVP', *advp), *vp), *rem):
                 register(30, t, vbg, phrase, len(advp), len(vp), len(rem))
                 classify(tuple(advp), phrase)
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
            case (('VP', ('VBG', 'doing'), *vp), *rem) \
              if len(vp) == 0: # VDG
                 register(31, t, 'doing', phrase, len(vp), len(rem))
                 classify(tuple(vp), phrase)
                 classify(tuple(rem), phrase)
#           --------------------------------------------------------------------
            case (tag, w) \
              if type(tag) == str and type(w) == str:   None
            case (tag, *rem) if type(tag) == str:       classify(tuple(rem), phrase)
            case (top, *rem):                           classify(top, phrase); \
                                                        classify(tuple(rem), phrase)
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
claws_info = \
    ( POS(0)
    + λ("mem = dict()")
    + ARBNO(
        ( SPAN(DIGITS) % "num" + σ('_CRD :_PUN')
        + λ("num = int(num)")
        + λ("mem[num] = dict()")
        | (NOTANY("_") + BREAK("_")) % "wrd"
        + σ('_')
        + (ANY(UCASE) + SPAN(DIGITS+UCASE)) % "tag"
        + λ("if wrd not in mem[num]:      mem[num][wrd] = dict()")
        + λ("if tag not in mem[num][wrd]: mem[num][wrd][tag] = 0")
        + λ("mem[num][wrd][tag] += 1")
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
    if not claws_data in claws_info:
        print("Yikes")
#------------------------------------------------------------------------------
with open("VBGinTASA.dat", "r") as bank_file:
    bank_source = bank_file.read()
    if bank_source in POS(0) + BAL() + RPOS(0):
        if bank_source in treebank:
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
#pprint(tags)
pprint(versus, width=80)
#------------------------------------------------------------------------------

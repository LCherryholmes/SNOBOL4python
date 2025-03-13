# -*- coding: utf-8 -*-
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS, REPLACE
from SNOBOL4python import ANY, ARBNO, BAL, BREAK, LEN, NOTANY, POS
from SNOBOL4python import REM, RPOS, SPAN
#-------------------------------------------------------------------------------
hex2Dec = {
     '0': 0,  '1': 1,  '2': 2,  '3': 3,
     '4': 4,  '5': 5,  '6': 6,  '7': 7,
     '8': 8,  '9': 9,  'a': 10, 'b': 11,
     'c': 12, 'd': 13, 'e': 14, 'f': 15}
#-------------------------------------------------------------------------------
lineno = 0
def inc():
    global lineno
    if lineno % 10_000 == 0:
        print(lineno)
    lineno += 1
    return True
#-------------------------------------------------------------------------------
lexs = {"noun", "verb", "adj", "adv"}
lexicon = dict()
def enter(word, dict_type):
    global lexicon
    word = REPLACE(word, '_', ' ')
    if word in lexicon:
        if dict_type not in lexicon[word]:
            lexicon[word] += dict_type
    else: lexicon[word] = dict_type 
    return True
#-------------------------------------------------------------------------------
GLOBALS(globals())
for lex in lexs:
    file_name = "C:/nltk_data/corpora/wordnet2022/data." + lex
    print(f"Reading: {file_name}")
#   ----------------------------------------------------------------------------
    with open(file_name, "r", encoding="utf-8") as file:
        lex_info = file.read()
#       ------------------------------------------------------------------------
        print(f"Parsing ....")
        lineno = 0
        if lex_info in \
            ( POS(0)
            + ARBNO(
                σ('  ') + SPAN('0123456789')
              + σ(' ') + BREAK("\n")
              + λ(lambda: inc())
              + σ('\n')
              )
            + ARBNO(
                SPAN('0123456789')
              + σ(' ') + SPAN('0123456789')
              + σ(' ') + ANY('asrnv') # @ "dict_type"
              + σ(' ') + SPAN('0123456789abcdef') # @ "nhex"
              + σ(' ')
              + ARBNO(
                  BREAK(' (') @ "word" # + λ(lambda: enter(word, dict_type))
                + (σ(' ') | σ('(') + BREAK(')') + σ(') '))
                + SPAN('0123456789abcdef') + σ(' ')
                )
              + ANY('0123456789')
              + ANY('0123456789')
              + ANY('0123456789')
              + σ(' ')
              + BREAK("\n")
              + λ(lambda: inc())
              + σ('\n')
              )
            + RPOS(0)
            ):
            print("#" * 80)
#-------------------------------------------------------------------------------
pprint(lexicon)
#-------------------------------------------------------------------------------

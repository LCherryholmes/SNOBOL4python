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
GLOBALS(globals())
lexicon = dict()
lexs = {"noun", "verb", "adj", "adv"}
for lex in lexs:
    file_name = "C:/nltk_data/corpora/wordnet2022/data." + lex
    print(f"Reading: {file_name}")
    with open(file_name, "r") as file:
        line = file.readline()
        while line in (POS(0) + σ('  ') + SPAN('0123456789') + σ(' ')):
            line = file.readline()
        while line in   ( POS(0)
                        + SPAN('0123456789')
                        + σ(' ') + SPAN('0123456789')
                        + σ(' ') + ANY('asrnv') % "dict_type"
                        + σ(' ') + SPAN('0123456789abcdef') % "nhex"
                        + σ(' ') + REM() % "line"
                        + RPOS(0)
                        ):
#           --------------------------------------------------------------------
            n_entries = hex2Dec[nhex[0]] * 16 + hex2Dec[nhex[1]]
            for n in range(n_entries):
#               ----------------------------------------------------------------
                if line not in  ( POS(0)
                                + BREAK(' (') % "word"
                                + σ('(') + BREAK(')') + σ(') ')
                                + REM() % "line"
                                + RPOS(0)
                                ):
                    if line in  ( POS(0)
                                + BREAK(' (') % "word"
                                + σ(' ')
                                + REM() % "line"
                                + RPOS(0)
                                ):
#                       word = REPLACE(word, '_', ' ')
                        if word in lexicon:
                            if dict_type not in lexicon[word]:
                                lexicon[word] += dict_type
                        else: lexicon[word] = dict_type 
                        print(f'"{word}"={lexicon[word]}', end=" ")
#               ----------------------------------------------------------------
                if line not in  ( POS(0)
                                + SPAN('0123456789abcdef') + σ(' ')
                                + REM() % "line"
                                + RPOS(0)
                                ):
                    raise Exception("Never say never!")
#           --------------------------------------------------------------------
            line = file.readline()
#-------------------------------------------------------------------------------
pprint(lexicon)
#-------------------------------------------------------------------------------

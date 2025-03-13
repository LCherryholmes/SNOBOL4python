# -*- coding: utf-8 -*-
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS, REPLACE
from SNOBOL4python import ANY, ARBNO, BAL, BREAK, LEN, NOTANY, POS
from SNOBOL4python import REM, RPOS, SPAN
#-------------------------------------------------------------------------------
lineno = 0
def inc():
    global lineno
    lineno += 1
    if lineno % 10_000 == 0:
        print(lineno)
    return True
#-------------------------------------------------------------------------------
lexs = ("adv", "verb", "adj", "noun")
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
@pattern
def sno_wordnet():
    yield from  ( POS(0)
                + ARBNO( # header / license banner
                    σ('  ') + SPAN('0123456789')
                  + σ(' ') + BREAK("\n")
                  + λ(lambda: inc())
                  + σ('\n')
                  )
                + ARBNO( # data rows
                    SPAN('0123456789')
                  + σ(' ') + SPAN('0123456789')
                  + σ(' ') + ANY('asrnv') % "dict_type"
                  + σ(' ') + SPAN('0123456789abcdef') @ "nhex"
                  + σ(' ')
                  + ARBNO(
                      BREAK(' (') % "word" + Λ("enter(word, dict_type)")
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
                )
#-------------------------------------------------------------------------------
import re
re_word_id = re.compile(r" ([^ ]+) [0123456789abcdef]{1,2}")
re_wordnet = re.compile(
    r"^[0123456789]{8}"
    r" [0123456789]{2}"
    r" ([asrnv])"
    r" [0123456789abcdef]{2}"
    r"( [^ ]+ [0123456789abcdef]{1,2})+"
    r" [0123456789]{3}"
     "("
        r" (?:\$|\\|\+|\*|<|=|&|!|-c|-r|-u|#m|#p|#s|~i|%m|%p|%s|;c|;r|;u|~|@|@i|>|\^)"
        r" [0123456789]{8}"
        r" [anrsv]"
        r" [0123456789abcdef]{4}"
     ")*"
    r"( [0123456789]{2}( \+( [0123456789abcdef]{2})*)*)?"
    r" \| .*\n$"
)
#-------------------------------------------------------------------------------
for lex in lexs:
    file_name = "C:/nltk_data/corpora/wordnet2022/data." + lex
    print(f"Reading: {file_name}")
    with open(file_name, "r", encoding="utf-8") as file:
        lineno = 0
        while lineno < 30:
            line = file.readline()
            lineno += 1
        while line := file.readline():
            lineno += 1
            wordnet = re.fullmatch(re_wordnet, line)
            if wordnet:
                dict_type = wordnet.group(1)
                word_list = wordnet.group(2)
                for word_id in re.finditer(re_word_id, word_list):
                    word = word_id.group(1)
                    enter(word, dict_type)
            elif line != "\n":
                print(f'{lineno}: <<<{line}>>>')
                exit()
print(len(lexicon))
exit()
#-------------------------------------------------------------------------------
GLOBALS(globals())
for lex in lexs:
    file_name = "C:/nltk_data/corpora/wordnet2022/data." + lex
    print(f"Reading: {file_name}")
    with open(file_name, "r", encoding="utf-8") as file:
        lex_info = file.read()
        print(f"Parsing ....")
        lineno = 0
        if lex_info in sno_wordnet():
            print("#" * 80)
#-------------------------------------------------------------------------------

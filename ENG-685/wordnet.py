# -*- coding: utf-8 -*-
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS, REPLACE
from SNOBOL4python import ANY, ARBNO, BAL, BREAK, LEN, NOTANY, POS
from SNOBOL4python import REM, RPOS, RTAB, SPAN, TAB
#-------------------------------------------------------------------------------
lineno = 0
def inc():
    global lineno
    lineno += 1
    if lineno % 10_000 == 0:
        print(lineno)
    return True
#-------------------------------------------------------------------------------
lexicon = dict()
def enter(word, word_pos):
    global lexicon
    word = REPLACE(word, '_', ' ')
    if word in lexicon:
        if word_pos not in lexicon[word]:
            lexicon[word] += word_pos
    else: lexicon[word] = word_pos 
    return True
#-------------------------------------------------------------------------------
def is_pos(wrd, word_pos):
    if wrd in lexicon:
        return word_pos in lexicon[wrd]
    else: return False    
#-------------------------------------------------------------------------------
def is_noun(wrd):
    wrd = wrd.lower()
    if is_pos(wrd, 'n'): return True
    lemma = wrd        
    if lemma == "is": return False
    if lemma in ( POS(0)
                + ( RTAB(4) % "stem" + σ('ches') + Λ("lemma = stem + 'ch'")
                  | RTAB(4) % "stem" + σ('shes') + Λ("lemma = stem + 'sh'")
                  | RTAB(3) % "stem" + σ('ies')  + Λ("lemma = stem + 'y'")
                  | RTAB(3) % "stem" + σ('ses')  + Λ("lemma = stem + 's'")
                  | RTAB(3) % "stem" + σ('xes')  + Λ("lemma = stem + 'x'")
                  | RTAB(3) % "stem" + σ('zes')  + Λ("lemma = stem + 'z'")
                  | RTAB(3) % "stem" + σ('men')  + Λ("lemma = stem + 'man'")
                  | RTAB(1) % "stem" + σ('s')    + Λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return is_pos(lemma, 'n')
    if lemma in ( POS(0)
                + RTAB(3) % "stem" + σ('ing')  + Λ("lemma = stem")
                + RPOS(0)
                ):
        return is_pos(lemma, 'v') or is_pos(f"{lemma}e", 'v')
    return False
#-------------------------------------------------------------------------------
def is_verb(wrd):
    wrd = wrd.lower()
    if is_pos(wrd, 'v'): return True
    lemma = wrd        
    if lemma in ( POS(0)
                + ( RTAB(3) % "stem" + σ('ied') + Λ("lemma = stem + 'y'")
                  | RTAB(3) % "stem" + σ('ies') + Λ("lemma = stem + 'y'")
                  | RTAB(1) % "stem" + σ('s')   + Λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return is_pos(lemma, 'v')
    if lemma in ( POS(0)
                + ( RTAB(2) % "stem" + σ('es')  + Λ("lemma = stem")
                  | RTAB(2) % "stem" + σ('ed')  + Λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return is_pos(lemma, 'v') or is_pos(f"{lemma}e", 'v')
    return False
#-------------------------------------------------------------------------------
def is_adjective(wrd):
    wrd = wrd.lower()
    if is_pos(wrd, 'a') or is_pos(wrd, 's'): return True
    lemma = wrd        
    if lemma in ( POS(0)
                + ( RTAB(3) % "stem" + σ('est') + Λ("lemma = stem")
                  | RTAB(2) % "stem" + σ('er')  + Λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return (  is_pos(lemma, 'a') or is_pos(f"{lemma}e", 'a')
               or is_pos(lemma, 's') or is_pos(f"{lemma}e", 's')
               )
    return False
#-------------------------------------------------------------------------------
def is_adverb(wrd):
    wrd = wrd.lower()
    return is_pos(wrd, 'r')
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
                  + σ(' ') + ANY('asrnv') % "word_pos"
                  + σ(' ') + SPAN('0123456789abcdef') @ "nhex"
                  + σ(' ')
                  + ARBNO(
                      BREAK(' (') % "word" + Λ("enter(word, word_pos)")
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
def Lexicon_sno():
    GLOBALS(globals())
    for lex in ("adv", "verb", "adj", "noun"):
        file_name = "C:/nltk_data/corpora/wordnet2022/data." + lex
        print(f"Reading: {file_name}")
        with open(file_name, "r", encoding="utf-8") as file:
            lex_info = file.read()
            print(f"Parsing ....")
            lineno = 0
            if lex_info in sno_wordnet():
                print("#" * 80)
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
def Lexicon():
    for lex in ("adv", "verb", "adj", "noun"):
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
                    word_pos = wordnet.group(1)
                    word_list = wordnet.group(2)
                    for word_id in re.finditer(re_word_id, word_list):
                        word = word_id.group(1)
                        enter(word, word_pos)
                elif line != "\n":
                    print(f'{lineno}: <<<{line}>>>')
                    exit()
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    Lexicon()
    print(len(lexicon))

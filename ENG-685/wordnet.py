# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint
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
        for letter in word_pos:
            if letter not in lexicon[word]:
                lexicon[word].add(letter)
    else: lexicon[word] = {word_pos}
    return True
#-------------------------------------------------------------------------------
def pos(wrd):
    if wrd.lower() in lexicon:
        return "".join(lexicon[wrd.lower()]).upper()
    else: return None
#-------------------------------------------------------------------------------
def is_pos(wrd, word_pos):
    if wrd in lexicon:
        result = word_pos in lexicon[wrd]
    else: result = False
#   print('', wrd, word_pos, result, lexicon[wrd] if wrd in lexicon else "None", end="")
    return result
#-------------------------------------------------------------------------------
def is_noun(wrd):
    wrd = wrd.lower()
    if is_pos(wrd, 'n'): return True
    lemma = wrd        
    if lemma == "is": return False
    if lemma in ( POS(0)
                + ( RTAB(4) % "stem" + σ('ches') + λ("lemma = stem + 'ch'")
                  | RTAB(4) % "stem" + σ('shes') + λ("lemma = stem + 'sh'")
                  | RTAB(3) % "stem" + σ('ies')  + λ("lemma = stem + 'y'")
                  | RTAB(3) % "stem" + σ('ses')  + λ("lemma = stem + 's'")
                  | RTAB(3) % "stem" + σ('xes')  + λ("lemma = stem + 'x'")
                  | RTAB(3) % "stem" + σ('zes')  + λ("lemma = stem + 'z'")
                  | RTAB(3) % "stem" + σ('men')  + λ("lemma = stem + 'man'")
                  | RTAB(1) % "stem" + σ('s')    + λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return is_pos(lemma, 'n')
    if lemma in ( POS(0)
                + RTAB(3) % "stem" + σ('ing')  + λ("lemma = stem")
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
                + ( RTAB(3) % "stem" + σ('ied') + λ("lemma = stem + 'y'")
                  | RTAB(3) % "stem" + σ('ies') + λ("lemma = stem + 'y'")
                  | RTAB(1) % "stem" + σ('s')   + λ("lemma = stem")
                  )  
                + RPOS(0)
                ):
        return is_pos(lemma, 'v')
    if lemma in ( POS(0)
                + ( RTAB(2) % "stem" + σ('es')  + λ("lemma = stem")
                  | RTAB(2) % "stem" + σ('ed')  + λ("lemma = stem")
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
                + ( RTAB(3) % "stem" + σ('est') + λ("lemma = stem")
                  | RTAB(2) % "stem" + σ('er')  + λ("lemma = stem")
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
sno_wordnet =   ( POS(0)
                + ARBNO( # header / license banner
                    σ('  ') + SPAN('0123456789')
                  + σ(' ') + BREAK("\n")
                  + Λ(lambda: inc())
                  + σ('\n')
                  )
                + ARBNO( # data rows
                    SPAN('0123456789')
                  + σ(' ') + SPAN('0123456789')
                  + σ(' ') + ANY('asrnv') % "word_pos"
                  + σ(' ') + SPAN('0123456789abcdef') @ "nhex"
                  + σ(' ')
                  + ARBNO(
                      BREAK(' (') % "word" + λ("enter(word, word_pos)")
                    + (σ(' ') | σ('(') + BREAK(')') + σ(') '))
                    + SPAN('0123456789abcdef') + σ(' ')
                    )
                  + ANY('0123456789')
                  + ANY('0123456789')
                  + ANY('0123456789')
                  + σ(' ')
                  + BREAK("\n")
                  + Λ(lambda: inc())
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
            if lex_info in sno_wordnet:
                print("#" * 80)
#-------------------------------------------------------------------------------
import re
re_word_id = re.compile(r" ([^ ]+) [0123456789abcdef]{1,2}")
re_wordnet_data = re.compile(
    r"^[0123456789]{8}"
    r" [0123456789]{2}"
    r" ([asrnv])"
    r" [0123456789abcdef]{2}"
    r"(( [^ ]+ [0123456789abcdef]{1,2})+)"
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
re_wordnet_exc = re.compile(r"^([^ ]+) (.*)\n$")
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
                wordnet = re.fullmatch(re_wordnet_data, line)
                if wordnet:
                    word_pos = wordnet.group(1)
                    word_list = wordnet.group(2)
                    for word_id in re.finditer(re_word_id, word_list):
                        word = word_id.group(1)
                        enter(word, word_pos)
                elif line != "\n":
                    print(f'{lineno}: <<<{line}>>>')
                    exit()
        file_name = "C:/nltk_data/corpora/wordnet2022/" + lex + ".exc"
        print(f"Reading: {file_name}")
        with open(file_name, "r", encoding="utf-8") as file:
            lineno = 0
            while line := file.readline():
                lineno += 1
                wordnet = re.fullmatch(re_wordnet_exc, line)
                if wordnet:
                    word_exc = wordnet.group(1)
                    word_alias = wordnet.group(2)
                    if word_alias in lexicon:
                        enter(word_exc, "".join(lexicon[word_alias]))
                    else: print("Warning:", word_alias, word_exc)
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    Lexicon()
    print(len(lexicon))

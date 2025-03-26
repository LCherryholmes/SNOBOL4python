# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ, φ, Φ
from SNOBOL4python import ANY, ARB, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from pprint import pprint
#-------------------------------------------------------------------------------
import os
import sys
import cProfile
import pstats
sys.path.append(os.getcwd())
#from transl8r_y import *
#from transl8r_yaml import *
#from transl8r_pop3 import *
#from transl8r_english import *
#------------------------------------------------------------------------------
keywords = [
     None, 
    { "a", "I" },
    { "an", "as", "at", "be", "by", "do", "go", "he", "if", "in", "is", "it"
    , "me", "my", "no", "of", "on", "or", "so", "to", "up", "us", "we" },
    { "act", "all", "and", "any", "are", "big", "but", "can", "day", "did"
    , "end", "few", "for", "get", "had", "has", "her", "him", "his", "how"
    , "its", "let", "may", "new", "not", "now", "oil", "old", "one", "our"
    , "out", "own", "put", "run", "say", "see", "set", "she", "the", "too"
    , "try", "two", "use", "was", "way", "who", "win", "yes", "you" },
    { "also", "back", "been", "call", "come", "cost", "down", "each", "even"
    , "ever", "face", "feel", "find", "form", "from", "give", "good", "grow"
    , "hand", "have", "hear", "here", "high", "hold", "home", "hope", "into"
    , "just", "keep", "know", "last", "like", "live", "long", "look", "made"
    , "make", "many", "mean", "meet", "mind", "most", "move", "much", "need"
    , "next", "only", "open", "over", "part", "plan", "play", "same", "seem"
    , "show", "some", "stop", "take", "talk", "than", "that", "them", "then"
    , "they", "this", "time", "turn", "want", "well", "were", "what", "when"
    , "will", "with", "word", "work", "year", "your" },
    { "about", "after", "again", "begin", "break", "bring", "could", "every"
    , "first", "great", "large", "learn", "leave", "might", "other", "right"
    , "small", "stand", "still", "their", "there", "these", "think", "watch"
    , "water", "which", "while", "would", "write" },
    { "always", "change", "follow", "listen", "little", "number", "people"
    , "really", "reason", "result", "should" },
    { "another", "because", "believe", "between", "problem" },
    { "continue" },
    { "something" },
    { "experience", "understand" }
]
#-------------------------------------------------------------------------------
@pattern
def wrd():      yield from  (ANY(_UCASE+_LCASE) + FENCE(SPAN(_LCASE) | ε())) % "w"
@pattern
def word():     yield from  wrd() @ "tx" + λ(lambda: (len(tx) > 10) or (tx not in keywords[len(tx)]))
@pattern
def keyword():  yield from  wrd() @ "tx" + λ(lambda: (len(tx) <= 10) and (tx in keywords[len(tx)]))
#-------------------------------------------------------------------------------
@pattern
def eTokens():
    yield from  \
    ( POS(0)                    + Λ("""P = "(\\n\"""")
    + ARBNO(
#       θ("OUTPUT") +
        ( σ(' ')                + Λ("""P += "σ(' ') + \"""")
        | σ('\n')               + Λ("""P += "σ('\\\\n') +\\n\"""") 
        | keyword()             + Λ("""P += "ς('" + w + "') + \"""")
        | word()                + Λ("""P += "word() + \"""")
        | SPAN(_DIGITS)         + Λ("""P += "SPAN(_DIGITS) + \"""")
        | SPAN(_UCASE)          + Λ("""P += "SPAN(_UCASE) + \"""")
        | SPAN(_LCASE)          + Λ("""P += "SPAN(_LCASE) + \"""")
        | NOTANY(_DIGITS+_UCASE+_LCASE) % "tx" + Λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) # @ "OUTPUT"
      )
    + RPOS(0)                   + Λ("""P += ")\\n\"""")
    )
#-------------------------------------------------------------------------------
def traverse(tree):
#   pprint((tree.label, tree.depth(), tree.is_preterminal(), tree.is_leaf()))
    if tree.is_preterminal():
        if tree.label == '.' or tree.label == ',':
            print(tree.children[0].label, end="")
        else:
            word = tree.children[0].label
            if len(word) <= 10 and word in keywords[len(word)]:
                print(' ', word, end="")
            else: print(' ', tree.label, end="")
    else:
        for child in tree.children:
            traverse(child)
#-------------------------------------------------------------------------------
import stanza
def main():
    nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,constituency')
    eInput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.txt"
    eOutput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.out"
    with open(eInput_nm, "r", encoding="utf-8") as eInput:
        with open(eOutput_nm, "w", encoding="utf-8") as eOutput:
            while eSource := eInput.readline():
                sentence = eSource[0:-1]
                bank = nlp(sentence)
                for root in bank.sentences:
                    constituency = root.constituency
                    traverse(constituency)
                    print(); # print(' #', sentence)
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------

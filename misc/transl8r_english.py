# -*- coding: utf-8 -*-
# ENG 685, Universal Tokenizer, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#------------------------------------------------------------------------------
from pprint import pprint
from pprint import PrettyPrinter
#------------------------------------------------------------------------------
def ς(s): return σ(f" {s}")
#-------------------------------------------------------------------------------
wrd =           SPAN(UCASE+LCASE) # (ANY(UCASE+LCASE) + FENCE(SPAN(LCASE) | ε()))
word =          wrd @ "tx" + Λ(lambda: (len(tx) > 10) or (tx not in keywords[len(tx)]))
keyword =       wrd @ "tx" + Λ(lambda: (len(tx) <= 10) and (tx in keywords[len(tx)]))
#------------------------------------------------------------------------------
Noun =          (wrd @ "tx" + Λ(lambda: is_noun(tx))) @ "OUTPUT"
Verb =          (wrd @ "tx" + Λ(lambda: is_verb(tx))) @ "OUTPUT"
Adjective =     (wrd @ "tx" + Λ(lambda: is_adjective(tx))) @ "OUTPUT"
Adverb =        (wrd @ "tx" + Λ(lambda: is_adverb(tx))) @ "OUTPUT"
SentenceEnd =   (σ("." ) | σ("!" ) | σ("?")) @ "OUTPUT"
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
import wordnet
from wordnet import Lexicon, lexicon, pos
from wordnet import is_noun, is_verb, is_adjective, is_adverb
def eTokens(x): return \
    ( POS(0)                                        + λ(f'''{x} = []''')
    + ARBNO(
#       Θ("OUTPUT") +
        ( σ(' ')                                  # + λ(f'''{x}.append("σ(' ')")''')
        | σ('\n')                                 # + λ(f'''{x}.append("σ('\\\\n')\\n"''')
        | wrd @ "tx" % "tx" + Λ(lambda: pos(tx))    + λ(f'''{x}.append(pos(tx))''')
        | wrd % "tx"                                + λ(f'''{x}.append("ς('" + tx + "')")''')
        | wrd @ "tx" + Λ(lambda: is_noun(tx))       + λ(f'''{x}.append("noun")''')
        | wrd @ "tx" + Λ(lambda: is_verb(tx))       + λ(f'''{x}.append("verb")''')
        | wrd @ "tx" + Λ(lambda: is_adjective(tx))  + λ(f'''{x}.append("adj")''')
        | wrd @ "tx" + Λ(lambda: is_adverb(tx))     + λ(f'''{x}.append("adv")''')
        | keyword                                   + λ(f'''{x}.append("ς('" + w + "')")''')
        | word                                      + λ(f'''{x}.append("word")''')
        | SPAN(DIGITS)                              + λ(f'''{x}.append("SPAN(DIGITS)")''')
        | SPAN(UCASE)                               + λ(f'''{x}.append("SPAN(UCASE)")''')
        | SPAN(LCASE)                               + λ(f'''{x}.append("SPAN(LCASE)")''')
        | NOTANY(DIGITS+UCASE+LCASE) % "tx"         + λ(f'''{x}.append("σ('" + tx + "')")''')
        ) # @ "OUTPUT"
      )
    + RPOS(0)
    )
#-------------------------------------------------------------------------------
eOutput = None
def traverse(tree):
#   pprint((tree.label, tree.depth(), tree.is_preterminal(), tree.is_leaf()))
    if tree.is_preterminal():
        if tree.label == '.' or tree.label == ',':
            eOutput.write(tree.children[0].label)
        else:
            word = tree.children[0].label
            if len(word) <= 10 and word in keywords[len(word)]:
                eOutput.write(' ' + word)
            else: eOutput.write(' ' + tree.label)
    else:
        for child in tree.children:
            traverse(child)
#-------------------------------------------------------------------------------
import stanza
ITERATIONS = 200
def main():
    global eOutput
    nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,constituency')
    Lexicon()
    eInput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.txt"
    eOutput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english_out.py"
    iterations = 0
    with open(eInput_nm, "r", encoding="utf-8") as eInput:
        with open(eOutput_nm, "w", encoding="utf-8") as eOutput:
            ppr = PrettyPrinter(indent=2, width=80, stream=eOutput)
            while eSource := eInput.readline():
                iterations += 1
                if iterations > ITERATIONS: break
                sentence = eSource[0:-1]
                eOutput.write(f'''#{'-' * 80}\n''')
                eOutput.write(f'''"{sentence}" in ''')
                if sentence in eTokens('P'):
                    eOutput.write("POS(0) + " + " + ".join(P) + " + RPOS(0)")
#                   if sentence.lower() in POS(0) + Sentence() + RPOS(0):
#                       eOutput.write("Yeah!!!\n")
                    eOutput.write("\n")
                bank = nlp(sentence)
                for root in bank.sentences:
                    constituency = root.constituency
                    eOutput.write("#")
                    ppr.pprint(constituency)
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------

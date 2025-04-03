# -*- coding: utf-8 -*-
# ENG 685, Universal Tokenizer, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#------------------------------------------------------------------------------
from pprint import pprint
from pprint import PrettyPrinter
ppr = PrettyPrinter(indent=2, width=80)
#------------------------------------------------------------------------------
@pattern
def ς(s): yield from σ(f" {s}")
#------------------------------------------------------------------------------
@pattern
def Sentence():
    yield from                   ( DeclarativeSentence()
                                 | InterrogativeSentence()
                                 | ImperativeSentence()
                                 ) @ "OUTPUT"
@pattern
def DeclarativeSentence():
    yield from                   ( SimpleSentence()
                                 + ARBNO(Coordinator() + SimpleSentence())
                                 + (SubordinateClause() | ε())
                                 ) @ "OUTPUT"
@pattern
def SimpleSentence():
    yield from                   (NounPhrase() + VerbPhrase() + SentenceEnd()) @ "OUTPUT"
@pattern
def InterrogativeSentence():
    yield from                   (InterroWord() + SimpleSentence() + σ("?"))  @ "OUTPUT"
@pattern
def ImperativeSentence():
    yield from                   (VerbPhraseImperative() + SentenceEnd())  @ "OUTPUT"
@pattern
def SubordinateClause():
    yield from                   (Subordinator() + SimpleSentence()) @ "OUTPUT"
@pattern
def NounPhrase():
    yield from                   ( (Determiner() | ε())
                                 + ARBNO(Adjective())
                                 + Noun()
                                 + (RelativeClause() | ε())
                                 | ProperNoun() + (RelativeClause() | ε())
                                 | NounPhrase() + Conjunction() + NounPhrase()
                                 ) @ "OUTPUT"
@pattern
def RelativeClause():
    yield from                   (RelativePronoun() + VerbPhrase()) @ "OUTPUT"
@pattern
def VerbPhrase():
    yield from                   ( Verb()
                                 + (NounPhrase() | ε())
                                 + (AdverbPhrase() | ε())
                                 + (PrepositionalPhraseList() | ε())
                                 | ARBNO(Auxiliary())
                                 + Verb()
                                 + (NounPhrase() | ε())
                                 + (PrepositionalPhraseList() | ε())
                                 ) @ "OUTPUT"
@pattern
def VerbPhraseImperative():
    yield from                   ( Verb()
                                 + (NounPhrase() | ε())
                                 + (PrepositionalPhraseList() | ε())
                                 ) @ "OUTPUT"
@pattern
def AdverbPhrase():
    yield from                   (Adverb() + ARBNO(Adverb())) @ "OUTPUT"
@pattern
def PrepositionalPhraseList():
    yield from                   (PrepositionalPhrase() + ARBNO(PrepositionalPhrase())) @ "OUTPUT"
@pattern
def PrepositionalPhrase():
    yield from                   (Preposition() + NounPhrase()) @ "OUTPUT"
#------------------------------------------------------------------------------
@pattern
def Coordinator():      yield from  (ς("and") | ς("or") | ς("but")) @ "OUTPUT"
@pattern
def Conjunction():      yield from  (ς("and") | ς("or")) @ "OUTPUT"
@pattern
def Subordinator():     yield from  (ς("because") | ς("since") | ς("when") | ς("although")) @ "OUTPUT"
@pattern
def RelativePronoun():  yield from  (ς("who") | ς("whom") | ς("which") | ς("that")) @ "OUTPUT"
@pattern
def InterroWord():      yield from  (ς("what") | ς("who") | ς("where") | ς("when") | ς("why") | ς("how")) @ "OUTPUT"
@pattern
def Determiner():       yield from  (ς("the") | ς("a") | ς("an") | ς("this") | ς("that") | ς("these") | ς("those")) @ "OUTPUT"
@pattern
def Noun():             yield from  (wrd() @ "tx" + Λ(lambda: is_noun(tx))) @ "OUTPUT"
@pattern
def ProperNoun():       yield from  (ς("John") | ς("Mary") | ς("Paris") | ς("London") | ς("Alice")) @ "OUTPUT"
@pattern
def Verb():             yield from  (wrd() @ "tx" + Λ(lambda: is_verb(tx))) @ "OUTPUT"
@pattern
def Auxiliary():        yield from  (ς("can") | ς("could") | ς("will") | ς("would") | ς("should") | ς("may") | ς("might")) @ "OUTPUT"
@pattern
def Adjective():        yield from  (wrd() @ "tx" + Λ(lambda: is_adjective(tx))) @ "OUTPUT"
@pattern
def Adverb():           yield from  (wrd() @ "tx" + Λ(lambda: is_adverb(tx))) @ "OUTPUT"
@pattern
def Preposition():      yield from  (ς("in") | ς("on") | ς("at") | ς("by") | ς("with") | ς("under") | ς("over") | ς("through")) @ "OUTPUT"
@pattern
def SentenceEnd():      yield from  (σ("." ) | σ("!" ) | σ("?")) @ "OUTPUT"
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
def wrd():      yield from  SPAN(UCASE+LCASE) # (ANY(UCASE+LCASE) + FENCE(SPAN(LCASE) | ε()))
@pattern
def word():     yield from  wrd() @ "tx" + Λ(lambda: (len(tx) > 10) or (tx not in keywords[len(tx)]))
@pattern
def keyword():  yield from  wrd() @ "tx" + Λ(lambda: (len(tx) <= 10) and (tx in keywords[len(tx)]))
#-------------------------------------------------------------------------------
import wordnet
from wordnet import Lexicon, lexicon, pos
from wordnet import is_noun, is_verb, is_adjective, is_adverb
@pattern
def eTokens(X):
    yield from  \
    ( POS(0)                                            + λ(f'''{X} = []''')
    + ARBNO(
#       Θ("OUTPUT") +
        ( σ(' ')                                        + λ(f'''{X}.append("σ(' ')")''')
        | σ('\n')                                       + λ(f'''{X}.append("σ('\\\\n')\\n"''')
        | wrd() @ "tx" % "tx" + Λ(lambda: pos(tx))      + λ(f'''{X}.append(pos(tx))''')
        | wrd() % "tx"                                  + λ(f'''{X}.append("ς('" + tx + "')")''')
        | wrd() @ "tx" + Λ(lambda: is_noun(tx))         + λ(f'''{X}.append("noun()")''')
        | wrd() @ "tx" + Λ(lambda: is_verb(tx))         + λ(f'''{X}.append("verb()")''')
        | wrd() @ "tx" + Λ(lambda: is_adjective(tx))    + λ(f'''{X}.append("adj()")''')
        | wrd() @ "tx" + Λ(lambda: is_adverb(tx))       + λ(f'''{X}.append("adv()")''')
        | keyword()                                     + λ(f'''{X}.append("ς('" + w + "')")''')
        | word()                                        + λ(f'''{X}.append("word()")''')
        | SPAN(DIGITS)                                  + λ(f'''{X}.append("SPAN(DIGITS)")''')
        | SPAN(UCASE)                                   + λ(f'''{X}.append("SPAN(UCASE)")''')
        | SPAN(LCASE)                                   + λ(f'''{X}.append("SPAN(LCASE)")''')
        | NOTANY(DIGITS+UCASE+LCASE) % "tx"             + λ(f'''{X}.append("σ('" + tx + "')")''')
        ) # @ "OUTPUT"
      )
    + RPOS(0)
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
ITERATIONS = 200
def main():
#   nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,constituency')
    Lexicon()
    eInput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.txt"
    eOutput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english_out.py"
    iterations = 0
    with open(eInput_nm, "r", encoding="utf-8") as eInput:
        with open(eOutput_nm, "w", encoding="utf-8") as eOutput:
            while eSource := eInput.readline():
                iterations += 1
                if iterations > ITERATIONS: break
                sentence = eSource[0:-1]
                eOutput.write(f'''"{sentence}" in ''')
                if sentence in eTokens('P'):
                    eOutput.write("POS(0) + " + " + ".join(P) + " + RPOS(0)")
#                   if sentence.lower() in POS(0) + Sentence() + RPOS(0):
#                       eOutput.write("Yeah!!!\n")
                    eOutput.write("\n")
#               bank = nlp(sentence)
#               for root in bank.sentences:
#                   constituency = root.constituency
#                   traverse(constituency)
#                   print()
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    GLOBALS(globals())
    main()
#-------------------------------------------------------------------------------

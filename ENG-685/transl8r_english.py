# -*- coding: utf-8 -*-
# ENG 685, Universal Tokenizer, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, pattern, ε, σ, Λ, λ
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ANY, ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
#------------------------------------------------------------------------------
from pprint import pprint
from pprint import PrettyPrinter
ppr = PrettyPrinter(indent=2, width=80)
#------------------------------------------------------------------------------
@pattern
def ς(s):            yield from  σ(f" {s}")
#------------------------------------------------------------------------------
@pattern
def Sentence():
    yield from                   ( DeclarativeSentence()
                                 | InterrogativeSentence()
                                 | ImperativeSentence()
                                 )
@pattern
def DeclarativeSentence():
    yield from                   ( SimpleSentence()
                                 + ARBNO(Coordinator() + SimpleSentence())
                                 + (SubordinateClause() | ε())
                                 )
@pattern
def SimpleSentence():
    yield from                   NounPhrase() + VerbPhrase() + SentenceEnd()
@pattern
def InterrogativeSentence():
    yield from                   InterroWord() + SimpleSentence() + σ("?")
@pattern
def ImperativeSentence():
    yield from                   VerbPhraseImperative() + SentenceEnd()
@pattern
def SubordinateClause():
    yield from                   Subordinator() + SimpleSentence()
@pattern
def NounPhrase():
    yield from                   ( (Determiner() | ε())
                                 + ARBNO(Adjective())
                                 + Noun()
                                 + (RelativeClause() | ε())
                                 | ProperNoun() + (RelativeClause() | ε())
                                 | NounPhrase() + Conjunction() + NounPhrase()
                                 )
@pattern
def RelativeClause():
    yield from                   RelativePronoun() + VerbPhrase()
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
                                 )
@pattern
def VerbPhraseImperative():
    yield from                   ( Verb()
                                 + (NounPhrase() | ε())
                                 + (PrepositionalPhraseList() | ε())
                                 )
@pattern
def AdverbPhrase():
    yield from                   Adverb() + ARBNO(Adverb())
@pattern
def PrepositionalPhraseList():
    yield from                   PrepositionalPhrase() + ARBNO(PrepositionalPhrase())
@pattern
def PrepositionalPhrase():
    yield from                   Preposition() + NounPhrase()
#------------------------------------------------------------------------------
@pattern
def Coordinator():      yield from  ς("and") | ς("or") | ς("but")
@pattern
def Conjunction():      yield from  ς("and") | ς("or")
@pattern
def Subordinator():     yield from  ς("because") | ς("since") | ς("when") | ς("although")
@pattern
def RelativePronoun():  yield from  ς("who") | ς("whom") | ς("which") | ς("that")
@pattern
def InterroWord():      yield from  ς("what") | ς("who") | ς("where") | ς("when") | ς("why") | ς("how")
@pattern
def Determiner():       yield from  ς("the") | ς("a") | ς("an") | ς("this") | ς("that") | ς("these") | ς("those")
@pattern
def Noun():             yield from  ς("dog") | ς("cat") | ς("man") | ς("woman") | ς("city") | ς("car") | ς("book") | ς("tree") | ς("child")
@pattern
def ProperNoun():       yield from  ς("John") | ς("Mary") | ς("Paris") | ς("London") | ς("Alice")
@pattern
def Verb():             yield from  ς("sees") | ς("likes") | ς("chases") | ς("finds") | ς("eats") | ς("drives") | ς("reads") | ς("walks") | ς("runs")
@pattern
def Auxiliary():        yield from  ς("can") | ς("could") | ς("will") | ς("would") | ς("should") | ς("may") | ς("might")
@pattern
def Adjective():        yield from  ς("big") | ς("small") | ς("red") | ς("quick") | ς("happy") | ς("sad")
@pattern
def Adverb():           yield from  ς("quickly") | ς("silently") | ς("eagerly") | ς("loudly") | ς("gracefully")
@pattern
def Preposition():      yield from  ς("in") | ς("on") | ς("at") | ς("by") | ς("with") | ς("under") | ς("over") | ς("through")
@pattern
def SentenceEnd():      yield from  σ("." ) | σ("!" ) | σ("?")
#------------------------------------------------------------------------------
GLOBALS(globals())
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
def wrd():      yield from  (ANY(UCASE+LCASE) + FENCE(SPAN(LCASE) | ε()))
@pattern
def word():     yield from  wrd() @ "tx" + Λ(lambda: (len(tx) > 10) or (tx not in keywords[len(tx)]))
@pattern
def keyword():  yield from  wrd() @ "tx" + Λ(lambda: (len(tx) <= 10) and (tx in keywords[len(tx)]))
#-------------------------------------------------------------------------------
import wordnet
from wordnet import Lexicon, lexicon
from wordnet import is_noun, is_verb, is_adjective, is_adverb
@pattern
def eTokens():
    yield from  \
    ( POS(0)                    + λ("""P = "(\\n\"""")
    + ARBNO(
#       θ("OUTPUT") +
        ( σ(' ')                + λ("""P += "σ(' ') + \"""")
        | σ('\n')               + λ("""P += "σ('\\\\n') +\\n\"""")
        | wrd() @ "tx" + Λ(lambda: is_noun(tx))         + λ("""P += "noun() + \"""")
        | wrd() @ "tx" + Λ(lambda: is_verb(tx))         + λ("""P += "verb() + \"""")
        | wrd() @ "tx" + Λ(lambda: is_adjective(tx))    + λ("""P += "adj() + \"""")
        | wrd() @ "tx" + Λ(lambda: is_adverb(tx))       + λ("""P += "adv() + \"""")
#       | keyword()             + λ("""P += "ς('" + w + "') + \"""")
#       | word()                + λ("""P += "word() + \"""")
        | SPAN(DIGITS)         + λ("""P += "SPAN(DIGITS) + \"""")
        | SPAN(UCASE)          + λ("""P += "SPAN(UCASE) + \"""")
        | SPAN(LCASE)          + λ("""P += "SPAN(LCASE) + \"""")
        | NOTANY(DIGITS+UCASE+LCASE) % "tx" + λ("""P += "ς('" + ("\\\\" if tx == "\\\\" else "") + tx + "') + \"""")
        ) # @ "OUTPUT"
      )
    + RPOS(0)                   + λ("""P += ")\\n\"""")
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
#   nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,constituency')
    Lexicon()
    eInput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.txt"
#   eOutput_nm = "C:/SNOBOL4python/ENG-685/transl8r_english.out"
    with open(eInput_nm, "r", encoding="utf-8") as eInput:
#       with open(eOutput_nm, "w", encoding="utf-8") as eOutput:
            while eSource := eInput.readline():
                sentence = eSource[0:-1]
                print('#', sentence)
                if sentence in eTokens():
                    print(P)
#               bank = nlp(sentence)
#               for root in bank.sentences:
#                   constituency = root.constituency
#                   traverse(constituency)
#                   print()
#-------------------------------------------------------------------------------

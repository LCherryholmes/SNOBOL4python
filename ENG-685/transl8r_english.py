# -*- coding: utf-8 -*-
# ENG 685, Universal Tokenizer, Lon Cherryholmes Sr.
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, pattern, ε, σ, λ, Λ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
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

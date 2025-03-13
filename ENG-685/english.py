# -*- coding: utf-8 -*-
from pprint import pprint
from SNOBOL4python import GLOBALS, pattern, ε, σ, π, λ, Λ, θ
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ARBNO, BAL, BREAK, NOTANY, POS, RPOS, SPAN
#---------- ----------------- ----- -------------------------------------------------------- ---------------------------
def space():            yield from SPAN(' ')
def white():            yield from SPAN(' ')
def whitespace():       yield from SPAN(' ')
def μ():                yield from FENCE(space() | ε())
def η():                yield from FENCE(whitespace() | ε())
def ς(s):               yield from η() + σ(s)
#---------- ----------------- ----- -------------------------------------------------------- ---------------------------
def eWordSegment():     yield from SPAN(_UCASE+_LCASE)
def eWordSegments():    yield from eWordSegment() + FENCE(σ('-') + eWordSegments() | ε())
def eWord():            yield from eWordSegment() + FENCE(σ('-') + eWordSegments() | ε())
def eUnknownWord():     yield from eWord() @ "tx" + notmatch(lambda: eWords, lambda: σ('/') + (σ(tx) | σ(lwr(tx))) + σ('/'))
def eKnownWord():       yield from eWord() @ "tx" + match(lambda: eWords,    lambda: σ('/') + (σ(tx) | σ(lwr(tx))) + σ('/'))
def eDQString():        yield from σ('"') + BREAK('"') + σ('"')
def eSQString():        yield from σ("`") + BREAK("'") + σ("'") | σ("'") + BREAK("'") + σ("'")
def eNumber():          yield from SPAN('0123456789')
#---------- ----------------- ----- -------------------------------------------------------- ---------------------------
eWords = (
    "/I/Shakespear/William/Winifred/children's/"
    'a/about/above/accordingly/across/after/again/against/all/along/also/although/am being/am/among/an/and/'
    'another/any/anybody/anyone/anything/appear/are being/are/as/at/be/because/become/before/beneath/beside/'
    'besides/beyond/both/but also/but/by/can be/can/cause/consequently/could be/could have been/could/'
    'did/do/does/double/down/each other/each/either/enough/even/every/everybody/everyone/everything/except/feel/'
    'few/finally/five/for/four/fourth/from/furthermore/give/grow/had been/had/half/has been/has/have been/have/'
    'he/her/hers/herself/him/himself/his/however/hundred/if/in/indeed/inside/into/is being/is/it/its/itself/'
    'less/little/long/look/many/may be/may have been/may/me/might be/might have been/might/mine/more/'
    'moreover/most/much/must be/must have been/must/my/myself/near/neither/nevertheless/next to/no one/nobody/'
    'none/nor/not only/not/nothing/now/of/on/once/one another/one/one-third/oneself/only/or/order/other/others/'
    'otherwise/our/ours/ourselves/out/over/quite/rather/remain/result/seem/several/shall be/shall have been/'
    'shall/she/should be/should have been/should/since/smell/so/some/somebody/someone/something/'
    'soon/sound/stay/such/taste/ten/than/that/the/their/theirs/them/themselves/then/there/therefore/these/they/this/'
    'those/though/thousand/three/three-quarters/through/thus/till/times/to/toward/turn/twice/two/'
    'under/unless/until/upon/us/was being/was/we/were being/were/what/when/whenever/where/whereas/wherever/whether/'
    'which/while/who/whom/whose/why/will be/will have been/will/with/without/would be/would have been/would/'
    'yet/you/your/yours/yourself/yourselves/zero/'
)
#---------- ----------------- ----- -------------------------------------------------------- ---------------------------
def ReadDict(): pass
def CideText(): pass
def Lexicon(P, v): pass
#---------- ----------------- ----- -------------------------------------------------------- ---------------------------
dictionary = dict()
ReadDict()
CideText()
#del dictionary['A']
#del dictionary['As']
#del dictionary['In']
#del dictionary['les']
#del dictionary['unde']
#del dictionary['i']
Lexicon(eWord(), eWords)
#===================================================================================================
#   NOUNS
#   A noun is the name of a person, place, or thing. Some of the things nouns name can be seen or
#   touched; some cannot. A compound noun is a noun that is made up of more than one word either
#   separated, hyphenated, or combined.
def eNoun():
    yield from  ( ePersonNoun()
                | ePlaceNoun()
                | eThingNoun()
                | eTimeNoun()
                | eProperNoun()
                | eDictNoun()
                )

def eDictNoun():
    yield from  ( eWord() @ "eW1"  + σ(' ')
                + eWord() @ "eW2"  + σ(' ')
                + eWord() @ "eW3"  + EngIsNoun(lambda: eW1+' '+eW2+' '+eW3)
                | eWord() @ "eW1"  + σ(' ')
                + eWord() @ "eW2"  + EngIsNoun(lambda: eW1+' '+eW2)
                | eWord() @ "eWrd" + EngIsNoun(lambda: eWrd)
                )

def ePersonNoun():
    yield from  ( σ('Shakespear')
                | σ('William')
                | σ('Winifred')
                )

def ePlaceNoun():
    yield from  ( σ('Alaska')
                | σ('Arizona')
                | σ('Colorado')
                | σ('Delaware')
                | σ('Honolulu')
                | σ('Nebraska')
                | σ('New Jersey')
                | σ('New Mexico')
                | σ('Connecticut')
                | σ('Puerto Rico')
                | σ('North Dakota')
                | σ('Rhode Island')
                | σ('Massachusetts')
                | σ('New Hampshire')
                | σ('Maine')
                | σ('Kansas')
                | σ('Nevada')
                | σ('Oregon')
                | σ('Vermont')
                | σ('Nebraska')
                | σ('United States')
                | σ('Washington')
                | σ('Wilmington')
                | σ('Bangor')
                | σ('Portland')
                | σ('Tucson') + σ(',') + σ('Arizona')
                )

def eParens():
    yield from  σ('(') + BREAK('()') + σ(')')

def eThingNoun():
    yield from  ( σ('Advisory Council on Historic Preservation')
                | σ('Appalachian Housing Fund')
                | σ('Capitol Building')
                | σ('Capitol police')
                | σ('Coast Guard Reserve')
                | σ('Cochairman')
                | σ('Cochairmen')
                | σ('Coordinating Board')
                | σ('Data Bank')
                | σ('Department of Homeland Security')
                | σ('Department of the Air Force')
                | σ('Federal Advisory Committee Act')
                | σ('Flag Day')
                | σ('Fort Jefferson National Monument')
                | σ('Government Accountability Office')
                | σ('Government Publishing Office')
                | σ('Immigration and Customs Enforcement')
                | σ('Inspector General Act')
                | σ('Joint Intelligence Community Council')
                | σ('Kerr Memorial Arboretum and Nature Center')
                | σ('Loyalty Day')
                | σ('Metropolitan Medical Response Program')
                | σ('National Intelligence Council')
                | σ('National Portrait Gallery Commission')
                | σ('National Reconnaissance Office')
                | σ('Public Health Service Act')
                | σ('Russell National School Lunch Act')
                | σ('Smithsonian Institution')
                | σ('Social Security Act')
                | σ('Steelmark Month')
                | σ('Under Secretary')
                | σ('Wright Brothers Day')
                | σ('Referenda')
                | σ('FINRA')
                | σ('SIPC')
                | σ('campus director')
                | σ('committee proceeding')
                | σ('community residence')
                | σ('conversion rate')
                | σ('market rents')
                | σ('risk assessment')
                | σ('staffing agency')
                | eNumber()
                | σ('$') + eNumber() + ARBNO(',' + eNumber())
                | (σ('Title') | σ('title')) + σ(' ') + eNumber()
                | (σ('Paragraph') | σ('paragraph')) + σ(' ') + eParens()
                | (σ('Paragraphs') | σ('paragraphs')) + σ(' ') + ARBNO(eParens()) + (σ('and') | σ('or')) + ARBNO(eParens())
                | (σ('Section') | σ('section')) + σ(' ') + eNumber() + ARBNO(eParens())
                | (σ('Subsection') | σ('subsection')) + σ(' ') + ARBNO(eParens())
                | (σ('Subchapter') | σ('subchapter'))
                | (σ('Subclause') | σ('subclause'))
                | (σ('Subparagraph') | σ('subparagraph')) + σ(' ') + ARBNO(eParens())
                | (σ('Subparagraph') | σ('subparagraph'))
                | (σ('Subparagraphs') | σ('subparagraphs'))
                | σ('order')
                | σ('through') + σ(' ') + σ('route')
                )

def eDayOfWeek():
    yield from  ( σ('Monday')
                | σ('Tuesday')
                | σ('Wednesday')
                | σ('Thursday')
                | σ('Friday')
                | σ('Saturday')
                | σ('Sunday')
                )

def eMonth():
    yield from  ( σ('January')
                | σ('February')
                | σ('March')
                | σ('April')
                | σ('May')
                | σ('June')
                | σ('July')
                | σ('August')
                | σ('September')
                | σ('October')
                | σ('November')
                | σ('December')
                )

def eTimeNoun(): \
    yield from \
    ( eWordSegment() @ "tx" + match(lambda: tx, lambda: POS(0) + eMonth() + RPOS(0)) + σ(' ') + eNumber() + σ(', ') + eNumber()
    | eWordSegment() @ "tx" + match(lambda: tx, lambda: POS(0) + eMonth() + RPOS(0)) + (σ(' ') + eNumber() | ε())
    | eWordSegment() @ "tx" + match(lambda: tx, lambda: POS(0) + eDayOfWeek() + RPOS(0))
    | σ('year ') + eNumber()
    )
def eSeparatedNoun():         yield ""
def eHyphenatedNoun():        yield ""
def eCombinedNoun():          yield ""
#   A common noun names any one of a class of people, places, or things. A proper noun names a
#   specific person, place, or thing. Proper nouns take capitals.
def eCommonNoun():            yield ""
def eProperNoun():            yield from σ('co-chairs') | σ('demonstration program')
def eCountNouns():            yield from eSingularCountNoun() | ePluralCountNoun()
def eSingularCountNoun():     yield ""
def ePluralCountNoun():       yield ""
def eMassNouns():             yield ""
def eCollectiveNoun():        yield ""
#===================================================================================================
#   PRONOUNS
#   A pronoun is a word used to take the place of a noun. The noun a pronoun substitutes for is
#   called an antecedent. Personal pronouns refer to (1) the person speaking, (2) the person
#   spoken to, or (3) the person, place, or thing spoken about.
def ePronoun():               yield from \
                              ( ePersonalPronoun()
                              | eReflexiveIntensivePronoun()
                              | eDemonstrativePronoun()
                              | eRelativePronoun()
                              | eInterrogativePronoun()
                              | eIndefinitePronoun()
                              | eReciprocalPronoun()
                              )
def ePersonalPronoun():       yield from \
                              ( eSubjectPersonalPronoun()
                              | ePossessivePersonalPronoun()
                              | eObjectPersonalPronoun()
                              )
def eSubjectPersonalPronoun():      yield from σ('I') | σ('you') | σ('he') |σ('she') | σ('it') | σ('we') | σ('they')
def ePossessivePersonalPronoun():   yield from σ('mine') | σ('yours') | σ('his') | σ('hers') | σ('its') | σ('ours') | σ('theirs')
def eObjectPersonalPronoun():       yield from σ('me') | σ('you') | σ('him') | σ('her') | σ('it') | σ('us') | σ('them')
#   A reflexive pronoun ends in "-self" or "-selves" and adds information to a sentence by
#   pointing back to a noun or pronoun that appears earlier in the sentence. An intensive pronoun
#   has the same ending as a reflexive pronoun but simply adds emphasis to a noun or pronoun in
#   the same sentence.
def eReflexiveIntensivePronoun():
    yield from  ( σ('myself')
                | σ('yourself')
                | σ('himself')
                | σ('herself')
                | σ('itself')
                | σ('oneself')
                | σ('ourselves')
                | σ('yourselves')
                | σ('themselves')
                )
#   A demonstrative pronoun directs attention to a specific person, place, or thing. A relative
#   pronoun begins a subordinate clause and connects it to another idea in the sentence. An
#   interrogative pronoun is used to begin a question.
def eDemonstrativePronoun():
    yield from                σ('this') | σ('that') | σ('these') | σ('those')
def eRelativePronoun():
    yield from                σ('that') | σ('which') | σ('who') | σ('whom') | σ('whose') # σ('when') σ('where') σ('why')
def eInterrogativePronoun():
    yield from                σ('who') | σ('whom') | σ('why') | σ('what')
#   Indefinite pronouns refer to people, places, or things, often without specifying which ones.
#   Some indefinite pronouns may have an antecedent, but many do not have a specific antecedent.
def eIndefinitePronoun():
    yield from                ( eIndefiniteSingularPronoun()
                              | eIndefinitePluralPronoun()
                              | eIndefiniteEitherPronoun()
                              )
def eIndefiniteSingularPronoun():
    yield from  ( σ('another')
                | σ('anybody')
                | σ('anyone')
                | σ('anything')
                | σ('each')
                | σ('either')
                | σ('everybody')
                | σ('everyone')
                | σ('everything')
                | σ('little')
                | σ('much')
                | σ('neither')
                | σ('nobody')
                | σ('no one')
                | σ('nothing')
                | σ('one')
                | σ('other')
                | σ('somebody')
                | σ('someone')
                | σ('something')
                )
def eIndefinitePluralPronoun():
    yield from  ( σ('both')
                | σ('few')
                | σ('many')
                | σ('others')
                | σ('several')
                )
def eIndefiniteEitherPronoun():
    yield from  ( σ('all')
                | σ('any')
                | σ('less')
                | σ('more')
                | σ('most')
                | σ('none')
                | σ('some')
                )
def eReciprocalPronoun():
    yield from  σ('each other') | σ('one another')
#===================================================================================================
#   VERBS
#   A verb is a word that expresses time while showing an action, a condition, or the fact that
#   something exists. An action verb is a verb that tells what action someone or something is
#   performing. An action verb may show mental action as well as visible action. An action verb
#   is transitive if it directs action toward someone or something. An action verb is intransitive
#   if it does not direct action toward someone or something.
#   1. simple present,             simple past,             simple future
#   2. present continuous,         past continuous,         future continuous
#   3. present perfect,            past perfect,            future perfect
#   4. present perfect continuous, past perfect continuous, future perfect continuous
def eVerb():
    yield from                ( eModalVerb()
                              | eModalVerb() + eDictVerb()
                              | eLinkingVerb()
                              | eFormOfBEVerb()
                              | eFormOfBEVerb() + eDictVerb()
                              | eHelpingVerb() + eDictVerb()
#                             | σ('made') + eDictAdjective()
                              )
def eDictVerb():
    yield from                ( eWord() @ "eW1"  + σ(' ')
                              + eWord() @ "eW2"  + σ(' ')
                              + eWord() @ "eW3"  + EngIsVerb(lambda: eW1+' '+eW2+' '+eW3)
                              | eWord() @ "eW1"  + σ(' ')
                              + eWord() @ "eW2"  + EngIsVerb(lambda: eW1+' '+eW2)
                              | eWord() @ "eWrd" + EngIsVerb(lambda: eWrd)
                              | σ('reappointed')
                              | σ('redelegated')
                              )
def eMainVerb():              yield from eTransitiveVerb() | eIntransitiveVerb()
def eTransitiveVerb():        yield ""
def eIntransitiveVerb():      yield ""
def eModalVerb():
    yield from                ( σ('can')         | σ('can')    + σ('not')
                              | σ('could')       | σ('could')  + σ('not')
                              | σ('may')         | σ('may')    + σ('not')
                              | σ('might')       | σ('might')  + σ('not')
                              | σ('shall')       | σ('shall')  + σ('not')
                              | σ('should')      | σ('should') + σ('not')
                              | σ('will')        | σ('will')   + σ('not')
                              | σ('would')       | σ('would')  + σ('not')
                              )
#   A linking verb is a verb that connects a word at or near the beginning of a sentence with a
#   word at or near the end. In English, the most common linking verb is some form of "be".
#   Other verbs may be used in the same was as "be" to link two parts of a sentence.
def eLinkingVerb():
    yield from                ( σ('appear')
                              | σ('become')
                              | σ('feel')
                              | σ('grow')
                              | σ('look')
                              | σ('remain')
                              | σ('seem')
                              | σ('smell')
                              | σ('sound')
                              | σ('stay')
                              | σ('taste')
                              | σ('turn')
                              )
#   Helping verbs are verbs that can be added to another verb to make a single verb phrase. Any of
#   the many forms of "be" as well as some other common verbs can be used as helping verbs.
def eHelpingVerb():
    yield from                ( σ('do')     + σ('not') | σ('do')
                              | σ('does')   + σ('not') | σ('does')
                              | σ('did')    + σ('not') | σ('did')
                              | σ('have')   + σ('not') | σ('have')
                              | σ('has')    + σ('not') | σ('has')
                              | σ('had')    + σ('not') | σ('had')
                              | σ('shall')  + σ('not') | σ('shall')
                              | σ('should') + σ('not') | σ('should')
                              | σ('will')   + σ('not') | σ('will')
                              | σ('would')  + σ('not') | σ('would')
                              | σ('can')    + σ('not') | σ('can')
                              | σ('could')  + σ('not') | σ('could')
                              | σ('may')    + σ('not') | σ('may')
                              | σ('might')  + σ('not') | σ('might')
                              | σ('must')   + σ('not') | σ('must')
                              )
def eFormOfBEVerb():
    yield from                ( σ('am')     + σ('not')                         | σ('am')
                              | σ('are')    + σ('not')                         | σ('are')
                              | σ('is')     + σ('not')                         | σ('is')
                              | σ('was')    + σ('not')                         | σ('was')
                              | σ('were')   + σ('not')                         | σ('were')
                              | σ('am')     + σ('not') + σ('being')            | σ('am being')
                              | σ('are')    + σ('not') + σ('being')            | σ('are being')
                              | σ('is')     + σ('not') + σ('being')            | σ('is being')
                              | σ('was')    + σ('not') + σ('being')            | σ('was being')
                              | σ('were')   + σ('not') + σ('being')            | σ('were being')
                              | σ('can')    + σ('not') + σ('be')               | σ('can be')
                              | σ('could')  + σ('not') + σ('be')               | σ('could be')
                              | σ('may')    + σ('not') + σ('be')               | σ('may be')
                              | σ('might')  + σ('not') + σ('be')               | σ('might be')
                              | σ('must')   + σ('not') + σ('be')               | σ('must be')
                              | σ('shall')  + σ('not') + σ('be')               | σ('shall be')
                              | σ('should') + σ('not') + σ('be')               | σ('should be')
                              | σ('will')   + σ('not') + σ('be')               | σ('will be')
                              | σ('would')  + σ('not') + σ('be')               | σ('would be')
                              | σ('have')   + σ('not') + σ('been')             | σ('have been')
                              | σ('has')    + σ('not') + σ('been')             | σ('has been')
                              | σ('had')    + σ('not') + σ('been')             | σ('had been')
                              | σ('could')  + σ('not') + σ('have') + σ('been') | σ('could have been')
                              | σ('may')    + σ('not') + σ('have') + σ('been') | σ('may have been')
                              | σ('might')  + σ('not') + σ('have') + σ('been') | σ('might have been')
                              | σ('must')   + σ('not') + σ('have') + σ('been') | σ('must have been')
                              | σ('shall')  + σ('not') + σ('have') + σ('been') | σ('shall have been')
                              | σ('should') + σ('not') + σ('have') + σ('been') | σ('should have been')
                              | σ('will')   + σ('not') + σ('have') + σ('been') | σ('will have been')
                              | σ('would')  + σ('not') + σ('have') + σ('been') | σ('would have been')
                              )
def eAuxiliaryVerb():
    yield from                σ('be') | σ('do') | σ('have')
def eDitransitiveVerb():
    yield from                σ('cause') | σ('give')
def eFiniteVerb():            yield ""
def eNonFiniteVerb():         yield ""
def eDynamicVerb():
    yield from                ( eActivityVerb()
                              | eProcessVerb()
                              | eBodilySensationVerb()
                              | eTransitionalEventVerb()
                              | eMomentaryVerb()
                              )
def eStativeVerb():
    yield from                eCognitionVerb() | eRelationalVerb()
def eActivityVerb():          yield ""
def eProcessVerb():           yield ""
def eBodilySensationVerb():   yield ""
def eTransitionalEventVerb(): yield ""
def eMomentaryVerb():         yield ""
def eCognitionVerb():         yield ""
def eRelationalVerb():        yield ""
#===================================================================================================
#   ADJECTIVES
def eAdjectives():
    yield from                eAdjective() + (eAdjectives() | ε())
def eAdjective():
    yield from                ( eArticle()
                              | eIntensifier()
                              | ePredeterminer()
                              | eDemonstrativeAdjective()
                              | eDescriptiveAdjective()
                              | eIndefiniteAdjective()
                              | eNumericalAdjective()
                              | ePossessiveAdjective()
                              | eProperAdjective()
                              | eDictAdjective()
                              )
def eDictAdjective():
    yield from                ( eWord() @ "eW1"  + σ(' ')
                              + eWord() @ "eW2"  + σ(' ')
                              + eWord() @ "eW3"  + EngIsAdj(lambda: eW1+' '+eW2+' '+eW3)
                              | eWord() @ "eW1"  + σ(' ')
                              + eWord() @ "eW2"  + EngIsAdj(lambda: eW1+' '+eW2)
                              | eWord() @ "eWrd" + EngIsAdj(lambda: eWrd)
                              )
def eArticle():               yield from σ('a') | σ('an') | σ('the')
def eIntensifier():           yield from σ('quite') | σ('rather') | σ('such')
def ePredeterminer():         yield from eMultiplier() | eFractionionalExpression() | σ('both') | σ('half') | σ('all')
def eMultiplier():            yield from σ('double') | σ('twice') | σ('four times') | σ('five times')
def eFractionionalExpression(): yield from σ('one-third') | σ('three-quarters')
#   A noun used as an adjective answers the question "What kind?" or "Which one?" about a noun
#   that follows it. A proper adjective is a proper noun used as an adjective or an adjective
#   formed from a proper noun. A compound adjective is an adjective made up of more than one word.
def eNounAdjective():         yield ""
def eProperAdjective():       yield "?"
def eCompoundAdjective():     yield ""
#   A pronoun is used as an adjective if it modifies a noun. A personal pronoun used as a
#   possesssive adjective answers the question "Which one?" about a noun that follows it.
def ePossessiveAdjective():
    yield from                ( σ('my')
                              | σ('your')
                              | σ('his')
                              | σ('her')
                              | σ('its')
                              | σ('our')
                              | σ('their')
                              | σ("children's")
                              )

#   A demonstrative, interrogative, or indefinite pronoun used as an adjective anwers the question
#   "Which one?", "How many?", or "How much?" about the noun that follows it.
def eDemonstrativeAdjective():
    yield from                σ('this') | σ('that') | σ('these') | σ('those')
def eInterrogativeAdjective():
    yield from                σ('what') | σ('which') | σ('whose')
def eIndefiniteAdjective():
    yield from                ( σ('all')
                              | σ('another')
                              | σ('any')
                              | σ('both')
                              | σ('each')
                              | σ('either')
                              | σ('enough')
                              | σ('every')
                              | σ('few')
                              | σ('less')
                              | σ('many')
                              | σ('more')
                              | σ('most')
                              | σ('much')
                              | σ('neither')
                              | σ('other')
                              | σ('several')
                              | σ('some')
                              | σ('what')
                              | σ('which')
                              )
def eDescriptiveAdjective():
    yield from                ( σ('agency-specific')
                              | σ('below-market')
                              | σ('asbestos-containing')
                              | σ('career-conditional')
                              | σ('crosscutting')
                              | σ('employer-sponsored')
                              | σ('medium-sized')
                              | σ('merit-based')
                              | σ('merit-reviewed')
                              | σ('multiyear')
                              | σ('non-criminal')
                              | σ('non-federal')
                              | σ('out-of-area')
                              | σ('public-private')
                              | σ('refundable')
                              | σ('security-based')
                              | σ('self-closing')
                              | σ('self-latching')
                              | σ('sixteen-year-old')
                              | σ('three-year')
                              | eNumber() + σ('-year')
                              )
def eNumericalAdjective():
    yield from                ( σ('four')
                              | σ('five')
                              | σ('five hundred')
                              | σ('fourth')
                              | σ('one')
                              | σ('ten')
                              | σ('three')
                              | σ('two')
                              | σ('zero')
                              | σ('thousand')
                              | eNumber()
                              )
#===================================================================================================
#   ADVERBS
#   An adverb is a word that modifies a verb, an adjective, or another adverb. An adverb
#   modifying a verb answers the question "Where?", "When?", "In what manner?", or
#   "To what extent?". An adverb modifying an adjective answers only one question:
#   "To what extent?". An adverb modifying another adverb also answers just one question:
#   "To what extent?".
def eAdverbs():
    yield from                eAdverb() + (eAdverbs() | ε())
def eAdverb():
    yield from                ( eWord() @ "eW1"  + σ(' ') 
                              + eWord() @ "eW2"  + σ(' ')
                              + eWord() @ "eW3"  + EngIsAdv(lambda: eW1+' '+eW2+' '+eW3)
                              | eWord() @ "eW1"  + σ(' ')
                              + eWord() @ "eW2"  + EngIsAdv(lambda: eW1+' '+eW2)
                              | eWord() @ "eWrd" + EngIsAdv(lambda: eWrd)
                              )
#===================================================================================================
#   PREPOSITIONS
#   A preposition is a word that relates a noun or pronoun that appears with it to another word in
#   the sentence. The choice of preposition affects the way the other words in a sentence relate
#   to each other.
def ePreposition():
    yield from                ( σ('about')
                              | σ('against')
                              | σ('above')
                              | σ('across')
                              | σ('after')
                              | σ('among')
                              | σ('beneath')
                              | σ('beside')
                              | σ('beyond')
                              | σ('by')
                              | σ('down')
                              | σ('except')
                              | σ('for')
                              | σ('from')
                              | σ('in')
                              | σ('inside')
                              | σ('into')
                              | σ('near')
                              | σ('next to')
                              | σ('of')
                              | σ('on')
                              | σ('out')
                              | σ('over')
                              | σ('since')
                              | σ('to')
                              | σ('toward')
                              | σ('under')
                              | σ('upon')
                              | σ('until')
                              | σ('with')
                              | σ('without')
                              | σ('along')
                              | σ('through')
                              | σ('at')
                              )
#===================================================================================================
#   CONJUNCTIONS
def eConjunction():
    yield from                ( eCoordinatingConjunction()
                              | eSubordinatingConjunction()
                              )

def eCoordinatingConjunction():
    yield from                ( σ('and')
                              | σ('or')
                              | σ('for')
                              | σ('nor')
                              | σ('so')
                              | σ('but')
                              | σ('yet')
                              )

def eSubordinatingConjunction():
    yield from                ( σ('after')
                              | σ('although')
                              | σ('as') + σ('if')
                              | σ('as') + σ('long') + σ('as')
                              | σ('as') + σ('soon') + σ('as')
                              | σ('as') + σ('though')
                              | σ('as')
                              | σ('because')
                              | σ('before')
                              | σ('even') + σ('if')
                              | σ('even') + σ('though')
                              | σ('if') + σ('only')
                              | σ('if')
                              | σ('in') + σ('order') + σ('that')
                              | σ('now') + σ('that')
                              | σ('once')
                              | σ('rather') + σ('than')
                              | σ('since')
                              | σ('so') + σ('that')
                              | σ('than')
                              | σ('that')
                              | σ('though')
                              | σ('till')
                              | σ('unless')
                              | σ('until')
                              | σ('when')
                              | σ('whenever')
                              | σ('where')
                              | σ('whereas')
                              | σ('wherever')
                              | σ('whether')
                              | σ('while')
                              )

def eCorrelativeConjunctions():
    yield from                ( σ('both') + σ('and')
                              | σ('not only') + σ('but also')
                              | σ('not') + σ('but')
                              | σ('either') + σ('or')
                              | σ('neither') + σ('nor')
                              | σ('whether') + σ('or')
                              | σ('as') + σ('as')
                              )
#===================================================================================================
#   INTERJECTIONS
def eConjunctiveAdverb():
    yield from                ( σ('however')
                              | σ('moreover')
                              | σ('nevertheless')
                              | σ('consequently')
                              | σ('as') + σ('a') + σ('result')
                              | σ('accordingly')
                              | σ('again')
                              | σ('also')
                              | σ('besides')
                              | σ('consequently')
                              | σ('finally')
                              | σ('furthermore')
                              | σ('however')
                              | σ('indeed')
                              | σ('moreover')
                              | σ('nevertheless')
                              | σ('otherwise')
                              | σ('then')
                              | σ('therefore')
                              | σ('thus')
                              )

def eInterjection(): yield ""
#===================================================================================================
#   SENTENCE
#   The two fundamental parts of every English sentence are the complete subject and the
#   predicate.  The complete subject is normally the topic of the sentence, and the predicate is
#   what is asserted of that topic.
def eCompleteSentence(): yield from eCompleteSubject() + eCompletePredicate() + σ('.')
#   The complete subject is the entire noun phrase, including the head noun and any modifiers
#   (e.g., "the" and "few") of that noun, that occurs in subject position in a sentence.
#   The simple subject is the essential noun, pronoun, or group of words acting as a noun that
#   cannot be left out of the complete subject. The simple predicate is the essential verb or verb
#   phrase that cannot be left out of the complete predicate.
def eCompleteSubject():       yield from eCompoundSubject() # eSubject() #
def eCompletePredicate():     yield from ePredicate()
def eSubject():               yield from eModifiedNounOrPronoun()
def ePredicate():             yield from \
                              ( eModifiedVerb()
                                ( eDirectObject() + (eObjectiveComplement() | ε())
                                | eIndirectObject() + eDirectObject()
                                | ε()
                                )
                              | (eLinkingVerb() | eFormOfBEVerb())
                                (eAdverbs() | ε())
                                (ePredicateNominative() | ePredicateAdjective())
                              )
def eModifiedVerb():          yield from \
                              ( eAdverbs() + eDictVerb()
                              | eDictVerb() + (eAdverbialPhrase() | σ('only') | ε())
                              )
def eAdverbialPhrase():       yield from eAdverb() | ePrepositionalPhrase()
def eIndirectObject():        yield from eModifiedNounOrPronoun()
def eDirectObject():          yield from eModifiedNounOrPronoun()
#   A predicate nominative is a noun or pronoun that follows a linking verb and renames,
#   identifies, or explains the subject of a sentence. A predicate adjective is an adjective that
#   follows a linking verb and describes the subject of the sentence.
def ePredicateNominative():   yield from eModifiedNoun() | eModifiedPronoun()
def ePredicateAdjective():    yield from eAdjective() | eAdjectivalPhrase()
def eAdjectivalPhrase():      yield from eAdjectives() | ePrepositionalPhrase() | eParticipialPhrase()
#   An objective complement is an adjective, noun, or group of words acting as a noun that follows
#   a direct object and describes or renames it.
def eObjectiveComplement():   yield from eAdjective() | eModifiedNoun()
def eObjectiveComplement():   yield from eNoun() | eAdjective()
#   A compound subject is two or more subjects that have the same verb and are joined by a
#   conjunction such as "and" or "or".
def eCompoundSubject():       yield from eCompoundOrSubject() | eCompoundAndSubject()
def eCompoundOrSubject():     yield from eSubject() + ((σ(',') + π(σ('or'))  | σ('or'))  + eCompoundOrSubject() | ε())
def eCompoundAndSubject():    yield from eSubject() + ((σ(',') + π(σ('and')) | σ('and')) + eCompoundAndSubject() | ε())
#   A compound verb is two or more verbs that have the same subject and are joined by a
#   conjunction such as "and" or "or".
def eCompoundVerb():          yield from \
                              ( eAdverbs()
                              + (eCompoundOrVerb() | eCompoundAndVerb())
                              | (eCompoundOrVerb() | eCompoundAndVerb())
                              + (eAdverbialPhrase() | ε())
                              )
def eCompoundOrVerb():        yield from eDictVerb() + ((σ(',') + π(σ('or'))  | σ('or'))  + eCompoundOrVerb() | ε())
def eCompoundAndVerb():       yield from eDictVerb() + ((σ(',') + π(σ('and')) | σ('and')) + eCompoundAndVerb() | ε())
#   Sentences can be:
#   Simple: One independent clause (subject or verb or both may be compound)
#   Compound: Two or more independent clauses
#   Complex: One independent clause and one or more subordinate clauses
#   Compound-Complex: Two or more independent clauses and one or more subordinate clauses.
def eIndependentClause():     yield from eCompoundSubject() + eCompoundVerb()
def eSimpleSentence():        yield from eIndependentClause()
def eCompoundSentence():      yield from \
                              ( eIndependentClause()
                              + (  π(σ(',')) + σ('and') + eCompoundAndClauses()
                                |  π(σ(',')) + σ('or')  + eCompoundOrClauses()
                                )
                              )
def eCompoundAndClauses():    yield from eIndependentClause() + (π(σ(',')) + σ('and') + eCompoundAndClauses() | ε())
def eCompoundOrClauses():     yield from eIndependentClause() + (π(σ(',')) + σ('or')  + eCompoundOrClauses() | ε())
def eComplexSentence():       yield from eIndependentClause() + eSubordinateClauses()
def eCompoundComplexSentence():     yield from \
                                    ( eComplexSentence()
                                    + (  π(σ(',')) + σ('and') + eCompoundAndSentences()
                                      |  π(σ(',')) + σ('or')  + eCompoundOrSentences()
                                      )
                                    )
def eCompoundAndSentences():  yield from eComplexSentence()   + (π(σ(',')) + σ('and') + eCompoundAndSentences() | ε())
def eCompoundOrSentences():   yield from eComplexSentence()   + (π(σ(',')) + σ('or')  + eCompoundOrSentences() | ε())
def eSubordinateClauses():    yield from eSubordinateClause() + (π(σ(',')) + eSubordinateClauses() | ε())
def eSubordinateClause():     yield from \
                              ( eRelativePronoun()
                              + (  eFormOfBEVerb() + eModifiedNoun()
                                |  eDictVerb() + eModifiedNoun()
                                )
                              | eSubordinatingConjunction()
                              + ( eAdjective()
                                | eDictVerb() + eModifiedNoun()
                                )
                              )
#   There are six basic sentence patterns in English. The patterns differ on the basis of what
#   type of complement structure they have within the predicate.
#   The first pattern is the simplest -- one without a verb complement, as verb complements are defined in traditional grammar.
#   The second pattern has as its defining characteristic the presence of a direct object.
#       Direct objects are noun phrases that come after the verb.
#   The third pattern has as its defining characteristic the presence of both indirect and direct objects.
#       Indirect objects do always come immediately after the verb.
#   The fourth pattern has as its defining characteristic the presence of a predicate nominative verb complement.
#       The predicate nominative is a noun or a pronoun that redefines, renames, or classifies the subject of the sentence.
#       The verb in a predicate nominative construction is always a linking verb, such as be, seem, or become.
#   The fifth pattern has as its defining characteristic the presence of a predicate adjective verb complement.
#       The predicate adjective is an adjective that characterizes the subject of the sentence.
#       The verb in a predicate adjective construction, like the verb in a predicate nominative construction,
#       is always a linking verb, such as be, seem, smell, look, taste, or become.
#   The sixth pattern has as its defining characteristic the presence as verb complements of both a direct object
#       and an objective complement.
#       We met the direct object earlier.
#       An objective complement is a noun or an adjective that occurs after the direct object and that describes the direct object.
def eBasicSentence(): \
    yield from \
    ( eSubject() + eVerb()
    | eSubject() + eVerb() + eDirectObject()
    | eSubject() + eVerb() + eIndirectObject() + eDirectObject()
    | eSubject() + eLinkingVerb() + ePredicateNominative()
    | eSubject() + eLinkingVerb() + ePredicateAdjective()
    | eSubject() + eVerb() + eDirectObject() + eObjectiveComplement()
    )
#   Sentences can also be classified by their function.
#   Declarative: States and idea. Ends in a period.
#   Interrogative: Asks a question. Ends in a question mark.
#   Imperative: Gives an order or a direction. Ends in a period or an exclamation mark.
#   Exclamatory: Conveys strong emotion.  Ends in an exclamation mark.
def ePlaySentence():
    yield from \
      (  eCompleteSubject() + σ('has') + eModifiedNoun()
      |  eCompleteSubject() + eModalVerb() + eDictVerb()
      |  eCompleteSubject() + eModalVerb() + eDictVerb() + eModifiedNoun()
      |  eCompleteSubject() + eModalVerb() + eDictVerb() + ePreposition() + eNoun()
      |  eCompleteSubject() + eDictVerb() + eModifiedNoun()
      |  eCompleteSubject() + eDictVerb() + ePrepositionalPhrase()
      |  eCompleteSubject() + eFormOfBEVerb() + eModifiedNoun()
      |  eCompleteSubject() + eFormOfBEVerb() + eModifiedNoun() + eModifiedNoun()
      |  eCompleteSubject() + eFormOfBEVerb() + eModifiedVerb()
      |  eCompleteSubject() + eFormOfBEVerb() + eAdjective()
      |  eCompleteSubject() + eFormOfBEVerb() + ePrepositionalPhrase()
      |  eCompleteSubject() + eFormOfBEVerb() + eDictVerb() + σ('as') + DictVerb()
      |  eCompleteSubject() + eFormOfBEVerb() + eDictVerb() + σ('to') + σ('be') + eAdjective()
      |  eCompleteSubject() + eFormOfBEVerb() + eDictVerb() + eAdverb() + σ('to') + eDictVerb() + eModifiedNoun()
      |  eCompleteSubject() + ePrepositionalPhrase() + eFormOfBEVerb() + eModifiedNoun()
      |  eCompleteSubject() + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + σ('have') + eModifiedNoun()
      |  eCompleteSubject() + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + eDictVerb() + eModifiedNoun()
      |  eCompleteSubject() + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + eDictVerb() + ePrepositionalPhrase()
      |  σ('there') + eFormOfBEVerb() + eModifiedNoun()
      )
    + σ('.')
#   A direct object is a noun, pronoun, or group of words acting as a noun that receives the
#   action of a transitive verb. A compound direct object is more that one direct object that
#   receives the action of the same transitive verb. A direct object is never the noun or pronoun
#   at the end of a prepositional phrase.
def eCompoundDirectObject():            yield from eCompoundOrDirectObject() | eCompoundAndDirectObject()
def eCompoundOrDirectObject():          yield from eDirectObject() + (π(σ(',')) + σ('or') + eCompoundOrDirectObject() | ε())
def eCompoundAndDirectObject():         yield from eDirectObject() + (π(σ(',')) + σ('and') + eCompoundAndDirectObject() | ε())
#   An indirect object is a noun or pronoun that appears with a direct object and names the person
#   or thing that something is given to or done for. A compound indirect object is two or more
#   nouns or pronouns that appear with a direct object and name the people or things that
#   something is given to or done for. An indirect object never follows the word "to" or "for".
def eCompoundIndirectObject():          yield from eCompoundOrIndirectObject() | eCompoundAndIndirectObject()
def eCompoundOrIndirectObject():        yield from eIndirectObject() + (π(σ(',')) + σ('or') + eCompoundOrIndirectObject() | ε())
def eCompoundAndIndirectObject():       yield from eIndirectObject() + (π(σ(',')) + σ('and') + eCompoundAndIndirectObject() | ε())
#   A compound predicate nominative is two or more nouns or pronouns that follow a linking verb
#   and rename the subject of the sentence. A compound predicate adjective is two or more
#   adjectives that follow a linking verb and describe the subject of the sentence.
def eCompoundPredicateNominative():     yield from eCompoundOrPredicateNominative() | eCompoundAndPredicateNominative()
def eCompoundOrPredicateNominative():   yield from ePredicateNominative() + (π(σ(',')) + σ('or') + eCompoundOrPredicateNominative() | ε())
def eCompoundAndPredicateNominative():  yield from ePredicateNominative() + (π(σ(',')) + σ('and') + eCompoundAndPredicateNominative() | ε())
def eCompoundPredicateAdjective():      yield from eCompoundOrPredicateAdjective() | eCompoundAndPredicateAdjective()
def eCompoundOrPredicateAdjective():    yield from ePredicateAdjective() + (π(σ(',')) + σ('or') + eCompoundOrPredicateAdjective() | ε())
def eCompoundAndPredicateAdjective():   yield from ePredicateAdjective() + (π(σ(',')) + σ('and') + eCompoundAndPredicateAdjective() | ε())
#===================================================================================================
#   PHRASES
#   A phrase is a group of words, without a subject and verb, that acts as one part of speech.
def eModifiedNoun():            yield from eAdjectivalPhrase() + eNoun() | eGerundivePhrase()
def eModifiedNoun():            yield from \
                                ( (eAdjectives() | ε())
                                + (eNoun() (eNoun() (eNoun() | ε()) | ε()) | ε())
                                + eNoun()
                                + (eAdjectivePhrase() | ε())
                                )
def eModifiedPronoun():         yield from (eAdjectives() | ε()) + ePronoun() + (eAdjectivePhrase() | ε())
def eModifiedNounOrPronoun():   yield from (eModifiedNoun() | eModifiedPronoun())
def eNounModifier():            yield from \
                                ( eAdjectives()
                                | eNoun()
#                               | eParticipialPhrase()
#                               | eInfinitivePhrase()
#                               | eModifyingClause()
#                               | ePrepositionalPhrase()
                                )
def eModifyingClause():         yield '?'
def eVerbPhrase():              yield from eAdverbialPhrase() + eDictVerb()
#   An adjective phrase is a prepositional phrase that modifies a noun or pronoun by telling what
#   kind or which one.
def eAdjectivePhrase():         yield from ePrepositionalPhrase()
#   An adverb phrase is a prepositional phrase that modifies a verb, adjective, or adverb by
#   pointing out where, when, in what manner, or to what extent.
def eAdverbPhrase():            yield from ePrepositionalPhrase()
#   An appositive is a noun or pronoun placed next to another noun or pronoun to identify, rename,
#   or explain it.  An appositive phrase is an appositive with modifiers.
def eAppositive():              yield from eNoun() | ePronoun()
def eAppositivePhrase():        yield from eModifiedNoun()
#   A compound appositive is two or more appositives or appositive phrases connected by a
#   conjunction and used to identify the same noun or pronoun.
def eCompoundAppositive():      yield from eCompoundOrAppositive() | eCompoundAndAppositive()
def eCompoundOrAppositive():    yield from (eAppositive() | eAppositivePhrase()) \
                                         + (π(σ(',')) + σ('or') + eCompoundOrAppositive() | ε())
def eCompoundAndAppositive():   yield from (eAppositive() | eAppositivePhrase()) \
                                         + (π(σ(',')) + σ('and') + eCompoundAndAppositive() | ε())
#   A participle is a form of a verb that acts as an adjective and modifies a noun or pronoun. A
#   verb phrase always begins with a helping verb, but a participle acting as an adjective stands
#   by itself.
def eParticiple():              yield from eDictVerb()
#   A participial phrase is a participle modified by an adverb or adverb phrase or accompanied by
#   a complement. The entire phrase acts as an adjective.
def eParticipialPhrase():       yield from eParticiple() (eAdverb() | eAdverbPhrase())
#   A gerund is a form of a verb that acts like a noun. Words ending in "-ing" that act as nouns
#   are gerunds. They do not have helping verbs, nor do they act as adjectives.
def eGerund():                  yield from ePresentParticipleVerb()
#   A gerund phrase is a gerund with modifiers or a complement, all acting together as a noun. The
#   possessive form of a noun or pronoun is used before a gerund.
def eGerundPhrase():            yield from eGerund() (eModifiers() | eComplements())
#   An infinitive is a form of a verb that comes after the word "to" and acts as a noun,
#   adjective, or adverb. A prepositional phrase always ends with a noun or pronoun. An infinitive
#   always ends with a verb.
def eInfinitive():              yield ""
#   An infinitive phrase is an infinitive with modifiers, complements, or a subject, all acting
#   together as a single part of speech. When an infinitive or infinitive phrase is used as the
#   direct object of certain verbs, "to" is often omitted.
def eInfinitivePhrase():        yield from eInfinitive() + eRootVerb() + σ('to') + (eModifiers() | eComplements() | ε())
#   A prepositional phrase is a group of words that includes a preposition and a noun or pronoun
#   called the object of the preposition.
#def ePrepositionalPhrase():     yield from \
#                                ( σ('in rem')
#                                | ( σ('of') + σ('less') + σ('than')
#                                  | σ('of') + σ('more') + σ('than')
#                                  | ePreposition()
#                                  ) eModifiedNounOrPronoun()
#                                )
def eAbsolutePhrase():    yield ""             
def eAppositivePhrase():  yield from σ(',') + (eModifiedNoun() | eGerundPhrase() | eInfinitivePhrase()) + σ(',')
def eAbsolutePhrase():    yield from (eNoun() | ePronoun()) + eModifiers() + eParticiple()
def eParticipialPhrase(): yield from (ePresentParticipleVerb() | ePastParticipleVerb()) + (eModifiers() | eComplements())
#---------------------------------------------------------------------------------------------------

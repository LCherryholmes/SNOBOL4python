# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint
#-----------------------------------------------------------------------------------------------------------------------
space =             SPAN(' ')
white =             SPAN(' ')
whitespace =        SPAN(' ')
μ =                 FENCE(space | ε())
η =                 FENCE(whitespace | ε())
def ς(s):           return η + σ(s)
#-----------------------------------------------------------------------------------------------------------------------
eWordSegment =      SPAN(UCASE+LCASE)
eWordSegments =     eWordSegment + FENCE(σ('-') + ζ("eWordSegments") | ε())
eWord =             eWordSegment + FENCE(σ('-') + eWordSegments | ε())
eUnknownWord =      eWord @ "tx" + Λ(lambda: notmatch(eWords, σ('/') + (σ(tx) | σ(tx.lower())) + σ('/')))
eKnownWord =        eWord @ "tx" + Λ(lambda: match(eWords,    σ('/') + (σ(tx) | σ(tx.lower())) + σ('/')))
eDQString =         σ('"') + BREAK('"') + σ('"')
eSQString =         σ("`") + BREAK("'") + σ("'") | σ("'") + BREAK("'") + σ("'")
eNumber =           SPAN('0123456789')
#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------
def ReadDict(): pass
def CideText(): pass
def Lexicon(P, v): pass
#-----------------------------------------------------------------------------------------------------------------------
dictionary = dict()
ReadDict()
CideText()
#del dictionary['A']
#del dictionary['As']
#del dictionary['In']
#del dictionary['les']
#del dictionary['unde']
#del dictionary['i']
Lexicon(eWord, eWords)
#=======================================================================================================================
#                                   NOUNS
#                                   A noun is the name of a person, place, or thing. Some of the things nouns name can
#                                   be seen or touched; some cannot. A compound noun is a noun that is made up of more
#                                   than one word either separated, hyphenated, or combined.
eNoun =                             ( ζ("ePersonNoun")
                                    | ζ("ePlaceNoun")
                                    | ζ("eThingNoun")
                                    | ζ("eTimeNoun")
                                    | ζ("eProperNoun")
                                    | ζ("eDictNoun")
                                    )
eDictNoun =                         ( eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + σ(' ')
                                    + eWord @ "eW3"  + Λ(lambda: EngIsNoun(eW1+' '+eW2+' '+eW3))
                                    | eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + Λ(lambda: EngIsNoun(eW1+' '+eW2))
                                    | eWord @ "eWrd" + Λ(lambda: EngIsNoun(eWrd))
                                    )
ePersonNoun =                       ( σ('Shakespear')
                                    | σ('William')
                                    | σ('Winifred')
                                    )
ePlaceNoun =                        ( σ('Alaska')
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
eParens =                           σ('(') + BREAK('()') + σ(')')
eThingNoun =                        ( σ('Advisory Council on Historic Preservation')
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
                                    | eNumber
                                    | σ('$') + eNumber + ARBNO(σ(',') + eNumber)
                                    | (σ('Title') | σ('title')) + σ(' ') + eNumber
                                    | (σ('Paragraph') | σ('paragraph')) + σ(' ') + eParens
                                    | (σ('Paragraphs') | σ('paragraphs')) + σ(' ')
                                      + ARBNO(eParens) + (σ('and') | σ('or')) + ARBNO(eParens)
                                    | (σ('Section') | σ('section')) + σ(' ') + eNumber + ARBNO(eParens)
                                    | (σ('Subsection') | σ('subsection')) + σ(' ') + ARBNO(eParens)
                                    | (σ('Subchapter') | σ('subchapter'))
                                    | (σ('Subclause') | σ('subclause'))
                                    | (σ('Subparagraph') | σ('subparagraph')) + σ(' ') + ARBNO(eParens)
                                    | (σ('Subparagraph') | σ('subparagraph'))
                                    | (σ('Subparagraphs') | σ('subparagraphs'))
                                    | σ('order')
                                    | σ('through') + σ(' ') + σ('route')
                                    )
eDayOfWeek =                        ( σ('Monday')
                                    | σ('Tuesday')
                                    | σ('Wednesday')
                                    | σ('Thursday')
                                    | σ('Friday')
                                    | σ('Saturday')
                                    | σ('Sunday')
                                    )
eMonth =                            ( σ('January')
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
eTimeNoun =                         ( eWordSegment @ "tx" + Λ(lambda: match(tx, POS(0) + eMonth + RPOS(0))) + σ(' ') + eNumber + σ(', ') + eNumber
                                    | eWordSegment @ "tx" + Λ(lambda: match(tx, POS(0) + eMonth + RPOS(0))) + (σ(' ') + eNumber | ε())
                                    | eWordSegment @ "tx" + Λ(lambda: match(tx, POS(0) + eDayOfWeek + RPOS(0)))
                                    | σ('year ') + eNumber
                                    )
eSeparatedNoun =                    ε()
eHyphenatedNoun =                   ε()
eCombinedNoun =                     ε()
#                                   A common noun names any one of a class of people, places, or things. A proper noun names a
#                                   specific person, place, or thing. Proper nouns take capitals.
eCommonNoun =                       ε()
eProperNoun =                       σ('co-chairs') | σ('demonstration program')
eCountNouns =                       ζ("eSingularCountNoun") | ζ("ePluralCountNoun")
eSingularCountNoun =                ε()
ePluralCountNoun =                  ε()
eMassNouns =                        ε()
eCollectiveNoun =                   ε()
#=======================================================================================================================
#                                   PRONOUNS
#                                   A pronoun is a word used to take the place of a noun. The noun a pronoun substitutes
#                                   for is called an antecedent. Personal pronouns refer to (1) the person speaking,
#                                   (2) the person spoken to, or (3) the person, place, or thing spoken about.
ePronoun =                          ( ζ("ePersonalPronoun")
                                    | ζ("eReflexiveIntensivePronoun")
                                    | ζ("eDemonstrativePronoun")
                                    | ζ("eRelativePronoun")
                                    | ζ("eInterrogativePronoun")
                                    | ζ("eIndefinitePronoun")
                                    | ζ("eReciprocalPronoun")
                                    )
ePersonalPronoun =                  ( ζ("eSubjectPersonalPronoun")
                                    | ζ("ePossessivePersonalPronoun")
                                    | ζ("eObjectPersonalPronoun")
                                    )
eSubjectPersonalPronoun =           σ('I') | σ('you') | σ('he') |σ('she') | σ('it') | σ('we') | σ('they')
ePossessivePersonalPronoun =        σ('mine') | σ('yours') | σ('his') | σ('hers') | σ('its') | σ('ours') | σ('theirs')
eObjectPersonalPronoun =            σ('me') | σ('you') | σ('him') | σ('her') | σ('it') | σ('us') | σ('them')
#                                   A reflexive pronoun ends in "-self" or "-selves" and adds information to a sentence
#                                   by pointing back to a noun or pronoun that appears earlier in the sentence. An
#                                   intensive pronoun has the same ending as a reflexive pronoun but simply adds emphasis
#                                   to a noun or pronoun in the same sentence.
eReflexiveIntensivePronoun =        ( σ('myself')
                                    | σ('yourself')
                                    | σ('himself')
                                    | σ('herself')
                                    | σ('itself')
                                    | σ('oneself')
                                    | σ('ourselves')
                                    | σ('yourselves')
                                    | σ('themselves')
                                    )
#                                   A demonstrative pronoun directs attention to a specific person, place, or thing. A
#                                   relative pronoun begins a subordinate clause and connects it to another idea in the
#                                   sentence. An interrogative pronoun is used to begin a question.
eDemonstrativePronoun =             σ('this') | σ('that') | σ('these') | σ('those')
eRelativePronoun =                  σ('that') | σ('which') | σ('who') | σ('whom') | σ('whose') # σ('when') σ('where') σ('why')
eInterrogativePronoun =             σ('who') | σ('whom') | σ('why') | σ('what')
#                                   Indefinite pronouns refer to people, places, or things, often without specifying
#                                   which ones. Some indefinite pronouns may have an antecedent, but many do not have a
#                                   specific antecedent.
eIndefinitePronoun =                ( ζ("eIndefiniteSingularPronoun")
                                    | ζ("eIndefinitePluralPronoun")
                                    | ζ("eIndefiniteEitherPronoun")
                                    )
eIndefiniteSingularPronoun =        ( σ('another')
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
eIndefinitePluralPronoun =          ( σ('both')
                                    | σ('few')
                                    | σ('many')
                                    | σ('others')
                                    | σ('several')
                                    )
eIndefiniteEitherPronoun =          ( σ('all')
                                    | σ('any')
                                    | σ('less')
                                    | σ('more')
                                    | σ('most')
                                    | σ('none')
                                    | σ('some')
                                    )
eReciprocalPronoun =                σ('each other') | σ('one another')
#=======================================================================================================================
#                                   VERBS
#                                   A verb is a word that expresses time while showing an action, a condition, or the
#                                   fact that something exists. An action verb is a verb that tells what action someone
#                                   or something is performing. An action verb may show mental action as well as visible
#                                   action. An action verb is transitive if it directs action toward someone or
#                                   something. An action verb is intransitive if it does not direct action toward
#                                   someone or something.
#                                   1. simple present,             simple past,             simple future
#                                   2. present continuous,         past continuous,         future continuous
#                                   3. present perfect,            past perfect,            future perfect
#                                   4. present perfect continuous, past perfect continuous, future perfect continuous
eDictVerb =                         ( eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + σ(' ')
                                    + eWord @ "eW3"  + Λ(lambda: EngIsVerb(eW1+' '+eW2+' '+eW3))
                                    | eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + Λ(lambda: EngIsVerb(eW1+' '+eW2))
                                    | eWord @ "eWrd" + Λ(lambda: EngIsVerb(eWrd))
                                    | σ('reappointed')
                                    | σ('redelegated')
                                    )
eTransitiveVerb =                   ε()
eIntransitiveVerb =                 ε()
eMainVerb =                         eTransitiveVerb | eIntransitiveVerb
eModalVerb =                        ( σ('can')         | σ('can')    + σ('not')
                                    | σ('could')       | σ('could')  + σ('not')
                                    | σ('may')         | σ('may')    + σ('not')
                                    | σ('might')       | σ('might')  + σ('not')
                                    | σ('shall')       | σ('shall')  + σ('not')
                                    | σ('should')      | σ('should') + σ('not')
                                    | σ('will')        | σ('will')   + σ('not')
                                    | σ('would')       | σ('would')  + σ('not')
                                    )
#                                   A linking verb is a verb that connects a word at or near the beginning of a
#                                   sentence with a word at or near the end. In English, the most common linking verb
#                                   is some form of "be". Other verbs may be used in the same was as "be" to link two
#                                   parts of a sentence.
eLinkingVerb =                      ( σ('appear')
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
#                                   Helping verbs are verbs that can be added to another verb to make a single verb
#                                   phrase. Any of the many forms of "be" as well as some other common verbs can be
#                                   used as helping verbs.
eHelpingVerb =                      ( σ('do')     + σ('not') | σ('do')
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
eFormOfBEVerb =                     ( σ('am')     + σ('not')                         | σ('am')
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
eAuxiliaryVerb =                    σ('be') | σ('do') | σ('have')
eDitransitiveVerb =                 σ('cause') | σ('give')
eFiniteVerb =                       ε()
eNonFiniteVerb =                    ε()
eActivityVerb =                     ε()
eProcessVerb =                      ε()
eBodilySensationVerb =              ε()
eTransitionalEventVerb =            ε()
eMomentaryVerb =                    ε()
eCognitionVerb =                    ε()
eRelationalVerb =                   ε()
eStativeVerb =                      eCognitionVerb | eRelationalVerb
eDynamicVerb =                      ( eActivityVerb
                                    | eProcessVerb
                                    | eBodilySensationVerb
                                    | eTransitionalEventVerb
                                    | eMomentaryVerb
                                    )
eVerb =                             ( eModalVerb
                                    | eModalVerb + eDictVerb
                                    | eLinkingVerb
                                    | eFormOfBEVerb
                                    | eFormOfBEVerb + eDictVerb
                                    | eHelpingVerb + eDictVerb
#                                   | σ('made') + eDictAdjective
                                    )
#=======================================================================================================================
#                                   ADJECTIVES
eDictAdjective =                    ( eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + σ(' ')
                                    + eWord @ "eW3"  + Λ(lambda: EngIsAdj(eW1+' '+eW2+' '+eW3))
                                    | eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + Λ(lambda: EngIsAdj(eW1+' '+eW2))
                                    | eWord @ "eWrd" + Λ(lambda: EngIsAdj(eWrd))
                                    )
eArticle =                          σ('a') | σ('an') | σ('the')
eIntensifier =                      σ('quite') | σ('rather') | σ('such')
eMultiplier =                       σ('double') | σ('twice') | σ('four times') | σ('five times')
eFractionionalExpression =          σ('one-third') | σ('three-quarters')
ePredeterminer =                    eMultiplier | eFractionionalExpression | σ('both') | σ('half') | σ('all')
#                                   A noun used as an adjective answers the question "What kind?" or "Which one?" about
#                                   a noun that follows it. A proper adjective is a proper noun used as an adjective or
#                                   an adjective formed from a proper noun. A compound adjective is an adjective made up
#                                   of more than one word.
eNounAdjective =                    ε()
eProperAdjective =                  σ("?")
eCompoundAdjective =                ε()
#                                   A pronoun is used as an adjective if it modifies a noun. A personal pronoun used as
#                                   a possesssive adjective answers the question "Which one?" about a noun that follows
#                                   it.
ePossessiveAdjective =              ( σ('my')
                                    | σ('your')
                                    | σ('his')
                                    | σ('her')
                                    | σ('its')
                                    | σ('our')
                                    | σ('their')
                                    | σ("children's")
                                    )
#                                   A demonstrative, interrogative, or indefinite pronoun used as an adjective anwers
#                                   the question "Which one?", "How many?", or "How much?" about the noun that follows
#                                   it.
eDemonstrativeAdjective =           σ('this') | σ('that') | σ('these') | σ('those')
eInterrogativeAdjective =           σ('what') | σ('which') | σ('whose')
eIndefiniteAdjective =              ( σ('all')
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
eDescriptiveAdjective =             ( σ('agency-specific')
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
                                    | eNumber + σ('-year')
                                    )
eNumericalAdjective =               ( σ('four')
                                    | σ('five')
                                    | σ('five hundred')
                                    | σ('fourth')
                                    | σ('one')
                                    | σ('ten')
                                    | σ('three')
                                    | σ('two')
                                    | σ('zero')
                                    | σ('thousand')
                                    | eNumber
                                    )
eAdjective =                        ( eArticle
                                    | eIntensifier
                                    | ePredeterminer
                                    | eDemonstrativeAdjective
                                    | eDescriptiveAdjective
                                    | eIndefiniteAdjective
                                    | eNumericalAdjective
                                    | ePossessiveAdjective
                                    | eProperAdjective
                                    | eDictAdjective
                                    )
eAdjectives =                       eAdjective + (ζ("eAdjectives") | ε())
#=======================================================================================================================
#                                   ADVERBS
#                                   An adverb is a word that modifies a verb, an adjective, or another adverb. An adverb
#                                   modifying a verb answers the question "Where?", "When?", "In what manner?", or
#                                   "To what extent?". An adverb modifying an adjective answers only one question:
#                                   "To what extent?". An adverb modifying another adverb also answers just one
#                                   question: "To what extent?".
eAdverb =                           ( eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + σ(' ')
                                    + eWord @ "eW3"  + Λ(lambda: EngIsAdv(eW1+' '+eW2+' '+eW3))
                                    | eWord @ "eW1"  + σ(' ')
                                    + eWord @ "eW2"  + Λ(lambda: EngIsAdv(eW1+' '+eW2))
                                    | eWord @ "eWrd" + Λ(lambda: EngIsAdv(eWrd))
                                    )
eAdverbs =                          eAdverb + (ζ("eAdverbs") | ε())
#=======================================================================================================================
#                                   PREPOSITIONS
#                                   A preposition is a word that relates a noun or pronoun that appears with it to
#                                   another word in the sentence. The choice of preposition affects the way the other
#                                   words in a sentence relate to each other.
ePreposition =                      ( σ('about')
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
#=======================================================================================================================
#                                   CONJUNCTIONS
eCoordinatingConjunction =          ( σ('and')
                                    | σ('or')
                                    | σ('for')
                                    | σ('nor')
                                    | σ('so')
                                    | σ('but')
                                    | σ('yet')
                                    )
eSubordinatingConjunction =         ( σ('after')
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
eCorrelativeConjunctions =          ( σ('both') + σ('and')
                                    | σ('not only') + σ('but also')
                                    | σ('not') + σ('but')
                                    | σ('either') + σ('or')
                                    | σ('neither') + σ('nor')
                                    | σ('whether') + σ('or')
                                    | σ('as') + σ('as')
                                    )
eConjunction =                      ( eCoordinatingConjunction
                                    | eSubordinatingConjunction
                                    )
#=======================================================================================================================
#                                   INTERJECTIONS
eConjunctiveAdverb =                ( σ('however')
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
eInterjection =                     ε()
#=======================================================================================================================
#                                   PHRASES
#                                   A phrase is a group of words, without a subject and verb, that acts as one part of
#                                   speech. A prepositional phrase is a group of words that includes a preposition and
#                                   a noun or pronoun called the object of the preposition.
eModifiedNoun =                     ζ("eAdjectivePhrase") + eNoun | ζ("eGerundivePhrase")
eModifiedNoun =                     ( (eAdjectives | ε())
                                    + (eNoun + (eNoun + (eNoun | ε()) | ε()) | ε())
                                    + eNoun
                                    + (ζ("eAdjectivePhrase") | ε())
                                    )
eModifiedPronoun =                  (eAdjectives | ε()) + ePronoun + (ζ("eAdjectivePhrase") | ε())
eModifiedNounOrPronoun =            (eModifiedNoun | eModifiedPronoun)
ePrepositionalPhrase =              ( σ('in rem')
                                    | ( σ('of') + σ('less') + σ('than')
                                      | σ('of') + σ('more') + σ('than')
                                      | ePreposition
                                      ) + eModifiedNounOrPronoun
                                    )
eAdjectivalPhrase =                 eAdjectives | ePrepositionalPhrase | ζ("eParticipialPhrase")
ePredicateAdjective =               eAdjective | eAdjectivalPhrase
eNounModifier =                     ( eAdjectives
                                    | eNoun
#                                   | eParticipialPhrase
#                                   | eInfinitivePhrase
#                                   | eModifyingClause
#                                   | ePrepositionalPhrase
                                    )
eModifyingClause =                  σ("?")
eVerbPhrase =                       ζ("eAdverbialPhrase") + eDictVerb
#                                   An adjective phrase is a prepositional phrase that modifies a noun or pronoun by
#                                   telling what kind or which one.
eAdjectivePhrase =                  ePrepositionalPhrase
#                                   An adverb phrase is a prepositional phrase that modifies a verb, adjective, or
#                                   adverb by pointing out where, when, in what manner, or to what extent.
eAdverbPhrase =                     ePrepositionalPhrase
#                                   An appositive is a noun or pronoun placed next to another noun or pronoun to
#                                   identify, rename, or explain it.  An appositive phrase is an appositive with
#                                   modifiers.
eAppositive =                       eNoun | ePronoun
eAppositivePhrase =                 eModifiedNoun
#                                   A compound appositive is two or more appositives or appositive phrases connected by
#                                   a conjunction and used to identify the same noun or pronoun.
eCompoundOrAppositive =             (eAppositive | eAppositivePhrase) + (π(σ(',')) + σ('or') + ζ("eCompoundOrAppositive") | ε())
eCompoundAndAppositive =            (eAppositive | eAppositivePhrase) + (π(σ(',')) + σ('and') + ζ("eCompoundAndAppositive") | ε())
eCompoundAppositive =               eCompoundOrAppositive | eCompoundAndAppositive
#                                   A participle is a form of a verb that acts as an adjective and modifies a noun or
#                                   pronoun. A verb phrase always begins with a helping verb, but a participle acting
#                                   as an adjective stands by itself.
eParticiple =                       eDictVerb
#                                   A participial phrase is a participle modified by an adverb or adverb phrase or
#                                   accompanied by a complement. The entire phrase acts as an adjective.
eParticipialPhrase =                eParticiple + (eAdverb | eAdverbPhrase)
#                                   A gerund is a form of a verb that acts like a noun. Words ending in "-ing" that act
#                                   as nouns are gerunds. They do not have helping verbs, nor do they act as adjectives.
ePresentParticipleVerb =            σ('?')
eGerund =                           ePresentParticipleVerb
#                                   A gerund phrase is a gerund with modifiers or a complement, all acting together as
#                                   a noun. The possessive form of a noun or pronoun is used before a gerund.
eModifiers =                        σ('?')
eComplements =                      σ('?')
eGerundPhrase =                     eGerund + (eModifiers | eComplements)
#                                   An infinitive is a form of a verb that comes after the word "to" and acts as a
#                                   noun, adjective, or adverb. A prepositional phrase always ends with a noun or
#                                   pronoun. An infinitive always ends with a verb.
eInfinitive =                       ε()
#                                   An infinitive phrase is an infinitive with modifiers, complements, or a subject,
#                                   all acting together as a single part of speech. When an infinitive or infinitive
#                                   phrase is used as the direct object of certain verbs, "to" is often omitted.
eRootVerb =                         σ('?')
eInfinitivePhrase =                 eInfinitive + eRootVerb + σ('to') + (eModifiers | eComplements | ε())
eAbsolutePhrase =                   ε()
eAppositivePhrase =                 σ(',') + (eModifiedNoun | eGerundPhrase | eInfinitivePhrase) + σ(',')
eAbsolutePhrase =                   (eNoun | ePronoun) + eModifiers + eParticiple
ePastParticipleVerb =               σ('?')
eParticipialPhrase =                (ePresentParticipleVerb | ePastParticipleVerb) + (eModifiers | eComplements)
#=======================================================================================================================
eAdverbialPhrase =                  eAdverb | ePrepositionalPhrase
eModifiedVerb =                     ( eAdverbs + eDictVerb
                                    | eDictVerb + (eAdverbialPhrase | σ('only') | ε())
                                    )
eIndirectObject =                   eModifiedNounOrPronoun
eDirectObject =                     eModifiedNounOrPronoun
#                                   A predicate nominative is a noun or pronoun that follows a linking verb and renames,
#                                   identifies, or explains the subject of a sentence. A predicate adjective is an
#                                   adjective that follows a linking verb and describes the subject of the sentence.
ePredicateNominative =              eModifiedNoun | eModifiedPronoun
#                                   An objective complement is an adjective, noun, or group of words acting as a noun
#                                   that follows a direct object and describes or renames it.
eObjectiveComplement =              eAdjective | eModifiedNoun
eObjectiveComplement =              eNoun | eAdjective
#                                   A compound verb is two or more verbs that have the same subject and are joined by a
#                                   conjunction such as "and" or "or".
eCompoundOrVerb =                   eDictVerb + ((σ(',') + π(σ('or'))  | σ('or'))  + ζ("eCompoundOrVerb") | ε())
eCompoundAndVerb =                  eDictVerb + ((σ(',') + π(σ('and')) | σ('and')) + ζ("eCompoundAndVerb") | ε())
eCompoundVerb =                     ( eAdverbs
                                    + (eCompoundOrVerb | eCompoundAndVerb)
                                    | (eCompoundOrVerb | eCompoundAndVerb)
                                    + (eAdverbialPhrase | ε())
                                    )
#                                   Sentences can be:
#                                   Simple: One independent clause (subject or verb or both may be compound)
#                                   Compound: Two or more independent clauses
#                                   Complex: One independent clause and one or more subordinate clauses
#                                   Compound-Complex: Two or more independent clauses and one or more subordinate
#                                   clauses.
eIndependentClause =                ζ("eCompoundSubject") + eCompoundVerb
eSimpleSentence =                   eIndependentClause
eCompoundAndClauses =               eIndependentClause + (π(σ(',')) + σ('and') + ζ("eCompoundAndClauses") | ε())
eCompoundOrClauses =                eIndependentClause + (π(σ(',')) + σ('or')  + ζ("eCompoundOrClauses") | ε())
eCompoundSentence =                 ( eIndependentClause
                                    + (  π(σ(',')) + σ('and') + eCompoundAndClauses
                                      |  π(σ(',')) + σ('or')  + eCompoundOrClauses
                                      )
                                    )
eSubordinateClause =                ( eRelativePronoun
                                    + (  eFormOfBEVerb + eModifiedNoun
                                      |  eDictVerb + eModifiedNoun
                                      )
                                    | eSubordinatingConjunction
                                    + ( eAdjective
                                      | eDictVerb + eModifiedNoun
                                      )
                                    )
eSubordinateClauses =               eSubordinateClause + (π(σ(',')) + ζ("eSubordinateClauses") | ε())
eComplexSentence =                  eIndependentClause + eSubordinateClauses
eCompoundAndSentences =             eComplexSentence   + (π(σ(',')) + σ('and') + ζ("eCompoundAndSentences") | ε())
eCompoundOrSentences =              eComplexSentence   + (π(σ(',')) + σ('or')  + ζ("eCompoundOrSentences") | ε())
eCompoundComplexSentence =          ( eComplexSentence
                                    + (  π(σ(',')) + σ('and') + eCompoundAndSentences
                                      |  π(σ(',')) + σ('or')  + eCompoundOrSentences
                                      )
                                    )
eSubject =                          eModifiedNounOrPronoun
ePredicate =                        ( eModifiedVerb
                                    + ( eDirectObject + (eObjectiveComplement | ε())
                                      | eIndirectObject + eDirectObject
                                      | ε()
                                      )
                                    | (eLinkingVerb | eFormOfBEVerb)
                                    + (eAdverbs | ε())
                                    + (ePredicateNominative | ePredicateAdjective)
                                    )
#                                   A compound subject is two or more subjects that have the same verb and are joined by a
#                                   conjunction such as "and" or "or".
eCompoundOrSubject =                eSubject + ((σ(',') + π(σ('or'))  | σ('or'))  + ζ("eCompoundOrSubject") | ε())
eCompoundAndSubject =               eSubject + ((σ(',') + π(σ('and')) | σ('and')) + ζ("eCompoundAndSubject") | ε())
eCompoundSubject =                  eCompoundOrSubject | eCompoundAndSubject
#                                   The complete subject is the entire noun phrase, including the head noun and any modifiers
#                                   (e.g., "the" and "few") of that noun, that occurs in subject position in a sentence.
#                                   The simple subject is the essential noun, pronoun, or group of words acting as a noun that
#                                   cannot be left out of the complete subject. The simple predicate is the essential verb or verb
#                                   phrase that cannot be left out of the complete predicate.
eCompleteSubject =                  eCompoundSubject # eSubject #
eCompletePredicate =                ePredicate
#                                   SENTENCE
#                                   The two fundamental parts of every English sentence are the complete subject and the
#                                   predicate.  The complete subject is normally the topic of the sentence, and the predicate is
#                                   what is asserted of that topic.
eCompleteSentence =                 eCompleteSubject + eCompletePredicate + σ('.')
#-----------------------------------------------------------------------------------------------------------------------
#                                   A direct object is a noun, pronoun, or group of words acting as a noun that receives
#                                   the action of a transitive verb. A compound direct object is more that one direct
#                                   object that receives the action of the same transitive verb. A direct object is
#                                   never the noun or pronoun at the end of a prepositional phrase.
eCompoundOrDirectObject =           eDirectObject + (π(σ(',')) + σ('or') + ζ("eCompoundOrDirectObject") | ε())
eCompoundAndDirectObject =          eDirectObject + (π(σ(',')) + σ('and') + ζ("eCompoundAndDirectObject") | ε())
eCompoundDirectObject =             eCompoundOrDirectObject | eCompoundAndDirectObject
#-----------------------------------------------------------------------------------------------------------------------
#                                   An indirect object is a noun or pronoun that appears with a direct object and names
#                                   the person or thing that something is given to or done for. A compound indirect
#                                   object is two or more nouns or pronouns that appear with a direct object and name
#                                   the people or things that something is given to or done for. An indirect object
#                                   never follows the word "to" or "for".
eCompoundOrIndirectObject =         eIndirectObject + (π(σ(',')) + σ('or') + ζ("eCompoundOrIndirectObject") | ε())
eCompoundAndIndirectObject =        eIndirectObject + (π(σ(',')) + σ('and') + ζ("eCompoundAndIndirectObject") | ε())
eCompoundIndirectObject =           eCompoundOrIndirectObject | eCompoundAndIndirectObject
#-----------------------------------------------------------------------------------------------------------------------
#                                   A compound predicate nominative is two or more nouns or pronouns that follow a
#                                   linking verb and rename the subject of the sentence. A compound predicate
#                                   adjective is two or more adjectives that follow a linking verb and describe the
#                                   subject of the sentence.
eCompoundOrPredicateNominative =    ePredicateNominative + (π(σ(',')) + σ('or') + ζ("eCompoundOrPredicateNominative") | ε())
eCompoundAndPredicateNominative =   ePredicateNominative + (π(σ(',')) + σ('and') + ζ("eCompoundAndPredicateNominative") | ε())
eCompoundPredicateNominative =      eCompoundOrPredicateNominative | eCompoundAndPredicateNominative
eCompoundOrPredicateAdjective =     ePredicateAdjective + (π(σ(',')) + σ('or') + ζ("eCompoundOrPredicateAdjective") | ε())
eCompoundAndPredicateAdjective =    ePredicateAdjective + (π(σ(',')) + σ('and') + ζ("eCompoundAndPredicateAdjective") | ε())
eCompoundPredicateAdjective =       eCompoundOrPredicateAdjective | eCompoundAndPredicateAdjective
#-----------------------------------------------------------------------------------------------------------------------
# There are six basic sentence patterns in English. The patterns differ on the basis of what type of complement
# structure they have within the predicate.
# The first pattern is the simplest -- one without a verb complement, as verb complements are defined in traditional
# grammar.
# The second pattern has as its defining characteristic the presence of a direct object.
#   Direct objects are noun phrases that come after the verb.
# The third pattern has as its defining characteristic the presence of both indirect and direct objects.
#   Indirect objects do always come immediately after the verb.
# The fourth pattern has as its defining characteristic the presence of a predicate nominative verb complement.
#   The predicate nominative is a noun or a pronoun that redefines, renames, or classifies the subject of the sentence.
#   The verb in a predicate nominative construction is always a linking verb, such as be, seem, or become.
# The fifth pattern has as its defining characteristic the presence of a predicate adjective verb complement.
#   The predicate adjective is an adjective that characterizes the subject of the sentence.
#   The verb in a predicate adjective construction, like the verb in a predicate nominative construction,
#   is always a linking verb, such as be, seem, smell, look, taste, or become.
# The sixth pattern has as its defining characteristic the presence as verb complements of both a direct object
#   and an objective complement.
#   We met the direct object earlier.
#   An objective complement is a noun or djective that occurs after the direct object and describes the direct object.
eBasicSentence =                    ( eSubject + eVerb
                                    | eSubject + eVerb + eDirectObject
                                    | eSubject + eVerb + eIndirectObject + eDirectObject
                                    | eSubject + eLinkingVerb + ePredicateNominative
                                    | eSubject + eLinkingVerb + ePredicateAdjective
                                    | eSubject + eVerb + eDirectObject + eObjectiveComplement
                                    )
#-----------------------------------------------------------------------------------------------------------------------
#   Sentences can also be classified by their function.
#   Declarative: States and idea. Ends in a period.
#   Interrogative: Asks a question. Ends in a question mark.
#   Imperative: Gives an order or a direction. Ends in a period or an exclamation mark.
#   Exclamatory: Conveys strong emotion.  Ends in an exclamation mark.
ePlaySentence = \
( ( eCompleteSubject + σ('has') + eModifiedNoun
  | eCompleteSubject + eModalVerb + eDictVerb
  | eCompleteSubject + eModalVerb + eDictVerb + eModifiedNoun
  | eCompleteSubject + eModalVerb + eDictVerb + ePreposition + eNoun
  | eCompleteSubject + eDictVerb + eModifiedNoun
  | eCompleteSubject + eDictVerb + ePrepositionalPhrase
  | eCompleteSubject + eFormOfBEVerb + eModifiedNoun
  | eCompleteSubject + eFormOfBEVerb + eModifiedNoun + eModifiedNoun
  | eCompleteSubject + eFormOfBEVerb + eModifiedVerb
  | eCompleteSubject + eFormOfBEVerb + eAdjective
  | eCompleteSubject + eFormOfBEVerb + ePrepositionalPhrase
  | eCompleteSubject + eFormOfBEVerb + eDictVerb + σ('as') + eDictVerb
  | eCompleteSubject + eFormOfBEVerb + eDictVerb + σ('to') + σ('be') + eAdjective
  | eCompleteSubject + eFormOfBEVerb + eDictVerb + eAdverb + σ('to') + eDictVerb + eModifiedNoun
  | eCompleteSubject + ePrepositionalPhrase + eFormOfBEVerb + eModifiedNoun
  | eCompleteSubject + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + σ('have') + eModifiedNoun
  | eCompleteSubject + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + eDictVerb + eModifiedNoun
  | eCompleteSubject + (σ('shall') | σ('must') | σ('does')) + (σ('not') | ε()) + eDictVerb + ePrepositionalPhrase
  | σ('there') + eFormOfBEVerb + eModifiedNoun
  )
+ σ('.')
)
#-----------------------------------------------------------------------------------------------------------------------

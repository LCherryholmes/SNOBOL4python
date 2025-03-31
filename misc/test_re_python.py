# -*- coding: utf-8 -*-
import SNOBOL4python
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
def RegRx():                yield from POS(0) + Expr() + RPOS(0)
def Expr():                 yield from Term() + ARBNO(σ('|') + Term())
def Term():                 yield from Factor() + ARBNO(Factor())
def Factor():               yield from Match() | Group() | Anchor() | Backreference()
def Match():                yield from MatchItem() + (Quantifier() | ε())
def MatchItem():            yield from σ('.') | CharacterSet() | CharacterClass() | UnicodeClass() | Character()
def Group():                yield from σ('(') + (σ('?:') | ε()) + Expr() + σ(')') + (Quantifier() | ε())
def Anchor():               yield from σ('\\A') | σ('^') | σ('\\b') | σ('\\B') | σ('$') | σ('\\Z')
def Backreference():        yield from σ('\\') + Integer()
def Quantifier():           yield from σ('*')  | σ('+')  | σ('?')
                                     | σ('*?') | σ('+?') | σ('??')
                                     | σ('*+') | σ('++') | σ('?+')
                                     | σ('{') + Integer() + (σ(',') + (Integer() | ε()) | ε()) + σ('}')
#------------------------------------------------------------------------------
def CharacterSet():         yield from σ('[') + (σ('^') | ε()) + CharacterSetItems() σ(']')
def CharacterSetItems():    yield from CharacterSetItem() ARBNO(CharacterSetItem())
def CharacterSetItem():     yield from CharacterClass() \
                                     | UnicodeClass() \
                                     | CharacterRange() \
                                     | Character()
def CharacterRange():       yield from Character() + (σ('-') + Character() | ε())
def CharacterClass():       yield from σ('\\d') | σ('\\D') | σ('\\s') | σ('\\S') | σ('\\w') | σ('\\W')
def UnicodeClass():         yield from σ('\\p{') + Letters() + σ('}')
#------------------------------------------------------------------------------
def Integer():              yield from SPAN('0123456789')
def Letters():              yield from SPAN(UCASE + LCASE)
def EscapeCharacter():      yield from σ('\\a') | σ('\\b') | σ('\\f') | σ('\\n') | σ('\\N') \
                                     | σ('\\r') | σ('\\t') | σ('\\v') | σ('\\x') \
                                     | σ('\\\\') | σ('\\^') | σ('\\$')
def Character():            yield from σ('\u0009') \
                                     | σ('\u000A') \
                                     | σ('\u000D') \
                                     | ANY(σ('\u0020'), σ('\uD7FF')) \
                                     | ANY(σ('\uE000'), σ('\uFFFD')) \
                                     | ANY(σ('\U00010000'), σ('\U0010FFFF'))
#------------------------------------------------------------------------------
# meta characterd: . ^ $ * + ? { } [ ] \\ | ( )
# . ^ $
# {m}
# {m,n}
# {m,n}?
# {m,n}+
# [...]
# (...)
# (?...)
# (?aiLmsux)
# (?:...)
# (?aiLmsux-imsx:...)
# (?>...)
# (?P<name>...)
# (?P=name)
# (?#...)
# (?=...)
# (?!...)
# (?<=...)
# (?<!...)
# (?(id/name)yes-pattern|no-pattern)
# \\number
# \\A \\b \\B \\d \\D \\s \\S \\w \\W \\Z
# \\. \\^ \\$ \\* \\+ \\? \\{ \\} \\[ \\] \\\\ \\| \\( \\)

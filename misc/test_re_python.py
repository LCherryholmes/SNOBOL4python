# -*- coding: utf-8 -*-
import SNOBOL4python
#------------------------------------------------------------------------------
# Parse Regular Expression language
#------------------------------------------------------------------------------
RegRx =             POS(0) + Expr + RPOS(0)
Expr =              Term + ARBNO(σ('|') + Term)
Term =              Factor + ARBNO(Factor)
Factor =            Match | Group | Anchor | Backreference
Match =             MatchItem + (Quantifier | ε())
MatchItem =         σ('.') | CharacterSet | CharacterClass | UnicodeClass | Character
Group =             σ('(') + (σ('?:') | ε()) + Expr + σ(')') + (Quantifier | ε())
Anchor =            σ('\\A') | σ('^') | σ('\\b') | σ('\\B') | σ('$') | σ('\\Z')
Backreference =     σ('\\') + Integer
Quantifier =        σ('*')  | σ('+')  | σ('?') \
                  | σ('*?') | σ('+?') | σ('??') \
                  | σ('*+') | σ('++') | σ('?+') \
                  | σ('{') + Integer + (σ(',') + (Integer | ε()) | ε()) + σ('}')
#------------------------------------------------------------------------------
CharacterSet =      σ('[') + (σ('^') | ε()) + CharacterSetItems σ(']')
CharacterSetItems = CharacterSetItem ARBNO(CharacterSetItem)
CharacterSetItem =  CharacterClass \
                  | UnicodeClass \
                  | CharacterRange \
                  | Character
CharacterRange =    Character + (σ('-') + Character | ε())
CharacterClass =    σ('\\d') | σ('\\D') | σ('\\s') | σ('\\S') | σ('\\w') | σ('\\W')
UnicodeClass =      σ('\\p{') + Letters + σ('}')
#------------------------------------------------------------------------------
Integer =           SPAN('0123456789')
Letters =           SPAN(UCASE + LCASE)
EscapeCharacter =   σ('\\a') | σ('\\b') | σ('\\f') | σ('\\n') | σ('\\N') \
                  | σ('\\r') | σ('\\t') | σ('\\v') | σ('\\x') \
                  | σ('\\\\') | σ('\\^') | σ('\\$')
Character =         σ('\u0009') \
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

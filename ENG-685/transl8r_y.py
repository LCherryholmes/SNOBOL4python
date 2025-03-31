# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import ALPHABET, UCASE, LCASE, DIGITS
from SNOBOL4python import ε, σ, π, Λ, λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
#-------------------------------------------------------------------------------
@pattern
def blanks():           yield from  σ('\\\n') | SPAN(" \t\r\f")
@pattern
def white():            yield from  σ('\\\n') | SPAN(" \t\r\f\n")
@pattern
def cStyleComment():    yield from  σ('/*') + BREAKX('*') + σ('*/')
@pattern
def cppStyleComment():  yield from  σ('//') + BREAK("\n") + σ('\n')
@pattern
def space():            yield from  (   blanks()
                                    |   cStyleComment()
                                    |   cppStyleComment()
                                    ) + FENCE(space() | ε())
@pattern
def whitespace():       yield from  (   white()
                                    |   cStyleComment()
                                    |   cppStyleComment()
                                    ) + FENCE(whitespace() | ε())
#-------------------------------------------------------------------------------
@pattern
def μ():                yield from  FENCE(space() | ε())
@pattern
def η():                yield from  FENCE(whitespace() | ε())
@pattern
def ς(s):               yield from  η() + σ(s)
#-------------------------------------------------------------------------------
@pattern
def exponent():         yield from  ( (σ('E') | σ('e'))
                                    + (σ('+') | σ('-') | ε())
                                    + SPAN('0123456789')
                                    )
@pattern
def floatingLiteral():  yield from  ( SPAN('0123456789') 
                                      + σ('.') + (SPAN('0123456789') | ε())
                                      + (exponent() | ε())
                                      + (ANY('Ll') | ε())
                                    | σ('.') + SPAN('0123456789')
                                      + (exponent() | ε())
                                      + (ANY('Ll') | ε())
                                    | SPAN('0123456789') + exponent() + (ANY('Ll') | ε())
                                    | SPAN('0123456789') + (exponent() | ε()) + ANY('Ll')
                                    )
@pattern
def decimalLiteral():   yield from  ANY('123456789') + FENCE(SPAN('0123456789') | ε())
@pattern
def hexLiteral():       yield from  σ('0') + (σ('X') | σ('x')) + SPAN('0123456789ABCDEFabcdef')
@pattern
def octalLiteral():     yield from  σ('0') + FENCE(SPAN('01234567') | ε())
@pattern
def integerLiteral():   yield from  (decimalLiteral() | hexLiteral() | octalLiteral()) + (ANY('Ll') | ε())
@pattern
def escapedCharacter(): yield from  (   σ('\\')
                                    +   (  ANY('"\\abfnrtv\n' + "'")
                                        |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                                        |  ANY('0123') + ANY('01234567') + ANY('01234567')
                                        |  ANY('Xx') + SPAN('0123456789ABCDEFabcdef')
                                        )
                                    )
@pattern
def characterLiteral(): yield from  σ("'") + (escapedCharacter() | NOTANY("'\\\r\n")) + σ("'")
@pattern
def stringLiteral():    yield from  σ('"') + ARBNO(escapedCharacter() | BREAK('"\\\r\n')) + σ('"')
#-------------------------------------------------------------------------------
keywords = {
    'break', 'case', 'continue', 'default', 'delete', 'do', 
    'else', 'for', 'goto', 'if', 'left', 'new', 'prec', 'right',
    'struct', 'switch', 'token', 'type', 'union', 'while'
    }
@pattern
def ident():            yield from  ( ANY(UCASE + '_' + LCASE)
                                    + FENCE(SPAN(DIGITS + UCASE + '_' + LCASE) | ε())
                                    )
@pattern
def keyword():          yield from  ident() @ "tx" + Λ("tx in keywords")
@pattern
def identifier():       yield from  ident() @ "tx" + Λ("tx not in keywords")
@pattern
def resword():          yield from  ( σ('%')
                                    + SPAN(LCASE)
                                    + FENCE(σ('-') + SPAN(LCASE) | ε())
                                    | σ('#') + SPAN(LCASE)
                                    )
#-------------------------------------------------------------------------------
@pattern
def operator():         yield from  ( σ('->*') | σ('...') | σ('<<=') | σ('>>=')
                                    | σ('--') | σ('-=') | σ('->') | σ('::') | σ('!=')
                                    | σ('.*') | σ('*=') | σ('/=') | σ('&&') | σ('&=')
                                    | σ('%=') | σ('^=') | σ('++') | σ('+=') | σ('<<') 
                                    | σ('<=') | σ('==') | σ('>=') | σ('>>') | σ('|=')
                                    | σ('||')
                                    | σ('-') | σ(',') | σ(';') | σ(':') | σ('!')
                                    | σ('?') | σ('.') | σ('(') | σ(')') | σ('[')
                                    | σ(']') | σ('*') | σ('/') | σ('&') | σ('#')
                                    | σ('%') | σ('^') | σ('+') | σ('<') | σ('=')
                                    | σ('>') | σ('|') | σ('~')
                                    )
#-------------------------------------------------------------------------------
@pattern
def ζ(name):
    match name:
        case '$#':      yield from σ('$') + SPAN('0123456789')
        case '@#':      yield from σ('@') + SPAN('0123456789')
        case '$<>$':    yield from σ('$<') + ident() + σ('>$')
        case '$<>#':    yield from σ('$<') + ident() + σ('>') + SPAN('0123456789')
        case _:         raise Exception()
#-------------------------------------------------------------------------------
@pattern
def cBlock():           yield from  ς('{') + ARBNO(cBlockBody()) + ς('}')
@pattern
def cExpr():            yield from  ς('(') + ARBNO(cExprBody()) + ς(')')
@pattern
def cBlockBody():       yield from  cToken(True) | cBlock() | cExpr()
@pattern
def cExprBody():        yield from  cToken(True) | cExpr()
#-------------------------------------------------------------------------------
@pattern
def pct_block():        yield from  ς('%{') + ARBNO(cBlockBody()) + ς('%}')
@pattern
def pct_union():        yield from  ς('%union') + cBlock()
@pattern
def pct_type():         yield from  ς('%type') + ς('<') + η() + identifier() + ς('>') + η() + identifier()
@pattern
def pct_token():        yield from  ς('%token') + (ς('<') + η() + identifier() + ς('>') | ε()) + pct_token_names()
@pattern
def pct_token_names():  yield from  η() + pct_token_name() + FENCE(pct_token_names() | ε())
@pattern
def pct_token_name():   yield from  identifier() | characterLiteral()
@pattern
def pct_left():         yield from  ς('%left') + pct_token_names()
@pattern
def pct_right():        yield from  ς('%right') + pct_token_names()
@pattern
def pct_start():        yield from  ς('%start') + η() + identifier()
@pattern
def pct_parse_param():  yield from  ς('%parse-param') + cBlock()
@pattern
def pct_lex_param():    yield from  ς('%lex-param') + cBlock()
@pattern
def pct_expect():       yield from  ς('%expect') + η() + integerLiteral()
@pattern
def pct_define():       yield from  σ('%define') + η() + identifier() + ς('.') + identifier() + η() + identifier()
#-------------------------------------------------------------------------------
@pattern
def yProduction():      yield from  η() + identifier() % 'tx' + ς(':') + yAlternates()
@pattern
def yAlternates():      yield from  yyAlternates()
@pattern
def yyAlternates():     yield from  ySubsequents() + (ς('|') + yyAlternates() | ε())
@pattern
def ySubsequents():     yield from  yySubsequents() | ε()
@pattern
def yySubsequents():    yield from  yElement() + (yySubsequents() | ε())
@pattern
def yElement():         yield from  ( η() + identifier()
                                    | η() + characterLiteral()
                                    | cBlock()
                                    | ς('[') + ARBNO(cBlockBody()) + ς(']')
                                    | ς('%prec')
                                    | ς(';')
                                    )
@pattern
def yRecognizer():      yield from  ( ARBNO(
                                        pct_block()
                                      | pct_union()
                                      | pct_token()
                                      | pct_type()
                                      | pct_left()
                                      | pct_right()
                                      | pct_start()
                                      | pct_parse_param()
                                      | pct_lex_param()
                                      | pct_expect()
                                      | pct_define()
                                      )
                                    + ς('%%')
                                    + ARBNO(yProduction())
                                    + η() + RPOS(0)
                                    )
#-------------------------------------------------------------------------------
@pattern
def cTokens():
    yield from ARBNO(cToken())
#-------------------------------------------------------------------------------
@pattern
def cToken(blind):
    yield from (
    	η() +
        ( cStyleComment()     + λ("""P += "cStyleComment() + \"""" if not blind else None)
        | cppStyleComment()   + λ("""P += "cppStyleComment() + \"""" if not blind else None)
        | floatingLiteral()   + λ("""P += "floatingLiteral() + \"""" if not blind else None)
        | integerLiteral()    + λ("""P += "integerLiteral() + \"""" if not blind else None)
        | characterLiteral()  + λ("""P += "characterLiteral() + \"""" if not blind else None)
        | stringLiteral()     + λ("""P += "stringLiteral() + \"""" if not blind else None)
        | keyword() % "tx"    + λ("""P += "ς('" + tx + "') + \"""" if not blind else None)
        | identifier()        + λ("""P += "identifier() + \"""" if not blind else None)
        | σ('$$')             + λ("""P += "ς('$$') + \"""" if not blind else None)
        | ζ('$#')             + λ("""P += "ζ('$#') + \"""" if not blind else None)
        | ζ('@#')             + λ("""P += "ζ('@#') + \"""" if not blind else None)
        | ζ('$<>$')           + λ("""P += "ζ('$<>$') + \"""" if not blind else None)
        | ζ('$<>#')           + λ("""P += "ζ('$<>#') + \"""" if not blind else None)
        | operator() % "tx"   + λ("""P += "ς('" + tx + "') + \"""" if not blind else None)
        )
    )
#-------------------------------------------------------------------------------
@pattern
def yTokens():
    yield from  ( POS(0)                + λ("""P = "yield from (\\n\"""")
                + ARBNO(
                    σ('\\\n')           + λ("""P += "σ('\\\n') + \"""")
                  | σ('\n')             + λ("""P += "η() +\\n\"""")
                  | SPAN(" \t\r\f\n") # + λ("""P += "η() +\\n\"""")
                  | SPAN(" \t\r\f")     + λ("""P += "μ() + \"""")
                  | pct_union()         + λ("""P += "pct_union() + \"""")
                  | pct_token()         + λ("""P += "pct_token() + \"""")
                  | pct_type()          + λ("""P += "pct_type() + \"""")
                  | pct_left()          + λ("""P += "pct_left() + \"""")
                  | pct_right()         + λ("""P += "pct_right() + \"""")
                  | pct_start()         + λ("""P += "pct_start() + \"""")
                  | pct_block()         + λ("""P += "pct_block() + \"""")
                  | pct_parse_param()   + λ("""P += "pct_parse_param() + \"""")
                  | pct_lex_param()     + λ("""P += "pct_lex_param() + \"""")
                  | pct_expect()        + λ("""P += "pct_expect() + \"""")
                  | pct_define()        + λ("""P += "pct_define() + \"""")
                  | resword() % "tx"    + λ("""P += "σ('" + tx + "') + \"""")
                  | σ('%{')             + λ("""P += "σ('%{') + \"""")
                  | σ('%}')             + λ("""P += "σ('%}') + \"""")
                  | σ('%%')             + λ("""P += "σ('%%') + \"""")
                  | yProduction()       + λ("""P += "yProduction() + \"""")
                  | cBlock()            + λ("""P += "cBlock() + \"""")
                  | cToken(False)     # + λ("""P += "cToken() + \"""")
                  | σ('{')              + λ("""P += "σ('{') + \"""")
                  | σ('}')              + λ("""P += "σ('}') + \"""")
                  | σ('(')              + λ("""P += "σ('(') + \"""")
                  | σ(')')              + λ("""P += "σ(')') + \"""")
                  )
                + RPOS(0)               + λ("""P += ")\\n\"""")
                )
#-------------------------------------------------------------------------------

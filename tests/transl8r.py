# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, MARBNO, NOTANY, POS, RPOS, SPAN
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce
#-------------------------------------------------------------------------------
class Token(object):
    def __init__(self, patr, expr=None):
        self.patr = patr
        self.expr = expr
        self.seen = dict()
        if self.patr is not None and self.expr is None:
            if type(self.patr) is str:
                self.expr = (lambda: "σ(" + self.self.patr + ")")
                self.patr = σ(self.patr)
            elif type(self.patr).__name__ == 'PATTERN':
                self.expr = (lambda: self.patr.func.__name__ + "()")
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
def ς(s):               yield from η() + σ(s)
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
keywords = set(['break', 'case', 'continue', 'default', 'delete', 'do', 
                'else', 'for', 'goto', 'if', 'left', 'new', 'prec', 'right',
                'start', 'struct', 'switch', 'token', 'type', 'union', 'while'])
@pattern
def ident():            yield from  ( ANY(_UCASE + '_' + _LCASE) 
                                    + FENCE(SPAN(_DIGITS + _UCASE + '_' + _LCASE) | ε())
                                    )
@pattern
def keyword():          yield from  ident() @ "tx" + λ("tx in keywords")
@pattern
def identifier():       yield from  ident() @ "tx" + λ("tx not in keywords")
@pattern
def resword():          yield from  ( σ('%')
                                    + SPAN(_LCASE)
                                    + FENCE(σ('-') + SPAN(_LCASE) | ε())
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
def cBlockBody():       yield from  cToken() | cBlock() | cExpr()
@pattern
def cExprBody():        yield from  cToken() | cExpr()
#-------------------------------------------------------------------------------
@pattern
def pct_block():        yield from  ς('%{') + ARBNO(cBlockBody()) + ς('%}')
@pattern
def pct_union():        yield from  ς('%union') + ς('{') + ARBNO(cBlockBody()) + ς('}')
@pattern
def pct_type():         yield from  ς('%type') + ς('<') + η() + identifier() + ς('>') + MARBNO(η() + identifier())
@pattern
def pct_token():        yield from  ( ς('%token')
                                    + (ς('<') + η() + identifier() + ς('>') | ε())
                                    + Shift('')
                                    + nPush() + pct_token_names() + Reduce('re_spec') + nPop()
                                    + Reduce('re_production', 2)
                                    )
@pattern
def pct_token_names():  yield from  η() + pct_token_name() + nInc() + FENCE(pct_token_names() | ε())
@pattern
def pct_token_name():   yield from  (  (identifier()       % 'tx' + Shift('identifier', "tx")) + Shift('string')
                                    |  (characterLiteral() % 'tx' + Shift('identifier', "tx")) + Shift('string', "tx")
                                    ) + Reduce('re', 2)
@pattern
def pct_left():         yield from  ς('%left') + MARBNO(η() + (identifier() | characterLiteral()))
@pattern
def pct_right():        yield from  ς('%right') + MARBNO(η() + (identifier() | characterLiteral()))
@pattern
def pct_start():        yield from  ς('%start') + η() + identifier()
@pattern
def pct_parse_param():  yield from  ς('%parse-param') + cBlock()
@pattern
def pct_lex_param():    yield from  ς('%lex-param') + cBlock()
@pattern
def pct_expect():       yield from  ς('%expect') + integerLiteral()
#-------------------------------------------------------------------------------
@pattern
def yProduction():      yield from  ( η() + identifier() % 'tx' + Shift('identifier', "tx") + ς(':')
                                    + yAlternates()
                                    + Reduce('bnf_production', 2)
                                    )
@pattern
def yAlternates():      yield from  nPush() + yyAlternates() + Reduce('|') + nPop()
@pattern
def yyAlternates():     yield from  ySubsequents() + nInc() + (ς('|') + yyAlternates() | ε())
@pattern
def ySubsequents():     yield from  ( nPush() + (yySubsequents() | ε())
                                    + Reduce('epsilon')
                                    + Reduce('&')
                                    + nPop()
                                    )
@pattern
def yySubsequents():    yield from  yElement() + (yySubsequents() | ε())
@pattern
def yElement():         yield from  ( η() + identifier() + Shift('identifier', "tx") + nInc()
                                    | η() + characterLiteral() + Shift('string', "tx") + nInc()
                                    | cBlock()
                                    | ς('[') + ARBNO(cBlockBody()) + ς(']')
                                    | ς('%') + prec()
                                    | ς(';')
                                    )
@pattern
def yRecognizer():      yield from  ( nPush()
                                    + ARBNO(
                                        pct_block()
                                      | pct_union()
                                      | pct_token() + nInc()
                                      | pct_type()
                                      | pct_left()
                                      | pct_right()
                                      | pct_start()
                                      )
                                    + ς('%%')
                                    + ARBNO(yProduction() + nInc())
                                    + Reduce('productions')
                                    + nPop()
                                    + η() + RPOS(0)
                                    )
#-------------------------------------------------------------------------------
@pattern
def cTokens():
    yield from  ARBNO(cToken())
#-------------------------------------------------------------------------------
@pattern
def cToken():
    yield from  (  η() +
                  ( cStyleComment()       # + Λ("""P += "cStyleComment() + \"""")
                  | cppStyleComment()     # + Λ("""P += "cppStyleComment() + \"""")
                  | floatingLiteral()     # + Λ("""P += "floatingLiteral() + \"""")
                  | integerLiteral()      # + Λ("""P += "integerLiteral() + \"""")
                  | characterLiteral()    # + Λ("""P += "characterLiteral() + \"""")
                  | stringLiteral()       # + Λ("""P += "stringLiteral() + \"""")
                  | keyword() % "tx"      # + Λ("""P += "ς('" + tx + "') + \"""")
                  | identifier()          # + Λ("""P += "identifier() + \"""")
                  | σ('$$')               # + Λ("""P += "ς('$$') + \"""")
                  | ζ('$#')               # + Λ("""P += "ζ('$#') + \"""")
                  | ζ('@#')               # + Λ("""P += "ζ('@#') + \"""")
                  | ζ('$<>$')             # + Λ("""P += "ζ('$<>$') + \"""")
                  | ζ('$<>#')             # + Λ("""P += "ζ('$<>#') + \"""")
                  | operator() % "tx"     # + Λ("""P += "ς('" + tx + "') + \"""")
                  )
                )
#-------------------------------------------------------------------------------
@pattern
def yTokens():
    yield from  ( POS(0)                + Λ("""P = "yield from (\\n\"""")
                + ARBNO(
                    σ('\\\n')           + Λ("""P += "σ('\\\n') + \"""")
                  | σ('\n')             + Λ("""P += "η() +\\n\"""") 
                  | SPAN(" \t\r\f\n") # + Λ("""P += "η() +\\n\"""")
                  | SPAN(" \t\r\f")     + Λ("""P += "μ() + \"""")
                  | pct_union()         + Λ("""P += "pct_union() + \"""")
                  | pct_token()         + Λ("""P += "pct_token() + \"""")
                  | pct_type()          + Λ("""P += "pct_type() + \"""")
                  | pct_start()         + Λ("""P += "pct_start() + \"""")
                  | pct_block()         + Λ("""P += "pct_block() + \"""")
                  | resword() % "tx"    + Λ("""P += "σ('" + tx + "') + \"""")
                  | σ('%{')             + Λ("""P += "σ('%{') + \"""")
                  | σ('%}')             + Λ("""P += "σ('%}') + \"""")
                  | σ('%%')             + Λ("""P += "σ('%%') + \"""")
                  | cToken()            + Λ("""P += "cToken() + \"""")
                  | cBlock()            + Λ("""P += "cBlock() + \"""")
                  | σ('{')              + Λ("""P += "σ('{') + \"""")
                  | σ('}')              + Λ("""P += "σ('}') + \"""")
                  | σ('(')              + Λ("""P += "σ('(') + \"""")
                  | σ(')')              + Λ("""P += "σ(')') + \"""")
                  )
                + RPOS(0)               + Λ("""P += ")\\n\"""")
                )
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    yInput_nm = r"""C:\anaconda3\envs\rstudio\Library\mingw-w64\share\gettext\intl\plural.y"""
    yOutput_nm = r""".\plural-y.py"""
    GLOBALS(globals())
    with open(yInput_nm, "r") as yInput:
        y = yInput.read()
        if MATCH(y, yTokens()):
            with open(yOutput_nm, "w", encoding="utf-8") as yOutput:
                yOutput.write(P[:-3])
#----------------------------------------------------------------------------------------------------------------------

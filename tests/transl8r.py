# -*- coding: utf-8 -*-
import SNOBOL4python
from SNOBOL4python import pattern, MATCH, GLOBALS
from SNOBOL4python import _ALPHABET, _UCASE, _LCASE, _DIGITS
from SNOBOL4python import ε, σ, π, λ, Λ, θ
from SNOBOL4python import ANY, ARBNO, BREAK, BREAKX, FENCE
from SNOBOL4python import LEN, NOTANY, POS, RPOS, SPAN
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
def blanks():           yield from  (σ('\\\n') | SPAN(" \t\r\f"))
@pattern
def white():            yield from  (σ('\\\n') | SPAN(" \t\r\f\n"))
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
#-------------------------------------------------------------------------------
@pattern
def exponent():         yield from  ( (σ('E') | σ('e'))
                                    + (σ('+') | σ('-') | ε())
                                    + SPAN('0123456789')
                                    )
@pattern
def floatingLiteral():  yield from  (   SPAN('0123456789') 
                                      + σ('.') + (SPAN('0123456789') | ε())
                                      + (exponent() | ε())
                                      + (ANY('Ll') | ε())
                                    |   σ('.') + SPAN('0123456789')
                                      + (exponent() | ε())
                                      + (ANY('Ll') | ε())
                                    |   SPAN('0123456789') + exponent() + (ANY('Ll') | ε())
                                    |   SPAN('0123456789') + (exponent() | ε()) + ANY('Ll')
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
#-------------------------------------------------------------------------------
@pattern
def operator():         yield from  ( σ('-') | σ(',') | σ(';') | σ(':') | σ('!')
                                    | σ('?') | σ('.') | σ('(') | σ(')') | σ('[')
                                    | σ(']') | σ('*') | σ('/') | σ('&') | σ('#')
                                    | σ('%') | σ('^') | σ('+') | σ('<') | σ('=')
                                    | σ('>') | σ('|') | σ('~')
                                    | σ('--') | σ('-=') | σ('->') | σ('::') | σ('!=')
                                    | σ('.*') | σ('*=') | σ('/=') | σ('&&') | σ('&=')
                                    | σ('%=') | σ('^=') | σ('++') | σ('+=') | σ('<<') 
                                    | σ('<=') | σ('==') | σ('>=') | σ('>>') | σ('|=')
                                    | σ('||')
                                    | σ('->*') | σ('...') | σ('<<=') | σ('>>=')
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
def cBlock():           yield from  σ('{') + ARBNO(cBlockBody()) + σ('}')
@pattern
def cExpr():            yield from  σ('(') + ARBNO(cExprBody()) + σ(')')
@pattern
def cBlockBody():       yield from  cToken() | cBlock() | cExpr()
@pattern
def cExprBody():        yield from  cToken() | cExpr()
#-------------------------------------------------------------------------------
@pattern
def pct_block():        yield from  σ('%{') + ARBNO(cBlockBody()) + σ('%}')
@pattern
def pct_union():        yield from  σ('%') + union() + σ('{') + ARBNO(cBlockBody()) + σ('}')
@pattern
def pct_type():         yield from  σ('%') + type() + σ('<') + η() + identifier() + σ('>') + MARBNO(η() + identifier())
@pattern
def pct_token():        yield from  ( σ('%') + token()
                                    + (σ('<') + η() + identifier() + σ('>') | ε())
                                    + ε() + Shift('')
                                    + nPush() + pct_token_names() + Reduce('re_spec') + nPop()
                                    + Reduce('re_production', 2)
                                    )
@pattern
def pct_token_names():  yield from  η() + pct_token_name() + nInc() + FENCE(pct_token_names() | ε())
@pattern
def pct_token_name():   yield from  (  (identifier()       % 'tx' + Shift('identifier', "tx")) + ε() + Shift('string')
                                    |  (characterLiteral() % 'tx' + Shift('identifier', "tx")) + Shift('string', "tx")
                                    ) + Reduce('re', 2)
@pattern
def pct_left():         yield from  σ('%') + left() + MARBNO(η() + (identifier() | characterLiteral()))
@pattern
def pct_right():        yield from  σ('%') + right() + MARBNO(η() + (identifier() | characterLiteral()))
@pattern
def pct_start():        yield from  σ('%') + start() + η() + identifier()
#-------------------------------------------------------------------------------
@pattern
def yProduction():      yield from  ( η() + identifier() % 'tx' + Shift('identifier', "tx") +  σ(':')
                                    + yAlternates()
                                    + Reduce('bnf_production', 2)
                                    )
@pattern
def yAlternates():      yield from  nPush() + yyAlternates() + Reduce('|') + nPop()
@pattern
def yyAlternates():     yield from  ySubsequents() + nInc() + (σ('|') + yyAlternates() | ε())
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
                                    | σ('[') + ARBNO(cBlockBody()) + σ(']')
                                    | σ('%') + prec()
                                    | σ(';')
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
                                    + σ('%%')
                                    + ARBNO(yProduction() + nInc())
                                    + Reduce('productions')
                                    + nPop()
                                    + η() + RPOS(0)
                                    )
#-------------------------------------------------------------------------------
@pattern
def cTokens():          yield from  POS(0) + ARBNO(cToken()) + RPOS(0)
@pattern
def cToken():           yield from  ( θ("OUTPUT")
                                    + ( σ('\\\n')
                                      | SPAN(" \t\r\f\n")                          
                                      | SPAN(" \t\r\f")
                                      | cStyleComment()
                                      | cppStyleComment()
                                      | floatingLiteral()
                                      | integerLiteral()
                                      | characterLiteral()
                                      | stringLiteral()
                                      | keyword()
                                      | identifier()
                                      | σ('%{')
                                      | σ('%}')
                                      | σ('%%')
                                      | σ('$$')
                                      | ζ('$#')
                                      | ζ('@#')
                                      | ζ('$<>$')
                                      | ζ('$<>#')
                                      | operator()
                                      | σ('{')
                                      | σ('}')
                                      | σ('(')
                                      | σ(')')
                                      ) @ "OUTPUT"
                                    )
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    spcpfx = "η() + "
    tokens = [
#       Token(yRecognizer),
##      Token(yProduction),
#       Token(pct_union),
#       Token(pct_token),
#       Token(pct_type),
#       Token(pct_start),
        Token('\\\n',                 (lambda: "σ('\\\n')")),
        Token(SPAN(" \t\r\f\n"),      (lambda: "η()")),
        Token(SPAN(" \t\r\f"),        (lambda: "μ()")),
        Token(cStyleComment(),        (lambda: "cStyleComment()")),
        Token(cppStyleComment(),      (lambda: "cppStyleComment()")),
        Token(floatingLiteral(),      (lambda: 'floatingLiteral()')),
        Token(integerLiteral(),       (lambda: 'integerLiteral()')),
        Token(characterLiteral(),     (lambda: 'characterLiteral()')),
        Token(stringLiteral(),        (lambda: 'stringLiteral()')),
        Token(keyword() % "tx",       (lambda: "σ('" + tx + "')")),
        Token(identifier(),           (lambda: 'identifier()')),
        Token(identifier() % "tx",    (lambda: "σ('" + tx + "')")),
        Token('%{'),
        Token('%}'),
        Token('%%'),
        Token('$$'),
        Token(ζ('$#') % "tx",         (lambda: "ζ('$#')")),
        Token(ζ('@#') % "tx",         (lambda: "ζ('@#')")),
        Token(ζ('$<>$') % "tx",       (lambda: "ζ('$<>$')")),
        Token(ζ('$<>#') % "tx",       (lambda: "ζ('$<>#')")),
        Token(operator() % "tx",      (lambda: "σ('" + tx + "')")),
        Token('{'),
        Token('}'),
        Token('('),
        Token(')')
    ]
#----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
MATCH('{ Id_99 = "Hello"; }', cTokens())
#----------------------------------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
#-------------------------------------------------------------------------------
blanks =            σ('\\\n') | SPAN(" \t\r\f")
white =             σ('\\\n') | SPAN(" \t\r\f\n")
cStyleComment =     σ('/*') + BREAKX('*') + σ('*/')
cppStyleComment =   σ('//') + BREAK("\n") + σ('\n')
space =             (   blanks
                    |   cStyleComment
                    |   cppStyleComment
                    ) + FENCE(ζ(lambda: space) | ε())
whitespace =        (   white
                    |   cStyleComment
                    |   cppStyleComment
                    ) + FENCE(ζ(lambda: whitespace) | ε())
#-------------------------------------------------------------------------------
μ =                 FENCE(space | ε())
η =                 FENCE(whitespace | ε())
def ς(s):           return η + σ(s)
#-------------------------------------------------------------------------------
exponent =          ( (σ('E') | σ('e'))
                    + (σ('+') | σ('-') | ε())
                    + SPAN('0123456789')
                    )
floatingLiteral =   ( SPAN('0123456789')
                      + σ('.') + (SPAN('0123456789') | ε())
                      + (exponent | ε())
                      + (ANY('Ll') | ε())
                    | σ('.') + SPAN('0123456789')
                      + (exponent | ε())
                      + (ANY('Ll') | ε())
                    | SPAN('0123456789') + exponent + (ANY('Ll') | ε())
                    | SPAN('0123456789') + (exponent | ε()) + ANY('Ll')
                    )
decimalLiteral =    ANY('123456789') + FENCE(SPAN('0123456789') | ε())
hexLiteral =        σ('0') + (σ('X') | σ('x')) + SPAN('0123456789ABCDEFabcdef')
octalLiteral =      σ('0') + FENCE(SPAN('01234567') | ε())
integerLiteral =    (decimalLiteral | hexLiteral | octalLiteral) + (ANY('Ll') | ε())
escapedCharacter =  (   σ('\\')
                    +   (  ANY('"\\abfnrtv\n' + "'")
                        |  ANY('01234567') + FENCE(ANY('01234567') | ε())
                        |  ANY('0123') + ANY('01234567') + ANY('01234567')
                        |  ANY('Xx') + SPAN('0123456789ABCDEFabcdef')
                        )
                    )
characterLiteral =  σ("'") + (escapedCharacter | NOTANY("'\\\r\n")) + σ("'")
stringLiteral =     σ('"') + ARBNO(escapedCharacter | BREAK('"\\\r\n')) + σ('"')
#-------------------------------------------------------------------------------
keywords = {
    'break', 'case', 'continue', 'default', 'delete', 'do', 
    'else', 'for', 'goto', 'if', 'left', 'new', 'prec', 'right',
    'struct', 'switch', 'token', 'type', 'union', 'while'
    }
ident =             ( ANY(UCASE + '_' + LCASE)
                    + FENCE(SPAN(DIGITS + UCASE + '_' + LCASE) | ε())
                    )
keyword =           ident @ "tx" + Λ("tx in keywords")
identifier =        ident @ "tx" + Λ("tx not in keywords")
resword =           ( σ('%')
                    + SPAN(LCASE)
                    + FENCE(σ('-') + SPAN(LCASE) | ε())
                    | σ('#') + SPAN(LCASE)
                    )
#-------------------------------------------------------------------------------
operator =          ( σ('->*') | σ('...') | σ('<<=') | σ('>>=')
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
def τ(name):
    match name:
        case '$#':      return σ('$') + SPAN('0123456789')
        case '@#':      return σ('@') + SPAN('0123456789')
        case '$<>$':    return σ('$<') + ident + σ('>$')
        case '$<>#':    return σ('$<') + ident + σ('>') + SPAN('0123456789')
        case _:         raise Exception()
#-------------------------------------------------------------------------------
def cToken(blind):
    return  ( η +
              ( cStyleComment     + λ("""P += "cStyleComment + \"""" if not blind else None)
              | cppStyleComment   + λ("""P += "cppStyleComment + \"""" if not blind else None)
              | floatingLiteral   + λ("""P += "floatingLiteral + \"""" if not blind else None)
              | integerLiteral    + λ("""P += "integerLiteral + \"""" if not blind else None)
              | characterLiteral  + λ("""P += "characterLiteral + \"""" if not blind else None)
              | stringLiteral     + λ("""P += "stringLiteral + \"""" if not blind else None)
              | keyword % "tx"    + λ("""P += "ς('" + tx + "') + \"""" if not blind else None)
              | identifier        + λ("""P += "identifier + \"""" if not blind else None)
              | σ('$$')           + λ("""P += "ς('$$') + \"""" if not blind else None)
              | τ('$#')           + λ("""P += "τ('$#') + \"""" if not blind else None)
              | τ('@#')           + λ("""P += "τ('@#') + \"""" if not blind else None)
              | τ('$<>$')         + λ("""P += "τ('$<>$') + \"""" if not blind else None)
              | τ('$<>#')         + λ("""P += "τ('$<>#') + \"""" if not blind else None)
              | operator % "tx"   + λ("""P += "ς('" + tx + "') + \"""" if not blind else None)
              )
            )
#-------------------------------------------------------------------------------
cBlock =            ς('{') + ARBNO(ζ(lambda: cBlockBody)) + ς('}')
cExpr =             ς('(') + ARBNO(ζ(lambda: cExprBody)) + ς(')')
cBlockBody =        cToken(True) | cBlock | cExpr
cExprBody =         cToken(True) | cExpr
#-------------------------------------------------------------------------------
pct_block =         ς(r'%{') + ARBNO(cBlockBody) + ς(r'%}')
pct_union =         ς(r'%union') + cBlock
pct_type =          ς(r'%type') + ς('<') + η + identifier + ς('>') + η + identifier
pct_token_name =    identifier | characterLiteral
pct_token_names =   η + pct_token_name + FENCE(ζ(lambda: pct_token_names) | ε())
pct_token =         ς(r'%token') + (ς('<') + η + identifier + ς('>') | ε()) + pct_token_names
pct_left =          ς(r'%left') + pct_token_names
pct_right =         ς(r'%right') + pct_token_names
pct_start =         ς(r'%start') + η + identifier
pct_parse_param =   ς(r'%parse-param') + cBlock
pct_lex_param =     ς(r'%lex-param') + cBlock
pct_expect =        ς(r'%expect') + η + integerLiteral
pct_define =        σ(r'%define') + η + identifier + ς('.') + identifier + η + identifier
#-------------------------------------------------------------------------------
yElement =          ( η + identifier
                    | η + characterLiteral
                    | cBlock
                    | ς('[') + ARBNO(cBlockBody) + ς(']')
                    | ς('%prec')
                    | ς(';')
                    )
yySubsequents =     yElement + (ζ(lambda: yySubsequents) | ε())
ySubsequents =      yySubsequents | ε()
yyAlternates =      ySubsequents + (ς('|') + ζ(lambda: yyAlternates) | ε())
yAlternates =       yyAlternates
yProduction =       η + identifier % 'tx' + ς(':') + yAlternates
yRecognizer =       ( ARBNO(
                        pct_block
                      | pct_union
                      | pct_token
                      | pct_type
                      | pct_left
                      | pct_right
                      | pct_start
                      | pct_parse_param
                      | pct_lex_param
                      | pct_expect
                      | pct_define
                      )
                    + ς('%%')
                    + ARBNO(yProduction)
                    + η + RPOS(0)
                    )
#-------------------------------------------------------------------------------
cTokens = ARBNO(cToken(True))
#-------------------------------------------------------------------------------
yTokens =   ( POS(0)                + λ("""P = "yield from (\\n\"""")
            + ARBNO(
                σ('\\\n')           + λ("""P += "σ('\\\n') + \"""")
              | σ('\n')             + λ("""P += "η +\\n\"""")
              | SPAN(" \t\r\f\n") # + λ("""P += "η +\\n\"""")
              | SPAN(" \t\r\f")     + λ("""P += "μ + \"""")
              | pct_union           + λ("""P += "pct_union + \"""")
              | pct_token           + λ("""P += "pct_token + \"""")
              | pct_type            + λ("""P += "pct_type + \"""")
              | pct_left            + λ("""P += "pct_left + \"""")
              | pct_right           + λ("""P += "pct_right + \"""")
              | pct_start           + λ("""P += "pct_start + \"""")
              | pct_block           + λ("""P += "pct_block + \"""")
              | pct_parse_param     + λ("""P += "pct_parse_param + \"""")
              | pct_lex_param       + λ("""P += "pct_lex_param + \"""")
              | pct_expect          + λ("""P += "pct_expect + \"""")
              | pct_define          + λ("""P += "pct_define + \"""")
              | resword % "tx"      + λ("""P += "σ('" + tx + "') + \"""")
              | σ('%{')             + λ("""P += "σ('%{') + \"""")
              | σ('%}')             + λ("""P += "σ('%}') + \"""")
              | σ('%%')             + λ("""P += "σ('%%') + \"""")
              | yProduction         + λ("""P += "yProduction + \"""")
              | cBlock              + λ("""P += "cBlock + \"""")
              | cToken(False)     # + λ("""P += "cToken() + \"""")
              | σ('{')              + λ("""P += "σ('{') + \"""")
              | σ('}')              + λ("""P += "σ('}') + \"""")
              | σ('(')              + λ("""P += "σ('(') + \"""")
              | σ(')')              + λ("""P += "σ(')') + \"""")
              )
            + RPOS(0)               + λ("""P += ")\\n\"""")
            )
#-------------------------------------------------------------------------------

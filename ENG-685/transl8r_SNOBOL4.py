# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# 31 flavors of patterns to choose from ...
from SNOBOL4python import ε, σ, π, λ, Λ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCESS, TAB
from SNOBOL4python import GLOBALS, pattern
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def nl():           yield from  σ('\n')
@pattern
def Integer():      yield from  SPAN(DIGITS) % "tx"
@pattern
def DQ():           yield from  σ('"') + BREAK('"\n') + σ('"') % "tx"
@pattern
def SQ():           yield from  σ("'") + BREAK("'\n") + σ("'") % "tx"
@pattern
def String():       yield from  SQ() | DQ()
@pattern
def Real():         yield from  ( SPAN(DIGITS)
                                    + (σ('.') + FENCE(SPAN(DIGITS) | ε()) | ε())
                                    + (σ('E') | σ('e'))
                                    + (σ('+') | σ('-') | ε())
                                    + SPAN(DIGITS)
                                    | SPAN(DIGITS) + σ('.') + FENCE(SPAN(DIGITS) | ε())
                                    ) % "tx"
@pattern
def Id():           yield from  (ANY(UCASE+LCASE) + FENCE(SPAN('.'+DIGITS+UCASE+'_'+LCASE) | ε())) % "tx"
@pattern
def Gray():         yield from  White() | ε()
@pattern
def White():        yield from  (  SPAN(' \t') + FENCE(nl() + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε()) | ε())
                                |  nl() + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε())
                                )
#-----------------------------------------------------------------------------------------------------------------------
SpecialNms      =   { 'ABORT', 'CONTINUE', 'END', 'FRETURN', 'NRETURN', 'RETURN', 'SCONTINUE', 'START' }
BuiltinVars     =   { 'ABORT', 'ARB', 'BAL', 'FAIL', 'FENCE', 'INPUT', 'OUTPUT', 'REM', 'TERMINAL' }
ProtKwds        =   { 'ABORT', 'ALPHABET', 'ARB', 'BAL', 'FAIL', 'FENCE', 'FILE', 'FNCLEVEL',
                      'LASTFILE', 'LASTLINE', 'LASTNO', 'LCASE', 'LINE', 'REM', 'RTNTYPE',
                      'STCOUNT', 'STNO', 'SUCCEED', 'UCASE' }
UnprotKwds      =   { 'ABEND', 'ANCHOR', 'CASE', 'CODE', 'COMPARE', 'DUMP', 'ERRLIMIT',
                      'ERRTEXT', 'ERRTYPE', 'FTRACE', 'INPUT', 'MAXLNGTH', 'OUTPUT',
                      'PROFILE', 'STLIMIT', 'TRACE', 'TRIM', 'FULLSCAN' }
Functions       =   { 'ANY', 'APPLY', 'ARBNO', 'ARG', 'ARRAY', 'ATAN', 'BACKSPACE', 'BREAK', 'BREAKX',
                      'CHAR', 'CHOP', 'CLEAR', 'CODE', 'COLLECT', 'CONVERT', 'COPY', 'COS', 'DATA',
                      'DATATYPE', 'DATE', 'DEFINE', 'DETACH', 'DIFFER', 'DUMP', 'DUPL', 'EJECT',
                      'ENDFILE', 'EQ', 'EVAL', 'EXIT', 'EXP', 'FENCE', 'FIELD', 'GE', 'GT', 'HOST',
                      'IDENT', 'INPUT', 'INTEGER', 'ITEM', 'LE', 'LEN', 'LEQ', 'LGE', 'LGT', 'LLE',
                      'LLT', 'LN', 'LNE', 'LOAD', 'LOCAL', 'LPAD', 'LT', 'NE', 'NOTANY', 'OPSYN', 'OUTPUT',
                      'POS', 'PROTOTYPE', 'REMDR', 'REPLACE', 'REVERSE', 'REWIND', 'RPAD', 'RPOS',
                      'RSORT', 'RTAB', 'SET', 'SETEXIT', 'SIN', 'SIZE', 'SORT', 'SPAN', 'SQRT', 'STOPTR',
                      'SUBSTR', 'TAB', 'TABLE', 'TAN', 'TIME', 'TRACE', 'TRIM', 'UNLOAD' }
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Function():     yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in Functions))   + ")\\b")
@pattern
def BuiltinVar():   yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in BuiltinVars)) + ")\\b")
@pattern
def SpecialNm():    yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in SpecialNms))  + ")\\b")
@pattern
def ProtKwd():      yield from  φ("(?P<nm>&"   + "|".join((nm for nm in ProtKwds))    + ")\\b")
@pattern
def UnprotKwd():    yield from  φ("(?P<nm>&"   + "|".join((nm for nm in UnprotKwds))  + ")\\b")
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def ζ(op):
    match op:
        case '=':   yield from  White() + σ('=') + White()
        case '?':   yield from  White() + σ('?') + White()
        case '|':   yield from  White() + σ('|') + White()
        case '+':   yield from  White() + σ('+') + White()
        case '-':   yield from  White() + σ('-') + White()
        case '/':   yield from  White() + σ('/') + White()
        case '*':   yield from  White() + σ('*') + White()
        case '^':   yield from  White() + σ('^') + White()
        case '!':   yield from  White() + σ('!') + White()
        case '**':  yield from  White() + σ('**') + White()
        case '$':   yield from  White() + σ('$') + White()
        case '.':   yield from  White() + σ('.') + White()
        case '&':   yield from  White() + σ('&') + White()
        case '@':   yield from  White() + σ('@') + White()
        case '#':   yield from  White() + σ('#') + White()
        case '%':   yield from  White() + σ('%') + White()
        case '~':   yield from  White() + σ('~') + White()
        case ',':   yield from  Gray() + σ(',') + Gray()
        case '(':   yield from  σ('(') + Gray()
        case '[':   yield from  σ('[') + Gray()
        case '<':   yield from  σ('<') + Gray()
        case ')':   yield from  Gray() + σ(')')
        case ']':   yield from  Gray() + σ(']')
        case '>':   yield from  Gray() + σ('>')
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def ExprList():     yield from  ( nPush()
                                + XList()
                                + Reduce('ExprList', -1)
                                + nPop()
                                )
@pattern
def XList():        yield from  nInc() + (Expr() | Shift()) + FENCE(ζ(',') + XList() | ε())
@pattern
def Expr():         yield from  Expr0()
@pattern
def Expr0():        yield from  Expr1() + FENCE(ζ('=') + Expr0()  + Reduce('=', 2) | ε())
@pattern
def Expr1():        yield from  Expr2() + FENCE(ζ('?') + Expr1()  + Reduce('?', 2) | ε())
@pattern
def Expr2():        yield from  Expr3() + FENCE(ζ('&') + Expr2()  + Reduce('&', 2) | ε())
@pattern
def Expr3():        yield from  nPush() + X3()    + Reduce('|', -1)  + nPop()
@pattern
def X3():           yield from  nInc()  + Expr4() + FENCE(ζ('|')     + X3() | ε())
@pattern
def Expr4():        yield from  nPush() + X4()    + Reduce('..', -1) + nPop()
@pattern
def X4():           yield from  nInc()  + Expr5() + FENCE(White() + X4() | ε())
@pattern
def Expr5():        yield from  Expr6() + FENCE(ζ('@') + Expr5()  + Reduce('@', 2) | ε())
@pattern
def Expr6():        yield from  ( Expr7()
                                + FENCE(
                                    ζ('+') + Expr6() + Reduce('+', 2)
                                  | ζ('-') + Expr6() + Reduce('-', 2)
                                  | ε()
                                  )
                                )
@pattern
def Expr7():        yield from  Expr8()  + FENCE(ζ('#') + Expr7()  + Reduce('#', 2) | ε())
@pattern
def Expr8():        yield from  Expr9()  + FENCE(ζ('/') + Expr8()  + Reduce('/', 2) | ε())
@pattern
def Expr9():        yield from  Expr10() + FENCE(ζ('*') + Expr9()  + Reduce('*', 2) | ε())
@pattern
def Expr10():       yield from  Expr11() + FENCE(ζ('%') + Expr10() + Reduce('%', 2) | ε())
@pattern
def Expr11():       yield from  ( Expr12()
                                + FENCE(
                                    (ζ('^') | ζ('!') | ζ('**')) + Expr11() + Reduce('^', 2)
                                  | ε()
                                  )
                                )
@pattern
def Expr12():       yield from  ( Expr13()
                                + FENCE(
                                    ζ('$') + Expr12() + Reduce('$', 2)
                                  | ζ('.') + Expr12() + Reduce('.', 2)
                                  | ε()
                                  )
                                )
@pattern
def Expr13():       yield from  Expr14() + FENCE(ζ('~') + Expr13() + Reduce('~', 2) | ε())
@pattern
def Expr14():       yield from  ( σ('@') + Expr14() + Reduce('@', 1)
                                | σ('~') + Expr14() + Reduce('~', 1)
                                | σ('?') + Expr14() + Reduce('?', 1)
                                | ProtKwd()         + Shift('ProtKwd', "nm")
                                | UnprotKwd()       + Shift('UnprotKwd', "nm")
                                | σ('&') + Expr14() + Reduce('&', 1)
                                | σ('+') + Expr14() + Reduce('+', 1)
                                | σ('-') + Expr14() + Reduce('-', 1)
                                | σ('*') + Expr14() + Reduce('*', 1)
                                | σ('$') + Expr14() + Reduce('$', 1)
                                | σ('.') + Expr14() + Reduce('.', 1)
                                | σ('!') + Expr14() + Reduce('!', 1)
                                | σ('%') + Expr14() + Reduce('%', 1)
                                | σ('/') + Expr14() + Reduce('/', 1)
                                | σ('#') + Expr14() + Reduce('#', 1)
                                | σ('=') + Expr14() + Reduce('=', 1)
                                | σ('|') + Expr14() + Reduce('|', 1)
                                | Expr15()
                                )
@pattern
def Expr15():       yield from  Expr17() + FENCE(nPush() + Expr16() + Reduce('[]', -2) + nPop() | ε())
@pattern
def Expr16():       yield from  nInc() + (ζ('[') + ExprList() + ζ(']') | ζ('<') + ExprList() + ζ('>')) + FENCE(Expr16() | ε())
@pattern
def Expr17():       yield from  FENCE(
                                  ( nPush()
                                  + ζ('(') + Expr()
                                  + (  ζ(',') + XList() + Reduce(',', -2)
                                    |  ε() + Reduce('()', 1)
                                    )
                                  + ζ(')')
                                  + nPop()
                                  )
                                | Function()   % "tx" + Shift('Function', "nm") + ζ('(') + ExprList() + ζ(')') + Reduce('Call', 2)
                                | Id()         % "tx" + Shift('Id', "tx") + ζ('(') + ExprList() + ζ(')') + Reduce('Call', 2)
                                | BuiltinVar() % "tx" + Shift('BuiltinVar', "nm")
                                | SpecialNm()  % "tx" + Shift('SpecialNm', "nm")
                                | Id()         % "tx" + Shift('Id', "tx")
                                | String()     % "tx" + Shift('String', "tx")
                                | Real()       % "tx" + Shift('Real', "tx")
                                | Integer()    % "tx" + Shift('Integer', "tx")
                                )

@pattern
def SGoto():        yield from  (σ('S') | σ('s')) + λ("SorF = 'S'")
@pattern
def FGoto():        yield from  (σ('F') | σ('f')) + λ("SorF = 'F'")
@pattern
def SorF():         yield from  SGoto() | FGoto()
@pattern
def Target():       yield from  ( ζ('(') + λ("Brackets = '()'") + Expr() + ζ(')')
                                | ζ('<') + λ("Brackets = '<>'") + Expr() + ζ('>')
                                )
@pattern
def Goto():         yield from  ( Gray() + σ(':')
                                + Gray()
                                + FENCE(
                                    Target()                               + Reduce("*(':' + Brackets)", 1) + Shift()
                                  | SorF() + Target()                   + Reduce("*(':' SorF + Brackets)", 1)
                                  + FENCE(Gray() + SorF() + Target() + Reduce("*(':' SorF Brackets)", 1) | Shift())
                                  )
                                )
@pattern
def Control():      yield from  σ('-') + BREAK("\n;")
@pattern
def Comment():      yield from  σ('*') + BREAK("\n")
@pattern
def Label():        yield from  BREAK(' \t\n;') % "tx" + Shift('Label', "tx")
@pattern
def Stmt():         yield from  ( Label()
                                + ( White()
                                  + Expr14()
                                  + FENCE(
                                      Shift()
                                    + White()
                                    + ( σ('=') + Shift('=') + White() + Expr()
                                      | σ('=') + Shift('=') + Shift()
                                      )
                                    | (ζ('?') | White()) + Expr1()
                                    + FENCE(
                                        White()
                                      + ( σ('=') + Shift('=') + White() + Expr()
                                        | σ('=') + Shift('=') + Shift()
                                        )
                                      | Shift() + Shift()
                                      )
                                    |  Shift() + Shift() + Shift()
                                    )
                                  | Shift() + Shift() + Shift() + Shift()
                                  )
                                + FENCE(Goto() | Shift() + Shift())
                                + Gray()
                                )
@pattern
def Commands():     yield from  Command() + FENCE(Commands() | ε())
@pattern
def Command():      yield from  ( nInc()
                                + FENCE(
                                    Comment() + Shift('comment') + Reduce('Comment', 1) + nl()
                                  | Control() + Shift('control') + Reduce('Control', 1) + (nl() | σ(';'))
                                  | Stmt() + Reduce('Stmt', 7) + (nl() | σ(';'))
                                  )
                                )
@pattern
def Compiland():    yield from  ( POS(0)
                                + nPush()
                                + ARBNO(Command())
                                + Reduce('Parse', -1)
                                + ( φ(r'[Ee][Nn][Dd]\b') + BREAK("\n") + nl()
                                  + ARBNO(BREAK("\n") + nl())
                                  | ε()
                                  )
                                + nPop()
                                + Pop('SNOBOL4_tree')
                                + RPOS(0)
                                )
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Parse():        yield from  ( POS(0)
                                + nPush()
                                + ARBNO(Command())
                                + Reduce('Parse', -1)
                                + nPop()
                                + Pop('SNOBOL4_tree')
                                + RPOS(0)
                                )
str_snoParse = """\
    Parse           =             POS(0)
+                                 nPush()
+                                 ARBNO(*Command)
+                                 ("'Parse'" & 'nTop()')
+                                 nPop()
+                                 RPOS(0)
"""
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
if str_snoParse in Parse() % "OUTPUT":
    pprint(SNOBOL4_tree)
#-----------------------------------------------------------------------------------------------------------------------

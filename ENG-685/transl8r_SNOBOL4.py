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
def nl():               yield from  σ('\n')
@pattern
def snoInteger():       yield from  SPAN(DIGITS) % "tx"
@pattern
def snoDQ():            yield from  σ('"') + BREAK('"\n') + σ('"') % "tx"
@pattern
def snoSQ():            yield from  σ("'") + BREAK("'\n") + σ("'") % "tx"
@pattern
def snoString():        yield from  snoSQ() | snoDQ()
@pattern
def snoReal():          yield from  ( SPAN(DIGITS)
                                    + (σ('.') + FENCE(SPAN(DIGITS) | ε()) | ε())
                                    + (σ('E') | σ('e'))
                                    + (σ('+') | σ('-') | ε())
                                    + SPAN(DIGITS)
                                    | SPAN(DIGITS) + σ('.') + FENCE(SPAN(DIGITS) | ε())
                                    ) % "tx"
@pattern
def snoId():            yield from  (ANY(UCASE+LCASE) + FENCE(SPAN('.'+DIGITS+UCASE+'_'+LCASE) | ε())) % "tx"
@pattern
def snoGray():          yield from  snoWhite() | ε()
@pattern
def snoWhite():         yield from  (  SPAN(' \t') + FENCE(nl() + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε()) | ε())
                                    |  nl() + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε())
                                    )
#-----------------------------------------------------------------------------------------------------------------------
snoSpecialNms   =       { 'ABORT', 'CONTINUE', 'END', 'FRETURN', 'NRETURN', 'RETURN', 'SCONTINUE', 'START' }
snoBuiltinVars  =       { 'ABORT', 'ARB', 'BAL', 'FAIL', 'FENCE', 'INPUT', 'OUTPUT', 'REM', 'TERMINAL' }
snoProtKwds     =       { 'ABORT', 'ALPHABET', 'ARB', 'BAL', 'FAIL', 'FENCE', 'FILE', 'FNCLEVEL',
                          'LASTFILE', 'LASTLINE', 'LASTNO', 'LCASE', 'LINE', 'REM', 'RTNTYPE',
                          'STCOUNT', 'STNO', 'SUCCEED', 'UCASE' }
snoUnprotKwds   =       { 'ABEND', 'ANCHOR', 'CASE', 'CODE', 'COMPARE', 'DUMP', 'ERRLIMIT',
                          'ERRTEXT', 'ERRTYPE', 'FTRACE', 'INPUT', 'MAXLNGTH', 'OUTPUT',
                          'PROFILE', 'STLIMIT', 'TRACE', 'TRIM', 'FULLSCAN' }
snoFunctions    =       { 'ANY', 'APPLY', 'ARBNO', 'ARG', 'ARRAY', 'ATAN', 'BACKSPACE', 'BREAK', 'BREAKX',
                          'CHAR', 'CHOP', 'CLEAR', 'CODE', 'COLLECT', 'CONVERT', 'COPY', 'COS', 'DATA',
                          'DATATYPE', 'DATE', 'DEFINE', 'DETACH', 'DIFFER', 'DUMP', 'DUPL', 'EJECT',
                          'ENDFILE', 'EQ', 'EVAL', 'EXIT', 'EXP', 'FENCE', 'FIELD', 'GE', 'GT', 'HOST',
                          'IDENT', 'INPUT', 'INTEGER', 'ITEM', 'LE', 'LEN', 'LEQ', 'LGE', 'LGT', 'LLE',
                          'LLT', 'LN', 'LNE', 'LOAD', 'LOCAL', 'LPAD', 'LT', 'NE', 'NOTANY', 'OPSYN', 'OUTPUT',
                          'POS', 'PROTOTYPE', 'REMDR', 'REPLACE', 'REVERSE', 'REWIND', 'RPAD', 'RPOS',
                          'RSORT', 'RTAB', 'SET', 'SETEXIT', 'SIN', 'SIZE', 'SORT', 'SPAN', 'SQRT', 'STOPTR',
                          'SUBSTR', 'TAB', 'TABLE', 'TAN', 'TIME', 'TRACE', 'TRIM', 'UNLOAD' }
#-----------------------------------------------------------------------------------------------------------------------
if False:
    @pattern
    def snoFunction():    yield from  SPAN('.'+DIGITS+UCASE+'_'+LCASE)
    @pattern
    def snoBuiltinVar():  yield from  SPAN('.'+DIGITS+UCASE+'_'+LCASE)
    @pattern
    def snoSpecialNm():   yield from  SPAN('.'+DIGITS+UCASE+'_'+LCASE)
    @pattern
    def snoProtKwd():     yield from  σ('&') + SPAN(UCASE+LCASE)
    @pattern
    def snoUnprotKwd():   yield from  σ('&') + SPAN(UCASE+LCASE)
#-----------------------------------------------------------------------------------------------------------------------
if True:
    @pattern
    def snoFunction():    yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in snoFunctions))   + ")\\b")
    @pattern
    def snoBuiltinVar():  yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in snoBuiltinVars)) + ")\\b")
    @pattern
    def snoSpecialNm():   yield from  φ("\\b(?P<nm>" + "|".join((nm for nm in snoSpecialNms))  + ")\\b")
    @pattern
    def snoProtKwd():     yield from  φ("(?P<nm>&"   + "|".join((nm for nm in snoProtKwds))    + ")\\b")
    @pattern
    def snoUnprotKwd():   yield from  φ("(?P<nm>&"   + "|".join((nm for nm in snoUnprotKwds))  + ")\\b")
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def ζ(op):
    match op:
        case '=':       yield from  snoWhite() + σ('=') + snoWhite()
        case '?':       yield from  snoWhite() + σ('?') + snoWhite()
        case '|':       yield from  snoWhite() + σ('|') + snoWhite()
        case '+':       yield from  snoWhite() + σ('+') + snoWhite()
        case '-':       yield from  snoWhite() + σ('-') + snoWhite()
        case '/':       yield from  snoWhite() + σ('/') + snoWhite()
        case '*':       yield from  snoWhite() + σ('*') + snoWhite()
        case '^':       yield from  snoWhite() + σ('^') + snoWhite()
        case '!':       yield from  snoWhite() + σ('!') + snoWhite()
        case '**':      yield from  snoWhite() + σ('**') + snoWhite()
        case '$':       yield from  snoWhite() + σ('$') + snoWhite()
        case '.':       yield from  snoWhite() + σ('.') + snoWhite()
        case '&':       yield from  snoWhite() + σ('&') + snoWhite()
        case '@':       yield from  snoWhite() + σ('@') + snoWhite()
        case '#':       yield from  snoWhite() + σ('#') + snoWhite()
        case '%':       yield from  snoWhite() + σ('%') + snoWhite()
        case '~':       yield from  snoWhite() + σ('~') + snoWhite()
        case ',':       yield from  snoGray() + σ(',') + snoGray()
        case '(':       yield from  σ('(') + snoGray()
        case '[':       yield from  σ('[') + snoGray()
        case '<':       yield from  σ('<') + snoGray()
        case ')':       yield from  snoGray() + σ(')')
        case ']':       yield from  snoGray() + σ(']')
        case '>':       yield from  snoGray() + σ('>')
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def snoExprList():      yield from  ( nPush()
                                    + snoXList()
                                    + Reduce('snoExprList', -1)
                                    + nPop()
                                    )
@pattern
def snoXList():         yield from  nInc() + (snoExpr() | Shift()) + FENCE(ζ(',') + snoXList() | ε())
@pattern
def snoExpr():          yield from  snoExpr0()
@pattern
def snoExpr0():         yield from  snoExpr1() + FENCE(ζ('=') + snoExpr0()  + Reduce('=', 2) | ε())
@pattern
def snoExpr1():         yield from  snoExpr2() + FENCE(ζ('?') + snoExpr1()  + Reduce('?', 2) | ε())
@pattern
def snoExpr2():         yield from  snoExpr3() + FENCE(ζ('&') + snoExpr2()  + Reduce('&', 2) | ε())
@pattern
def snoExpr3():         yield from  nPush() + snoX3()    + Reduce('|', -1)  + nPop()
@pattern
def snoX3():            yield from  nInc()  + snoExpr4() + FENCE(ζ('|')     + snoX3() | ε())
@pattern
def snoExpr4():         yield from  nPush() + snoX4()    + Reduce('..', -1) + nPop()
@pattern
def snoX4():            yield from  nInc()  + snoExpr5() + FENCE(snoWhite() + snoX4() | ε())
@pattern
def snoExpr5():         yield from  snoExpr6() + FENCE(ζ('@') + snoExpr5()  + Reduce('@', 2) | ε())
@pattern
def snoExpr6():         yield from  ( snoExpr7()
                                    + FENCE(
                                        ζ('+') + snoExpr6() + Reduce('+', 2)
                                      | ζ('-') + snoExpr6() + Reduce('-', 2)
                                      | ε()
                                      )
                                    )
@pattern
def snoExpr7():         yield from  snoExpr8()  + FENCE(ζ('#') + snoExpr7()  + Reduce('#', 2) | ε())
@pattern
def snoExpr8():         yield from  snoExpr9()  + FENCE(ζ('/') + snoExpr8()  + Reduce('/', 2) | ε())
@pattern
def snoExpr9():         yield from  snoExpr10() + FENCE(ζ('*') + snoExpr9()  + Reduce('*', 2) | ε())
@pattern
def snoExpr10():        yield from  snoExpr11() + FENCE(ζ('%') + snoExpr10() + Reduce('%', 2) | ε())
@pattern
def snoExpr11():        yield from  ( snoExpr12()
                                    + FENCE(
                                        (ζ('^') | ζ('!') | ζ('**')) + snoExpr11() + Reduce('^', 2)
                                      | ε()
                                      )
                                    )
@pattern
def snoExpr12():        yield from  ( snoExpr13()
                                    + FENCE(
                                        ζ('$') + snoExpr12() + Reduce('$', 2)
                                      | ζ('.') + snoExpr12() + Reduce('.', 2)
                                      | ε()
                                      )
                                    )
@pattern
def snoExpr13():        yield from  snoExpr14() + FENCE(ζ('~') + snoExpr13() + Reduce('~', 2) | ε())
@pattern
def snoExpr14():        yield from  ( σ('@') + snoExpr14() + Reduce('@', 1)
                                    | σ('~') + snoExpr14() + Reduce('~', 1)
                                    | σ('?') + snoExpr14() + Reduce('?', 1)
                                    | snoProtKwd()         + Shift('snoProtKwd', "nm")
                                    | snoUnprotKwd()       + Shift('snoUnprotKwd', "nm")
                                    | σ('&') + snoExpr14() + Reduce('&', 1)
                                    | σ('+') + snoExpr14() + Reduce('+', 1)
                                    | σ('-') + snoExpr14() + Reduce('-', 1)
                                    | σ('*') + snoExpr14() + Reduce('*', 1)
                                    | σ('$') + snoExpr14() + Reduce('$', 1)
                                    | σ('.') + snoExpr14() + Reduce('.', 1)
                                    | σ('!') + snoExpr14() + Reduce('!', 1)
                                    | σ('%') + snoExpr14() + Reduce('%', 1)
                                    | σ('/') + snoExpr14() + Reduce('/', 1)
                                    | σ('#') + snoExpr14() + Reduce('#', 1)
                                    | σ('=') + snoExpr14() + Reduce('=', 1)
                                    | σ('|') + snoExpr14() + Reduce('|', 1)
                                    | snoExpr15()
                                    )
@pattern
def snoExpr15():        yield from  snoExpr17() + FENCE(nPush() + snoExpr16() + Reduce('[]', -2) + nPop() | ε())
@pattern
def snoExpr16():        yield from  nInc() + (ζ('[') + snoExprList() + ζ(']') | ζ('<') + snoExprList() + ζ('>')) + FENCE(snoExpr16() | ε())
@pattern
def snoExpr17():        yield from  FENCE(
                                      ( nPush()
                                      + ζ('(')
                                      + snoExpr()
                                      + (  ζ(',') + snoXList() + Reduce(',', -2)
                                        |  ε() + Reduce('()', 1)
                                        )
                                      + ζ(')')
                                      + nPop()
                                      )
                                    | snoFunction()   % "tx" + Shift('snoFunction', "nm") + ζ('(') + snoExprList() + ζ(')') + Reduce('snoCall', 2)
                                    | snoId()         % "tx" + Shift('snoId', "tx") + ζ('(') + snoExprList() + ζ(')') + Reduce('snoCall', 2)
                                    | snoBuiltinVar() % "tx" + Shift('snoBuiltinVar', "nm")
                                    | snoSpecialNm()  % "tx" + Shift('snoSpecialNm', "nm")
                                    | snoId()         % "tx" + Shift('snoId', "tx")
                                    | snoString()     % "tx" + Shift('snoString', "tx")
                                    | snoReal()       % "tx" + Shift('snoReal', "tx")
                                    | snoInteger()    % "tx" + Shift('snoInteger', "tx")
                                    )

@pattern
def snoSGoto():         yield from  (σ('S') | σ('s')) + λ("SorF = 'S'")
@pattern
def snoFGoto():         yield from  (σ('F') | σ('f')) + λ("SorF = 'F'")
@pattern
def snoSorF():          yield from  snoSGoto() | snoFGoto()
@pattern
def snoTarget():        yield from  ( ζ('(') + λ("snoBrackets = '()'") + snoExpr() + ζ(')')
                                    | ζ('<') + λ("snoBrackets = '<>'") + snoExpr() + ζ('>')
                                    )
@pattern
def snoGoto():          yield from  ( snoGray() + σ(':')
                                    + snoGray()
                                    + FENCE(
                                        snoTarget()                               + Reduce("*(':' + snoBrackets)", 1) + Shift()
                                      | snoSorF() + snoTarget()                   + Reduce("*(':' SorF + snoBrackets)", 1)
                                      + FENCE(snoGray() + snoSorF() + snoTarget() + Reduce("*(':' SorF snoBrackets)", 1) | Shift())
                                      )
                                    )
@pattern
def snoControl():       yield from  σ('-') + BREAK("\n;")
@pattern
def snoComment():       yield from  σ('*') + BREAK("\n")
@pattern
def snoLabel():         yield from  BREAK(' \t\n;') % "tx" + Shift('snoLabel', "tx")
@pattern
def snoStmt():          yield from  ( snoLabel()
                                    + ( snoWhite()
                                      + snoExpr14()
                                      + FENCE(
                                          Shift()
                                        + snoWhite()
                                        + ( σ('=') + Shift('=') + snoWhite() + snoExpr()
                                          | σ('=') + Shift('=') + Shift()
                                          )
                                        | (ζ('?') | snoWhite()) + snoExpr1()
                                        + FENCE(
                                            snoWhite()
                                          + ( σ('=') + Shift('=') + snoWhite() + snoExpr()
                                            | σ('=') + Shift('=') + Shift()
                                            )
                                          | Shift() + Shift()
                                          )
                                        |  Shift() + Shift() + Shift()
                                        )
                                      | Shift() + Shift() + Shift() + Shift()
                                      )
                                    + FENCE(snoGoto() | Shift() + Shift())
                                    + snoGray()
                                    )
@pattern
def snoCommands():      yield from  snoCommand() + FENCE(snoCommands() | ε())
@pattern
def snoCommand():       yield from  ( nInc()
                                    + FENCE(
                                        snoComment() + Shift('comment') + Reduce('snoComment', 1) + nl()
                                      | snoControl() + Shift('control') + Reduce('snoControl', 1) + (nl() | σ(';'))
                                      | snoStmt() + Reduce('snoStmt', 7) + (nl() | σ(';'))
                                      )
                                    )
@pattern
def snoCompiland():     yield from  ( POS(0)
                                    + nPush()
                                    + ARBNO(snoCommand())
                                    + Reduce('snoParse', -1)
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
def snoParse():         yield from  ( POS(0)
                                    + nPush()
                                    + ARBNO(snoCommand())
                                    + Reduce('snoParse', -1)
                                    + nPop()
                                    + Pop('SNOBOL4_tree')
                                    + RPOS(0)
                                    )
str_snoParse = """\
    snoParse            =           POS(0)
+                                   nPush()
+                                   ARBNO(*snoCommand)
+                                   ("'snoParse'" & 'nTop()')
+                                   nPop()
+                                   RPOS(0)
"""
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
if str_snoParse in snoParse() % "OUTPUT":
    pprint(SNOBOL4_tree)
#-----------------------------------------------------------------------------------------------------------------------

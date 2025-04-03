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
str_SorF = None
str_Brackets = None
def set_SorF(goto):     global str_SorF; str_SorF = goto; return True
def set_Brackets(pair): global str_Brackets; str_Brackets = pair; return True
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
def Id():           yield from  (ANY(UCASE+LCASE) + FENCE(SPAN('.'+DIGITS+UCASE+'_'+LCASE) | ε())) % "nm"
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
def Function():     yield from  φ(r"\b(?P<nm>" + "|".join((nm for nm in Functions))   + ")\b")
@pattern
def BuiltinVar():   yield from  φ(r"\b(?P<nm>" + "|".join((nm for nm in BuiltinVars)) + ")\b")
@pattern
def SpecialNm():    yield from  φ(r"\b(?P<nm>" + "|".join((nm for nm in SpecialNms))  + ")\b")
@pattern
def ProtKwd():      yield from  φ(r"\&(?P<nm>"   + "|".join((nm for nm in ProtKwds))    + ")\b")
@pattern
def UnprotKwd():    yield from  φ(r"\&(?P<nm>"   + "|".join((nm for nm in UnprotKwds))  + ")\b")
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
def Expr3():        yield from  nPush() + X3() + Reduce('|', -1)  + nPop()
@pattern
def X3():           yield from  nInc()  + Expr4() + FENCE(ζ('|')  + X3() | ε())
@pattern
def Expr4():        yield from  nPush() + X4() + Reduce('..', -1) + nPop()
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
                                | Function()          + Shift('Function', "nm") + ζ('(') + ExprList() + ζ(')') + Reduce('Call', 2)
                                | Id()                + Shift('Id', "nm") + ζ('(') + ExprList() + ζ(')') + Reduce('Call', 2)
                                | BuiltinVar()        + Shift('BuiltinVar', "nm")
                                | SpecialNm()         + Shift('SpecialNm', "nm")
                                | Id()                + Shift('Id', "nm")
                                | String()     % "tx" + Shift('String', "tx")
                                | Real()       % "tx" + Shift('Real', "tx")
                                | Integer()    % "tx" + Shift('Integer', "tx")
                                )

@pattern
def SGoto():        yield from  (σ('S') | σ('s')) + Λ(lambda: set_SorF('S'))
@pattern
def FGoto():        yield from  (σ('F') | σ('f')) + Λ(lambda: set_SorF('F'))
@pattern
def SorF():         yield from  SGoto() | FGoto()
@pattern
def Target():       yield from  ( ζ('(') + Λ(lambda: set_Brackets('()')) + Expr() + ζ(')')
                                | ζ('<') + Λ(lambda: set_Brackets('<>')) + Expr() + ζ('>')
                                )
@pattern
def Goto():         yield from  ( Gray() + σ(':')
                                + Gray()
                                + FENCE(
                                    Target()                         + Reduce(lambda: f"{str_Brackets}", 1) + Shift()
                                  | SorF() + Target()                + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1)
                                  + FENCE(Gray() + SorF() + Target() + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1) | Shift())
                                  )
                                )
@pattern
def Control():      yield from  σ('-') + BREAK("\n;") % "tx"
@pattern
def Comment():      yield from  σ('*') + BREAK("\n") % "tx"
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
                                    Comment() + Shift('comment', "tx") + Reduce('Comment', 1) + nl()
                                  | Control() + Shift('control', "tx") + Reduce('Control', 1) + (nl() | σ(';'))
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
#----------------------------------------------------------------------------------------------------------------------
def xl8(t):
    global display
    match t:
        case [''                 ]: return ""
        case ['comment',       tx]: return tx
        case ['Label',         tx]: return tx
        case ['Integer',       tx]: return tx
        case ['String',        tx]: return tx
        case ['Real',          tx]: return tx
        case ['Id',            nm]: return nm
        case ['Function',      nm]: return nm.upper()
        case ['SpecialNm',     nm]: return nm.upper()
        case ['ProtKwd',       nm]: return f"&{nm.upper()}"
        case ['UnprotKwd',     nm]: return f"&{nm.upper()}"
        case ['=', lvalue, rvalue]: return f"{xl8(lvalue)} = {xl8(rvalue)}"
        case ['='                ]: return "="
        case ['&',         *exprs]: #
                                    if len(exprs) == 1:   return f"&{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} & {xl8(exprs[1])}"
        case ['.',         *exprs]: #
                                    if len(exprs) == 1:   return f".{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} . {xl8(exprs[1])}"
        case ['*',         *exprs]: #
                                    if len(exprs) == 1:   return f"*{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} * {xl8(exprs[1])}"
        case ['()',          expr]: return f"({xl8(expr)})"
        case ['S()',         expr]: return f"S({xl8(expr)})"
        case ['F()',         expr]: return f"F({xl8(expr)})"
        case ['Call',   nm, elist]: return f"{xl8(nm)}({xl8(elist)})"
        case ['..',        *exprs]: return " + ".join((xl8(expr) for expr in exprs))
        case ['|',         *exprs]: return " | ".join((xl8(expr) for expr in exprs))
        case ['ExprList',  *exprs]: return ", ".join((xl8(expr) for expr in exprs))
        case ['Parse',  *commands]: return "\n".join((xl8(command) for command in commands))
#       ----------------------------------------------------------------------------------------------------------------
        case ['Comment',     part]: return xl8(part)
        case ['Control',     part]: return xl8(part)
        case ['Stmt', labl, subj,
             patrn, asgn, repl,
             go1, go2]:             return f"{xl8(labl)} {xl8(subj)}" \
                                           f"{' ' if patrn != [''] else ''}{xl8(patrn)}" \
                                           f"{' ' if asgn  != [''] else ''}{xl8(asgn)}" \
                                           f"{' ' if repl  != [''] else ''}{xl8(repl)}" \
                                        + (f" :{xl8(go1)}{xl8(go2)}" if go1 != [''] or go2 != [''] else "")
#       ----------------------------------------------------------------------------------------------------------------
        case _: print("Yikes!", type(t), t)
#-----------------------------------------------------------------------------------------------------------------------
@pattern
def Parse():        yield from  ( POS(0)
                                + nPush()
                                + ARBNO(Command())
                                + Reduce('Parse', -1)
                                + nPop()
                                + Pop('SNOBOL4_tree')
                                + λ("pprint(SNOBOL4_tree)")
                                + λ("print(xl8(SNOBOL4_tree))")
                                + RPOS(0)

                                )
str_Parse = """\
    snoParse        =             POS(0)
+                                 nPush()
+                                 ARBNO(*snoCommand)
+                                 ("'snoParse'" & 'nTop()')
+                                 nPop() . *Pop("SNOBOL4_tree)
+                                        . *pprint(SNOBOL4_tree)
+                                        . *print(xl8(SNOBOL4_tree))
+                                 RPOS(0)
"""
#-----------------------------------------------------------------------------------------------------------------------
GLOBALS(globals())
str_Parse in Parse()
#----------------------------------------------------------------------------------------------------------------------

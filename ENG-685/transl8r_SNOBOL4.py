# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# 31 flavors of patterns to choose from ...
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import PATTERN, Ϩ, STRING, NULL
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint
#-----------------------------------------------------------------------------------------------------------------------
str_SorF = None
str_Brackets = None
def set_SorF(goto):     global str_SorF; str_SorF = goto; return True
def set_Brackets(pair): global str_Brackets; str_Brackets = pair; return True
#-----------------------------------------------------------------------------------------------------------------------
nl              =   σ('\n')
Integer         =   SPAN(DIGITS) % "tx"
DQ              =   (σ('"') + BREAK('"\n') + σ('"')) % "tx"
SQ              =   (σ("'") + BREAK("'\n") + σ("'")) % "tx"
String          =   SQ | DQ
Real            =   ( SPAN(DIGITS)
                    + (σ('.') + FENCE(SPAN(DIGITS) | ε()) | ε())
                    + (σ('E') | σ('e'))
                    + (σ('+') | σ('-') | ε())
                    + SPAN(DIGITS)
                    | SPAN(DIGITS) + σ('.') + FENCE(SPAN(DIGITS) | ε())
                    ) % "tx"
Id              =   (ANY(UCASE+LCASE) + FENCE(SPAN('.'+DIGITS+UCASE+'_'+LCASE) | ε())) % "nm"
White           =   (  SPAN(' \t') + FENCE(nl + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε()) | ε())
                    |  nl + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε())
                    )
Gray            =   White | ε()
#-----------------------------------------------------------------------------------------------------------------------
SpecialNms      =   { 'ABORT', 'CONTINUE', 'END', 'FRETURN', 'NRETURN', 'RETURN', 'SCONTINUE', 'START' }
BuiltinVars     =   { 'ABORT', 'ARB', 'BAL', 'FAIL', 'FENCE', 'INPUT', 'OUTPUT', 'REM', 'TERMINAL' }
ProtKwds        =   { 'ABORT', 'ALPHABET', 'ARB', 'BAL', 'FAIL', 'FENCE', 'FILE', 'FNCLEVEL',
                      'LASTFILE', 'LASTLINE', 'LASTNO', 'LCASE', 'LINE', 'REM', 'RTNTYPE',
                      'STCOUNT', 'STNO', 'SUCCEED', 'UCASE'
                    }
UnprotKwds      =   { 'ABEND', 'ANCHOR', 'CASE', 'CODE', 'COMPARE', 'DUMP', 'ERRLIMIT',
                      'ERRTEXT', 'ERRTYPE', 'FTRACE', 'INPUT', 'MAXLNGTH', 'OUTPUT',
                      'PROFILE', 'STLIMIT', 'TRACE', 'TRIM', 'FULLSCAN'
                    }
Functions       =   { 'ANY', 'APPLY', 'ARBNO', 'ARG', 'ARRAY', 'ATAN', 'BACKSPACE', 'BREAK', 'BREAKX',
                      'CHAR', 'CHOP', 'CLEAR', 'CODE', 'COLLECT', 'CONVERT', 'COPY', 'COS', 'DATA',
                      'DATATYPE', 'DATE', 'DEFINE', 'DETACH', 'DIFFER', 'DUMP', 'DUPL', 'EJECT',
                      'ENDFILE', 'EQ', 'EVAL', 'EXIT', 'EXP', 'FENCE', 'FIELD', 'GE', 'GT', 'HOST',
                      'IDENT', 'INPUT', 'INTEGER', 'ITEM', 'LE', 'LEN', 'LEQ', 'LGE', 'LGT', 'LLE',
                      'LLT', 'LN', 'LNE', 'LOAD', 'LOCAL', 'LPAD', 'LT', 'NE', 'NOTANY', 'OPSYN', 'OUTPUT',
                      'POS', 'PROTOTYPE', 'REMDR', 'REPLACE', 'REVERSE', 'REWIND', 'RPAD', 'RPOS',
                      'RSORT', 'RTAB', 'SET', 'SETEXIT', 'SIN', 'SIZE', 'SORT', 'SPAN', 'SQRT', 'STOPTR',
                      'SUBSTR', 'TAB', 'TABLE', 'TAN', 'TIME', 'TRACE', 'TRIM', 'UNLOAD'
                    }
#-----------------------------------------------------------------------------------------------------------------------
Function        =   φ("\\b(?P<nm>" + "|".join((nm for nm in Functions))   + ")\\b")
BuiltinVar      =   φ("\\b(?P<nm>" + "|".join((nm for nm in BuiltinVars)) + ")\\b")
SpecialNm       =   φ("\\b(?P<nm>" + "|".join((nm for nm in SpecialNms))  + ")\\b")
ProtKwd         =   φ("\\&(?P<nm>" + "|".join((nm for nm in ProtKwds))    + ")\\b")
UnprotKwd       =   φ("\\&(?P<nm>" + "|".join((nm for nm in UnprotKwds))  + ")\\b")
#-----------------------------------------------------------------------------------------------------------------------
def τ(op):
    match op:
        case '=':   return White + σ('=') + White
        case '?':   return White + σ('?') + White
        case '|':   return White + σ('|') + White
        case '+':   return White + σ('+') + White
        case '-':   return White + σ('-') + White
        case '/':   return White + σ('/') + White
        case '*':   return White + σ('*') + White
        case '^':   return White + σ('^') + White
        case '!':   return White + σ('!') + White
        case '**':  return White + σ('**') + White
        case '$':   return White + σ('$') + White
        case '.':   return White + σ('.') + White
        case '&':   return White + σ('&') + White
        case '@':   return White + σ('@') + White
        case '#':   return White + σ('#') + White
        case '%':   return White + σ('%') + White
        case '~':   return White + σ('~') + White
        case ',':   return Gray + σ(',') + Gray
        case '(':   return σ('(') + Gray
        case '[':   return σ('[') + Gray
        case '<':   return σ('<') + Gray
        case ')':   return Gray + σ(')')
        case ']':   return Gray + σ(']')
        case '>':   return Gray + σ('>')
        case _:     raise Exception("tau error")
#-----------------------------------------------------------------------------------------------------------------------
Expr17          =   FENCE(
                      ( nPush()
                      + τ('(') + ζ(lambda: Expr)
                      + (  τ(',') + ζ(lambda: XList) + Reduce(',', -2)
                        |  ε() + Reduce('()', 1)
                        )
                      + τ(')')
                      + nPop()
                      )
                    | Function            + Shift('Function', "nm")
                                          + τ('(') + ζ(lambda: ExprList) + τ(')')
                                          + Reduce('Call', 2)
                    | Id                  + Shift('Id', "nm")
                                          + τ('(') + ζ(lambda: ExprList) + τ(')')
                                          + Reduce('Call', 2)
                    | BuiltinVar          + Shift('BuiltinVar', "nm")
                    | SpecialNm           + Shift('SpecialNm', "nm")
                    | Id                  + Shift('Id', "nm")
                    | String       % "tx" + Shift('String', "tx")
                    | Real         % "tx" + Shift('Real', "tx")
                    | Integer      % "tx" + Shift('Integer', "tx")
                    )
Expr16          =   ( nInc()
                    + ( τ('[') + ζ(lambda: ExprList) + τ(']')
                      | τ('<') + ζ(lambda: ExprList) + τ('>')
                      )
                    + FENCE(ζ(lambda: Expr16) | ε())
                    )
Expr15          =   Expr17 + FENCE(nPush() + Expr16 + Reduce('[]', -2) + nPop() | ε())
Expr14          =   ( σ('@') + ζ(lambda: Expr14) + Reduce('@', 1)
                    | σ('~') + ζ(lambda: Expr14) + Reduce('~', 1)
                    | σ('?') + ζ(lambda: Expr14) + Reduce('?', 1)
                    | ProtKwd                    + Shift('ProtKwd', "nm")
                    | UnprotKwd                  + Shift('UnprotKwd', "nm")
                    | σ('&') + ζ(lambda: Expr14) + Reduce('&', 1)
                    | σ('+') + ζ(lambda: Expr14) + Reduce('+', 1)
                    | σ('-') + ζ(lambda: Expr14) + Reduce('-', 1)
                    | σ('*') + ζ(lambda: Expr14) + Reduce('*', 1)
                    | σ('$') + ζ(lambda: Expr14) + Reduce('$', 1)
                    | σ('.') + ζ(lambda: Expr14) + Reduce('.', 1)
                    | σ('!') + ζ(lambda: Expr14) + Reduce('!', 1)
                    | σ('%') + ζ(lambda: Expr14) + Reduce('%', 1)
                    | σ('/') + ζ(lambda: Expr14) + Reduce('/', 1)
                    | σ('#') + ζ(lambda: Expr14) + Reduce('#', 1)
                    | σ('=') + ζ(lambda: Expr14) + Reduce('=', 1)
                    | σ('|') + ζ(lambda: Expr14) + Reduce('|', 1)
                    | Expr15
                    )
Expr13          =   Expr14 + FENCE(τ('~') + ζ(lambda: Expr13) + Reduce('~', 2) | ε())
Expr12          =   ( Expr13
                    + FENCE(
                        τ('$') + ζ(lambda: Expr12) + Reduce('$', 2)
                      | τ('.') + ζ(lambda: Expr12) + Reduce('.', 2)
                      | ε()
                      )
                    )
Expr11          =   ( Expr12
                    + FENCE(
                        (τ('^') | τ('!') | τ('**')) + ζ(lambda: Expr11) + Reduce('^', 2)
                      | ε()
                      )
                    )
Expr10          =   Expr11 + FENCE(τ('%') + ζ(lambda: Expr10) + Reduce('%', 2) | ε())
Expr9           =   Expr10 + FENCE(τ('*') + ζ(lambda: Expr9)  + Reduce('*', 2) | ε())
Expr8           =   Expr9  + FENCE(τ('/') + ζ(lambda: Expr8)  + Reduce('/', 2) | ε())
Expr7           =   Expr8  + FENCE(τ('#') + ζ(lambda: Expr7)  + Reduce('#', 2) | ε())
Expr6           =   ( Expr7
                    + FENCE(
                        τ('+') + ζ(lambda: Expr6) + Reduce('+', 2)
                      | τ('-') + ζ(lambda: Expr6) + Reduce('-', 2)
                      | ε()
                      )
                    )
Expr5           =   Expr6 + FENCE(τ('@') + ζ(lambda: Expr5)  + Reduce('@', 2) | ε())
X4              =   nInc()  + Expr5 + FENCE(White + ζ(lambda: X4) | ε())
Expr4           =   nPush() + X4 + Reduce('..', -1) + nPop()
X3              =   nInc()  + Expr4 + FENCE(τ('|')  + ζ(lambda: X3) | ε())
Expr3           =   nPush() + X3 + Reduce('|', -1)  + nPop()
Expr2           =   Expr3 + FENCE(τ('&') + ζ(lambda: Expr2)  + Reduce('&', 2) | ε())
Expr1           =   Expr2 + FENCE(τ('?') + ζ(lambda: Expr1)  + Reduce('?', 2) | ε())
Expr0           =   Expr1 + FENCE(τ('=') + ζ(lambda: Expr0)  + Reduce('=', 2) | ε())
Expr            =   Expr0
XList           =   nInc() + (Expr | Shift()) + FENCE(τ(',') + ζ(lambda: XList) | ε())
ExprList        =   ( nPush()
                    + XList
                    + Reduce('ExprList', -1)
                    + nPop()
                    )
#-----------------------------------------------------------------------------------------------------------------------
SGoto           =   (σ('S') | σ('s')) + Λ(lambda: set_SorF('S'))
FGoto           =   (σ('F') | σ('f')) + Λ(lambda: set_SorF('F'))
SorF            =   SGoto | FGoto
Target          =   ( τ('(') + Λ(lambda: set_Brackets('()')) + Expr + τ(')')
                    | τ('<') + Λ(lambda: set_Brackets('<>')) + Expr + τ('>')
                    )
Goto            =   ( Gray + σ(':')
                    + Gray
                    + FENCE(
                        Target                      + Reduce(lambda: f"{str_Brackets}", 1) + Shift()
                      | SorF + Target               + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1)
                      + FENCE(Gray + SorF + Target  + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1) | Shift())
                      )
                    )
Control         =   σ('-') + BREAK("\n;") % "tx"
Comment         =   σ('*') + BREAK("\n") % "tx"
Label           =   BREAK(' \t\n;') % "tx" + Shift('Label', "tx")
Stmt            =   ( Label
                    + ( White
                      + Expr14
                      + FENCE(
                          Shift()
                        + White
                        + ( σ('=') + Shift('=') + White + Expr
                          | σ('=') + Shift('=') + Shift()
                          )
                        | (τ('?') | White) + Expr1
                        + FENCE(
                            White
                          + ( σ('=') + Shift('=') + White + Expr
                            | σ('=') + Shift('=') + Shift()
                            )
                          | Shift() + Shift()
                          )
                        |  Shift() + Shift() + Shift()
                        )
                      | Shift() + Shift() + Shift() + Shift()
                      )
                    + FENCE(Goto | Shift() + Shift())
                    + Gray
                    )
Commands        =   ζ(lambda: Command) + FENCE(ζ(lambda: Commands) | ε())
Command         =   ( nInc()
                    + FENCE(
                        Comment + Shift('comment', "tx") + Reduce('Comment', 1) + nl
                      | Control + Shift('control', "tx") + Reduce('Control', 1) + (nl | σ(';'))
                      | Stmt + Reduce('Stmt', 7) + (nl | σ(';'))
                      )
                    )
Compiland       =   ( POS(0)
                    + nPush()
                    + ARBNO(Command)
                    + Reduce('Parse', -1)
                    + ( φ(r'[Ee][Nn][Dd]\b') + BREAK("\n") + nl
                      + ARBNO(BREAK("\n") + nl)
                      | ε()
                      )
                    + nPop()
                    + Pop('SNOBOL4_tree')
                    + RPOS(0)
                    )
#----------------------------------------------------------------------------------------------------------------------
def xl8(t):
    match t:
        case [''                 ]: return ""
        case ['comment',       tx]: return tx
        case ['Label',         tx]: return tx
        case ['Integer',       tx]: return tx
        case ['String',        tx]: return tx
        case ['Real',          tx]: return tx
        case ['Id',     'epsilon']: return "ε()"
        case ['Id',            nm]: return nm
        case ['Function',      nm]: return nm.upper()
        case ['SpecialNm',     nm]: return nm.upper()
        case ['ProtKwd',       nm]: return f"&{nm.upper()}"
        case ['UnprotKwd',     nm]: return f"&{nm.upper()}"
        case ['=', lvalue, rvalue]: return f"{xl8(lvalue)} := {xl8(rvalue)}"
        case ['='                ]: return "="
        case ['&',     ['Id', nm]]: return nm
        case ['&',         *exprs]: #
                                    if len(exprs) == 1:   return f"&{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} & {xl8(exprs[1])}"
        case ['.',         *exprs]: #
                                    if len(exprs) == 1:   return f"'{xl8(exprs[0])}'"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} % {xl8(exprs[1])}"
        case ['~',         *exprs]: #
                                    if len(exprs) == 1:   return f"~{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} ~ {xl8(exprs[1])}"
        case ['+',         *exprs]: #
                                    if len(exprs) == 1:   return f"+{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} + {xl8(exprs[1])}"
        case ['-',         *exprs]: #
                                    if len(exprs) == 1:   return f"-{xl8(exprs[0])}"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} - {xl8(exprs[1])}"
        case ['$',         *exprs]: #
                                    if len(exprs) == 1:   return f"globals()[{xl8(exprs[0])}]"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} @ {xl8(exprs[1])}"
        case ['*',         *exprs]: #
                                    if len(exprs) == 1:   return f"ζ(lambda: {xl8(exprs[0])})"
                                    elif len(exprs) == 2: return f"{xl8(exprs[0])} * {xl8(exprs[1])}"
        case ['()'|'S()'|'F()', ['Id', nm]]:
                                    match nm:
                                        case "END": return "END"
                                        case "RETURN": return "RETURN"
                                        case "FRETURN": return "FRETURN"
                                        case "NRETURN": return "NRETURN"
                                        case _: return f"Ξ{nm}"
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
             go1, go2]:
                s_goto = None
                f_goto = None
                match go1:
                    case ['S()', expr]: s_goto = go1
                    case ['F()', expr]: f_goto = go1
                    case ['()',  expr]: s_goto = f_goto = go1
                match go2:
                    case ['S()', expr]: s_goto = go2
                    case ['F()', expr]: f_goto = go2
                stmt = ""
                if labl[1] != "":
                    stmt += f"def Ξ{labl[1]}():\n"
                else: stmt +=  f"def Ξ{stmtno}():\n"
                stmt += f"{' ' * 20}try:\n"
                if asgn != ['']:
                    if subj[0] != '$': stmt += f"{' ' * 20}global    {xl8(subj)}\n"
                    if patrn != ['']:
                        stmt += f"{' ' * 30}{xl8(subj)} = SUBSTITUTE({xl8(subj)}, {xl8(subj)} == {xl8(patrn)}, {xl8(repl)})\n"
                    else: stmt += f"{' ' * 30}{xl8(subj)} = {xl8(repl)}\n"
                elif patrn != ['']: stmt += f"{' ' * 30}{xl8(subj)} == {xl8(patrn)}\n"
                else: stmt += f"{' ' * 30}{xl8(subj)}\n"
                if s_goto: stmt += f"{' ' * 30}return {xl8(s_goto)}\n"
                if f_goto: stmt += f"{' ' * 20}except F: return {xl8(f_goto)}\n"
                else: stmt += f"{' ' * 20}except F: pass\n"
                return stmt
#       ----------------------------------------------------------------------------------------------------------------
        case STRING(s): print("Yipper!", s)
        case _: print("Yikes!", type(t), t)
#-----------------------------------------------------------------------------------------------------------------------
Space =         SPAN(' \t') | ε()
Parse =         ( POS(0)
                + ε() @ "SNOBOL4_tree"
                + nPush()
                + ARBNO(Command)
                + Reduce('Parse', -1)
                + nPop()
                + Pop('SNOBOL4_tree')
#               + λ("pprint(SNOBOL4_tree)")
#               + λ("print(xl8(SNOBOL4_tree))")
                + Space
                + RPOS(0)
                )
str_Parse = """\
    snoParse  = POS(0)
+               nPush()
+               ARBNO(*snoCommand)
+               ("'snoParse'" & 'nTop()')
+               nPop() . *Pop("SNOBOL4_tree")
+                      . *pprint(SNOBOL4_tree)
+                      . *print(xl8(SNOBOL4_tree))
+               RPOS(0)
"""
#-----------------------------------------------------------------------------------------------------------------------
TRACE(50)
GLOBALS(globals())
#print(str_Parse)
#str_Parse in Parse
#-----------------------------------------------------------------------------------------------------------------------
#""" x = *y *z""" in Parse
#exit(0)
stmtno = 0
with open("C:/snobol4/src/sno/beauty.sno", "r") as beauty:
    line = beauty.readline(); lineno = 1
    while line != "":
        while line != "":
            if not line in POS(0) + ANY('*-'): break
            line = beauty.readline(); lineno += 1
        src = ""
        while line != "":
            src += line
            line = beauty.readline(); lineno += 1
            if line not in POS(0) + ANY('+.'): break
        if src in Parse:
#           pprint([lineno, stmtno, SNOBOL4_tree])
            print(xl8(SNOBOL4_tree))
        else: print("ERROR:", src)
        stmtno += 1
#-----------------------------------------------------------------------------------------------------------------------
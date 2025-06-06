# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------
# 31 flavors of patterns to choose from ...
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import PATTERN, STRING, NULL
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pformat, pprint
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
ς               =   (  SPAN(' \t') + FENCE(nl + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε()) | ε())
                    |  nl + (σ('+') | σ('.')) + FENCE(SPAN(' \t') | ε())
                    ) # white space
η               =   ς | ε() # grey space
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
        case '=':   return ς + σ('=') + ς
        case '?':   return ς + σ('?') + ς
        case '|':   return ς + σ('|') + ς
        case '+':   return ς + σ('+') + ς
        case '-':   return ς + σ('-') + ς
        case '/':   return ς + σ('/') + ς
        case '*':   return ς + σ('*') + ς
        case '^':   return ς + σ('^') + ς
        case '!':   return ς + σ('!') + ς
        case '**':  return ς + σ('**') + ς
        case '$':   return ς + σ('$') + ς
        case '.':   return ς + σ('.') + ς
        case '&':   return ς + σ('&') + ς
        case '@':   return ς + σ('@') + ς
        case '#':   return ς + σ('#') + ς
        case '%':   return ς + σ('%') + ς
        case '~':   return ς + σ('~') + ς
        case ',':   return η + σ(',') + η
        case '(':   return σ('(') + η
        case '[':   return σ('[') + η
        case '<':   return σ('<') + η
        case ')':   return η + σ(')')
        case ']':   return η + σ(']')
        case '>':   return η + σ('>')
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
                    | Function            + Shift('Function', "nm.upper()")
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
X4              =   nInc()  + Expr5 + FENCE(ς + ζ(lambda: X4) | ε())
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
Goto            =   ( η + σ(':')
                    + η
                    + FENCE(
                        Target                      + Reduce(lambda: f"{str_Brackets}", 1) + Shift()
                      | SorF + Target               + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1)
                      + FENCE(η + SorF + Target  + Reduce(lambda: f"{str_SorF}{str_Brackets}", 1) | Shift())
                      )
                    )
Control         =   σ('-') + BREAK("\n;") % "tx"
Comment         =   σ('*') + BREAK("\n") % "tx"
Label           =   BREAK(' \t\n;') % "tx" + Shift('Label', "tx")
Stmt            =   ( Label
                    + ( ς
                      + Expr14 + Reduce("Subject", 1)
                      + FENCE(
                          Shift()
                        + ς
                        + ( σ('=') + Shift('=') + ς + Expr
                          | σ('=') + Shift('=') + Shift()
                          )
                        | (τ('?') | ς) + Expr1
                        + FENCE(
                            ς
                          + ( σ('=') + Shift('=') + ς + Expr
                            | σ('=') + Shift('=') + Shift()
                            )
                          | Shift() + Shift()
                          )
                        |  Shift() + Shift() + Shift()
                        )
                      | Shift() + Shift() + Shift() + Shift()
                      )
                    + FENCE(Goto | Shift() + Shift())
                    + η
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
def process_file():
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
               #pprint([lineno, stmtno, SNOBOL4_tree])
                print(xl8(SNOBOL4_tree))
            else: print("ERROR:", src)
            stmtno += 1
#------------------------------------------------------------------------------
lcurly = '{'
rcurly = '}'
#------------------------------------------------------------------------------
def verb(C, line=''): C.append(line) # verbatim
def decl(C, type, var): # declare
    C.append("    %-14s%s" % (type, var))
def code(C, label=None, body=None, goto=None):
    if goto is None:
        C.append("    %-14s%s" % (label, body))
    else: C.append("    %-14s%-42s%s" % (label, body, goto))
#-----------------------------------------------------------------------------------------------------------------------
def module_head(C):
    verb(C, '#ifdef __GNUC__')
    verb(C, '#define __kernel')
    verb(C, '#define __global')
    verb(C, '#include <malloc.h>')
    verb(C, '#include <string.h>')
    verb(C, '#include <stdbool.h>')
    verb(C, 'extern int printf(const char *, ...);')
    verb(C, 'extern void assert(int a);')
    verb(C, '#endif')
    verb(C, '/*----------------------------------------------------------------------------*/')
    verb(C, 'typedef struct { const char * σ; int δ; } str_t;')
    verb(C, 'typedef struct { unsigned int pos; __global char * buffer; } output_t;')
    verb(C, '/*----------------------------------------------------------------------------*/')
    verb(C, '#if 0')
    verb(C, 'void write_nl(output_t * out) {}')
    verb(C, 'int  write_int(output_t * out, int v) {}')
    verb(C, 'void write_sz(output_t * out, const char * s) {}')
    verb(C, 'void write_flush(output_t * out) {}')
    verb(C, '#else')
    verb(C, '#if 1')
    verb(C, 'void    write_nl(output_t * out)                 { printf("%s", "\\n"); }')
    verb(C, 'int     write_int(output_t * out, int v)         { printf("%d", v); return v; }')
    verb(C, 'void    write_sz(output_t * out, const char * s) { printf("%s", s); }')
    verb(C, 'str_t   write_str(output_t * out, str_t str) {')
    verb(C, '            printf("%.*s", str.δ, str.σ);')
    verb(C, '            return str;')
    verb(C, '        }')
    verb(C, 'void    write_flush(output_t * out) {}')
    verb(C, '#else')
    verb(C, '    void write_nl(output_t * out) {')
    verb(C, "        out->buffer[out->pos++] = '\\n';")
    verb(C, '        out->buffer[out->pos] = 0;')
    verb(C, '    }')
    verb(C, '')
    verb(C, '    int write_int(output_t * out, int v) {')
    verb(C, '        int n = v;')
    verb(C, "        if (v < 0) { out->buffer[out->pos++] = '-'; n = -v; }")
    verb(C, "        if (n == 0) out->buffer[out->pos++] = '0';")
    verb(C, '        else {')
    verb(C, '            int i = 0;')
    verb(C, '            char temp[16] = "";')
    verb(C, "            while (n > 0) { temp[i++] = '0' + (n % 10); n /= 10; }")
    verb(C, '            while (i > 0) out->buffer[out->pos++] = temp[--i];')
    verb(C, '        }')
    verb(C, "        out->buffer[out->pos++] = '\\n';")
    verb(C, "        out->buffer[out->pos] = '\\0';")
    verb(C, '        return v;')
    verb(C, '    }')
    verb(C, '')
    verb(C, '    void write_sz(output_t * out, const char * s) {')
    verb(C, '        for (int i = 0; s[i]; i++)')
    verb(C, '            out->buffer[out->pos++] = s[i];')
    verb(C, "        out->buffer[out->pos++] = '\\n';")
    verb(C, '        out->buffer[out->pos] = 0;')
    verb(C, '    }')
    verb(C, '')
    verb(C, '    void write_flush(output_t * out) {')
    verb(C, '#   ifdef __GNUC__')
    verb(C, '        printf("%s", out->buffer);')
    verb(C, '#   endif')
    verb(C, '    }')
    verb(C, '#endif')
    verb(C, '#endif')
    verb(C, '/*----------------------------------------------------------------------------*/')
    verb(C, 'static int Δ = 0;')
    verb(C, 'static int Ω = 0;')
    verb(C, 'static const char * Σ = (const char *) 0;')
    verb(C, 'static const int α = 0;')
    verb(C, 'static const int β = 1;')
    verb(C, 'static const str_t empty = (str_t) {(const char *) 0, 0};')
    verb(C, 'static inline bool is_empty(str_t x) { return x.σ == (const char *) 0; }')
    verb(C, 'static inline int len(const char * s) { int δ = 0; for (; *s; δ++) s++; return δ; }')
    verb(C, 'static inline str_t str(const char * σ, int δ) { return (str_t) {σ, δ}; }')
    verb(C, 'static inline str_t cat(str_t x, str_t y) { return (str_t) {x.σ, x.δ + y.δ}; }')
    verb(C, 'static output_t * out = (output_t *) 0;')
    verb(C, '/*----------------------------------------------------------------------------*/')
    verb(C, 'static inline void * enter(void ** ζζ, size_t size) {')
    verb(C, '    void * ζ = *ζζ;')
    verb(C, '    if (size)')
    verb(C, '        if (ζ) memset(ζ, 0, size);')
    verb(C, '        else ζ = *ζζ = calloc(1, size);')
    verb(C, '    return ζ;')
    verb(C, '}')
#-----------------------------------------------------------------------------------------------------------------------
def program_head(C):
    verb(C, '/*============================================================================*/')

    verb(C, '__kernel void snobol(')
    verb(C, '    __global const char * in,')
    verb(C, '    __global       char * buffer,')
    verb(C, '             const int    num_chars) {')
    verb(C, '    /*------------------------------------------------------------------------*/')
    verb(C, '    const char cszFailure[9] = "Failure.";')
    verb(C, '    const char cszSuccess[10] = "Success: ";')
    verb(C, '    output_t output = {0, buffer};')
    verb(C, '    output_t * out = &output;')
    verb(C, '    for (int i = 0; i < num_chars; i++)')
    verb(C, '        buffer[i] = 0;')
    verb(C, "    /*------------------------------------------------------------------------*/")
#-----------------------------------------------------------------------------------------------------------------------
def program_tail(C):
    verb(C, '}')
    verb(C, '')
    verb(C, '#ifdef __GNUC__')
    verb(C, 'static char szOutput[1024] = {0};')
    verb(C, 'int main() {')
    verb(C, '    snobol((const char *) 0, szOutput, sizeof(szOutput));')
    verb(C, '    return 0;')
    verb(C, '}')
    verb(C, '#endif')
#-----------------------------------------------------------------------------------------------------------------------
counter = 0
#-----------------------------------------------------------------------------------------------------------------------
def eParse(ctx, t):
    L = f'main{counter}'
    T = []
    C = []
    module_head(C)
    ctx[1] = dict()
    Es = [emit(ctx, c) for c in t]
    for sid in ctx[1]:
        temps = ctx[1][sid]
        if len(temps) > 0:
            verb(C, "/*----------------------------------------------------------------------------*/")
            verb(C, f'typedef struct _{sid} {lcurly}')
            for temp in temps:
                    verb(C, f'    {temp[0]} {temp[1]};')
            verb(C, f'{rcurly} _{sid}_t;')
    verb(C, "/*----------------------------------------------------------------------------*/")
    for LTC in Es[:-1]:
        EL = LTC[0]
        verb(C, f'typedef struct _{EL} {EL}_t;')
    for LTC in Es[:-1]:
        EL = LTC[0]
        ET = LTC[1]
        verb(C, "/*----------------------------------------------------------------------------*/")
        verb(C, f'typedef struct _{EL} {lcurly}')
        for temp in ET:
            verb(C, f'    {temp[0]} {temp[1]};')
        verb(C, f'{rcurly} {EL}_t;')
    verb(C, "/*----------------------------------------------------------------------------*/")
    for LTC in Es[:-1]:
        EL = LTC[0]
        verb(C, f'str_t {EL}({EL}_t **, int);')
    for LTC in Es[:-1]:
        C += LTC[2]
    program_head(C)
    code(C, f'',              f'', f'goto {L}_α;')
    E = Es[-1][0]
    C += Es[-1][2]
    code(C, f'{L}_α:',        f'', f'goto {E}_α;')
    code(C, f'{L}_β:',        f'', f'return;')
    code(C, f'{E}_γ:',        f'write_sz(out, cszSuccess);', f'')
    code(C, f'',              f'write_str(out, {E});', f'')
    code(C, f'',              f'write_nl(out);', f'goto {E}_β;')
    code(C, f'{E}_ω:',        f'write_sz(out, cszFailure);', f'')
    code(C, f'',              f'write_nl(out);', f'return;')
    program_tail(C)
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eStmt(ctx, subject, pattern, equals, predicate):
    T = []
    C = []
    if equals[0] == '=':
        L = f'{subject[1][1]}'
        P, PT, PC = emit(ctx, predicate); T += PT
        verb(C, f'/*============================================================================*/')
        verb(C, f'str_t {L}({L}_t ** ζζ, int entry) {lcurly}')
        verb(C, f'    {L}_t * ζ = *ζζ;')
        code(C, f'if (entry == α)', f'{lcurly} ζ = enter((void **) ζζ, sizeof({L}_t));', f'goto {L}_α; {rcurly}')
        code(C, f'if (entry == β)', f'{lcurly}', f'goto {L}_β; {rcurly}')
        verb(C, f'    /*------------------------------------------------------------------------*/')
        C += PC
        code(C, f'{L}_α:',    f'', f'goto {P}_α;')
        code(C, f'{L}_β:',    f'', f'goto {P}_β;')
        code(C, f'{P}_γ:',    f'return {P};')
        code(C, f'{P}_ω:',    f'return empty;')
        verb(C, f'{rcurly}')
    else:
        L = f'match{counter}'
        S, ST, SC = emit(ctx, subject); T += ST; C += SC
        P, PT, PC = emit(ctx, pattern); T += PT; C += PC
        decl(C, f'str_t',     f'{L};')
        code(C, f'{L}_α:',    f'', f'goto {S}_α;')
        code(C, f'{L}_β:',    f'', f'goto {L}_ω;')
        code(C, f'{S}_γ:',    f'', f'goto {P}_α;')
        code(C, f'{S}_ω:',    f'', f'goto {L}_ω;')
        code(C, f'{P}_γ:',    f'{L} = {P};', f'goto {L}_γ;')
        code(C, f'{P}_ω:',    f'', f'goto {L}_ω;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eSubject(ctx, subject):
    C = []
    if subject[0] == 'String':
        L = f'subj{counter}'
        decl(C, f'str_t',         f'{L};')
        code(C, f'{L}_α:',        f'Δ = 0; Σ = "{eval(subject[1])}";', f'')
        code(C, f'',              f'Ω = len(Σ); {L} = str(Σ,Ω);', f'goto {L}_γ;')
        code(C, f'{L}_β:',        f'', f'goto {L}_ω;')
    else: raise Exception(f'eSubject: {subject[0]}')
    return (L, [], C)
#-----------------------------------------------------------------------------------------------------------------------
def eCall(ctx, func, arg):
    T = []
    C = []
    if   func == 'POS':    L = f'POS{counter}';     pos = f'{int(arg[1])}'
    elif func == 'RPOS':   L = f'RPOS{counter}';    pos = f'Ω-{int(arg[1])}'
    elif func == 'TAB':    L = f'TAB{counter}';     pos = f'{int(arg[1])}'
    elif func == 'RTAB':   L = f'RTAB{counter}';    pos = f'Ω-{int(arg[1])}'
    elif func == 'LEN':    L = f'LEN{counter}';     length = f'{int(arg[1])}'
    elif func == 'ANY':    L = f'ANY{counter}';     chars = eval(str(arg[1]))
    elif func == 'NOTANY': L = f'NOTANY{counter}';  chars = eval(str(arg[1]))
    elif func == 'SPAN':   L = f'SPAN{counter}';    chars = eval(str(arg[1]))
    elif func == 'BREAK':  L = f'BREAK{counter}';   chars = eval(str(arg[1]))
    elif func == 'ARBNO':
        n = counter
        L = f'ARBNO{n}'
        E, ET, EC = emit([f'ψ{n}->', ctx[1]], arg)
        if len(ET) > 0:
            ET.append(('str_t', f'ARBNO'))
            decl(C, f'_{n}_t *', f'ψ{n};')
        ctx[1][n] = ET
        C += EC
    else: raise Exception(f'eCall: {func} {arg}')
    decl(C, f'str_t', f'{L};')
    match func:
        case 'POS'|'RPOS':
            code(C, f'{L}_α:',    f'if (Δ != {pos})', f'goto {L}_ω;')
            code(C, f'',          f'{L} = str(Σ+Δ,0);', f'goto {L}_γ;')
            code(C, f'{L}_β:',    f'', f'goto {L}_ω;')
        case 'LEN':
            code(C, f'{L}_α:',    f'if (Δ+{length} > Ω)', f'goto {L}_ω;')
            code(C, f'',          f'{L} = str(Σ+Δ,{length}); Δ+={length};', f'goto {L}_γ;')
            code(C, f'{L}_β:',    f'Δ-={length};', f'goto {L}_ω;')
        case 'ANY':
            label = f'{L}_α:'
            for c in chars:
                code(C, label,    f"if (Σ[Δ] == '{c}')",               f'goto {L}_αγ;')
                label = ''
            code(C, f'',          f'',                                 f'goto {L}_ω;')
            code(C, f'{L}_αγ:',   f'{L} = str(Σ+Δ,1); Δ+=1;',          f'goto {L}_γ;')
            code(C, f'{L}_β:',    f'Δ-=1;',                            f'goto {L}_ω;')
        case 'NOTANY':
            label = f'{L}_α:'
            for c in chars:
                code(C, label,    f"if (Σ[Δ] == '{c}')",               f'goto {L}_αω;')
                label = ''
            code(C, f'',          f'{L} = str(Σ+Δ,1); Δ+=1;',          f'goto {L}_γ;')
            code(C, f'{L}_αω:',   f'',                                 f'goto {L}_ω;')
            code(C, f'{L}_β:',    f'Δ-=1;',                            f'goto {L}_ω;')
        case 'SPAN':
            T += [('int', f'{L}_δ')]
            R = ctx[0] if ctx[0] != '' else 'ζ->'
            label = f'{L}_α:'
            code(C, label,        f"for ({R}{L}_δ = 0; Σ[Δ+{R}{L}_δ]; {R}{L}_δ++) {lcurly}", f'')
            for c in chars:
                code(C, f'',      f"    if (Σ[Δ+{R}{L}_δ] == '{c}') continue;")
            code(C, f'',          f'    break;', f'')
            code(C, f'',          f"{rcurly}", f'')
            code(C, f'',          f'if ({R}{L}_δ <= 0)',                     f'goto {L}_ω;')
            code(C, f'',          f'{L} = str(Σ+Δ,{R}{L}_δ); Δ+={R}{L}_δ;',  f'goto {L}_γ;')
            code(C, f'{L}_β:',    f'Δ-={R}{L}_δ;',                           f'goto {L}_ω;')
        case 'BREAK':
            T += [('int', f'{L}_δ')]
            R = ctx[0] if ctx[0] != '' else 'ζ->'
            label = f'{L}_α:'
            code(C, label,        f"for ({R}{L}_δ = 0; Σ[Δ+{R}{L}_δ]; {R}{L}_δ++) {lcurly}", f'')
            for c in chars:
                code(C, f'',      f"    if (Σ[Δ+{R}{L}_δ] == '{c}') break;")
            code(C, f'',          f"{rcurly}", f'')
            code(C, f'',          f'if (Δ+{R}{L}_δ >= Ω)',                   f'goto {L}_ω;')
            code(C, f'',          f'{L} = str(Σ+Δ,{R}{L}_δ); Δ+={R}{L}_δ;',  f'goto {L}_γ;')
            code(C, f'{L}_β:',    f'Δ-={R}{L}_δ;',                           f'goto {L}_ω;')
        case 'ARBNO': # Wrong, Fix ARBNO to handle epsilon first
            if len(ET) > 0:
                T.append(('int', f'_{n}_i'))
                T.append((f'_{n}_t', f'_{n}_a[64]'))
                code(C, f'{L}_α:',     f'ψ{n} = &ζ->_{n}_a[ζ->_{n}_i=0];')
                code(C, f'',           f'ψ{n}->ARBNO = str(Σ+Δ, 0);',        f'goto {E}_γ;')
                code(C, f'{L}_β:',     f'ψ{n} = &ζ->_{n}_a[++ζ->_{n}_i];')
                code(C, f'',           f'ψ{n}->ARBNO = {L};',                f'goto {E}_α;')
                code(C, f'{E}_γ:',     f'{L} = cat(ψ{n}->ARBNO, {E});',      f'goto {L}_γ;')
                code(C, f'{E}_ω:',     f'if (--ζ->_{n}_i < 0)',              f'goto {L}_ω;')
                code(C, f'',           f'ψ{n} = &ζ->_{n}_a[ζ->_{n}_i];',     f'goto {E}_β;')
            else:
                T.append(('int', f'_{n}_i'))
                T.append(('str_t', f'_{n}_s'))
                code(C, f'{L}_α:',     f'{ctx[0]}_{n}_i = 0;')
                code(C, f'',           f'{ctx[0]}_{n}_s = str(Σ+Δ, 0);',     f'goto {E}_γ;')
                code(C, f'{L}_β:',     f'{ctx[0]}_{n}_i++;')
                code(C, f'',           f'{ctx[0]}_{n}_s = {L};',             f'goto {E}_α;')
                code(C, f'{E}_γ:',     f'{L} = cat({ctx[0]}_{n}_s, {E});',   f'goto {L}_γ;')
                code(C, f'{E}_ω:',     f'if (--{ctx[0]}_{n}_i < 0)',         f'goto {L}_ω;')
                code(C, f'',           f'else',                              f'goto {E}_β;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eInteger(ctx, i):
    L = f'i{counter}_{t[1]}'
    C = []
    decl(C, f'int',           f'{L};')
    code(C, f'{L}_α:',        f'{L} = {i};', f'goto {L}_γ;')
    code(C, f'{L}_β:',        f'', f'goto {L}_ω;')
    return (L, [], C)
#-----------------------------------------------------------------------------------------------------------------------
def eString(ctx, s):
    L = f's{counter}'
    C = []
    decl(C, f'str_t',         f'{L};')
    label = f'{L}_α:'
    for i, c in enumerate(s):
        code(C, label,        f"if (Σ[Δ+{i}] != '{c}')", f'goto {L}_ω;')
        label = ''
    code(C, f'',              f'{L} = str(Σ+Δ,{len(s)}); Δ+={len(s)};', f'goto {L}_γ;')
    code(C, f'{L}_β:',        f'Δ-={len(s)};', f'goto {L}_ω;')
    return (L, [], C)
#-----------------------------------------------------------------------------------------------------------------------
def eId(ctx, var):
    L = f'{var}{counter}'
    T = [(f'{var}_t *', f'{L}_ζ')]
    C = []
    deref = ctx[0] if ctx[0] != '' else 'ζ->'
    if (var in ["NULL", "null", "epsilon"]):
        decl(C, f'str_t',       f'{L};')
        code(C, f'{L}_α:',      f'{L} = str(Σ+Δ,0);',               f'goto {L}_γ;')
        code(C, f'{L}_β:',      f'',                                f'goto {L}_ω;')
    else:
        decl(C, f'str_t',       f'{L};')
        code(C, f'{L}_α:',      f'{L} = {var}(&{deref}{L}_ζ, α);',  f'goto {L}_λ;')
        code(C, f'{L}_β:',      f'{L} = {var}(&{deref}{L}_ζ, β);',  f'goto {L}_λ;')
        code(C, f'{L}_λ:',      f'if (is_empty({L}))',              f'goto {L}_ω;')
        code(C, f'',            f'else',                            f'goto {L}_γ;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eBuiltinVar(ctx, variable):
    L = f'ARB{counter}'
    T = []
    C = []
    if t[1] == 'ARB':
        T.append(('int', f'{L}_i'))
        decl(C, f'int',       f'{L}_i;')
        decl(C, f'str_t',     f'{L};')
        code(C, f'{L}_α:',    f'{L}_i = 0;', f'goto {L}_λ;')
        code(C, f'{L}_β:',    f'{L}_i++;', f'goto {L}_λ;')
        code(C, f'{L}_λ:',    f'if (Δ+{L}_i >= Ω)', f'goto {L}_ω;')
        code(C, f'',          f'{L} = str(Σ+Δ,{L}_i);', f'goto {L}_γ;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eImmediate_assign(ctx, pattern, V):
    L = f'OUTPUT{counter}'
    T = []
    C = []
    E, ET, EC = emit(ctx, pattern); T += ET; C += EC
    if (V == "OUTPUT"):
        decl(C, f'str_t',     f'{L};')
        code(C, f'{L}_α:',    f'', f'goto {E}_α;')
        code(C, f'{L}_β:',    f'', f'goto {E}_β;')
        code(C, f'{E}_γ:',    f'{L} = write_str(out, {E});', f'')
        code(C, f'',          f'write_nl(out);', f'goto {L}_γ;')
        code(C, f'{E}_ω:',    f'', f'goto {L}_ω;')
    else: raise Exception("OUTPUT is the only variable.")
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eUnop(ctx, op, E):
    if   op == '+': L = f'uplus{counter}'; E, ET, EC = emit(ctx, E);  T += ET; C += EC
    elif op == '-': L = f'uminus{counter}'; E, ET, EC = emit(ctx, E); T += ET; C += EC
    elif op == '*': return eId(ctx, E[1])
    else: raise Exception(f'eUnop: {op}')
    T = []
    C = []
    if op == '*': # currently unused
        decl(C, f'str_t',     f'{L};')
    else: decl(C, f'int',     f'{L};')
    code(C, f'{L}_α:',        f'', f'goto {E}_α;')
    code(C, f'{L}_β:',        f'', f'goto {E}_β;')
    if op == '*': # currently unused
        code(C, f'{E}_γ:',    f'{L} = lookup("{E}");', f'goto {L}_γ;')
    else: code(C, f'{E}_γ:',  f'{L} = {op}{E};', f'goto {L}_γ;')
    code(C, f'{E}_ω:',        f'', f'goto {L}_ω;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eBinop(ctx, op, E1, E2):
    if   op == '+': L = f'plus{counter}'
    elif op == '-': L = f'minus{counter}'
    elif op == '*': L = f'mult{counter}'
    elif op == '/': L = f'divide{counter}'
    else: raise Exception(f'eBinop: {op}')
    T = []
    C = []
    E1, E1T, E1C = emit(ctx, E1); T += E1T; C += E1C
    E2, E2T, E2C = emit(ctx, E2); T += E2T; C += E2C
    decl(C, f'int',           f'{L};')
    code(C, f'{L}_α:',        f'', f'goto {E1}_α;')
    code(C, f'{L}_β:',        f'', f'goto {E2}_β;')
    code(C, f'{E1}_γ:',       f'', f'goto {E2}_α;')
    code(C, f'{E1}_ω:',       f'', f'goto {L}_ω;')
    code(C, f'{E2}_γ:',       f'{L} = {E1} {op} {E2};', f'goto {L}_γ;')
    code(C, f'{E2}_ω:',       f'', f'goto {E1}_β;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eComparison(ctx, op, E1, E2):
    if op == '<':  L = f'lt{counter}'; negop = '>='
    if op == '>':  L = f'gt{counter}'; negop = '<='
    if op == '==': L = f'eq{counter}'; negop = '!='
    if op == '<=': L = f'le{counter}'; negop = '>'
    if op == '>=': L = f'ge{counter}'; negop = '<'
    if op == '!=': L = f'ne{counter}'; negop = '=='
    T = []
    C = []
    E1, E1T, E1C = emit(ctx, E1); T += E1T; C += E1C
    E2, E2T, E2C = emit(ctx, E2); T += E2T; C += E2C
    decl(C, f'int',           f'{L};')
    code(C, f'{L}_α:',        f'', f'goto {E1}_α;')
    code(C, f'{L}_β:',        f'', f'goto {E2}_β;')
    code(C, f'{E1}_γ:',       f'', f'goto {E2}_α;')
    code(C, f'{E1}_ω:',       f'', f'goto {L}_ω;')
    code(C, f'{E2}_γ:',       f'if ({E1} {negop} {E2})', f'goto {E2}_β;')
    code(C, f'',              f'{L} = {E2};', f'goto {L}_γ;')
    code(C, f'{E2}_ω:',       f'', f'goto {E1}_β;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eSeq(ctx, t):
    L = f'seq{counter}'
    T = []
    C = []
    Es = []
    for c in t:
        E, ET, EC = emit(ctx, c)
        Es.append(E)
        T += ET
        C += EC
    decl(C, f'str_t',                 f'{L};')
    code(C, f'{L}_α:',                f'{L} = str(Σ+Δ,0);', f'goto {Es[0]}_α;')
    code(C, f'{L}_β:',                f'', f'goto {Es[-1]}_β;')
    for i in range(len(Es)):
        if i < len(Es)-1:
            code(C, f'{Es[i]}_γ:',    f'{L} = cat({L}, {Es[i]});', f'goto {Es[i+1]}_α;')
        else: code(C, f'{Es[i]}_γ:',  f'{L} = cat({L}, {Es[i]});', f'goto {L}_γ;')
        if i == 0:
            code(C, f'{Es[i]}_ω:',    f'', f'goto {L}_ω;')
        else: code(C, f'{Es[i]}_ω:',  f'', f'goto {Es[i-1]}_β;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def eAlt(ctx, t):
    L = f'alt{counter}'
    T = [('int', f'{L}_i')]
    C = []
    Es = []
    for c in t:
        E, ET, EC = emit(ctx, c)
        Es.append(E)
        T += ET
        C += EC
    deref = ctx[0] if ctx[0] != '' else 'ζ->'
    decl(C, f'str_t',                 f'{L};')
    code(C, f'{L}_α:',                f'{deref}{L}_i = 1;', f'goto {Es[0]}_α;')
    label = f'{L}_β:'
    for i in range(len(Es)):
        code(C, label,                f'if ({deref}{L}_i == {i+1})', f'goto {Es[i]}_β;')
        label = ''
    code(C, f'',                      f'', f'goto {L}_ω;')
    for i in range(len(Es)-1):
        code(C, f'{Es[i]}_γ:',        f'{L} = {Es[i]};', f'goto {L}_γ;')
        code(C, f'{Es[i]}_ω:',        f'{deref}{L}_i++;', f'goto {Es[i+1]}_α;')
    code(C, f'{Es[-1]}_γ:',           f'{L} = {Es[-1]};', f'goto {L}_γ;')
    code(C, f'{Es[-1]}_ω:',           f'', f'goto {L}_ω;')
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def emit(ctx, t):
    global counter
    if t is None: return
    if t[0] != '()': counter += 1
    L = None
    T = None
    C = None
    match t[0]:
        case 'Parse':           L, T, C = eParse(ctx, t[1:])
        case 'Stmt':            return eStmt(ctx, t[2], t[3], t[4], t[5])
        case 'Subject':         L, T, C = eSubject(ctx, t[1])
        case 'Call':            L, T, C = eCall(ctx, t[1][1], t[2][1])
        case 'Integer':         L, T, C = eInteger(ctx, t[1])
        case 'String':          L, T, C = eString(ctx, eval(t[1]))
        case 'Id':              L, T, C = eId(ctx, t[1])
        case 'BuiltinVar':      L, T, C = eBuiltinVar(ctx, t[1])
        case '$':               L, T, C = eImmediate_assign(ctx, t[1], t[2][1])
        case '+'|'-'|\
             '*'|'/':
             if len(t) == 2:    L, T, C = eUnop(ctx, t[0], t[1])
             elif len(t) == 3:  L, T, C = eBinop(ctx, t[0], t[1], t[2])
             else:              raise Exception(f'emit: "{t[0]} {len(t)}"')
        case '<'|'<='|\
             '>'|'>='|\
             '=='|'!=':         L, T, C = eComparison(ctx, t[0], t[1], t[2])
        case '..':              L, T, C = eSeq(ctx, t[1:])
        case '|':               L, T, C = eAlt(ctx, t[1:])
        case '()':              return emit(ctx, t[1])
        case _:                 raise Exception(f'emit: {pformat(t)}')
    verb(C, "    /*------------------------------------------------------------------------*/")
    return (L, T, C)
#-----------------------------------------------------------------------------------------------------------------------
def genc(C): return "\n".join(C)
#-----------------------------------------------------------------------------------------------------------------------
TRACE(40)
GLOBALS(globals())
snobol4_source = ''' "SNOBOL4" POS(0) ARB $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO('Bird' | 'Blue' | LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO(LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" (BIRD | BLUE | LEN(1)) $ OUTPUT\n'''
snobol4_source = ''' "BlueBirdGoldFish" ARB\n'''
#-----------------------------------------------------------------------------------------------------------------------
snobol4_source = """\
 delim      =   SPAN(" ")
 word       =   (NOTANY("( )") BREAK("( )")) $ OUTPUT
 group      =   '(' word ARBNO(delim *group | word) ')'
 treebank   =   POS(0) ARBNO(ARBNO(group) delim) RPOS(0)
 '(S (NP (FW i)) (VP (VBP am)) (.  .)) ' treebank
"""
#-----------------------------------------------------------------------------------------------------------------------
snobol4_source = """\
  Quantifier = "*" | "+" | "?"
  Item       = ( "."
+              | ("//" ANY(".//(|*+?)"))
+              | ANY("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
+              | ("(" *Expression ")")
+              )
  Factor     = Item (Quantifier | epsilon)
  Term       = ARBNO(Factor)
  Expression = Term ARBNO("|" Term)
  RegEx      = POS(0) Expression RPOS(0)
  "x|yz"     RegEx
"""
snobol4_source = """\
  V = ANY('abcdefghijklmnopqrstuvwxyz')
  I = SPAN('0123456789')
  E = V | I | "(" *X ")"
  X = ( E "+" *X
+     | E "-" *X
+     | E "*" *X
+     | E "/" *X
+     | "+" *X
+     | "-" *X
+     | E
+     )
  C = POS(0) X RPOS(0)
  "x+y*z" C
"""
if snobol4_source in Parse:
    counter = 0
#   pprint(SNOBOL4_tree)
    L, T, C, = emit(['', None], SNOBOL4_tree)
    kernel_source = genc(C)
    for num, line in enumerate(C):
        print(line)
else: print("Boo!")
#-----------------------------------------------------------------------------------------------------------------------
exit()
import timeit
import pyopencl as cl
import numpy as np
#-----------------------------------------------------------------------------------------------------------------------
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
input_text = "\0" * 1024
input_array = np.frombuffer(input_text.encode('ascii'), dtype=np.uint8)
mf = cl.mem_flags
input_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_array)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, input_array.nbytes)
#-----------------------------------------------------------------------------------------------------------------------
while True:
    snobol4_source = input("Enter SNOBOL4 (or 'exit'): ")
    if snobol4_source.lower() == "exit": break
    if snobol4_source == "": continue
    print("Parsing SNOBOL4 ...")
    print(snobol4_source)
    snobol4_source += '\n'
    if snobol4_source in Parse:
        print("Translating SNOBOL4 to C ...")
        L, T, C = emit(SNOBOL4_tree)
        kernel_source = genc(C)
        for num, line in kernel_source:
#           print("%4d %s" % (num + 1, line))
            print(line)
        if False:
            print("Compiling C ...")
            program = cl.Program(ctx, kernel_source).build()
            print("Executing ...")
            global_size = (1,) # (input_array.size,)
            if False:
                time = timeit.timeit(
                    lambda: program.snobol4(
                        queue, global_size,
                        None, input_buf, output_buf,
                        np.uint32(input_array.size))
                    , number = 10_000, globals = globals());
                print(time)
            else:
                program.snobol4(
                    queue, global_size,
                    None, input_buf, output_buf,
                    np.uint32(input_array.size))
            output_array = np.empty_like(input_array)
            cl.enqueue_copy(queue, output_array, output_buf)
            queue.finish()
            output_text = output_array.tobytes().decode('ascii')
            print(output_text)
    else: print("Parse error!")
#-----------------------------------------------------------------------------------------------------------------------

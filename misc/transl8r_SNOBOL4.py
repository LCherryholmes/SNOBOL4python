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
c_source = []
#------------------------------------------------------------------------------
def verbatim(line=''):       c_source.append(line)
def decl(type, var):         c_source.append("    %-14s%s" % (type, var))
def code(label, body, goto): c_source.append("    %-14s%-42s%s" % (label, body, goto))
#-----------------------------------------------------------------------------------------------------------------------
def program_head():
    verbatim('#ifdef __GNUC__')
    verbatim('#define __kernel')
    verbatim('#define __global')
    verbatim('extern int printf(char *, ...);')
    verbatim('extern void assert(int a);')
    verbatim('#endif')
    verbatim('/*----------------------------------------------------------------------------*/')
    verbatim('typedef struct { const char * σ; int δ; } str_t;')
    verbatim('typedef struct { unsigned int pos; __global char * buffer; } output_t;')
    verbatim('/*----------------------------------------------------------------------------*/')
    verbatim('#if 0')
    verbatim('void write_nl(output_t * out) {}')
    verbatim('int  write_int(output_t * out, int v) {}')
    verbatim('void write_sz(output_t * out, const char * s) {}')
    verbatim('void write_flush(output_t * out) {}')
    verbatim('#else')
    verbatim('#if 1')
    verbatim('extern int printf(char *, ...);')
    verbatim('void    write_nl(output_t * out)                 { printf("%s", "\\n"); }')
    verbatim('int     write_int(output_t * out, int v)         { printf("%d", v); return v; }')
    verbatim('void    write_sz(output_t * out, const char * s) { printf("%s", s); }')
    verbatim('str_t   write_str(output_t * out, str_t str) {')
    verbatim('            printf("%.*s", str.δ, str.σ);')
    verbatim('            return str;')
    verbatim('        }')
    verbatim('void    write_flush(output_t * out) {}')
    verbatim('#else')
    verbatim('    void write_nl(output_t * out) {')
    verbatim("        out->buffer[out->pos++] = '\\n';")
    verbatim('        out->buffer[out->pos] = 0;')
    verbatim('    }')
    verbatim('')
    verbatim('    int write_int(output_t * out, int v) {')
    verbatim('        int n = v;')
    verbatim("        if (v < 0) { out->buffer[out->pos++] = '-'; n = -v; }")
    verbatim("        if (n == 0) out->buffer[out->pos++] = '0';")
    verbatim('        else {')
    verbatim('            int i = 0;')
    verbatim('            char temp[16] = "";')
    verbatim("            while (n > 0) { temp[i++] = '0' + (n % 10); n /= 10; }")
    verbatim('            while (i > 0) out->buffer[out->pos++] = temp[--i];')
    verbatim('        }')
    verbatim("        out->buffer[out->pos++] = '\\n';")
    verbatim("        out->buffer[out->pos] = '\\0';")
    verbatim('        return v;')
    verbatim('    }')
    verbatim('')
    verbatim('    void write_sz(output_t * out, const char * s) {')
    verbatim('        for (int i = 0; s[i]; i++)')
    verbatim('            out->buffer[out->pos++] = s[i];')
    verbatim("        out->buffer[out->pos++] = '\\n';")
    verbatim('        out->buffer[out->pos] = 0;')
    verbatim('    }')
    verbatim('')
    verbatim('    void write_flush(output_t * out) {')
    verbatim('#   ifdef __GNUC__')
    verbatim('        printf("%s", out->buffer);')
    verbatim('#   endif')
    verbatim('    }')
    verbatim('#endif')
    verbatim('#endif')
    verbatim('/*----------------------------------------------------------------------------*/')
    verbatim('__kernel void snobol(')
    verbatim('    __global const char * in,')
    verbatim('    __global       char * buffer,')
    verbatim('             const int    num_chars) {')
    verbatim('    /*------------------------------------------------------------------------*/')
    verbatim('    const char cszFailure[9] = "Failure.";')
    verbatim('    const char cszSuccess[10] = "Success: ";')
    verbatim('    output_t output = {0, buffer};')
    verbatim('    output_t * out = &output;')
    verbatim('    for (int i = 0; i < num_chars; i++)')
    verbatim('        buffer[i] = 0;')
    verbatim('    /*------------------------------------------------------------------------*/')
    verbatim('    inline int len(const char * s) { int δ = 0; for (; *s; δ++) s++; return δ; }')
    verbatim('    inline str_t str(const char * σ, int δ) { return (str_t) {σ, δ}; }')
    verbatim('    inline str_t cat(str_t x, str_t y) { return (str_t) {x.σ, x.δ + y.δ}; }')
    verbatim('    /*------------------------------------------------------------------------*/')
    verbatim('    int Δ = 0;')
    verbatim('    int Ω = 0;')
    verbatim('    const char * Σ = (const char *) 0;')
    verbatim("    /*------------------------------------------------------------------------*/")
#-----------------------------------------------------------------------------------------------------------------------
def program_tail():
    verbatim('}')
    verbatim('')
    verbatim('#ifdef __GNUC__')
    verbatim('static char szOutput[1024] = {0};')
    verbatim('int main() {')
    verbatim('    snobol((const char *) 0, szOutput, sizeof(szOutput));')
    verbatim('    return 0;')
    verbatim('}')
    verbatim('#endif')
#-----------------------------------------------------------------------------------------------------------------------
counter = 0
#-----------------------------------------------------------------------------------------------------------------------
def eParse(t):
    L = f'main{counter}'
    program_head()
    for c in t[1:]:
        E = emit(c)
    code(f'',              f'', f'goto {L}_α;')
    code(f'{L}_α:',        f'', f'goto {E}_α;')
    code(f'{L}_β:',        f'', f'return;')
    code(f'{E}_γ:',        f'write_sz(out, cszSuccess);', f'')
    code(f'',              f'write_str(out, {E});', f'')
    code(f'',              f'write_nl(out);', f'goto {E}_β;')
    code(f'{E}_ω:',        f'write_sz(out, cszFailure);', f'')
    code(f'',              f'write_nl(out);', f'return;')
    program_tail()
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eStmt(subject, pattern, equals, predicate):
    if equals[0] == '=':
        V = subject[1][1]
        L = f'{V}'
        P = emit(predicate) # any object or pattern
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'', f'goto {P}_α;')
        code(f'{L}_β:',    f'', f'goto {P}_β;')
        code(f'{P}_γ:',    f'{L} = {P};', f'goto {L}_γ;')
        code(f'{P}_ω:',    f'', f'goto {L}_ω;')
    else:
        L = f'match{counter}'
        S = emit(subject)
        P = emit(pattern)
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'', f'goto {S}_α;')
        code(f'{L}_β:',    f'', f'goto {L}_ω;')
        code(f'{S}_γ:',    f'', f'goto {P}_α;')
        code(f'{S}_ω:',    f'', f'goto {L}_ω;')
        code(f'{P}_γ:',    f'{L} = {P};', f'goto {L}_γ;')
        code(f'{P}_ω:',    f'', f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eSubject(subject):
    if subject[0] == 'String':
        L = f'subj{counter}'
        decl(f'str_t',         f'{L};')
        code(f'{L}_α:',        f'Δ = 0; Σ = "{eval(subject[1])}";', f'')
        code(f'',              f'Ω = len(Σ); {L} = str(Σ,Ω);', f'goto {L}_γ;')
        code(f'{L}_β:',        f'', f'goto {L}_ω;')
    else: raise Exception(f'eSubject: {subject[0]}')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eCall(func, arg):
    L = None
    if   func == 'POS':    L = f'POS{counter}';     pos = f'{int(arg[1])}'
    elif func == 'RPOS':   L = f'RPOS{counter}';    pos = f'Ω-{int(arg[1])}'
    elif func == 'TAB':    L = f'TAB{counter}';     pos = f'{int(arg[1])}'
    elif func == 'RTAB':   L = f'RTAB{counter}';    pos = f'Ω-{int(arg[1])}'
    elif func == 'LEN':    L = f'LEN{counter}';     length = f'{int(arg[1])}'
    elif func == 'ANY':    L = f'ANY{counter}';     chars = eval(str(arg[1]))
    elif func == 'NOTANY': L = f'NOTANY{counter}';  chars = eval(str(arg[1]))
    elif func == 'SPAN':   L = f'SPAN{counter}';    chars = eval(str(arg[1]))
    elif func == 'BREAK':  L = f'BREAK{counter}';   chars = eval(str(arg[1]))
    elif func == 'ARBNO':  L = f'ARBNO{counter}';   E = emit(arg)
    else: raise Exception(f'eCall: {func} {arg}')
    decl(f'str_t', f'{L};')
    match func:
        case 'POS'|'RPOS':
            code(f'{L}_α:',    f'if (Δ != {pos})', f'goto {L}_ω;')
            code(f'',          f'{L} = str(Σ+Δ,0);', f'goto {L}_γ;')
            code(f'{L}_β:',    f'', f'goto {L}_ω;')
        case 'LEN':
            code(f'{L}_α:',    f'if (Δ+{length} > Ω)', f'goto {L}_ω;')
            code(f'',          f'{L} = str(Σ+Δ,{length}); Δ+={length};', f'goto {L}_γ;')
            code(f'{L}_β:',    f'Δ-={length};', f'goto {L}_ω;')
        case 'ANY':
            label = f'{L}_α:'
            for c in chars:
                code(label,    f"if (Σ[Δ] == '{c}')",               f'goto {L}_αγ;')
                label = ''
            code(f'',          f'',                                 f'goto {L}_ω;')
            code(f'{L}_αγ:',   f'{L} = str(Σ+Δ,1); Δ+=1;',          f'goto {L}_γ;')
            code(f'{L}_β:',    f'Δ-=1;',                            f'goto {L}_ω;')
        case 'NOTANY':
            label = f'{L}_α:'
            for c in chars:
                code(label,    f"if (Σ[Δ] == '{c}')",               f'goto {L}_αω;')
                label = ''
            code(f'',          f'{L} = str(Σ+Δ,1); Δ+=1;',          f'goto {L}_γ;')
            code(f'{L}_αω:',   f'',                                 f'goto {L}_ω;')
            code(f'{L}_β:',    f'Δ-=1;',                            f'goto {L}_ω;')
        case 'SPAN':
            label = f'{L}_α:'
            decl(f'int',       f'{L}_δ;')
            code(label,        f"for ({L}_δ = 0; Σ[Δ+{L}_δ]; {L}_δ++) {lcurly}", f'')
            for c in chars:
                code(f'',      f"    if (Σ[Δ+{L}_δ] == '{c}') continue;", f'')
            code(f'',          f'    break;', f'')
            code(f'',          f"{rcurly}", f'')
            if func == 'SPAN':
                code(f'',      f'if ({L}_δ <= 0)',                  f'goto {L}_ω;')
            if func == 'BREAK':
                code(f'',      f'if (Δ+{L}_δ >= Ω)',                f'goto {L}_ω;')
            code(f'',          f'{L} = str(Σ+Δ,{L}_δ); Δ+={L}_δ;',  f'goto {L}_γ;')
            code(f'{L}_β:',    f'Δ-={L}_δ;',                        f'goto {L}_ω;')
        case 'BREAK':
            label = f'{L}_α:'
            decl(f'int',       f'{L}_δ;')
            code(label,        f"for ({L}_δ = 0; Σ[Δ+{L}_δ]; {L}_δ++) {lcurly}", f'')
            for c in chars:
                code(f'',      f"    if (Σ[Δ+{L}_δ] == '{c}') break;", f'')
            code(f'',          f"{rcurly}", f'')
            if func == 'SPAN':
                code(f'',      f'if ({L}_δ <= 0)',                  f'goto {L}_ω;')
            if func == 'BREAK':
                code(f'',      f'if (Δ+{L}_δ >= Ω)',                f'goto {L}_ω;')
            code(f'',          f'{L} = str(Σ+Δ,{L}_δ); Δ+={L}_δ;',  f'goto {L}_γ;')
            code(f'{L}_β:',    f'Δ-={L}_δ;',                        f'goto {L}_ω;')
        case 'ARBNO':
            decl(f'int',       f'{L}_i;')
            code(f'{L}_α:',    f'ζ = &z[{L}_i=0];', f'')
            code(f'',          f'ζ->{L} = str(Σ+Δ, 0);',      f'goto {E}_α;')
            code(f'{L}_β:',    f'ζ = &z[++{L}_i];', f'')
            code(f'',          f'ζ->{L} = {L};',              f'goto {E}_α;')
            code(f'{E}_γ:',    f'{L} = cat(ζ->{L}, ζ->{E});', f'goto {L}_γ;')
            code(f'{E}_ω:',    f'if ({L}_i <= 0)',            f'goto {L}_ω;')
            code(f'',          f'{L}_i--; ζ = &z[{L}_i];',    f'goto {E}_β;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eInteger(i):
    L = f'i{counter}_{t[1]}'
    decl(f'int',           f'{L};')
    code(f'{L}_α:',        f'{L} = {i};', f'goto {L}_γ;')
    code(f'{L}_β:',        f'', f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eString(s):
    L = f's{counter}'
    decl(f'str_t',         f'{L};')
    label = f'{L}_α:'
    for i, c in enumerate(s):
        code(label,        f"if (Σ[Δ+{i}] != '{c}')", f'goto {L}_ω;')
        label = ''
    code(f'',              f'{L} = str(Σ+Δ,{len(s)}); Δ+={len(s)};', f'goto {L}_γ;')
    code(f'{L}_β:',        f'Δ-={len(s)};', f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eId(var):
    L = f'{var}{counter}'
    if (var in ["NULL", "null", "epsilon"]):
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'{L} = str(Σ+Δ,0);',    f'goto {L}_γ;')
        code(f'{L}_β:',    f'',                     f'goto {L}_ω;')
    else:
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'',                     f'goto {var}_α;')
        code(f'{L}_β:',    f'',                     f'goto {var}_β;')
        code(f'{var}_γ:',  f'{L} = {var};',         f'goto {L}_γ;')
        code(f'{var}_ω:',  f'',                     f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eBuiltinVar(variable):
    L = f'ARB{counter}'
    if t[1] == 'ARB':
        decl(f'int',       f'{L}_i;')
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'{L}_i = 0;', f'goto {L}_λ;')
        code(f'{L}_β:',    f'{L}_i++;', f'goto {L}_λ;')
        code(f'{L}_λ:',    f'if (Δ+{L}_i >= Ω)', f'goto {L}_ω;')
        code(f'',          f'{L} = str(Σ+Δ,{L}_i);', f'goto {L}_γ;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eImmediate_assign(E, V):
    L = f'immed{counter}'
    if (V == "OUTPUT"):
        decl(f'str_t',     f'{L};')
        code(f'{L}_α:',    f'', f'goto {E}_α;')
        code(f'{L}_β:',    f'', f'goto {E}_β;')
        code(f'{E}_γ:',    f'{L} = write_str(out, {E});', f'')
        code(f'',          f'write_nl(out);', f'goto {L}_γ;')
        code(f'{E}_ω:',    f'', f'goto {L}_ω;')
    else: raise Exception("OUTPUT is the only variable.")
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eUnop(op, E):
#   if   op == '*': return emit(E)
    if   op == '+': L = f'uplus{counter}'; emit(E)
    elif op == '-': L = f'uminus{counter}'; emit(E)
    elif op == '*': L = f'defer{counter}'; E = E[1];
    else: raise Exception(f'eUnop: {op}')
    if op == '*':
        decl(f'str_t',     f'{L};')
    else: decl(f'int',     f'{L};')
    code(f'{L}_α:',        f'', f'goto {E}_α;')
    code(f'{L}_β:',        f'', f'goto {E}_β;')
    if op == '*':
        code(f'{E}_γ:',    f'{L} = lookup("{E}");', f'goto {L}_γ;')
    else: code(f'{E}_γ:',  f'{L} = {op}{E};', f'goto {L}_γ;')
    code(f'{E}_ω:',        f'', f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eBinop(op, E1, E2):
    if   op == '+': L = f'plus{counter}'
    elif op == '-': L = f'minus{counter}'
    elif op == '*': L = f'mult{counter}'
    elif op == '/': L = f'divide{counter}'
    else: raise Exception(f'eBinop: {op}')
    decl(f'int',           f'{L};')
    code(f'{L}_α:',        f'', f'goto {E1}_α;')
    code(f'{L}_β:',        f'', f'goto {E2}_β;')
    code(f'{E1}_γ:',       f'', f'goto {E2}_α;')
    code(f'{E1}_ω:',       f'', f'goto {L}_ω;')
    code(f'{E2}_γ:',       f'{L} = {E1} {op} {E2};', f'goto {L}_γ;')
    code(f'{E2}_ω:',       f'', f'goto {E1}_β;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eComparison(op, E1, E2):
    if op == '<':  L = f'lt{counter}'; negop = '>='
    if op == '>':  L = f'gt{counter}'; negop = '<='
    if op == '==': L = f'eq{counter}'; negop = '!='
    if op == '<=': L = f'le{counter}'; negop = '>'
    if op == '>=': L = f'ge{counter}'; negop = '<'
    if op == '!=': L = f'ne{counter}'; negop = '=='
    decl(f'int',           f'{L};')
    code(f'{L}_α:',        f'', f'goto {E1}_α;')
    code(f'{L}_β:',        f'', f'goto {E2}_β;')
    code(f'{E1}_γ:',       f'', f'goto {E2}_α;')
    code(f'{E1}_ω:',       f'', f'goto {L}_ω;')
    code(f'{E2}_γ:',       f'if ({E1} {negop} {E2})', f'goto {E2}_β;')
    code(f'',              f'{L} = {E2};', f'goto {L}_γ;')
    code(f'{E2}_ω:',       f'', f'goto {E1}_β;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eSeq(t):
    L = f'seq{counter}'
    Es = [emit(c) for c in t[1:]]
    decl(f'str_t',                 f'{L};')
    code(f'{L}_α:',                f'{L} = str(Σ+Δ,0);', f'goto {Es[0]}_α;')
    code(f'{L}_β:',                f'', f'goto {Es[-1]}_β;')
    for i in range(len(Es)):
        if i < len(Es)-1:
            code(f'{Es[i]}_γ:',    f'{L} = cat({L}, {Es[i]});', f'goto {Es[i+1]}_α;')
        else: code(f'{Es[i]}_γ:',  f'{L} = cat({L}, {Es[i]});', f'goto {L}_γ;')
        if i == 0:
            code(f'{Es[i]}_ω:',    f'', f'goto {L}_ω;')
        else: code(f'{Es[i]}_ω:',  f'', f'goto {Es[i-1]}_β;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def eAlt(t):
    L = f'alt{counter}'
    Es = [emit(c) for c in t[1:]]
    decl(f'int',                   f'{L}_i;')
    decl(f'str_t',                 f'{L};')
    code(f'{L}_α:',                f'{L}_i = 1;', f'goto {Es[0]}_α;')
    label = f'{L}_β:'
    for i in range(len(Es)):
        code(label,                f'if ({L}_i == {i+1})', f'goto {Es[i]}_β;')
        label = ''
    code(f'',                      f'', f'goto {L}_ω;')
    for i in range(len(Es)-1):
        code(f'{Es[i]}_γ:',        f'{L} = {Es[i]};', f'goto {L}_γ;')
        code(f'{Es[i]}_ω:',        f'{L}_i++;', f'goto {Es[i+1]}_α;')
    code(f'{Es[-1]}_γ:',           f'{L} = {Es[-1]};', f'goto {L}_γ;')
    code(f'{Es[-1]}_ω:',           f'', f'goto {L}_ω;')
    return L
#-----------------------------------------------------------------------------------------------------------------------
def emit(t):
    L = None
    global counter
    if t is None: return
    if t[0] != '()': counter += 1
    match t[0]:
        case 'Parse':       L = eParse(t)
        case 'Stmt':        L = eStmt(t[2], t[3], t[4], t[5])
        case 'Subject':     L = eSubject(t[1])
        case 'Call':        L = eCall(t[1][1], t[2][1])
        case 'Integer':     L = eInteger(t[1])
        case 'String':      L = eString(eval(t[1]))
        case 'Id':          L = eId(t[1])
        case 'BuiltinVar':  L = eBuiltinVar(t[1])
        case '$':           L = eImmediate_assign(emit(t[1]), t[2][1])
        case '+'|'-'|\
             '*'|'/':       # unary and binary operators
                            if len(t) == 2: L = eUnop(t[0], t[1])
                            elif len(t) == 3: L = eBinop(t[0], emit(t[1]), emit(t[2]))
                            else: raise Exception(f'emit: "{t[0]}"')
        case '<'|'<='|\
             '>'|'>='|\
             '=='|'!=':     L = eComparison(t[0], emit(t[1]), emit(t[2]))
        case '..':          L = eSeq(t)
        case '|':           L = eAlt(t)
        case '()':          return emit(t[1])
    verbatim("    /*------------------------------------------------------------------------*/")
    return L
#-----------------------------------------------------------------------------------------------------------------------
TRACE(40)
GLOBALS(globals())
snobol4_source = ''' "SNOBOL4" POS(0) ARB $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO('Bird' | 'Blue' | LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO(LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" (BIRD | BLUE | LEN(1)) $ OUTPUT\n'''
snobol4_source = ''' "BlueBirdGoldFish" ARB\n'''
snobol4_source = """\
 delim      =   SPAN(" ")
 word       =   (NOTANY("( )") BREAK("( )")) $ OUTPUT
 group      =   '(' word ARBNO(delim *group | word) ')'
 treebank   =   POS(0) ARBNO(ARBNO(group) delim) RPOS(0)
 '(S (NP (FW i)) (VP (VBP am)) (.  .)) ' treebank
"""
if snobol4_source in Parse:
    counter = 0
#   pprint(SNOBOL4_tree)
    kernel_source = emit(SNOBOL4_tree)
    for num, line in enumerate(c_source):
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
        c_source = []
        kernel_source = emit(SNOBOL4_tree)
        for num, line in enumerate(c_source):
#           print("%4d %s" % (num + 1, line))
            print(line)
        kernel_source = "\n".join(c_source)
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

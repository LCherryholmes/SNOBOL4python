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
c_source = []
left_curly = '{'
right_curly = '}'
def emit_line(line=''):           c_source.append(line)
def emit_decl(type, var):         c_source.append("    %-14s%s" % (type, var))
def emit_code(label, body, goto): c_source.append("    %-14s%-42s%s" % (label, body, goto))
#-----------------------------------------------------------------------------------------------------------------------
def program_head():
    emit_line('#ifdef __GNUC__')
    emit_line('#define __kernel')
    emit_line('#define __global')
    emit_line('extern int printf(char *, ...);')
    emit_line('extern void assert(int a);')
    emit_line('#endif')
    emit_line('/*----------------------------------------------------------------------------*/')
    emit_line('typedef struct { const char * σ; int δ; } str_t;')
    emit_line('typedef struct { unsigned int pos; __global char * buffer; } output_t;')
    emit_line('/*----------------------------------------------------------------------------*/')
    emit_line('#if 0')
    emit_line('void write_nl(output_t * out) {}')
    emit_line('int  write_int(output_t * out, int v) {}')
    emit_line('void write_sz(output_t * out, const char * s) {}')
    emit_line('void write_flush(output_t * out) {}')
    emit_line('#else')
    emit_line('#if 1')
    emit_line('extern int printf(char *, ...);')
    emit_line('void    write_nl(output_t * out)                 { printf("%s", "\\n"); }')
    emit_line('int     write_int(output_t * out, int v)         { printf("%d", v); return v; }')
    emit_line('void    write_sz(output_t * out, const char * s) { printf("%s", s); }')
    emit_line('str_t   write_str(output_t * out, str_t str) {')
    emit_line('            printf("%.*s", str.δ, str.σ);')
    emit_line('            return str;')
    emit_line('        }')
    emit_line('void    write_flush(output_t * out) {}')
    emit_line('#else')
    emit_line('    void write_nl(output_t * out) {')
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line('        out->buffer[out->pos] = 0;')
    emit_line('    }')
    emit_line('')
    emit_line('    int write_int(output_t * out, int v) {')
    emit_line('        int n = v;')
    emit_line("        if (v < 0) { out->buffer[out->pos++] = '-'; n = -v; }")
    emit_line("        if (n == 0) out->buffer[out->pos++] = '0';")
    emit_line('        else {')
    emit_line('            int i = 0;')
    emit_line('            char temp[16] = "";')
    emit_line("            while (n > 0) { temp[i++] = '0' + (n % 10); n /= 10; }")
    emit_line('            while (i > 0) out->buffer[out->pos++] = temp[--i];')
    emit_line('        }')
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line("        out->buffer[out->pos] = '\\0';")
    emit_line('        return v;')
    emit_line('    }')
    emit_line('')
    emit_line('    void write_sz(output_t * out, const char * s) {')
    emit_line('        for (int i = 0; s[i]; i++)')
    emit_line('            out->buffer[out->pos++] = s[i];')
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line('        out->buffer[out->pos] = 0;')
    emit_line('    }')
    emit_line('')
    emit_line('    void write_flush(output_t * out) {')
    emit_line('#   ifdef __GNUC__')
    emit_line('        printf("%s", out->buffer);')
    emit_line('#   endif')
    emit_line('    }')
    emit_line('#endif')
    emit_line('#endif')
    emit_line('/*----------------------------------------------------------------------------*/')
    emit_line('__kernel void snobol(')
    emit_line('    __global const char * in,')
    emit_line('    __global       char * buffer,')
    emit_line('             const int    num_chars) {')
    emit_line('    /*------------------------------------------------------------------------*/')
    emit_line('    const char cszFailure[9] = "Failure.";')
    emit_line('    const char cszSuccess[10] = "Success: ";')
    emit_line('    output_t output = {0, buffer};')
    emit_line('    output_t * out = &output;')
    emit_line('    for (int i = 0; i < num_chars; i++)')
    emit_line('        buffer[i] = 0;')
    emit_line('    /*------------------------------------------------------------------------*/')
    emit_line('    inline int len(const char * s) { int δ = 0; for (; *s; δ++) s++; return δ; }')
    emit_line('    inline str_t str(const char * σ, int δ) { return (str_t) {σ, δ}; }')
    emit_line('    inline str_t cat(str_t x, str_t y) { return (str_t) {x.σ, x.δ + y.δ}; }')
    emit_line('    /*------------------------------------------------------------------------*/')
    emit_line('    int Δ = 0;')
    emit_line('    int Ω = 0;')
    emit_line('    const char * Σ = (const char *) 0;')
    emit_line("    /*------------------------------------------------------------------------*/")

def program_tail():
    emit_line('}')
    emit_line('')
    emit_line('#ifdef __GNUC__')
    emit_line('static char szOutput[1024] = {0};')
    emit_line('int main() {')
    emit_line('    snobol((const char *) 0, szOutput, sizeof(szOutput));')
    emit_line('    return 0;')
    emit_line('}')
    emit_line('#endif')
#-----------------------------------------------------------------------------------------------------------------------
counter = 0
def genc(t):
    if t is None: return
    L = None
    global counter; counter += 1
    match t[0]:
        case 'Parse':
            L = f'main{counter}'
            program_head()
            emit_code(f'',              f'', f'goto {L}_α;')
            E = genc(t[1])
            emit_code(f'{L}_α:',        f'', f'goto {E}_α;')
            emit_code(f'{L}_β:',        f'', f'return; ')
            emit_code(f'{E}_γ:',        f'write_sz(out, cszSuccess);', f'')
            emit_code(f'',              f'write_str(out, {E});', f'')
            emit_code(f'',              f'write_nl(out);', f'goto {E}_β;')
            emit_code(f'{E}_ω:',        f'write_sz(out, cszFailure);', f'')
            emit_code(f'',              f'write_nl(out);', f'return;')
            program_tail()
        case 'Stmt':
            L = f'match{counter}'
            S = genc(t[2]) # subject
            P = genc(t[3]) # pattern
            emit_decl(f'str_t',         f'{L};')
            emit_code(f'{L}_α:',        f'', f'goto {S}_α;')
            emit_code(f'{L}_β:',        f'', f'goto {L}_ω;')
            emit_code(f'{S}_γ:',        f'', f'goto {P}_α;')
            emit_code(f'{S}_ω:',        f'', f'goto {L}_ω;')
            emit_code(f'{P}_γ:',        f'{L} = {P};', f'goto {L}_γ;')
            emit_code(f'{P}_ω:',        f'{L} = {P};', f'goto {L}_ω;')
        case 'Subject':
            L = f'subj{counter}'
            subject = eval(t[1][1])
            emit_decl(f'str_t',         f'{L};')
            emit_code(f'{L}_α:',        f'Δ = 0; Σ = "{subject}";', f'')
            emit_code(f'',              f'Ω = len(Σ); {L} = str(Σ,Ω);', f'goto {L}_γ;')
            emit_code(f'{L}_β:',        f'', f'goto {L}_ω;')
        case 'Call':
            func = t[1][1]
            arg = t[2][1][1]
            if func == 'POS':    L = f'POS{counter}';    pos = f'{int(arg)}'
            if func == 'RPOS':   L = f'RPOS{counter}';   pos = f'Ω-{int(arg)}'
            if func == 'TAB':    L = f'TAB{counter}';    pos = f'{int(arg)}'
            if func == 'RTAB':   L = f'RTAB{counter}';   pos = f'Ω-{int(arg)}'
            if func == 'LEN':    L = f'LEN{counter}';    length = f'{int(arg)}'
            if func == 'ANY':    L = f'ANY{counter}';    chars = eval(str(arg)); op = '=='
            if func == 'NOTANY': L = f'NOTANY{counter}'; chars = eval(str(arg)); op = '!='
            if func == 'SPAN':   L = f'SPAN{counter}';   chars = eval(str(arg)); op = '=='
            if func == 'BREAK':  L = f'BREAK{counter}';  chars = eval(str(arg)); op = '!='
            emit_decl(f'str_t', f'{L};')
            match t[1][1]:
                case 'POS'|'RPOS':
                    emit_code(f'{L}_α:',    f'if (Δ != {pos})', f'goto {L}_ω;')
                    emit_code(f'',          f'{L} = str(Σ+Δ,0);', f'goto {L}_γ;')
                    emit_code(f'{L}_β:',    f'', f'goto {L}_ω;')
                case 'LEN':
                    emit_code(f'{L}_α:',    f'if (Δ+{length} > Ω)', f'goto {L}_ω;')
                    emit_code(f'',          f'{L} = str(Σ+Δ,{length}); Δ+={length};', f'goto {L}_γ;')
                    emit_code(f'{L}_β:',    f'Δ-={length};', f'goto {L}_ω;')
                case 'ANY'|'NOTANY':
                    label = f'{L}_α:'
                    for c in chars:
                        emit_code(label,    f"if (Σ[Δ] {op} '{c}')", f'goto {L}_αγ;')
                        label = ''
                    emit_code(f'',          f'', f'goto {L}_ω;')
                    emit_code(f'{L}_αγ:',   f'{L} = str(Σ+Δ,1); Δ+=1;', f'goto {L}_γ;')
                    emit_code(f'{L}_β:',    f'Δ-=1;', f'goto {L}_ω;')
                case 'SPAN'|'BREAK':
                    label = f'{L}_α:'
                    emit_decl(f'int',       f'{L}_δ;')
                    emit_code(label,        f"for ({L}_δ = 0; Σ[Δ+{L}_δ]; {L}_δ++) {left_curly}", f'')
                    for c in chars:
                        emit_code(f'',      f"    if (Σ[Δ+{L}_δ] {op} '{c}') continue;", f'')
                    emit_code(f'',          f'    break;', f'')
                    emit_code(f'',          f"{right_curly}", f'')
                    if func == 'SPAN':
                        emit_code(f'',      f'if ({L}_δ <= 0)', f'goto {L}_ω;')
                    if func == 'BREAK':
                        emit_code(f'',      f'if ({L}_δ >= Ω)', f'goto {L}_ω;')
                    emit_code(f'',          f'{L} = str(Σ+Δ,{L}_δ); Δ+={L}_δ;', f'goto {L}_γ;')
                    emit_code(f'{L}_β:',    f'Δ-={L}_δ;', f'goto {L}_ω;')

        case 'Integer':
            L = f'i{counter}_{t[1]}'
            emit_decl(f'int',           f'{L};')
            emit_code(f'{L}_α:',        f'{L} = {t[1]};', f'goto {L}_γ;')
            emit_code(f'{L}_β:',        f'', f'goto {L}_ω;')
        case 'String':
            L = f's{counter}'
            V = eval(t[1])
            emit_decl(f'str_t',         f'{L};')
            label = f'{L}_α:'
            for i, c in enumerate(eval(t[1])):
                emit_code(label,        f"if (Σ[Δ+{i}] != '{c}')", f'goto {L}_ω;')
                label = ''
            emit_code(f'',              f'{L} = str(Σ+Δ,{len(V)}); Δ+={len(V)};', f'goto {L}_γ;')
            emit_code(f'{L}_β:',        f'Δ-={len(V)};', f'goto {L}_ω;')
        case 'Id':
            L = f'{t[1]}{counter}'
            identifier = t[1]
            if (identifier in ["NULL", "null", "epsilon"]):
                emit_decl(f'str_t',     f'{L};')
                emit_code(f'{L}_α:',    f'{L} = str(Σ+Δ,0);', f'goto {L}_γ;')
                emit_code(f'{L}_β:',    f'', f'goto {L}_ω;')
            else:
                emit_decl(f'int',       f'{L};')
                emit_code(f'{L}_α:',    f'{L} = {t[1]};', f'goto {L}_γ;')
                emit_code(f'{L}_β:',    f'', f'goto {L}_ω;')
        case 'BuiltinVar':
            L = f'ARB{counter}'
            variable = t[1]
            if t[1] == 'ARB':
                emit_decl(f'int',       f'{L}_i;')
                emit_decl(f'str_t',     f'{L};')
                emit_code(f'{L}_α:',    f'{L}_i = 0;', f'goto {L}_λ;')
                emit_code(f'{L}_β:',    f'{L}_i++;', f'goto {L}_λ;')
                emit_code(f'{L}_λ:',    f'if (Δ+{L}_i >= Ω)', f'goto {L}_ω;')
                emit_code(f'',          f'{L} = str(Σ+Δ,{L}_i);', f'goto {L}_γ;')
        case '$':
            L = f'assign{counter}'
            E = genc(t[1])
            variable = t[2][1]
            if (variable == "OUTPUT"):
                emit_decl(f'str_t',     f'{L};')
                emit_code(f'{L}_α:',    f'', f'goto {E}_α;')
                emit_code(f'{L}_β:',    f'', f'goto {E}_β;')
                emit_code(f'{E}_γ:',    f'{L} = write_str(out, {E});', f'')
                emit_code(f'',          f'write_nl(out);', f'goto {L}_γ;')
                emit_code(f'{E}_ω:',    f'', f'goto {L}_ω;')
            else: raise Exception("Unknown variable.")
        case '+'|'-':
            if len(t) == 2:
                op = t[0]
                if op == '+': L = f'uplus{counter}'
                if op == '-': L = f'uminus{counter}'
                E = genc(t[1])
                emit_decl(f'int',       f'{L};')
                emit_code(f'{L}_α:',    f'', f'goto {E}_α;')
                emit_code(f'{L}_β:',    f'', f'goto {E}_β;')
                emit_code(f'{E}_γ:',    f'{L} = {op}{E};', f'goto {L}_γ;')
                emit_code(f'{E}_ω:',    f'', f'goto {L}_ω;')
            elif len(t) == 3:
                op = t[0]
                if op == '+': L = f'plus{counter}'
                if op == '-': L = f'minus{counter}'
                E1 = genc(t[1])
                E2 = genc(t[2])
                emit_decl(f'int',       f'{L};')
                emit_code(f'{L}_α:',    f'', f'goto {E1}_α;')
                emit_code(f'{L}_β:',    f'', f'goto {E2}_β;')
                emit_code(f'{E1}_γ:',   f'', f'goto {E2}_α;')
                emit_code(f'{E1}_ω:',   f'', f'goto {L}_ω;')
                emit_code(f'{E2}_γ:',   f'{L} = {E1} {op} {E2};', f'goto {L}_γ;')
                emit_code(f'{E2}_ω:',   f'', f'goto {E1}_β;')
        case '*'|'/':
            op = t[0]
            if op == '*': L = f'mult{counter}'
            if op == '/': L = f'divide{counter}'
            E1 = genc(t[1])
            E2 = genc(t[2])
            emit_decl(f'int',           f'{L};')
            emit_code(f'{L}_α:',        f'', f'goto {E1}_α;')
            emit_code(f'{L}_β:',        f'', f'goto {E2}_β;')
            emit_code(f'{E1}_γ:',       f'', f'goto {E2}_α;')
            emit_code(f'{E1}_ω:',       f'', f'goto {L}_ω;')
            emit_code(f'{E2}_γ:',       f'{L} = {E1} {op} {E2};', f'goto {L}_γ;')
            emit_code(f'{E2}_ω:',       f'', f'goto {E1}_β;')
        case '<'|'>'|'=='|'<='|'>='|'!=':
            op = t[0]
            if op == '<':  L = f'lt{counter}'; nop = '>='
            if op == '>':  L = f'gt{counter}'; nop = '<='
            if op == '==': L = f'eq{counter}'; nop = '!='
            if op == '<=': L = f'le{counter}'; nop = '>'
            if op == '>=': L = f'ge{counter}'; nop = '<'
            if op == '!=': L = f'ne{counter}'; nop = '=='
            E1 = genc(t[1])
            E2 = genc(t[2])
            emit_decl(f'int',           f'{L};')
            emit_code(f'{L}_α:',        f'', f'goto {E1}_α;')
            emit_code(f'{L}_β:',        f'', f'goto {E2}_β;')
            emit_code(f'{E1}_γ:',       f'', f'goto {E2}_α;')
            emit_code(f'{E1}_ω:',       f'', f'goto {L}_ω;')
            emit_code(f'{E2}_γ:',       f'if ({E1} {nop} {E2})', f'goto {E2}_β;')
            emit_code(f'',              f'{L} = {E2};', f'goto {L}_γ;')
            emit_code(f'{E2}_ω:',       f'', f'goto {E1}_β;')
        case '..':
            L = f'seq{counter}'
            Es = [genc(c) for c in t[1:]]
            emit_decl(f'str_t',                 f'{L};')
            emit_code(f'{L}_α:',                f'{L} = str(Σ+Δ,0);', f'goto {Es[0]}_α;')
            emit_code(f'{L}_β:',                f'', f'goto {Es[-1]}_β;')
            for i in range(len(Es)):
                if i < len(Es)-1:
                    emit_code(f'{Es[i]}_γ:',    f'{L} = cat({L}, {Es[i]});', f'goto {Es[i+1]}_α;')
                else: emit_code(f'{Es[i]}_γ:',  f'{L} = cat({L}, {Es[i]});', f'goto {L}_γ;')
                if i == 0:
                    emit_code(f'{Es[i]}_ω:',    f'', f'goto {L}_ω;')
                else: emit_code(f'{Es[i]}_ω:',  f'', f'goto {Es[i-1]}_β;')
        case '|':
            L = f'alt{counter}'
            Es = [genc(c) for c in t[1:]]
            emit_decl(f'int',             f'{L}_i;')
            emit_decl(f'str_t',           f'{L};')
            emit_code(f'{L}_α:',          f'{L}_i = 1;', f'goto {Es[0]}_α;')
            label = f'{L}_β:'
            for i in range(len(Es)):
                emit_code(label,          f'if ({L}_i == {i+1})', f'goto {Es[i]}_β;')
                label = ''
            emit_code(f'',                f'', f'goto {L}_ω;')
            for i in range(len(Es)-1):
                emit_code(f'{Es[i]}_γ:',  f'{L} = {Es[i]};', f'goto {L}_γ;')
                emit_code(f'{Es[i]}_ω:',  f'{L}_i++;', f'goto {Es[i+1]}_α;')
            emit_code(f'{Es[-1]}_γ:',     f'{L} = {Es[-1]};', f'goto {L}_γ;')
            emit_code(f'{Es[-1]}_ω:',     f'', f'goto {L}_ω;')
        case '()': return genc(t[1])
    emit_line("    /*------------------------------------------------------------------------*/")
    return L
#-----------------------------------------------------------------------------------------------------------------------
TRACE(40)
GLOBALS(globals())
snobol4_source = ''' "SNOBOL4" POS(0) ARB $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO('Bird' | 'Blue' | LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" POS(0) ARBNO(LEN(1)) $ OUTPUT RPOS(0)\n'''
snobol4_source = ''' "BlueBirdGoldFish" (BIRD | BLUE | LEN(1)) $ OUTPUT\n'''
snobol4_source = ''' "BlueBirdGoldFish" ARB\n'''
if snobol4_source in Parse:
    pprint(SNOBOL4_tree)
    kernel_source = genc(SNOBOL4_tree)
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
        kernel_source = genc(SNOBOL4_tree)
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

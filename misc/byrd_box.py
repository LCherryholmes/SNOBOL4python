# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
from SNOBOL4python import GLOBALS, TRACE, ε, σ, π, λ, Λ, ζ, θ, Θ, φ, Φ, α, ω
from SNOBOL4python import ABORT, ANY, ARB, ARBNO, BAL, BREAK, BREAKX, FAIL
from SNOBOL4python import FENCE, LEN, MARB, MARBNO, NOTANY, POS, REM, RPOS
from SNOBOL4python import RTAB, SPAN, SUCCEED, TAB
from SNOBOL4python import PATTERN, STRING, NULL
from SNOBOL4python import ALPHABET, DIGITS, UCASE, LCASE
from SNOBOL4python import nPush, nInc, nPop, Shift, Reduce, Pop
from pprint import pprint, pformat
GLOBALS(globals())
TRACE(40)
#------------------------------------------------------------------------------
icon_source = "every write(5 > ((1 to 2) * (3 to 4)));"
#------------------------------------------------------------------------------
η           =   SPAN(" \t\r\n") | ε()
def ς(s):       return η + σ(s) @ "text"
integer     =   η + SPAN(DIGITS) @ "text" % "value"
word        =   η + SPAN(LCASE) @ "text" % "word"
to          =   word + Λ(lambda: text == "to")
every       =   word + Λ(lambda: text == "every")
write       =   word + Λ(lambda: text == "write")
variable    =   word + Λ(lambda: text not in ["every", "to"])
function    =   word + Λ(lambda: text in ["write"])
#------------------------------------------------------------------------------
expr6       =   ( ς('(') + ζ("expr1") + ς(')')
                | write + ς('(') + ζ("expr1") + ς(')') + Reduce("WRITE", 1)
                | variable + Shift("V", "word")
                | integer + Shift("I", "int(value)")
                )
#------------------------------------------------------------------------------
expr5       =   ( ς('+') + ζ("expr5") + Reduce('+', 1)
                | ς('-') + ζ("expr5") + Reduce('-', 1)
                | expr6
                )
#------------------------------------------------------------------------------
expr4       =   ( expr5
                + ( ς('*') + ζ("expr4") + Reduce('*', 2)
                  | ς('/') + ζ("expr4") + Reduce('/', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
expr3       =   ( expr4
                + ( ς('+') + ζ("expr3") + Reduce('+', 2)
                  | ς('-') + ζ("expr3") + Reduce('-', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
expr2       =   ( expr3 + to + expr3 + Reduce('TO', 2)
                | expr3
                )
#------------------------------------------------------------------------------
expr1       =   ( expr2
                + ( ς('<')  + expr2 + Reduce('<', 2)
                  | ς('>')  + expr2 + Reduce('>', 2)
                  | ς('==') + expr2 + Reduce('==', 2)
                  | ς('<=') + expr2 + Reduce('<=', 2)
                  | ς('>=') + expr2 + Reduce('>=', 2)
                  | ς('!=') + expr2 + Reduce('!=', 2)
                  | ε()
                  )
                )
#------------------------------------------------------------------------------
stmt        =   every + expr1 + Reduce('EVERY', 1) | expr1
#------------------------------------------------------------------------------
program     =   ( POS(0)
                + nPush()
                + ARBNO(stmt + nInc() + ς(';'))
                + Reduce("ICON")
                + nPop()
                + Pop('icon')
                + RPOS(0)
                )
#------------------------------------------------------------------------------
def out(s): print(s, end="")
def dump_tree(t): print('// ', end=""); dump(t); print()
def dump(t):
    if t is None: return
    match t[0]:
        case 'ICON':  # entire compiland
                      out('(icon')
                      for c in t[1:]: out(' '); dump(c)
                      out(')')
        case 'I':     out(t[1])
        case 'V':     out(t[1])
        case 'EVERY': out('(every '); dump(t[1]); out(')')
        case 'WRITE': out('(write '); dump(t[1]); out(')')
        case 'TO':    out('(to ');    dump(t[1]); out(' '); dump(t[2]); out(')')
        case '+':     out('(+ ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '-':     out('(- ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '*':     out('(* ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '/':     out('(/ ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '<':     out('(< ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '>':     out('(> ');     dump(t[1]); out(' '); dump(t[2]); out(')')
        case '==':    out('(== ');    dump(t[1]); out(' '); dump(t[2]); out(')')
        case '<=':    out('(<= ');    dump(t[1]); out(' '); dump(t[2]); out(')')
        case '>=':    out('(>= ');    dump(t[1]); out(' '); dump(t[2]); out(')')
        case '!=':    out('(!= ');    dump(t[1]); out(' '); dump(t[2]); out(')')
#------------------------------------------------------------------------------
counter = 0
def gen(t):
    global counter; counter += 1
    if t is None: return
    L = None
    fmt = "    %-20s%s"
    vfmt = "%-4s%s"
    match t[0]:
        case 'ICON':
            dump_tree(t)
            print('#include <stdio.h>')
            print('static int write(int n) { printf("%d\\n", n); }')
            print('int main() {')
            L = f'main{counter}'
            print(fmt % (f'',               f'goto {L}_start;'))
            E = gen(t[1]) # for c in t[1:]: # just one for now
            print(fmt % (f'{L}_start:',     f'goto {E}_start;'))
            print(fmt % (f'{E}_fail:',      f'printf("Failure.\\n"); return 0;'))
            print(fmt % (f'{E}_succeed:',   f'printf("Success!\\n"); goto {E}_resume;'))
            print("}")
        case 'EVERY': L = gen(t[1])
        case 'I'|'V':
            L = f'_{str(t[1])}' # _{counter}
            print(vfmt % (f'int', f'{L}_value;'))
            print(fmt % (f'{L}_start:',     f'{L}_value = {t[1]};'))
            print(fmt % ('',                f'goto {L}_succeed;'))
            print(fmt % (f'{L}_resume:',    f'goto {L}_fail;'))
        case 'WRITE':
            L = f'write{counter}'
            E = gen(t[1])
            print(vfmt % (f'int', f'{L}_value;'))
            print(fmt % (f'{L}_start:',    f'goto {E}_start;'))
            print(fmt % (f'{L}_resume:',   f'goto {E}_resume;'))
            print(fmt % (f'{E}_fail:',     f'goto {L}_fail;'))
            print(fmt % (f'{E}_succeed:',  f'{L}_value = write({E}_value);'))
            print(fmt % (f'',              f'goto {L}_succeed;'))
        case '+'|'-':
            if len(t) == 2:
                op = t[0]
                if op == '+': L = f'uplus{counter}'
                if op == '-': L = f'uminus{counter}'
                E = gen(t[1])
                print(vfmt % (f'int', f'{L}_value;'))
                print(fmt % (f'{L}_start:',    f'goto {E}_start;'))
                print(fmt % (f'{L}_resume:',   f'goto {E}_resume;'))
                print(fmt % (f'{E}_fail:',     f'goto {L}_fail;'))
                print(fmt % (f'{E}_succeed:',  f'{L}_value = {op}{E}_value;'))
                print(fmt % (f'',              f'goto {L}_succeed;'))
            elif len(t) == 3:
                op = t[0]
                if op == '+': L = f'plus{counter}'
                if op == '-': L = f'minus{counter}'
                E1 = gen(t[1])
                E2 = gen(t[2])
                print(vfmt % (f'int', f'{L}_value;'))
                print(fmt % (f'{L}_start:',    f'goto {E1}_start;'))
                print(fmt % (f'{L}_resume:',   f'goto {E2}_resume;'))
                print(fmt % (f'{E1}_fail:',    f'goto {L}_fail;'))
                print(fmt % (f'{E1}_succeed:', f'goto {E2}_start;'))
                print(fmt % (f'{E2}_fail:',    f'goto {E1}_resume;'))
                print(fmt % (f'{E2}_succeed:', f'{L}_value = {E1}_value {op} {E2}_value;'))
                print(fmt % (f'',              f'goto {L}_succeed;'))
        case '*'|'/':
            op = t[0]
            if op == '*': L = f'mult{counter}'
            if op == '/': L = f'divide{coiunter}'
            E1 = gen(t[1])
            E2 = gen(t[2])
            print(vfmt % (f'int', f'{L}_value;'))
            print(fmt % (f'{L}_start:',        f'goto {E1}_start;'))
            print(fmt % (f'{L}_resume:',       f'goto {E2}_resume;'))
            print(fmt % (f'{E1}_fail:',        f'goto {L}_fail;'))
            print(fmt % (f'{E1}_succeed:',     f'goto {E2}_start;'))
            print(fmt % (f'{E2}_fail:',        f'goto {E1}_resume;'))
            print(fmt % (f'{E2}_succeed:',     f'{L}_value = {E1}_value {op} {E2}_value;'))
            print(fmt % (f'',                  f'goto {L}_succeed;'))
        case '<'|'>'|'=='|'<='|'>='|'!=':
            op = t[0]
            if op == '<':  L = f'lt{counter}'
            if op == '>':  L = f'gt{counter}'
            if op == '==': L = f'eq{counter}'
            if op == '<=': L = f'le{counter}'
            if op == '>=': L = f'ge{counter}'
            if op == '!=': L = f'ne{counter}'
            E1 = gen(t[1])
            E2 = gen(t[2])
            print(vfmt % (f'int', f'{L}_value;'))
            print(fmt % (f'{L}_start:',        f'goto {E1}_start;'))
            print(fmt % (f'{L}_resume:',       f'goto {E2}_resume;'))
            print(fmt % (f'{E1}_fail:',        f'goto {L}_fail;'))
            print(fmt % (f'{E1}_succeed:',     f'goto {E2}_start;'))
            print(fmt % (f'{E2}_fail:',        f'goto {E1}_resume;'))
            print(fmt % (f'{E2}_succeed:',     f'if ({E1}_value {op} {E2}_value) goto {E2}_resume;'))
            print(fmt % (f'',                  f'{L}_value = {E2}_value;'))
            print(fmt % (f'',                  f'goto {L}_succeed;'))
        case 'TO':
            L = f'to{counter}'
            E1 = gen(t[1])
            E2 = gen(t[2])
            print(vfmt % (f'int', f'{L}_value;'))
            print(vfmt % (f'int', f'{L}_I;'))
            print(fmt % (f'{L}_start:',        f'goto {E1}_start;'))
            print(fmt % (f'{L}_resume:',       f'{L}_I = {L}_I + 1;'))
            print(fmt % (f'',                  f'goto {L}_code;'))
            print(fmt % (f'{E1}_fail:',        f'goto {L}_fail;'))
            print(fmt % (f'{E1}_succeed:',     f'goto {E2}_start;'))
            print(fmt % (f'{E2}_fail:',        f'goto {E1}_resume;'))
            print(fmt % (f'{E2}_succeed:',     f'{L}_I = {E1}_value;'))
            print(fmt % (f'',                  f'goto {L}_code;'))
            print(fmt % (f'{L}_code:',         f'if ({L}_I > {E2}_value) goto {E2}_resume;'))
            print(fmt % (f'',                  f'{L}_value = {L}_I;'))
            print(fmt % (f'',                  f'goto {L}_succeed;'))
        case 'IF':
            L = f'ifstmt{counter}'
            E1 = gen(t[1])
            E2 = gen(t[2])
            E2 = gen(t[3])
            print(vfmt % (f'int', f'{L}_value;'))
            print(fmt % (f'{L}_start:',        f'goto {E1}_start;'))
            print(fmt % (f'{L}_resume:',       f'goto [{L}_gate];'))
            print(fmt % (f'{E1}_fail:',        f'{L}_gate = addrOf({E3}_resume);'))
            print(fmt % (f'',                  f'goto {E3}_start;'))
            print(fmt % (f'{E1}_succeed:',     f'{L}_gate = addrOf({E2}_resume);'))
            print(fmt % (f'',                  f'goto {E2}_start;'))
            print(fmt % (f'{E2}_fail:',        f'goto {L}_fail;'))
            print(fmt % (f'{E2}_succeed:',     f'{L}_value = {E2}_value;'))
            print(fmt % (f'',                  f'goto {L}_succeed;'))
            print(fmt % (f'{E3}_fail:',        f'goto {L}_fail;'))
            print(fmt % (f'{E3}_succeed:',     f'{L}_value = {E3}_value;'))
            print(fmt % (f'',                  f'goto {L}_succeed;'))
    print()
    return L
#------------------------------------------------------------------------------
if icon_source in program:
    gen(icon)
else: print("Boo!")
#------------------------------------------------------------------------------

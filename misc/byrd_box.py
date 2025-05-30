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
TRACE(30)
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
stmt        =   every + expr1 + Reduce('EVERY', 1)
#------------------------------------------------------------------------------
ICON        =   ( POS(0)
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
c_source = []
def emit_line(line=''): c_source.append(line)
def emit_decl(type, var): c_source.append("%-4s%s" % (type, var))
def emit_code(label, body): c_source.append("%-4s%-20s%s" % ('', label, body))
#------------------------------------------------------------------------------
def program_head():
    emit_line('#ifdef __GNUC__')
    emit_line('#define __kernel')
    emit_line('#define __global')
    emit_line('extern int printf(char *, ...);')
    emit_line('extern void assert(int a);')
    emit_line('#endif')
    emit_line()
    emit_line('typedef struct {')
    emit_line('             unsigned int    pos;')
    emit_line('    __global unsigned char * buffer;')
    emit_line('} output_t;')
    emit_line()
    emit_line('#if 0')
    emit_line('void write_nl(output_t * out)         {}')
    emit_line('int  write_int(output_t * out, int v) {}')
    emit_line('void write_str(output_t * out, const unsigned char * s) {}')
    emit_line('void write_flush(output_t * out)      {}')
    emit_line('#else')
    emit_line('#if 0')
    emit_line('extern int printf(char *, ...);')
    emit_line('void write_nl(output_t * out)         { printf("%s", "\\n"); }')
    emit_line('int  write_int(output_t * out, int v) { printf("%d\\n", v); return v; }')
    emit_line('void write_str(output_t * out, const unsigned char * s) { printf("%s\\n", s); }')
    emit_line('void write_flush(output_t * out)      {}')
    emit_line('#else')
    emit_line('    void write_nl(output_t * out) {')
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line('        out->buffer[out->pos] = 0;')
    emit_line('    }')
    emit_line()
    emit_line('    int write_int(output_t * out, int v) {')
    emit_line("        out->buffer[out->pos++] = '0' + v;")
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line('        out->buffer[out->pos] = 0;')
    emit_line('        return v;')
    emit_line('    }')
    emit_line()
    emit_line('    void write_str(output_t * out, const unsigned char * s) {')
    emit_line('        for (int i = 0; s[i]; i++)')
    emit_line('            out->buffer[out->pos++] = s[i];')
    emit_line("        out->buffer[out->pos++] = '\\n';")
    emit_line('        out->buffer[out->pos] = 0;')
    emit_line('    }')
    emit_line()
    emit_line('    void write_flush(output_t * out) {')
    emit_line('#   ifdef __GNUC__')
    emit_line('        printf("%s", out->buffer);')
    emit_line('#   endif')
    emit_line('    }')
    emit_line('#endif')
    emit_line('#endif')
    emit_line()
    emit_line('__kernel void icon(')
    emit_line('    __global const unsigned char * in,')
    emit_line('    __global       unsigned char * buffer,')
    emit_line('             const unsigned int num_chars)')
    emit_line('{')
    emit_line('    const unsigned char cszFailure[9] = "Failure.";')
    emit_line('    const unsigned char cszSuccess[9] = "Success!";')
    emit_line('    output_t output = { 0, buffer };')
    emit_line('    output_t * out = &output;')
    emit_line('    buffer[0] = 0;')
    emit_line('    for (int i = 0; i < num_chars; i++)')
    emit_line('        buffer[i] = 0;')

def program_tail():
    emit_line('}')
    emit_line()
    emit_line('#ifdef __GNUC__')
    emit_line('static unsigned char buffer[1024] = {0};')
    emit_line('int main() {')
    emit_line('    icon(0, buffer, sizeof(buffer));')
    emit_line('    return 0;')
    emit_line('}')
    emit_line('#endif')
#------------------------------------------------------------------------------
counter = 0
def genc(t):
    if t is None: return
    global counter; counter += 1
    L = None
    match t[0]:
        case 'ICON':
            L = f'main{counter}'
            dump_tree(t)
            program_head()
            emit_code(f'',              f'goto {L}_start;')
            E = genc(t[1])
            emit_code(f'{L}_start:',    f'goto {E}_start;')
            emit_code(f'{L}_resume:',   f'return; /* function re-entry? */')
            emit_code(f'{E}_fail:',     f'write_str(out, cszFailure);')
            emit_code(f'',              f'return;')
            emit_code(f'{E}_succeed:',  f'write_str(out, cszSuccess);')
            emit_code(f'',              f'goto {E}_resume;')
            program_tail()
        case 'EVERY': L = genc(t[1])
        case 'I':
            L = f'x{counter}_{t[1]}'
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'{L}_value = {t[1]};')
            emit_code('',               f'goto {L}_succeed;')
            emit_code(f'{L}_resume:',   f'goto {L}_fail;')
        case 'V':
            L = f'{t[1]}{counter}'
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'{L}_value = {t[1]};')
            emit_code('',               f'goto {L}_succeed;')
            emit_code(f'{L}_resume:',   f'goto {L}_fail;')
        case 'WRITE':
            L = f'write{counter}'
            E = genc(t[1])
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'goto {E}_start;')
            emit_code(f'{L}_resume:',   f'goto {E}_resume;')
            emit_code(f'{E}_fail:',     f'goto {L}_fail;')
            emit_code(f'{E}_succeed:',  f'{L}_value = write_int(out, {E}_value);')
            emit_code(f'',              f'goto {L}_succeed;')
        case '+'|'-':
            if len(t) == 2:
                op = t[0]
                if op == '+': L = f'uplus{counter}'
                if op == '-': L = f'uminus{counter}'
                E = genc(t[1])
                emit_decl(f'int',           f'{L}_value;')
                emit_code(f'{L}_start:',    f'goto {E}_start;')
                emit_code(f'{L}_resume:',   f'goto {E}_resume;')
                emit_code(f'{E}_fail:',     f'goto {L}_fail;')
                emit_code(f'{E}_succeed:',  f'{L}_value = {op}{E}_value;')
                emit_code(f'',              f'goto {L}_succeed;')
            elif len(t) == 3:
                op = t[0]
                if op == '+': L = f'plus{counter}'
                if op == '-': L = f'minus{counter}'
                E1 = genc(t[1])
                E2 = genc(t[2])
                emit_decl(f'int',           f'{L}_value;')
                emit_code(f'{L}_start:',    f'goto {E1}_start;')
                emit_code(f'{L}_resume:',   f'goto {E2}_resume;')
                emit_code(f'{E1}_fail:',    f'goto {L}_fail;')
                emit_code(f'{E1}_succeed:', f'goto {E2}_start;')
                emit_code(f'{E2}_fail:',    f'goto {E1}_resume;')
                emit_code(f'{E2}_succeed:', f'{L}_value = {E1}_value {op} {E2}_value;')
                emit_code(f'',              f'goto {L}_succeed;')
        case '*'|'/':
            op = t[0]
            if op == '*': L = f'mult{counter}'
            if op == '/': L = f'divide{coiunter}'
            E1 = genc(t[1])
            E2 = genc(t[2])
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'goto {E1}_start;')
            emit_code(f'{L}_resume:',   f'goto {E2}_resume;')
            emit_code(f'{E1}_fail:',    f'goto {L}_fail;')
            emit_code(f'{E1}_succeed:', f'goto {E2}_start;')
            emit_code(f'{E2}_fail:',    f'goto {E1}_resume;')
            emit_code(f'{E2}_succeed:', f'{L}_value = {E1}_value {op} {E2}_value;')
            emit_code(f'',              f'goto {L}_succeed;')
        case '<'|'>'|'=='|'<='|'>='|'!=':
            op = t[0]
            if op == '<':  L = f'lt{counter}'
            if op == '>':  L = f'gt{counter}'
            if op == '==': L = f'eq{counter}'
            if op == '<=': L = f'le{counter}'
            if op == '>=': L = f'ge{counter}'
            if op == '!=': L = f'ne{counter}'
            E1 = genc(t[1])
            E2 = genc(t[2])
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'goto {E1}_start;')
            emit_code(f'{L}_resume:',   f'goto {E2}_resume;')
            emit_code(f'{E1}_fail:',    f'goto {L}_fail;')
            emit_code(f'{E1}_succeed:', f'goto {E2}_start;')
            emit_code(f'{E2}_fail:',    f'goto {E1}_resume;')
            emit_code(f'{E2}_succeed:', f'if ({E1}_value {op} {E2}_value) goto {E2}_resume;')
            emit_code(f'',              f'{L}_value = {E2}_value;')
            emit_code(f'',              f'goto {L}_succeed;')
        case 'TO':
            L = f'to{counter}'
            E1 = genc(t[1])
            E2 = genc(t[2])
            emit_decl(f'int',           f'{L}_value;')
            emit_decl(f'int',           f'{L}_i;')
            emit_code(f'{L}_start:',    f'goto {E1}_start;')
            emit_code(f'{L}_resume:',   f'{L}_i = {L}_i + 1;')
            emit_code(f'',              f'goto {L}_code;')
            emit_code(f'{E1}_fail:',    f'goto {L}_fail;')
            emit_code(f'{E1}_succeed:', f'goto {E2}_start;')
            emit_code(f'{E2}_fail:',    f'goto {E1}_resume;')
            emit_code(f'{E2}_succeed:', f'{L}_i = {E1}_value;')
            emit_code(f'',              f'goto {L}_code;')
            emit_code(f'{L}_code:',     f'if ({L}_i > {E2}_value) goto {E2}_resume;')
            emit_code(f'',              f'{L}_value = {L}_i;')
            emit_code(f'',              f'goto {L}_succeed;')
        case 'IF':
            L = f'ifstmt{counter}'
            E1 = genc(t[1])
            E2 = genc(t[2])
            E2 = genc(t[3])
            emit_decl(f'int',           f'{L}_value;')
            emit_code(f'{L}_start:',    f'goto {E1}_start;')
            emit_code(f'{L}_resume:',   f'goto [{L}_gate];')
            emit_code(f'{E1}_fail:',    f'{L}_gate = addrOf({E3}_resume);')
            emit_code(f'',              f'goto {E3}_start;')
            emit_code(f'{E1}_succeed:', f'{L}_gate = addrOf({E2}_resume);')
            emit_code(f'',              f'goto {E2}_start;')
            emit_code(f'{E2}_fail:',    f'goto {L}_fail;')
            emit_code(f'{E2}_succeed:', f'{L}_value = {E2}_value;')
            emit_code(f'',              f'goto {L}_succeed;')
            emit_code(f'{E3}_fail:',    f'goto {L}_fail;')
            emit_code(f'{E3}_succeed:', f'{L}_value = {E3}_value;')
            emit_code(f'',              f'goto {L}_succeed;')
    print()
    return L
#------------------------------------------------------------------------------
import timeit
import pyopencl as cl
import numpy as np
#------------------------------------------------------------------------------
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
input_text = "\0" * 1024
input_array = np.frombuffer(input_text.encode('ascii'), dtype=np.uint8)
mf = cl.mem_flags
input_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=input_array)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, input_array.nbytes)
#------------------------------------------------------------------------------
while True:
    icon_source = input("Enter ICON (or 'exit'): ")
    print(icon_source)
    if icon_source.lower() == "exit": break
    if icon_source == "": continue
    print("Parsing ICON ...")
    if icon_source in ICON:
        print("Translating ICON to C ...")
        c_source = []
        kernel_source = genc(icon)
        for num, line in enumerate(c_source):
            print("%-4d%s" % (num, line))
        kernel_source = "\n".join(c_source)
        print("Compiling C ...")
        program = cl.Program(ctx, kernel_source).build()
        print("Executing ...")
        global_size = (1,) # (input_array.size,)
        if False:
            time = timeit.timeit(
                lambda: program.icon(
                    queue, global_size,
                    None, input_buf, output_buf,
                    np.uint32(input_array.size)
                ), number = 10_000, globals = globals());
            print(time)
        else: program.icon(queue, global_size, None, input_buf, output_buf, np.uint32(input_array.size))
        output_array = np.empty_like(input_array)
        cl.enqueue_copy(queue, output_array, output_buf)
        queue.finish()
        output_text = output_array.tobytes().decode('ascii')
        print(output_text)
    else: print("Parse error!")
#------------------------------------------------------------------------------

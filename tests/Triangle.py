jumps = \
    [ 'xx x           ' # vertical moves
    , 'x x  x         '
    , ' x x  x        '
    , ' x  x   x      '
    , '  x x  x       '
    , '  x  x   x     '
    , '   x  x   x    '
    , '   x   x    x  '
    , '    x  x   x   '
    , '    x   x    x '
    , '     x  x   x  '
    , '     x   x    x'
    , '   xxx         ' # horizontal moves
    , '      xxx      '
    , '       xxx     '
    , '          xxx  '
    , '           xxx '
    , '            xxx'
    ]

def render_board(B, n=0):
    return \
        ( f"    {B[0]}    \n"
        + f"   {B[1]} {B[2]}   \n"
        + f"  {B[3]} {B[4]} {B[5]}  \n"
        + f" {B[6]} {B[7]} {B[8]} {B[9]} \n"
        + f"{B[10]} {B[11]} {B[12]} {B[13]} {B[14]}"
        )

def print_boards():
    lines =  [''] * 5
    print(f"Trys={N} Wins={W}")
    space = ""
    for X in B :
        if X is not None:
            i = 0
            for subline in render_board(X).split('\n'):
                lines[i] += space + subline
                i += 1
            space = "  "
    for line in lines:
        print(line)
    print()

import re
reg_exs = []
def generate_regexs():
    global reg_exs
    re_jump = r"^([ ]*)(x)([ ]*)(x)([ ]*)(x)([ ]*)$"
    re_jump = re.compile(re_jump)
    for jump in jumps:
        rc = re_jump.search(jump)
        g = ['(' + s.replace(' ', '.') + ')' for s in rc.groups()];
        j1 = '^' + g[0] + '(o)' + g[2] + '(o)' + g[4] + '(\\.)' + g[6] + '$'
        j2 = '^' + g[0] + '(\\.)' + g[2] + '(o)' + g[4] + '(o)' + g[6] + '$'
        reg_exs.append(re.compile(j1))
        reg_exs.append(re.compile(j2))
    return

N = 0
swap = {'o' : '.', '.' : 'o'}
def make_jump(X):
    global N, swap
    for rex in reg_exs:
        rr = rex.search(X)
        if rr is not None:
            N += 1
            g = rr.groups()
            yield (g[0]
                 + swap[g[1]] + g[2]
                 + swap[g[3]] + g[4]
                 + swap[g[5]] + g[6])

generate_regexs()
W = 0
B = [None] * 14
B[0] = 'oooo.oooooooooo'
for B[1] in make_jump(B[0]):
    for B[2] in make_jump(B[1]):
        for B[3] in make_jump(B[2]):
            for B[4] in make_jump(B[3]):
                for B[5] in make_jump(B[4]):
                    for B[6] in make_jump(B[5]):
                        for B[7] in make_jump(B[6]):
                            for B[8] in make_jump(B[7]):
                                for B[9] in make_jump(B[8]):
                                    for B[10] in make_jump(B[9]):
                                        for B[11] in make_jump(B[10]):
                                            for B[12] in make_jump(B[11]):
                                                for B[13] in make_jump(B[12]):
                                                   W += 1
                                                   print_boards()

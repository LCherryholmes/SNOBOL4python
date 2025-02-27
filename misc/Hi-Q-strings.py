#     b'111222333333344444445555555666777'
J = [ b'x  x    x                        '
    , b' x  x    x                       '
    , b'  x  x    x                      '
    , b'   x    x      x                 '
    , b'    x    x      x                '
    , b'     x    x      x               '
    , b'      x      x        x          '
    , b'       x      x        x         '
    , b'        x      x        x        '
    , b'         x      x        x       '
    , b'          x      x        x      '
    , b'               x      x    x     '
    , b'                x      x    x    '
    , b'                 x      x    x   '
    , b'                      x    x  x  '
    , b'                       x    x  x '
    , b'                        x    x  x'
    , b'xxx                              '
    , b'   xxx                           '
    , b'      xxx                        '
    , b'       xxx                       '
    , b'        xxx                      '
    , b'         xxx                     '
    , b'          xxx                    '
    , b'             xxx                 '
    , b'              xxx                '
    , b'               xxx               '
    , b'                xxx              '
    , b'                 xxx             '
    , b'                    xxx          '
    , b'                     xxx         '
    , b'                      xxx        '
    , b'                       xxx       '
    , b'                        xxx      '
    , b'                           xxx   '
    , b'                              xxx'
    ]
#------------------------------------------------------------------------------
def render_board(B, n=0):
    return \
        ( f"                {B[ 0]} {B[ 1]} {B[ 2]}\n"
        + f"                {B[ 3]} {B[ 4]} {B[ 5]}\n"
        + f"{B[ 6]} {B[ 7]} {B[ 8]} {B[ 9]} {B[10]} {B[11]} {B[12]}\n"
        + f"{B[13]} {B[14]} {B[15]} {B[16]} {B[17]} {B[18]} {B[19]}\n"
        + f"{B[20]} {B[21]} {B[22]} {B[23]} {B[24]} {B[25]} {B[26]}\n"
        + f"                {B[27]} {B[28]} {B[29]}\n"
        + f"                {B[30]} {B[31]} {B[32]}\n"
        )
#------------------------------------------------------------------------------
def print_boards():
    lines =  [''] * 7
    print(f"Trys={N} Wins={W}")
    space = ""
    for X in B :
        if X is not None:
            i = 0
            for subline in render_board(X).split('\n'):
                lines[i] += space + str(subline)
                i += 1
            space = "  "
    for line in lines:
        print(line)
    print()
#------------------------------------------------------------------------------
import re
reg_exs = []
def generate_regexs():
    global reg_exs
    re_jump = r"^([ ]*)(x)([ ]*)(x)([ ]*)(x)([ ]*)$"
    re_jump = re.compile(re_jump)
    for jump in J:
        rc = re_jump.search(jump)
        g = ['(' + s.replace(' ', '.') + ')' for s in rc.groups()];
        j1 = '^' + g[0] + '(o)' + g[2] + '(o)' + g[4] + '(\\.)' + g[6] + '$'
        j2 = '^' + g[0] + '(\\.)' + g[2] + '(o)' + g[4] + '(o)' + g[6] + '$'
        print(j1, j2)
        reg_exs.append(re.compile(j1))
        reg_exs.append(re.compile(j2))
    return

N = 0
swap = {'o' : '.', '.' : 'o'}
def make_jump(X):
    global N, swap
    for rex in reg_exs:
        rr = rex.fullmatch(X)
        if rr is not None:
            N += 1
            g = rr.groups()
            yield (g[0]
                + swap[g[1]] + g[2]
                + swap[g[3]] + g[4]
                + swap[g[5]] + g[6])

generate_regexs()
W = 0
B = [None] * 32
G =    b'................o................'
B[0] = b'oooooooooooooooo.oooooooooooooooo'
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
                          for B[14] in make_jump(B[13]):
                            for B[15] in make_jump(B[14]):
                              for B[16] in make_jump(B[15]):
                                for B[17] in make_jump(B[16]):
                                  for B[18] in make_jump(B[17]):
                                    for B[19] in make_jump(B[18]):
                                      for B[20] in make_jump(B[19]):
                                        for B[21] in make_jump(B[20]):
                                          for B[22] in make_jump(B[21]):
                                            for B[23] in make_jump(B[22]):
                                              for B[24] in make_jump(B[23]):
                                                for B[25] in make_jump(B[24]):
                                                  for B[26] in make_jump(B[25]):
                                                    for B[27] in make_jump(B[26]):
                                                      for B[28] in make_jump(B[27]):
                                                        for B[29] in make_jump(B[28]):
                                                          for B[30] in make_jump(B[29]):
                                                            for B[31] in make_jump(B[30]):
                                                               W += 1
                                                               print_boards()
def main():
    for _ in moves(0):
        print("WINNER!!!")
        print_board(B, 31, attempts)
        print_boards()

main()

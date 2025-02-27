B = bytearray.fromhex('FFFF010101FFFFFFFF010101FFFF010101010101010101010001010101010101010101FFFF010101FFFFFFFF010101FFFF')
W = bytearray.fromhex('FFFF000000FFFFFFFF000000FFFF000000000000000000000100000000000000000000FFFF000000FFFFFFFF000000FFFF')
trials =  (       (0,2),
                  (1,2),
    (2,0), (2,1), (2,2), (2,3), (2,4),
    (3,0), (3,1), (3,2), (3,3), (3,4),
    (4,0), (4,1), (4,2), (4,3), (4,4),
                  (5,2),
                  (6,2),)

def make_jump(j): return (j[0] ^ 1, j[1] ^ 1, j[2] ^ 1)
def set_horizontal (r, c, j): B[r * 7 + c+0] = j[0]; \
                              B[r * 7 + c+1] = j[1]; \
                              B[r * 7 + c+2] = j[2]
def set_vertical   (r, c, j): B[(r+0) * 7 + c] = j[0]; \
                              B[(r+1) * 7 + c] = j[1]; \
                              B[(r+2) * 7 + c] = j[2]
def is_horizontal  (r, c, j): return B[r * 7 + c+0] == j[0] \
                                 and B[r * 7 + c+1] == j[1] \
                                 and B[r * 7 + c+2] == j[2]
def is_vertical    (r, c, j): return B[(r+0) * 7 + c] == j[0] \
                                 and B[(r+1) * 7 + c] == j[1] \
                                 and B[(r+2) * 7 + c] == j[2]

attempts = 0
def print_board(board, n, attempts=None):
    print(f"{n} ({attempts:,}):\n")
    for r in range(0, 7):
        for c in range(0, 7):
            match board[r * 7 + c]:
                case 0: print(" .", end='')
                case 1: print(" o", end='')
                case 255: print("  ", end='')
        print()
    print()

Attempts = []
S = []
def print_boards():
    global S
    for i, s in enumerate(S):
        print_board(s, i, Attempts[i]) 

import copy
def moves(n):
    global S, B, attempts; attempts += 1
    if (attempts % 100000) == 0:
        print_board(B, n, attempts)
    N = copy.deepcopy(B)
    if n < 31:
        S.append(N)
        Attempts.append(attempts)
    else:
       if B == W:
           S.append(N)
           Attempts.append(attempts)
           yield
       else: return
    for seen in ((1, 1, 0), (0, 1, 1)):
        jump = make_jump(seen)
        for x, y in trials:
            if is_vertical(y, x, seen):
               set_vertical(y, x, jump)
               try: yield next(moves(n + 1))
               except StopIteration: None
               set_vertical(y, x, seen)
            if is_horizontal(x, y, seen):
               set_horizontal(x, y, jump)
               try: yield next(moves(n + 1))
               except StopIteration: None
               set_horizontal(x, y, seen)
    Attempts.pop()
    S.pop()

def main():
    for _ in moves(0):
        print("WINNER!!!")
        print_board(B, 31, attempts)
        print_boards()

main()

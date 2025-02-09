import numpy as np
X = -1
B = np.array(
    [[X,X,1,1,1,X,X]
    ,[X,X,1,1,1,X,X]
    ,[1,1,1,1,1,1,1]
    ,[1,1,1,0,1,1,1]
    ,[1,1,1,1,1,1,1]
    ,[X,X,1,1,1,X,X]
    ,[X,X,1,1,1,X,X]], dtype=np.int8)

W = np.array(
    [[X,X,0,0,0,X,X]
    ,[X,X,0,0,0,X,X]
    ,[0,0,0,0,0,0,0]
    ,[0,0,0,1,0,0,0]
    ,[0,0,0,0,0,0,0]
    ,[X,X,0,0,0,X,X]
    ,[X,X,0,0,0,X,X]], dtype=np.int8)

trials =  (       (0,2),
                  (1,2),
    (2,0), (2,1), (2,2), (2,3), (2,4),
    (3,0), (3,1), (3,2), (3,3), (3,4),
    (4,0), (4,1), (4,2), (4,3), (4,4),
                  (5,2),
                  (6,2),)

def make_jump(j): return (j[0] ^ 1, j[1] ^ 1, j[2] ^ 1)
def set_horizontal (r, c, j): B[r, c:c+3] = j
def set_vertical   (r, c, j): B[r:r+3, c] = j
def is_horizontal  (r, c, j): return all(B[r, c:c+3] == j)
def is_vertical    (r, c, j): return all(B[r:r+3, c] == j)

attempts = 0
def print_board(board, n, attempts=None):
    print(f"{n} ({attempts:,}):\n")
    for r in range(0, 7):
        for c in range(0, 7):
            print(("  ", " .", " o")[board[r, c] + 1], end = '')
        print()
    print()

Attempts = []
S = []
def print_boards():
    global S
    for i, s in enumerate(S):
        print_board(s, i, Attempts[i]) 

def moves(n):
    global S, B, attempts; attempts += 1
    if (attempts % 1000) == 0:
        print_board(B, n, attempts)
    N = np.asarray(B)
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
        print_board((B, attempts), 31)
        print_boards()

main()

squares([], [], []).
squares([N1, N2, N3 | Ns1],
        [N4, N5, N6 | Ns2],
        [N7, N8, N9 | Ns3]) :-
        all_distinct([N1, N2, N3, N4, N5, N6, N7, N8, N9]),
        squares(Ns1, Ns2, Ns3).

sudoku(Rows) :-
   length(Rows, 9),
   maplist(same_length(Rows), Rows),
   append(Rows, Vs),
   Vs ins 1..9,
   maplist(all_distinct, Rows),
   transpose(Rows, Columns),
   maplist(all_distinct, Columns),
   Rows = [As, Bs, Cs, Ds, Es, Fs, Gs, Hs, Is],
   squares(As, Bs, Cs),
   squares(Ds, Es, Fs),
   squares(Gs, Hs, Is).
   
puzle :-
   Rows = [[1,_,_], [], []],
   sudoku(Rows).


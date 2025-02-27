%-------------------------------------------------------------------------------
% 5.
% Brown, Clark, Jones, and Smith are the names of the men who hold, though not
% necessarily respectively, the positions of accountant, cashier, manager, and
% president in the First National Bank of Fairport.  Although the cashier beats
% him consistently, the president will play chess with no one else in the bank.
% Both the manager and the cashier are better chess players than the accountant.
% Jones and Smith are nextdoor neighbors and frequently play chess together in
% the evening.  Clark plays a better game of chess than Jones.  The accountant
% lives near the president but not near any of the others.  What position does
% each man hold?
:- initialization(main).
person(brown).
person(clark).
person(jones).
person(smith).
livesNear(jones, smith).
playsChess(jones, smith).
betterAtChess(clark, jones).
doesLiveNear(X, Y) :- livesNear(X, Y).
doesLiveNear(X, Y) :- livesNear(Y, X).
doesLiveNear(X, Z) :- livesNear(X, Y), livesNear(Y, Z).
%-------------------------------------------------------------------------------
main :-
   person(Accountant),
   person(Cashier),
   person(Manager),
   person(President),
   differ(Accountant, Cashier, Manager, President),
%  betterAtChess(Cashier, President),
%  \+playsChess(President, Manager),
%  \+playsChess(President, Accountant),
%  betterAtChess(Manager, Accountant),
%  betterAtChess(Cashier, Accountant),
%  doesLiveNear(Accountant, President),
%  \+doesLiveNear(Accountant, Cashier),
%  \+doesLiveNear(Accountant, Manager)
   display(Accountant, Cashier, Manager, President),
   fail
.
%-------------------------------------------------------------------------------
differ(X, X, _, _) :- !, fail.
differ(X, _, X, _) :- !, fail.
differ(X, _, _, X) :- !, fail.
differ(_, X, X, _) :- !, fail.
differ(_, X, _, X) :- !, fail.
differ(_, _, X, X) :- !, fail.
differ(_, _, _, _).
%-------------------------------------------------------------------------------
display(Accountant, Cashier, Manager, President) :-
   write('Accountant='), write(Accountant),
   write(' Cashier='), write(Cashier),
   write(' Manager='), write(Manager),
   write(' President='), write(President),
   write('\n').
%-------------------------------------------------------------------------------

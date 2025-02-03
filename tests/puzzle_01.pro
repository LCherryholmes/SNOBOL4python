%-------------------------------------------------------------------------------
% 1
% In a certain bank the positions of cashier, manager, and teller are held by
% Brown, Jones, and Smith, though not necessarily respectively.  The teller, who
% was an only child, earns the least.  Smith, who married Brown's sister, earns
% more than the manager. What position does each man fill?
:- initialization(main). main :- puzzle; true.
person(brown).
person(jones).
person(smith).
puzzle :-
   person(Cashier),
   person(Manager),
   person(Teller),
   differ(Cashier, Manager, Teller),
   differ(smith, Manager),
   differ(Teller, brown),
   differ(smith, Teller),
   display(Cashier, Manager, Teller),
%  Smith is the cashier.
%  Brown is the manager.
%  Jones is the teller.
   fail.
%-------------------------------------------------------------------------------
display(Cashier, Manager, Teller) :-
   write('Cashier='), write(Cashier),
   write(' Manager='), write(Manager),
   write(' Teller='), write(Teller),
   write('\n').
%-------------------------------------------------------------------------------
differ(X, X) :- !, fail.
differ(_, _).
differ(X, X, _) :- !, fail.
differ(X, _, X) :- !, fail.
differ(_, X, X) :- !, fail.
differ(_, _, _).
%-------------------------------------------------------------------------------
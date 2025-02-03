%-------------------------------------------------------------------------------
% 2
% Clark, Daw and Fuller make their living as carpenter,   painter and plumber,
% though not necessarliy respectively.  The painter recently tried to get the
% carpenter to do some work for him, but was told that the carpenter was out
% doing some remodeling for the plumber.  The plumber makes more money than the
% painter.  Daw makes more money than Clark.  Fuller has never heard of Daw.
% What is each man's occupation?
:- initialization(main).
person(clark).
person(daw).
person(fuller).
differ(X, X, _) :- !, fail.
differ(X, _, X) :- !, fail.
differ(_, X, X) :- !, fail.
differ(_, _, _).
hasHeardOf(fuller, daw) :- !, fail.
hasHeardOf(_, _).
earnsMore(daw, clark).
doesEarnMore(X, Y) :- earnsMore(X, Y).
doesEarnMore(X, Y) :- earnsMore(Y, X), !, fail.
doesEarnMore(X, Z) :- earnsMore(X, Y), earnsMore(X, Z).
statement(X, V, Y) :- write(X), write(V), write(Y), write('.\n').
main :-
   person(Carpenter),
   person(Painter),
   person(Plumber),
   write('\n'),
   differ(Carpenter, Painter, Plumber),
   write('Carpenter:'), write(Carpenter),
   write(' Painter:'),  write(Painter),
   write(' Plumber:'),  write(Plumber),
   write('\n'),
   hasHeardOf(Painter, Carpenter), statement(Painter,   ' has heard 1st of ', Carpenter),
   hasHeardOf(Carpenter, Painter), statement(Carpenter, ' has heard 2nd of ', Painter),
   hasHeardOf(Carpenter, Plumber), statement(Carpenter, ' has heard 3rd of ', Plumber),
   hasHeardOf(Plumber, Carpenter), statement(Plumber,   ' has heard 4th of ', Carpenter),
   doesEarnMore(Plumber, Painter), statement(Plumber, ' makes more money than ', Painter),
   write('WINNER'),
   fail.
%  Carpenter=clark
%  Painter=daw
%  Plumber=fuller

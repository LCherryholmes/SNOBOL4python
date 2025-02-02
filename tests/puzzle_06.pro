%-------------------------------------------------------------------------------
% 6
% Clark, Jones, Morgan, and Smith are four men whose occupation are butcher,
% druggist, grocer, and policeman, though not necessarily respectively.  Clark
% and Jones are neighbors and take turns driving each other to work.  Jones
% makes more money than Morgan.  Clark beats Smith regularly at bowling.  The
% butcher always walks to work.  The policeman does not not live near the
% druggist.  The only time the grocer and the policeman ever met was when the
% policeman arrested the grocer for speeding.  The policeman makes more money
% than the druggist or the grocer.  What is each man's occupation?
:- initialization(main).
differ(X, X, _, _) :- !, fail.
differ(X, _, X, _) :- !, fail.
differ(X, _, _, X) :- !, fail.
differ(_, X, X, _) :- !, fail.
differ(_, X, _, X) :- !, fail.
differ(_, _, X, X) :- !, fail.
differ(_, _, _, _).

knows(policeman, grocer) :- !, fail. % The only time the grocer and the policeman ever met was
knows(grocer, policeman) :- !, fail. % when the policeman arrested the grocer for speeding.
knows(_, _).

livesNear(policeman, druggist) :- !, fail. % The policeman does not not live near the druggist.
livesNear(druggist, policeman) :- !, fail.
livesNear(_, _).

drives(butcher) :- !, fail. % The butcher always walks to work.
drives(_).

earnsMore(druggist, policeman) :- !, fail. % The policeman makes more money than the druggist
earnsMore(grocer, policeman) :- !, fail. % or the grocer.
earnsMore(_, _).

display(Clark, Jones, Morgan, Smith) :-
   write('Clark='), write(Clark),
   write(' Jones='), write(Jones),
   write(' Morgan='), write(Morgan),
   write(' Smith='), write(Smith),
   write('\n').

% Clark, Jones, Morgan, and Smith are four men whose occupation are butcher,
% druggist, grocer, and policeman, though not necessarily respectively.
occupation(butcher).
occupation(druggist).
occupation(grocer).
occupation(policeman).
main :-
   occupation(Clark),
   occupation(Jones),
   occupation(Morgan),
   occupation(Smith),
   differ(Clark, Jones, Morgan, Smith),
   livesNear(Clark, Jones), %  Clark and Jones are neighbors
   knows(Clark, Jones), % and take turns driving each other to work.
   drives(Clark),
   drives(Jones),
   earnsMore(Jones, Morgan), % Jones makes more money than Morgan.
   knows(Clark, Smith), % Clark beats Smith regularly at bowling.
   display(Clark, Jones, Morgan, Smith), % What is each man's occupation?
%  Clark is the druggist
%  Jones the grocer
%  Morgan the butcher
%  Smith the policeman.
   fail.
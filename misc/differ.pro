%-------------------------------------------------------------------------------
differ(X, X) :- !, fail.
differ(_, _).
differ(X, X, _) :- !, fail.
differ(X, _, X) :- !, fail.
differ(_, X, X) :- !, fail.
differ(_, _, _).
differ(X, X, _, _) :- !, fail.
differ(X, _, X, _) :- !, fail.
differ(X, _, _, X) :- !, fail.
differ(_, X, X, _) :- !, fail.
differ(_, X, _, X) :- !, fail.
differ(_, _, X, X) :- !, fail.
differ(_, _, _, _).
differ(X, X, _, _, _) :- !, fail.
differ(X, _, X, _, _) :- !, fail.
differ(X, _, _, X, _) :- !, fail.
differ(X, _, _, _, X) :- !, fail.
differ(_, X, X, _, _) :- !, fail.
differ(_, X, _, X, _) :- !, fail.
differ(_, X, _, _, X) :- !, fail.
differ(_, _, X, X, _) :- !, fail.
differ(_, _, X, _, X) :- !, fail.
differ(_, _, _, X, X) :- !, fail.
differ(_, _, _, _, _).
%-------------------------------------------------------------------------------

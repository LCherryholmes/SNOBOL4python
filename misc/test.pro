% https://www.metalevel.at/prolog/puzzles
%-----------------------------------------------------------------------------------------------------------------------
% Which answer is correct?
%     1. All of the below.
%     2. None of the below.
%     3. All of the above.
%     4. At least one of the above.
%     5. None of the above.
%     6. None of the above.

solution(
    [A1,A2,A3,A4,A5,A6]) :-
        sat(A1 =:= A2 * A3 * A4 * A5 * A6),
        sat(A2 =:= ~(A3 + A4 + A5 + A6)),
        sat(A3 =:= A1 * A2),
        sat(A4 =:= A1 + A2 + A3),
        sat(A5 =:= ~(A1 + A2 + A3 + A4)),
        sat(A6 =:= ~(A1 + A2 + A3 + A4 + A5)).
%-----------------------------------------------------------------------------------------------------------------------
% Lewis Carroll
% None of the unnoticed things, met with at sea, are mermaids.
% Things entered in the log, as met with at sea, are sure to be worth remembering.
% I have never met with anything worth remembering, when on a voyage.
% Things met with at sea, that are noticed, are sure to be recorded in the log.

% N   it is noticed
% M   it is a mermaid
% L   it is entered in the log
% R   it is worth remembering
% I   I have seen it

sea([N,M,L,R,I]) :-
        sat(M =< N),   % statement 1
        sat(L =< R),   % statement 2
        sat(I =< ~R),  % statement 3
        sat(N =< L).   % statement 4

implication_chain([], Prev) --> [Prev].
implication_chain(Vs0, Prev) --> [Prev],
        { select(V, Vs0, Vs) },
        (   { taut(Prev =< V, 1) } -> implication_chain(Vs, V)
        ;   { taut(Prev =< ~V, 1) } -> implication_chain(Vs, ~V)
        ).

?- sea(Vs),
   Vs = [N,M,L,R,I],
   select(Start, Vs, Rest),
   phrase(implication_chain(Rest, Start), Cs).
%-----------------------------------------------------------------------------------------------------------------------
% Cryptoarithmetic puzzles
%     CP
% +   IS
% +  FUN
% --------
% = TRUE

digits_number(Ds, N) :-
        length(Ds, _),
        Ds ins 0..9,
        reverse(Ds, RDs),
        foldl(pow, RDs, 0-0, N-_).

pow(D, N0-I0, N-I) :-
        N #= N0 + D*10^I0,
        I #= I0 + 1.

?- digits_number([C,P], CP),
   digits_number([I,S], IS),
   digits_number([F,U,N], FUN),
   digits_number([T,R,U,E], TRUE),
   CP + IS + FUN #= TRUE,
   Vs = [C,P,I,S,F,U,N,T,R,E],
   all_distinct(Vs),
   label(Vs).
%-----------------------------------------------------------------------------------------------------------------------
% Zebra Puzzle: There are five houses, each painted in a unique color. Their inhabitants are from different nations, own different pets, drink different beverages and smoke different brands of cigarettes.
%     The Englishman lives in the red house.
%     The Spaniard owns the dog.
%     Coffee is drunk in the green house.
%     The Ukrainian drinks tea.
%     From your perspective, the green house is immediately to the right of the ivory house.
%     The Old Gold smoker owns snails.
%     Kools are smoked in the yellow house.
%     Milk is drunk in the middle house.
%     The Norwegian lives in the first house.
%     The man who smokes Chesterfields lives in the house next to the man with the fox.
%     Kools are smoked in the house next to the house where the horse is kept.
%     The Lucky Strike smoker drinks orange juice.
%     The Japanese smokes Parliaments.
%     The Norwegian lives next to the blue house.
% Who drinks water? Who owns the zebra?

solution(Pairs, Water, Zebra, Vs) :-
        Table   = [Houses,Nations,Drinks,Smokes,Animals],
        Houses  = [Red,Green,Yellow,Blue,Ivory],
        Nations = [England,Spain,Ukraine,Norway,Japan],
        Names   = [england,spain,ukraine,norway,japan],
        Drinks  = [Coffee,Milk,OrangeJuice,Tea,Water],
        Smokes  = [OldGold,Kools,Chesterfield,LuckyStrike,Parliaments],
        Animals = [Dog,Snails,Horse,Fox,Zebra],
        pairs_keys_values(Pairs, Nations, Names),
        maplist(all_distinct, Table),
        append(Table, Vs),
        Vs ins 1..5,
        England #= Red,               % hint 1
        Spain #= Dog,                 % hint 2
        Coffee #= Green,              % hint 3
        Ukraine #= Tea,               % hint 4
        Green #= Ivory + 1,           % hint 5
        OldGold #= Snails,            % hint 6
        Kools #= Yellow,              % hint 7
        Milk #= 3,                    % hint 8
        Norway #= 1,                  % hint 9
        next_to(Chesterfield, Fox),   % hint 10
        next_to(Kools, Horse),        % hint 11
        LuckyStrike #= OrangeJuice,   % hint 12
        Japan #= Parliaments,         % hint 13
        next_to(Norway, Blue).        % hint 14

next_to(H, N) :- abs(H-N) #= 1.

?- solution(Pairs, Water, Zebra, Vs), label(Vs).
       Pairs = [3-england,4-spain,2-ukraine,1-norway,5-japan],
       Water = 1,
       Zebra = 5,
       Vs = [3,5,1,2,4,3,4,2,1,5,5,3,4,2,1,3,1,2,4,5|...]
    ;  false.
%-----------------------------------------------------------------------------------------------------------------------
% Escape from Zurg
% Buzz, Woody, Rex, and Hamm have to escape from Zurg. They merely have to cross one last bridge before they are free.
% However, the bridge is fragile and can hold at most two of them at the same time. Moreover, to cross the bridge a
% flashlight is needed to avoid traps and broken parts. The problem is that our friends have only one flashlight with
% one battery that lasts for only 60 minutes. The toys need different times to cross the bridge (in either direction):

% Toy   Time
% Buzz     5
% Woody   10
% Rex     20
% Hamm    25

% Since there can be only two toys on the bridge at the same time, they cannot cross the bridge all at once. Since
% they need the flashlight to cross the bridge, whenever two have crossed the bridge, somebody has to go back and
% bring the flashlight to those toys on the other side that still have to cross the bridge. The problem now is: In
% which order can the four toys cross the bridge in time (that is, within 60 minutes) to be saved from Zurg?

toy_time(buzz,   5).
toy_time(woody, 10).
toy_time(rex,   20).
toy_time(hamm,  25).

moves(Ms) :- phrase(moves(state(0,[buzz,woody,rex,hamm],[])), Ms).

moves(state(T0,Ls0,Rs0)) -->
        { select(Toy1, Ls0, Ls1), select(Toy2, Ls1, Ls2),
          Toy1 @< Toy2,
          toy_time(Toy1, Time1), toy_time(Toy2, Time2),
          T1 #= T0 + max(Time1,Time2), T1 #=< 60 },
        [left_to_right(Toy1,Toy2)],
        moves_(state(T1,Ls2,[Toy1,Toy2|Rs0])).

moves_(state(_,[],_))     --> [].
moves_(state(T0,Ls0,Rs0)) -->
        { select(Toy, Rs0, Rs1),
          toy_time(Toy, Time),
          T1 #= T0 + Time, T1 #=< 60 },
        [right_to_left(Toy)],
        moves(state(T1,[Toy|Ls0],Rs1)).
%-----------------------------------------------------------------------------------------------------------------------
% Cryptoarithmetic puzzles
% FOSSO+FOSSO=CISCO

puzzle([F,O,S,S,O] + [F,O,S,S,O] = [C,I,S,C,O]) :-
        Vars = [F,O,S,C,I],
        Vars ins 0..9,
        all_different(Vars),
                  F*10000 + O*1000 + S*100 + S*10 + O +
                  F*10000 + O*1000 + S*100 + S*10 + O #=
                  C*10000 + I*1000 + S*100 + C*10 + O,
        F #\= 0, C #\= 0.
%-----------------------------------------------------------------------------------------------------------------------
% SODOKU
%
%  Problem statement                 Solution
%
%   .  .  4 | 8  .  . | .  1  7      9  3  4 | 8  2  5 | 6  1  7
%           |         |                      |         |
%   6  7  . | 9  .  . | .  .  .      6  7  2 | 9  1  4 | 8  5  3
%           |         |                      |         |
%   5  .  8 | .  3  . | .  .  4      5  1  8 | 6  3  7 | 9  2  4
%   --------+---------+--------      --------+---------+--------
%   3  .  . | 7  4  . | 1  .  .      3  2  5 | 7  4  8 | 1  6  9
%           |         |                      |         |
%   .  6  9 | .  .  . | 7  8  .      4  6  9 | 1  5  3 | 7  8  2
%           |         |                      |         |
%   .  .  1 | .  6  9 | .  .  5      7  8  1 | 2  6  9 | 4  3  5
%   --------+---------+--------      --------+---------+--------
%   1  .  . | .  8  . | 3  .  6      1  9  7 | 5  8  2 | 3  4  6
%           |         |                      |         |
%   .  .  . | .  .  6 | .  9  1      8  5  3 | 4  7  6 | 2  9  1
%           |         |                      |         |
%   2  4  . | .  .  1 | 5  .  .      2  4  6 | 3  9  1 | 5  7  8
%-----------------------------------------------------------------------------------------------------------------------
% Nonograms
%
%     Problem statement:          Solution:
%
%         |_|_|_|_|_|_|_|_| 3         |_|X|X|X|_|_|_|_| 3
%         |_|_|_|_|_|_|_|_| 2 1       |X|X|_|X|_|_|_|_| 2 1
%         |_|_|_|_|_|_|_|_| 3 2       |_|X|X|X|_|_|X|X| 3 2
%         |_|_|_|_|_|_|_|_| 2 2       |_|_|X|X|_|_|X|X| 2 2
%         |_|_|_|_|_|_|_|_| 6         |_|_|X|X|X|X|X|X| 6
%         |_|_|_|_|_|_|_|_| 1 5       |X|_|X|X|X|X|X|_| 1 5
%         |_|_|_|_|_|_|_|_| 6         |X|X|X|X|X|X|_|_| 6
%         |_|_|_|_|_|_|_|_| 1         |_|_|_|_|X|_|_|_| 1
%         |_|_|_|_|_|_|_|_| 2         |_|_|_|X|X|_|_|_| 2
%          1 3 1 7 5 3 4 3             1 3 1 7 5 3 4 3
%          2 1 5 1                     2 1 5 1
%-----------------------------------------------------------------------------------------------------------------------
% river crossing puzzles
% 2. You have a fox, a chicken, and a sack of grain. You need to get all three across a river in a boat. The boat can only carry one item at a time. If left alone, the fox will eat the chicken, and the chicken will eat the grain. How do you get them all across safely?
%-----------------------------------------------------------------------------------------------------------------------
% Five friends (Alex, Benjamin, Chloe, David, and Emily) are sitting down to eat at a restaurant. They each have a different favorite color (red, blue, green, yellow, and purple), and they each have a favorite dessert (cake, ice cream, pie, cookies, and brownies). Can you figure out each friend's favorite color and favorite dessert, using the following clues?
%   Benjamin is sitting next to the person whose favorite color is blue.
%   David's favorite dessert is pie.
%   Emily is sitting next to the person whose favorite dessert is cookies.
%   Alex's favorite color is not green.
%   The person who likes cake is sitting next to the person who likes ice cream.
%   Chloe does not like blue or yellow.
%-----------------------------------------------------------------------------------------------------------------------
% 10. Jane went to visit Jill. Jill is Jane’s only husband’s mother-in-law’s only husband’s only daughter’s only daughter. What relation is Jill to Jane?
%-----------------------------------------------------------------------------------------------------------------------
% 17. Four girls are in line to buy smoothies. Lacey is behind Stacy but not last. Casey is in front of Macy. Stacy is directly behind Casey. Who is at the end of the line?
%-----------------------------------------------------------------------------------------------------------------------
% Tom works Monday, Thursday, and Friday nights. Jay works all day Tuesday, Thursday, and Friday, and mornings on weekends. Tom dances Wednesday and Saturday night, while Jay swims Sunday and Monday mornings. When do both of their schedules allow them to meet?
%-----------------------------------------------------------------------------------------------------------------------
% 36. Jasmine is four times as old as her little sister, April. In 20 years, April will be half as old as Jasmine. How old could Jasmine be right now?
%-----------------------------------------------------------------------------------------------------------------------
%-----------------------------------------------------------------------------------------------------------------------
%-----------------------------------------------------------------------------------------------------------------------
%-----------------------------------------------------------------------------------------------------------------------
%-----------------------------------------------------------------------------------------------------------------------

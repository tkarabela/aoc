?- use_module(library(clpfd)).

%% ----------------------------------------------------------------------------
%% part 1, counting positive differences
%% ----------------------------------------------------------------------------

foo([X|Xs], R) :- foo_(Xs, X, 0, R).

foo_([], Prev, Carry, Carry).
foo_([X|Xs], Prev, Carry, Result) :- X #> Prev, foo_(Xs, X, CarryNext, Result), Carry + 1 #= CarryNext.
foo_([X|Xs], Prev, Carry, Result) :- X #=< Prev, foo_(Xs, X, Carry,   Result).

%% ----------------------------------------------------------------------------
%% part 2, list of 3-sums
%% ----------------------------------------------------------------------------

bar(X, R) :-
    prefix([X1, X2, X3], X) -> (
        X1 + X2 + X3 #= Xsum,
        [_|Xs] = X,
        bar(Xs, Rrest),
        append([Xsum], Rrest, R)
    ); R = [].


%% X in 1..100, A in 1..100, bar([1,A,X,4], [5,8]), label([A,X]).
%% [X,A] ins 1..100, bar([1,A,X,4], [5,8]), label([A,X])
%% [X,A] ins 1..sup, bar([1,A,X,4], [5,8]), label([A,X]).
%% [A,B,C,D] ins 1..sup, bar([A,B,C,D], [5,8]), label([A,B,C,D]).
%% [A,B,C,D] ins 1..sup, A #> C, bar([A,B,C,D], [5,8]), label([A,B,C,D]).

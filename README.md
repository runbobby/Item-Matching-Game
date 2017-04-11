# Item-Matching-Game
algorithms to exactly solve "Item Matching," a one-player game, which seems infeasible analytically.


Section 0: Results (probably should put after Section 1, but whatever, you know).

For S = 5, T = 4, 

I = 5: 3119 / 3125 = max probability of winning
I = 6: 7735 / 7776
I = 7: 16621 / 16807
I = 8: 31322 / 32768
I = 9: 49728 / 59045
I = 10: 68327 / 100000

Section 1: Rules

"Item Matching" is a one-player game with some randomness. Each "match" is either a win or a loss. The goal is to maximize the probability of winning. Each match has known parameters, S, I, and T. These are the starting number of slots, the number of items, and the number of turns/tries. Call the slots s_1, ..., s_S.

During each match, first each slot receives an item, allowing replacement, and "Bob" doesn't know them. To be precise, the assignment is a uniformly random element of {1, ..., I}^S. Call this assignment A.

For concreteness, we will show examples in which S = 5, I = 7, T = 4, items are in {1, ..., 7}, and sequences of items are represented as strings. We will also use one-indexing.

Next "Bob" makes query Q_1, then receives information/response R_2, then makes query Q_2, then receives information R_2, all the way up to Q_t.
Each Query is an element of {1, ..., I}^S. Bob wins iff at least one of the Q_i equals A (and we can say that match ends early). The information R_i is solely a function of Q_i and A, call it F(Q_i, A).

Definition of F(Q_i, A). F maps (Q_i, A) to a length S sequence with values in {Incorrect, Wrong slot, Correct}, and this corresponds to the slots. (These may be abbreviated I, W, C.) There are 3 rules. 

1. For j in {1, ..., S}, F(Q\_i, A)\_j = Correct iff (Q\_i)\_j = A\_j. 

2. For j in {1, ..., S}, F(Q\_i, A)\_j = Incorrect iff item (Q\_i)\_j doesn't occur in A except possibly in a "Correct" index. To be precise, F(Q_i, A)\_j = Incorrect iff for all k with A\_k = (Q\_i)\_j, we have (Q\_i)\_k = A\_k.

3. For j in {1, ..., S}, F(Q\_i, A)\_j = Wrong slot in any other case.

Examples. F(12345, 12345) = CCCCC. F(12345, 34567) = IIWWW. F(11234, 51155) = WCIII. F(11234, 44444) = IIIIC.

We impose certain restrictions on Q\_i. These rules could be adjusted without conceptually changing the game much, but they do change the exact solution quite a bit. 

Restriction 1: If item l was marked as Incorrect in any previous response R\_i, then item l can't be used in any query Q\_{i+1} .... To be precise, if we have F(Q\_i, A)\_j = R\_j = I, then the item (Q\_i)\_j cannot be used (as a term) in any query Q\_{i+1}, ...

Restriction 2: If slot j was marked as correct in any previous response R\_i, say F(Q\_i, A)\_j = R\_j = C, then all future queries Q\_{i+1} ... must have term j equal to A\_j. Equivalently, slot j becomes useless.

Examples. A = 12345. Q_1 = 12567. R_1 = CCIIW. Now, future queries must have first two terms equal to 1 and 2. Equivalently, the first two slots become useless. Items 3 and 4 cannot be used in future queries. Thus possible queries have the form 1, 2, {5,6,7}, {5,6,7}, {5,6,7}.

Note 1: Queries don't have to satisfy previous responses $R_i.$

Note 2: There's many other reasonable things to optimize. For example, the number of items used (if we don't count items forced by Restriction 2. Instead of Restriction 2, we might say that the query has no items in those slots, and we want to use few items while maximizing win probability). Another example is to give the items different costs. For example, item 1 has cost 10, and item 2 has cost 40. What's the minimum combination of win probability and item cost?

Remark 1: Let S = 5, I = 7, T = 4. I claim that we can't guarantee winning. Indeed, consider query Q_1. No matter what Q_1 is, there is a probability of 30 / 7^5 that the response will be (CCCCI) or a permutation. This is because there are exactly 30 out of 7^5 sequences A which match Q_1 in exactly 4 spots (and CCCCW is an impossible response). Suppose that this is our response. It's easy to see that we are reduced to guessing an unknown item out of six items, we have 3 guesses, and no information at all. The conditional probability of winning is 1/2. Therefore, we've bounded the max probability of winning by 1 - 15 / 16807. The true maximum is exactly 16621 / 16807. In general, we can't guarantee winning if I > T, but the probability can be very high. 

(If I <= T, we can guarantee winning by guessing all item 1 for query 1, then all item 2 (except known correct spots) for query 2, then all item 3, etc.)

-----------------------------------------------------
Section 2. _Method of Exact Solution_

There is one main lemma about probabilities that simplifies the analysis and reduces this to a counting problem. The rest of the simplifying steps are algorithmic in nature. Broadly speaking, we use a lot of isomorphisms to reduce the number of cases computed. Certain states are isomorphic, and for a certain guess, certain queries are isomorphic.

(Definition: A state is a possible sequence of past queries and responses. This completely determines the subproblem.)

We also precompute certain data structures to reject certain ordered triples of (state, query, response). Another main step is to quite efficiently test if a certain state has at least one valid assignment. For example, we can loop through all I^S item sequences and test satisfiability, but this is slow.  The last main step is to recursively evaluate a state by maximizing over all possible guesses. This involves memoization to recall previously computed evaluations.

Main Lemma: (to be continued, maybe)

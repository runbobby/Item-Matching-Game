# Item-Matching-Game
algorithms to exactly solve "Item Matching," a one-player game


Section 1: Rules

"Item Matching" is a one-player game with some randomness. Each "match" is either a win or a loss. The goal is to maximize the probability of winning. Each match has known parameters, S, I, and T. These are the starting number of slots, the number of items, and the number of turns/tries. Call the slots s_1, ..., s_S.

During each match, first each slot receives an item, allowing replacement, and "Bob" doesn't know them. To be precise, the assignment is a uniformly random element of {1, ..., I}^S. Call this assignment A.

Next "Bob" makes query Q_1, then receives information R_2, then makes query Q_2, then receives information R_2, all the way up to Q_t.
Each Query is an element of {1, ..., I}^S. Bob wins iff at least one of the Q_i equals A (and we can say that match ends early). The information R_i is solely a function of Q_i and A, call it F(Q_i, A).

Definition of F(Q_i, A). F maps (Q_i, A) to a length S sequence with values in {Incorrect, Wrong slot, Correct}, and this corresponds to the slots. For j in {1, ..., S}, F(Q_i, A)\_S = Correct iff (F\_i)\_S = A\_S. 

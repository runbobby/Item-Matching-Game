import numpy as np
%cd 
%cd Documents\item_matching\data
import copy
import json


# warning!!!!!!!!!!!!!!!!!
# this code uses integer division twice
# may need to rewrite code depending on environment

# update: gg my lyf, I forgot "yellow items."
# def: an item is yellow if we know some slots where that item can't go
# but don't know if there is at least one
# it occurs when an item is previously orange and in a certain query, we get some correct spots
# and zero incorrect spots / wrong spots
# It is possible for a yellow item to not have any available slots (NOT a red item)

# prop: y + u <= max_s

# how is a yellow item encoded?
# variable y counting # yellow items and base (2^u) number, y digits

# how is a yellow item turned managed with grid isomorphism classes?
# when we map all binary grids to valid representatives via
# class[grid_integer],
# we need to encode the associated transformation in S_u, call it
# Sn[u, o, grid_integer] -> S_u
# then the pair (grid_integer, y1, y2)
# transforms to (vr[Class[gi]], Sn[u, o, gi][y1], Sn[u, o, g2][y2])

# now, a state is a pair (u, o, g, y, grid, y_grid), turns_left

# we encode S5 as a 5-tuple a_0 a_1 a_2 a_3 a_4 in {0, ..., 4}^5
# for example (12340) (01100) = (00110). old item 0 goes to new item a_0, etc.
# we precompute action(u, perm, y), which maps S_u x {0,1}^u -> {0,1}^u

# note that there are multiple possible values of the function Sn, but just one suffices


# how does a yellow item affect guess isomorphism classes?
# instead of {0, ..., o-1}^u, we have {o, ..., o+y-1}^u

# no early rejection for yellow items
# rejection for yellow items: we reject if in a certain spot

# how does a yellow item transform?
# C, I, -> red
# C, W, -> orange
# C,    -> yellow
# I     -> red
# W     -> orange
#       -> yellow

# for completeness, whole transformation rules
# anything + (I) or (CI) -> red
# anything + (W) or (CW) -> orange
# gray + (C) -> gray
# orange/yellow + (C) -> yellow
# anything + ( ) -> nothing happens


# parameters
# u = # unsolved, o = # orange items; o <= u
# max_s = max number of slots (so the starting number)
# max_i = max number of items
# max_t = max number of turns
max_s = 5
max_i = 10
max_t = 6

# possible grids.
# the integer i corresponds to a grid as follows:
# i = i_{uo-1} i_{uo-2} ... i_1 i_0 in binary
# digit 0 means "known incorrect." digit 1 means "no info"

# example
#        slot0, slot1, slot2, slot3
# item1  i_0    i_1    i_2    i_3
# item2  i_4    i_5    i_6    i_7
# item3  i_8    i_9    i_10   i_11


# a state is an ordered pair (# slots, # orange, # gray, # grid, # turns left)

# task 1: for each grid, we want to find a somewhat short list of possible
# non-isomorphic guesses.
# this slightly depends on the # of gray items
# For each guess, there's <= 3^5 outcomes
# which we encode as a base 3 integer a_4 a_3 a_2 a_1 a_0
# a_i is the outcome for slot i
# 0: incorrect
# 1: wrong place
# 2: cocrrect

# task 2: for each (state, guess, outcome), we want to update to a new state



# input: (# unsolved slots, # orange items)
# output: an array of arrays of all possible (guess, outcome) pairs,
# any number of grays
# element g of output will be the array of pairs whose guesses use exactly
# g gray items


# NOTE: b/c of isomorphism stuff, there are no guesses with >= 2 gray items
# if u = o


# reduced by some isomorphisms, but not all (too hard)
# also reduced by certain deduction rules of impossible pairs
# but not all (?)

# the encoding of a (guess, outcome) pair will be rather long
# in order to facilitate fast rejection

# a guess is an ordered pair (g_array, g_decomps)
# g_array is an array of length u with values in {0, ..., o-1, -1, ..., -g}
# which is the array of items guessed
# positive values are orange items; negative values are gray
# g_decomps is array of length >= o which decomposes g_array
# into guess per item
# g_decomps[i] is an integer in [0, 2^u) whose binary repr is a_{u-1} ... a_0
# such that a_j equals 1 if object i was guessed in slot j

# an outcome is an ordered pair (o_array, o_decomps)
# o_array is an integer in base 3, u digits: [0, 3^u)
# 0: incorrect    1: wrong place    2: correct
# o_decomps is array of length >= o which decomposes o_array
# with base 4 encoding; in [0, 4^u).
# 0: didn't guess 1: incorrect 2: wrong place 3: correct

# preliminary rejection: For i < o, we can eliminate some pairs of
# (g_decomps[i], o_decomps[i])
# ignore digits of o_decomps[i] which correspond to 0s in g_decomps[o]
# rule 1: if o_decomps[i] has no 2's, then it also has no 0's
# rule 2: o_decomps[i] cannot have a 1 and a 0
# huh, I thought there were other rules
##### are there other rules? ????????

# For i >= 0, we can eliminate some pairs, but less pairs
# rule 1: o_decomps[i] cannot have a 1 and a 0

# jk, I will encode it as a 4-tuple (g_array, o_array, g_decomps, o_decomps)


####################################################################################
# precomputed. hooray!
# one way to compute this algorithmically is to loop through [k]^k
# keep only those tuples in which the list of first appearances is
# an initial sequence of [k]
# e.g. k = 6, one 6-tuple is (2, 1, 3, 3, 1, 2)
# the list of first appearances is (2, 1, 3)
# this is not an initial sequence of (1, 2, 3, 4, 5, 6).
# instead, the isomorphic tuple is (1, 2, 3, 3, 2, 1)
# runtime: bogosort

# according to OEIS, these are counted by the Bell numbers, A000110, 1, 1, 2, 5, 15, 52, ...
gray_guesses = [
    [[]],
    [[1]],
    [[1,1],
     [1,2]],
    [[1,1,1],
     [1,1,2],[1,2,1],[1,2,2],
     [1,2,3]],
    [[1,1,1,1],
     [1,1,1,2],[1,1,2,1],[1,1,2,2],[1,2,1,1],[1,2,1,2],[1,2,2,1],[1,2,2,2],
     [1,1,2,3],[1,2,1,3],[1,2,3,1],[1,2,2,3],[1,2,3,2],[1,2,3,3],
     [1,2,3,4]],
    [[1,1,1,1,1],
     [1,1,1,1,2],[1,1,1,2,1],[1,1,1,2,2],[1,1,2,1,1],[1,1,2,1,2],[1,1,2,2,1],[1,1,2,2,2],[1,2,1,1,1],[1,2,1,1,2],[1,2,1,2,1],[1,2,1,2,2],[1,2,2,1,1],[1,2,2,1,2],[1,2,2,2,1],[1,2,2,2,2],
     [1,1,1,2,3],[1,1,2,1,3],[1,1,2,3,1],[1,2,1,1,3],[1,2,1,3,1],[1,2,3,1,1],[1,2,2,2,3],[1,2,2,3,2],[1,2,3,2,2],[1,2,3,3,3],
     [1,1,2,2,3],[1,1,2,3,2],[1,1,2,3,3],[1,2,1,2,3],[1,2,1,3,2],[1,2,1,3,3],[1,2,2,1,3],[1,2,3,1,2],[1,2,3,1,3],[1,2,2,3,1],[1,2,3,2,1],[1,2,3,3,1],[1,2,2,3,3],[1,2,3,2,3],[1,2,3,3,2],
     [1,1,2,3,4],[1,2,1,3,4],[1,2,3,1,4],[1,2,3,4,1],[1,2,2,3,4],[1,2,3,2,4],[1,2,3,4,2],[1,2,3,3,4],[1,2,3,4,3],[1,2,3,4,4],
     [1,2,3,4,5]]
    ]
num_distinct_gray_data = [
    [0],
    [1],
    [1, 2],
    [1, 2, 2, 2, 3],
    [1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5]
    ]

# construct the array
# orange_item_early_reject[num_o][o_decomps]
orange_item_early_reject = [0]
def construct_oier():
    for u in range(1, max_s + 1):
        oier_u = []
        for i in range(pow(4, u)):
            hasI = False
            hasW = False
            hasC = False
            ii = i
            for j in range(u):
                if ii%4 == 1:
                    hasI = True
                elif ii%4 == 2:
                    hasW = True
                elif ii%4 == 3:
                    hasC = True
                ii = ii // 4
            oier_u.append(not hasI or (hasC and not hasW))
        orange_item_early_reject.append(oier_u)

orange_item_lower_bound = [0]
def construct_oilb():
    for u in range(1, max_s + 1):
        oilb_u = []
        for i in range(pow(4, u)):
            hasW = False
            count = 0
            ii = i
            for j in range(u):
                if ii % 4 == 2:
                    hasW = True
                elif ii % 4 == 3:
                    count += 1
                ii = ii // 4
            if hasW: count+= 1
            if count == 0: count = 1
            # assuming not rejected in oier, count is at least 1
            oilb_u.append(count)
        orange_item_lower_bound.append(oilb_u)


# construct the array
# gray_item_reject[num_g][o_decomps]

# important!!!!!!!!!!1 This is also used for yellow item early reject
# gilb is also used for yellow item lower bound
gray_item_reject = [0]
def construct_gir():  
    for u in range(1, max_s + 1):
        gir_u = []
        for i in range(pow(4, u)):
            hasI = False
            hasW = False
            hasN = False
            ii = i
            for j in range(u):
                if ii%4 == 1:
                    hasI = True
                elif ii%4 == 2:
                    hasW = True
                elif ii%4 == 0:
                    hasN = True
                ii = ii // 4
            
            gir_u.append((not (hasI and hasW)) and ( not (hasW and not hasN)))
        gray_item_reject.append(gir_u)

gray_item_lower_bound = [0]
def construct_gilb():
    for u in range(1, max_s + 1):
        gilb_u = []
        for i in range(pow(4, u)):
            hasW = False
            count = 0
            ii = i
            for j in range(u):
                if ii % 4 == 2:
                    hasW = True
                elif ii % 4 == 3:
                    count += 1
                ii = ii // 4
            if hasW: count+= 1
            gilb_u.append(count)
        gray_item_lower_bound.append(gilb_u)

construct_oier()
construct_oilb()
construct_gir()
construct_gilb()

# def compute_guess_outcomes_old(u, o):

def compute_guess_outcomes(u, o, y):
    # TODO: this whole thing
    
    if u < o: return None
    if u + y > max_s: return None
    go_data = [0]*(u+1)
    for i in range(u+1):
        go_data[i] = []

    
    # ogv = orangeyellow-gray vector; an integer in [0, 2^u); if digit j = 1
    # then orange/yellow item
    # otherwise, gray item
    for oyg_vector in range(pow(3, u)):
        # num_g, num_o = # gray, # orange
        # oi = orane_indices = array, len num_o,
        # oi[j] = (j+1)^(th) orange index
        # gi[j] is similar
        # example: ogv = 01011_2
        # oi = [0, 1, 3]
        # gi = [2, 4]
        num_o = 0
        num_y = 0
        num_g = 0
        oi = []
        yi = []
        gi = []
        oygv = oyg_vector
        for i in range(u):
            if oygv % 3 == 0:
                num_o += 1
                oi.append(i)
            elif oygv % 3 == 1:
                num_y += 1
                yi.append(i)
            else:
                num_g += 1
                gi.append(i)
            oygv = oygv // 3
            
        for orange_vector in range(pow(o, num_o)):
            # convert orange_vector into array of orange guesses
            orange_guess = []
            ov = orange_vector
            g_decomps = [0]*(o + y)
            for i in range(num_o):
                orange_guess.append(ov % o)
                # we use oi[i] for example because
                # if u = 5, oi [0,1,3] and orange_vector base o is 1, 4, 3
                # then g_decomps[1] = 00001_2, g_decomps[3] = 01000_2, g_decomps[4] = 00010_2
                g_decomps[ov % o] += pow(2, oi[i])
                ov = ov // o
            for yellow_vector in range(pow(y, num_y)):
                yellow_guess = []
                yv = yellow_vector
                for i in range(num_y):
                    yellow_guess.append(yv % y)
                    g_decomps[0 + (yv % y)] += pow(2, yi[i])
                    yv = yv // y

                gd_static = g_decomps
                
                for gg_index in range(len(gray_guesses[num_g])):
                    # inside this loop, we have a single orange_guess and a single gray_guess
                    # this constitutes one guess
                    # we compute g_decomps

                    # next, for this guess, there are <= 3^u possible outcomes
                    # we will compute these outcomes, perform early rejection on the outcomes
                    # and compute o_decomps
                    
                    gray_guess = gray_guesses[num_g][gg_index]
                    num_distinct_grays = num_distinct_gray_data[num_g][gg_index]
                    # reject if u == o and num_distinct_grays > 1
                    if (u == o) and num_distinct_grays > 1:
                        continue
                    
                    g_decomps = copy.copy(gd_static)
                    # given oi, gi, orange_guess, and gray_guess
                    # compute the array of guesses, or g_array
                    g_array = [0]*u
                    for a in range(num_o):
                        g_array[oi[a]] = orange_guess[a]
                    for a in range(num_y):
                        g_array[yi[a]] = yellow_guess[a] + o
                    for a in range(num_g):
                        g_array[gi[a]] = o + y - 1 + gray_guess[a]

                    # we have already computed g_decomps for orange and yellow items
                    # need to compute for gray items
                    for i in range(num_distinct_grays):
                        gd = 0
                        for j in range(num_g):
                            # use gi[j] instead of j
                            if gray_guess[j] == i + 1:
                                gd += pow(2, gi[j])
                        g_decomps.append(gd)
                        
                    for outcome_vector in range(pow(3, u)):
                        # compute o_decomps
                        ov = outcome_vector
                        o_array = outcome_vector
                        
                        o_decomps = [0]*(o + y + num_distinct_grays)
                        for i in range(u):
                            o_decomps[g_array[i]] += pow(4, i) * (1 + (ov % 3))
                            ov = ov // 3
                        

                        # perform early rejection
                        rejected = False
                        for i in range(o):
                            if not orange_item_early_reject[u][o_decomps[i]]:
                                rejected = True
                                break
                        if rejected: continue
                        for i in range(y):
                            if not gray_item_reject[u][o_decomps[o + i]]:
                                rejected = True
                                break
                        if rejected: continue
                        for i in range(num_distinct_grays):
                            if not gray_item_reject[u][o_decomps[o + y + i]]:
                                rejected = True
                                break
                        if rejected: continue

                        # more rejection: compute a lower bound on the number of items accounted for
                        count = 0
                        for i in range(o):
                            count += orange_item_lower_bound[u][o_decomps[i]]
                        for i in range(y):
                            count += gray_item_lower_bound[u][o_decomps[o + i]]
                        for i in range(num_distinct_grays):
                            count += gray_item_lower_bound[u][o_decomps[o + y + i]]
                        if count > u:
                            continue
                            
                        # now we have a (guess, outcome) pair which is not rejected. 
                        go_data[num_distinct_grays].append(
                            [copy.copy(g_array), o_array, copy.copy(g_decomps), o_decomps])
                    
    return go_data
                            


go_data = [0]*(max_s+1)
for i in range(max_s + 1):
    go_data[i] = [0]*(max_s+1)
    for j in range(max_s + 1):
        go_data[i][j] = [0]*(max_s + 1)
for num_slots in range(1, max_s+1):
    for num_orange in range(num_slots + 1):
        for num_yellow in range(max_s + 1 - num_slots):
            f = open('go_data'+str(num_slots)+str(num_orange)+str(num_yellow)+'.txt', 'w')
            go_data[num_slots][num_orange][num_yellow] = compute_guess_outcomes(num_slots, num_orange, num_yellow)
            json.dump(go_data[num_slots][num_orange][num_yellow], f)
            f.close()
            print(num_slots, num_orange, num_yellow)
         

    


     
    
    
# construct the array
# orange_item_full_reject[existing_grid_row][o_decomps]
# additional rule: o_decomps cannot have a 2 in a spot that
# existing_grid_row has a 0

# consider also precomputing the new grid row as a function of these
orange_item_full_reject = [0]
orange_item_new_row = [0]
yellow_item_full_reject = [0]
yellow_item_new_row = [0]
def construct_oifr():
    for u in range(1, max_s + 1):
        oinr_u = []
        oifr_u = []
        yifr_u = []
        yinr_u = []
        for row in range(pow(2, u)):
            # these cases should never be accessed by the rest of the program
            #if row == 0:
            #    oifr_u.append([False] * pow(4, u))
            #    oinr_u.append([0] * pow(4, u))
            #    continue
            oinr_u_row = []
            oifr_u_row = []
            yinr_u_row = []
            yifr_u_row = []
            
            row_bin = []
            r = row
            for j in range(u):
                row_bin.append(r % 2)
                r = r // 2
            for i in range(pow(4, u)):
                # if u == 3 and row == 0:
                #     print i
                ii = i
                rejected = False
                hasI = False
                hasC = False
                hasW = False
                new_row_bin = copy.copy(row_bin)
                for j in range(u):
                    
                    if ii % 4 == 3:
                        hasC = True
                        new_row_bin[j] = 0
                    if row_bin[j] == 0 and ii % 4 == 3:
                        # new_row_bin[j] = 0
                        oifr_u_row.append(False)
                        oinr_u_row.append(0)
                        yifr_u_row.append(False)
                        yinr_u_row.append(0)
                        rejected = True
                        break
                    elif ii % 4 == 1:
                        hasI = True
                    elif ii % 4 == 2:
                        new_row_bin[j] = 0
                        hasW = True
                    ii = ii // 4
                if rejected:
                    continue  
                # compute new row as a binary number [0, 2^u)
                # note that digits where item is correct are irrelevant after update
                # if o_decomp has an "Incorrect", we encode that as "-2"
                # default: 0
                if hasI and hasW:
                    oinr_u_row.append(0)
                    oifr_u_row.append(False)
                    yinr_u_row.append(0)
                    yifr_u_row.append(False)
                    continue                    
                if hasI: # assuming that !hasC, !hasW, hasI, orange rejected already
                    yinr_u_row.append(-2)
                    yifr_u_row.append(True)
                    oinr_u_row.append(-2)
                    oifr_u_row.append(True)
                    continue
                
                new_row = 0
                for j in range(u):
                    new_row += new_row_bin[j] * pow(2, j)

                if (not hasW) and hasC:
                # in this case, we need to indicate that the item should
                # become a yellow row
                # yellow rows are encoded by adding 2^u
                    oifr_u_row.append(True)
                    yifr_u_row.append(True)
                    oinr_u_row.append(new_row + pow(2, u))
                    yinr_u_row.append(new_row + pow(2, u))
                    continue
                if not hasW:
                    oifr_u_row.append(True)
                    yifr_u_row.append(True)
                    oinr_u_row.append(new_row)
                    yinr_u_row.append(new_row + pow(2, u))
                    continue
                if new_row == 0:
                    oinr_u_row.append(0)
                    oifr_u_row.append(False)
                    yinr_u_row.append(0)
                    yifr_u_row.append(True)
                    continue
                oinr_u_row.append(new_row)
                oifr_u_row.append(True)
                yinr_u_row.append(new_row)
                yifr_u_row.append(True)
            oinr_u.append(oinr_u_row)
            oifr_u.append(oifr_u_row)
            yinr_u.append(yinr_u_row)
            yifr_u.append(yifr_u_row)
        orange_item_new_row.append(oinr_u)
        orange_item_full_reject.append(oifr_u)
        yellow_item_new_row.append(yinr_u)
        yellow_item_full_reject.append(yifr_u)



# construct_ginr[o_decomps]
gray_item_new_row = [0]
def construct_ginr():
    for u in range(1, max_s + 1):
        ginr_u = []
        for i in range(pow(4, u)):
            ii = i
            hasI = False
            hasW = False
            hasC = False
            # we initialize with 1's because new_row_bin is used in the case
            # hasW and not hasI, note that in this case, we get a new orange item
            # and generally, most of the spots are avaliable, so they start at 1
            # and then we correct
            new_row_bin = [1] * u
            for j in range(u):
                if ii % 4 == 3:
                    hasC = True
                    new_row_bin[j] = 0
                elif ii % 4 == 2:
                    hasW = True
                    new_row_bin[j] = 0
                elif ii % 4 == 1:
                    hasI = True
                ii = ii // 4
            if hasI:
                ginr_u.append(-2)
            elif hasC and not hasW:
                ginr_u.append(-1)
            elif not hasC and not hasW:
            # uhh then i = 0 in this case, whatever
                ginr_u.append(-1)
            else:
                # compute new_row
                new_row = 0
                for j in range(u):
                    new_row += new_row_bin[j] * pow(2, j)
                ginr_u.append(new_row)
        gray_item_new_row.append(ginr_u)


construct_oifr()
construct_ginr()



# load grid classes
classes = [0]*6
for i in range(6):
    classes[i] = [0] * 6
    for j in range(6):
        classes[i][j] = [0] * 6
valid_reprs = [0]*6
for i in range(6):
    valid_reprs[i] = [0] * 6
    for j in range(6):
        valid_reprs[i][j] = [0] * 6
num_1_valid = [0]*6
for i in range(6):
    num_1_valid[i] = [0] * 6
    for j in range(6):
        num_1_valid[i][j] = [0] * 6

for u in range(0, 6):
    for o in range(0, u + 1):
        for y in range(0, 6 - u):
            f = open('class'+str(u)+str(o)+str(y)+'.txt', 'r')
            classes[u][o][y] = json.load(f)
            f.close()
            f = open('vr'+str(u)+str(o)+str(y)+'.txt', 'r')
            valid_reprs[u][o][y] = json.load(f)
            # consider dropping the last element of valid_reprs[u][o][y]
            f.close()
            num_1_valid[u][o][y] = valid_reprs[u][o][y][-1]





# test validity of a tuple (# slot, # orange, grid, # gray, (g_array, o_array, g_decomps, o_decomps))
# grid is encoded as its grid repr index so that
# valid_reprs[u][o][grid] = the actual grid in binary
# if not valid, return None
# if valid, return new state (u, o, grid, gray)

# the new_row precomputation has certain values of -1, -2
# a value of -1 means don't add the new row, and that item becomes gray
# a value of -2 means don't add the new row, and that item becomes red
# a nonnegative value means add the new row, and that item becomes orange

def test_validity(u, o, y, grid, g, guess_outcome):
    assert g >= len(guess_outcome[3]) - o - y

    if u == 0: return None #this line might be incorrect

    g_array, o_array, g_decomps, o_decomps = guess_outcome
    # if o = 0, the grid doesn't matter
    grid_bin = valid_reprs[u][o][y][grid]
    # compute grid_bin into a length o array to [0, 2^u)
    rows = []
    for i in range(o + y):
        rows.append(grid_bin % pow(2, u))
        grid_bin = grid_bin // pow(2 , u)
    # use orange_item_full_reject to test first
    for i in range(o):
        if not orange_item_full_reject[u][rows[i]][o_decomps[i]]:
            return None
    # next use yellow_item_full_reject
    try:
        for i in range(y):
            if not yellow_item_full_reject[u][rows[o + i]][o_decomps[o + i]] :
                return None
    except IndexError:
        print (u, o, y, grid, g, guess_outcome), u, o+i, rows, o_decomps, len(rows), len(o_decomps)

    
    # compute new rows
    # our convention was that if new_row data from precomputation
    # was -1, that means don't add a new row
    # for example: old row = (0,1,1,1,1)
    # outcome = (0,3,0,0,0)
    # we have one correct thing, and don't add a new row
    new_rows = []
    new_yellow_rows = []
    # is_orange = [False] * len(o_decomps)
    # is_red    = [False] * len(o_decomps)
    is_gray   = [False] * len(o_decomps)
    # is_yellow = [False] * len(o_decomps)
    
    for i in range(o):
        new_row = orange_item_new_row[u][rows[i]][o_decomps[i]]
        # if new_row == -1:
        #     is_gray[i] = True
        #     continue
        if new_row == -2:
            # is_red[i] = True
            continue
        if new_row >= pow(2, u):
            # is_yellow[i] = True
            new_yellow_rows.append(new_row - pow(2, u))
            continue
        new_rows.append(new_row)
        # is_orange[i] = True
        
    for i in range(y):
        new_row = yellow_item_new_row[u][rows[o + i]][o_decomps[o + i]]
        # if new_row == -1:
        #     is_gray[o + i] = True
        #     continue
        if new_row == -2:
            # is_red[o + i] = True
            continue
        if new_row >= pow(2, u):
            # is_yellow[o + i] = True
            new_yellow_rows.append(new_row - pow(2, u))
            continue
        new_rows.append(new_row)
        # is_orange[o + i] = True
        
    for i in range(len(o_decomps) - o - y):
        new_row = gray_item_new_row[u][o_decomps[i + o + y]]
        if new_row == -1:
            is_gray[i + o + y] = True
            continue
        if new_row == -2:
            # is_red[i + o + y] = True
            continue
        # gray row can't become yellow
        new_rows.append(new_row)
        # is_orange[i + o] = True
    new_o = len(new_rows)
    for r in new_yellow_rows:
        new_rows.append(r)
    new_y = len(new_yellow_rows)
    # we now have a new array of rows
    # we need to take a certain minor of it.
    # I think we have already eliminated enough rows, but not sure
    # compute new number of rows, or new_u
    # compute new number of orange items, or new_o
    # compute new grid, or new_grid_bin -> new_grid (ID)
    # compute new number of gray items, or new_g
    eliminate_column = [False] * u
    # recall that o_array is an integer in base 3 encoding
    oa = o_array
    new_u = 0
    new_g = sum(is_gray) + g - (len(o_decomps) - o - y)
    
    for i in range(u):
        if oa % 3 == 2:
            eliminate_column[i] = True
        else:
            new_u += 1
        oa = oa // 3
    
    new_grid_bin = [0] * (new_o + new_y)

    new_rows_copy = copy.copy(new_rows)
    place_value = 1
    # columns_empty = [True] * new_u
    new_column_index = 0
    for i in range(u):
        if eliminate_column[i]:
            for j in range(len(new_rows_copy)):
                new_rows_copy[j] = new_rows_copy[j] // 2
            continue
        
        for j in range(len(new_rows_copy)):
            new_grid_bin[j] += (new_rows_copy[j] % 2) * place_value
            # if new_rows_copy[j] % 2 == 1:
                # columns_empty[new_column_index] = False
            new_rows_copy[j] = new_rows_copy[j] // 2
        place_value *= 2
        new_column_index += 1
    new_grid_integer = 0
    for i in range(new_o + new_y):
        new_grid_integer += new_grid_bin[i] * pow(2, new_u * i)
    # print ((u, o, grid, g, guess_outcome), new_u, new_o, new_grid_integer)
    # very hacky bandaid
    # if new_u < new_o: return None


    # print ((u, o, y, grid, g, guess_outcome), new_u, new_o, new_y, new_grid_integer)

    
    new_grid_id = classes[new_u][new_o][new_y][new_grid_integer]
    if new_grid_id < 0: return None
    # need another test for validity
    # if new_g == 0, need to check that
    # all u columns if new_grid_integer are nonempty
    if new_g == 0:
        if new_grid_id < num_1_valid[new_u][new_o][new_y]:
            return None

    # after all of these tests, I think we can say that the new state has >= 1 assignment
    assert new_u >= new_o
    assert new_u + new_y <= max_s
    return (new_u, new_o, new_y, new_grid_id, new_g)
        



# evaluate the number of possible sets one can distinguish from the given state
# recursive and memoized
# memoized_evals[t][u][o][g] is a dictionary from grid classes to evals
memoized_evals = []
# umm this doesn't work as intended
def reset_memo(memoized_evals):
    memoized_evals = [0] * (max_t + 1)
    for t in range(2, max_t + 1):
        memoized_evals[t] = [0] * (max_s + 1)
        for u in range(1, max_s + 1):
            memoized_evals[t][u] = [0] * (max_s + 1)
            for o in range(0, max_s + 1):
                memoized_evals[t][u][o] = [0] * (max_s)
                for y in range(0, max_s):
                    memoized_evals[t][u][o][y] = [0] * (max_i + 1)
                    for g in range(0, max_i + 1):
                        memoized_evals[t][u][o][y][g] = {}
    

def evaluate(u, o, y, grid, g, turns_left):
    if turns_left == 0: return 0
    if turns_left == 1: return 1
    if u == 0: return 1
    t = turns_left
    data = memoized_evals[t][u][o][y][g].get(grid)
    if data:
        # data has the form (eval, optimum move)
        return data[0]
    #go_uo are the possible (guess, outcome) values
    go_uoy = go_data[u][o][y]
    dict_guess_total = {}
    # we only use (guess, outcome pairs) which reference a number of
    # distinct grays which is <= g
    for num_distinct_grays_used in range(min(g + 1, len(go_uoy))):
        for guess_outcome in go_uoy[num_distinct_grays_used]:
            guess = tuple(guess_outcome[0])
            new_state = test_validity(u, o, y, grid, g, guess_outcome)
            if new_state is None:
                continue
            new_state_eval = evaluate(new_state[0], new_state[1], new_state[2], new_state[3], new_state[4], turns_left - 1)
            # print "eval_update: (new_state, new_state_eval, valid_reprs[new_state[0]][new_state[1]][new_state[2]][new_state[3]])"
            guess_entry = dict_guess_total.get(guess)
            if guess_entry:
                dict_guess_total[guess] += new_state_eval
            else:
                dict_guess_total[guess] = new_state_eval
    max_guess = 0
    max_total = 0
    for guess in dict_guess_total.keys():
        if dict_guess_total[guess] > max_total:
            max_guess = guess
            max_total = dict_guess_total[guess]
    memoized_evals[t][u][o][y][g][grid] = (max_total, max_guess)
    return max_total


# evaluate a state but only using a single guess
# in contrast, evaluate() takes the max total over all possible guesses.
# input guess is a list/duple with the same encoding as guess_outcome[0]
def evaluate_guess(u, o, y, grid, g, turns_left, guess):
    guess = tuple(guess)
    if turns_left == 0: return 0
    if turns_left == 1: return 1
    if u == 0: return 1
    t = turns_left
    #go_uo are the possible (guess, outcome) values
    go_uoy = go_data[u][o][y]
    total = 0
    # we only use (guess, outcome pairs) which reference a number of
    # distinct grays which is <= g
    for num_distinct_grays_used in range(min(g + 1, len(go_uoy))):
        for guess_outcome in go_uoy[num_distinct_grays_used]:
            if tuple(guess_outcome[0]) != guess: continue
            
            new_state = test_validity(u, o, y, grid, g, guess_outcome)
            if new_state is None:
                continue
            # print new_state
            new_state_eval = evaluate(new_state[0], new_state[1], new_state[2], new_state[3], new_state[4], turns_left - 1)
            # print "eval_update: (new_state, new_state_eval, valid_reprs[new_state[0]][new_state[1]][new_state[2]][new_state[3]])"
            total += new_state_eval
    return total
    



f = open('oifr.txt', 'w')
json.dump(orange_item_full_reject, f)
f.close()
f = open('oinr.text', 'w')
json.dump(orange_item_new_row, f)
f.close()
f = open('yifr.txt', 'w')
json.dump(yellow_item_full_reject, f)
f.close()
f = open('yinr.txt', 'w')
json.dump(yellow_item_new_row, f)
f.close()
f = open('ginr.txt', 'w')
json.dump(gray_item_new_row, f)
f.close()
    
    
        
    

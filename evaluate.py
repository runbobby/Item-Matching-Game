import numpy as np
%cd
%cd Documents\item_matching\data
import json
import copy
# the evaluation steps only
# instructions: compile all functions, then run the stuff.
# the data and functions should be global. 

# globals
max_s = 5
max_i = 10
max_t = 6
# load data and define functions
data = load_data()
funs = define_functions()
go_data, classes, valid_reprs, num_1_valid, orange_item_full_reject, orange_item_new_row, yellow_item_full_reject, yellow_item_new_row, gray_item_new_row = data
test_validity, evaluate = funs
memoized_evals = new_memo()


evaluate(5,0,0,0,5,3)



def load_data():
    go_data = [0]*(max_s+1)
    for i in range(max_s + 1):
        go_data[i] = [0]*(max_s+1)
        for j in range(max_s + 1):
            go_data[i][j] = [0]*(max_s + 1)
    for num_slots in range(1, max_s+1):
        for num_orange in range(num_slots + 1):
            for num_yellow in range(max_s + 1 - num_slots):
                f = open('go_data'+str(num_slots)+str(num_orange)+str(num_yellow)+'.txt', 'r')
                go_data[num_slots][num_orange][num_yellow] = json.load(f)
                f.close()
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

    f = open('oifr.txt', 'r')
    oifr = json.load(f)
    f.close()
    f = open('oinr.txt', 'r')
    oinr = json.load(f)
    f.close()
    f = open('yifr.txt', 'r')
    yifr = json.load(f)
    f.close()
    f = open('yinr.txt', 'r')
    yinr = json.load(f)
    f.close()
    f = open('ginr.txt', 'r')
    ginr = json.load(f)
    f.close()

    return go_data, classes, valid_reprs, num_1_valid, oifr, oinr, yifr, yinr, ginr

    
def define_functions():
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

    return test_validity, evaluate

def new_memo():
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
    return memoized_evals
    
    



import numpy as np
%cd
%cd Documents\item_matching\data
import json
# warning!!!!!!!!!!!!!!!!!
# this code uses integer division twice
# may need to rewrite code depending on environment

# parameters
# u = # unsolved slots, o = # orange items; o <= u
# y = # yellow
# also y + u <= max_s, in this case, 5

# possible grids. we want to find isomorphism classes of grids
# the integer i corresponds to a grid as follows:
# i = i_{uo-1} i_{uo-2} ... i_1 i_0 in binary
# digit 0 means "known incorrect." digit 1 means "no info"

# example
#        slot0, slot1, slot2, slot3
# item1  i_0    i_1    i_2    i_3
# item2  i_4    i_5    i_6    i_7
# item3  i_8    i_9    i_10   i_11

# NEW!!!!!!!!!!!!!!!!!!!!!!!!!!
# now, a grid has the form(u,


for u in range(0, 6):
    for o in range(0, u + 1):
        for y in range(0, 6 - u):
            grid_classes(u, o, y)
            print (u, o, y)

        


def grid_classes(u, o, y):
    N = pow(2, u * (o + y))
    oy = o + y
    nss = [0] * max(0, u-1)
    nsi = [0] * max(0, o-1)
    nsy = [0] * max(0, y-1)
    for a in range(len(nss)):
        nss[a] = [-1] * N
    for a in range(len(nsi)):
        nsi[a] = [-1] * N
    for a in range(len(nsy)):
        nsy[a] = [-1] * N

    # compute transposes as in old, but replace o in old with o+y
    transpose = [0]*N
    transpose2 = [0]*N
    adjustment = [0] * (u * (o + y))
    adj = 0
    k = 0
    for j in range(o + y):
        for i in range(u):
            adjustment[k] = adj + pow(2, i * (o + y) + j)
            adj -= pow(2, i * (o + y) + j)
            k += 1

    j = 0
    for i in range(N):
        transpose[i] = j
        transpose2[j] = i

        # j += 1
        # a = number of powers of 2 dividing i+1
        a = 0
        b = i+1
        while b%2 == 0:
            a += 1
            b /= 2
        if a == u * (o + y): break

        # if a = 0, we do j+= 1. otherwise, we need to add something tricky
        j += adjustment[a]

    # populate nss
    p2o = pow(2, o + y)
    for a in range(u-1):
        # print nss[a]
        p2ao = pow(2, a*(o + y))
        place_value = pow(2, (1+a)*(o + y))
        grid = 0
        for i in range(p2o):
            # print(a, i)
            for j in range(pow(2, (o + y)*(u-1))):
                # grid += 1
                grid = i + p2o * j
                # print (a, i, j, transpose2[grid], nss[a][transpose2[grid]])
                if nss[a][transpose2[grid]] != -1: continue
                r = (j // p2ao) % p2o
                neighbor = grid + (r - i) + (i - r)*place_value
                # print a, transpose2[grid], transpose2[neighbor]
                nss[a][transpose2[grid]] = transpose2[neighbor]
                nss[a][transpose2[neighbor]] = transpose2[grid]


    # populate nsi
    p2u = pow(2, u)
    for a in range(o-1):
        # populate nsi[a]
        place_value = pow(2, (1+a)*u)
        p2au = pow(2, a*u)
        grid = 0
        for i in range(p2u):
            for j in range(pow(2, u*(o + y - 1))):
                # grid += 1
                grid = i + p2u * j
                if nsi[a][grid] != -1: continue
                # r = row to be switched; it's ablock of j in binary
                r = (j // p2au) % p2u
                # neighbor is formed by switching two digits in base p2u
                # namely the ones digit and the (p2u)^(a+1)'s place
                neighbor = grid + (r - i) + (i - r)*place_value
                nsi[a][grid] = neighbor
                nsi[a][neighbor] = grid

    # populate nsy
    C = pow(2, u * (1 + o))
    p2ou = pow(2, u * o)
    for a in range(y - 1):
        place_value = pow(2, (1 + o + a)*u)
        D = pow(2, u * (a + o))
        p2au = pow(2, a * u)
        grid = 0
        for i in range(C):
            ii = i // p2ou
            for j in range(pow(2, u * (y - 1))):
                grid = i + C * j
                if nsy[a][grid] != -1: continue
                r = (j // p2au) % p2u
                neighbor = grid + (r - ii) * p2ou + (ii - r) * place_value
                nsy[a][grid] = neighbor
                nsy[a][neighbor] = grid

    # dfs traversal
    visited = [False] * N
    vv = 0
    Class = [-1] * N
    while vv < N:
        while vv < N and visited[vv]:
            vv += 1
        if vv == N: break
        vertex = vv
        visited[vertex] = True
        # vertex is the lowest representative in its isomorphism class
        Class[vertex] = vertex
        v_not_visited = [True] * N
        v_not_visited[vertex] = False
        in_v_component = [vertex]
        ivc_index = 0
        while ivc_index < len(in_v_component):
            x = in_v_component[ivc_index]
            for a in range(o-1):
                w = nsi[a][x]
                if v_not_visited[w]:
                    in_v_component.append(w)
                    v_not_visited[w] = False
                    visited[w] = True
                    Class[w] = vertex
            for a in range(u-1):
                w = nss[a][x]
                if v_not_visited[w]:
                    in_v_component.append(w)
                    v_not_visited[w] = False
                    visited[w] = True
                    Class[w] = vertex
            for a in range(y-1):
                w = nsy[a][x]
                if v_not_visited[w]:
                    in_v_component.append(w)
                    v_not_visited[w] = False
                    visited[w] = True
                    Class[w] = vertex
            ivc_index += 1




    reprs = []
    for i in range(N):
        if Class[i] == i:
            reprs.append(i)

    ###############################################################################
    # next: for each representative, determine if there exist valid assignments or not
    # a grid is valid iff there is a valid injective map from items -> slots; digits are 1
    # method: hall's lemma?
    # return 0 if invalid
    # return 1 if valid, but needs gray items
    # return 2 if valid without gray items
    def is_valid(grid):
        # g_bin = grid in binary as an array
        # g_bin[item][slot]
        # gg = only the u x o grid, or the orange items 
        gg = grid % pow(2, o * u)
        g_bin = [0]*o
        for a in range(o):
            g_bin[a] = [0]*u
        for item in range(o):
            for slot in range(u):
                g_bin[item][slot] = gg % 2
                gg = gg // 2

        violating_subset = False
        for i in range(pow(2, o)):
            # a = num ones in i in binary
            # i_bin = i in binary; i[d] = 2^d place
            i_bin = [0]*o
            b_index = 0
            a = 0
            ii = i
            while ii > 0:
                if ii % 2 == 1:
                    a += 1
                    i_bin[b_index] = 1
                ii = ii // 2
                b_index += 1
            # count of # slots available for the subset i
            # recall that by Hall's theorem, this should be >= a
            c = 0
            for slot in range(u):
                for item in range(o):
                    if i_bin[item] == 1 and g_bin[item][slot] == 1:
                        c+= 1
                        break
            if c < a:
                violating_subset = True
                break
        if violating_subset:
            return 0
        # now we need to deal with yellow items. by now, we assume that the orange grid is
        # valid wrt. Hall's lemma
        # lemma: an orange/yellow grid is exactly 1-valid if there exists a column (out of u)
        # such that all orange/yellow items are forbidden from it
        # if there exists no such column, then the orange/yellow grid is 2-valid
        gg = grid
        rows = []
        for i in range(o + y):
            rows.append(gg % pow(2, u))
            gg = gg // pow(2, u)
        
        empty_columns = [True] * u
        for i in range(u):
            for j in range(o + y):
                if rows[j] % 2 == 1:
                    empty_columns[i] = False
                rows[j] = rows[j] // 2
        if sum(empty_columns) > 0:
            return 1
        else:
            return 2

    valid_reprs = []
    number_1_valid = 0
    for r in reprs:
        if is_valid(r)== 1:
            valid_reprs.append(r)
            number_1_valid += 1
    for r in reprs:
        if is_valid(r) == 2:
            valid_reprs.append(r)
    valid_reprs.append(number_1_valid)
    # now, the last term of valid_reprs is the number of one-valid reprs.

    dict_vr_to_i = {}
    for i in range(len(reprs)):
        dict_vr_to_i[reprs[i]] = -1
    for i in range(len(valid_reprs) - 1):     # don't incluce the last term
        dict_vr_to_i[valid_reprs[i]] = i
    # rewrite Class so that it points to the representative's index, not the representative
    # (smaller numbers)
    for i in range(len(Class)):
        Class[i] = dict_vr_to_i[Class[i]]

    f = open('class'+str(u)+str(o)+str(y)+'.txt', 'w')
    json.dump(Class, f)
    f.close()
    f = open('vr'+str(u)+str(o)+str(y)+'.txt', 'w')
    json.dump(valid_reprs, f)
    f.close()




# compute isomorphism classes of grids with u unsolved slots and o orange items
# compute which classes are valid
# store one representative of each valid class in
# Documents\item_matching\vr+str(u)+str(o)+.txt
# store map from all grids -> valid representative (or -1 if invalid)
# in Documents\item_matching\class+str(u)+str(o)+.txt

# estimated time. grid_classes(5, 5): 30 min?
# others are < 2 min

def grid_classes_old(u, o):
    N = pow(2, u*o)

    # need to make array objects different, so nss = [[0]*N]*(u-1) doesn't work
    nss = [0]*(u-1)
    nsi = [0]*(o-1)
    for a in range(u-1):
        nss[a] = [-1]*N
    for a in range(o-1):
        nsi[a] = [-1] * N
    transpose = [0]*N
    transpose2 = [0]*N
    adjustment = [0] * (u * o)
    adj = 0
    k = 0
    for j in range(o):
        for i in range(u):
            adjustment[k] = adj + pow(2, i * o + j)
            adj -= pow(2, i * o + j)
            k += 1

    j = 0
    for i in range(N):
        transpose[i] = j
        transpose2[j] = i

        # j += 1
        # a = number of powers of 2 dividing i+1
        a = 0
        b = i+1
        while b%2 == 0:
            a += 1
            b /= 2
        if a == u*o: break

        # if a = 0, we do j+= 1. otherwise, we need to add something tricky
        j += adjustment[a]
        
    # populate nsi
    p2u = pow(2, u)
    for a in range(o-1):
        # populate nsi[a]
        place_value = pow(2, (1+a)*u)
        p2au = pow(2, a*u)
        grid = 0
        for i in range(p2u):
            for j in range(pow(2, u*(o-1))):
                # grid += 1
                grid = i + p2u * j
                if nsi[a][grid] != -1: continue
                # r = row to be switched; it's ablock of j in binary
                r = (j // p2au) % p2u
                # neighbor is formed by switching two digits in base p2u
                # namely the ones digit and the (p2u)^(a+1)'s place
                neighbor = grid + (r - i) + (i - r)*place_value
                nsi[a][grid] = neighbor
                nsi[a][neighbor] = grid


    # populate nss
    p2o = pow(2, o)
    for a in range(u-1):
        # print nss[a]
        p2ao = pow(2, a*o)
        place_value = pow(2, (1+a)*o)
        grid = 0
        for i in range(p2o):
            # print(a, i)
            for j in range(pow(2, o*(u-1))):
                # grid += 1
                grid = i + p2o * j
                # print (a, i, j, transpose2[grid], nss[a][transpose2[grid]])
                if nss[a][transpose2[grid]] != -1: continue
                r = (j // p2ao) % p2o
                neighbor = grid + (r - i) + (i - r)*place_value
                # print a, transpose2[grid], transpose2[neighbor]
                nss[a][transpose2[grid]] = transpose2[neighbor]
                nss[a][transpose2[neighbor]] = transpose2[grid]

                
    # dfs traversal
    visited = [False] * N
    vv = 0
    Class = [-1] * N
    while vv < N:
        while vv < N and visited[vv]:
            vv += 1
        if vv == N: break
        vertex = vv
        visited[vertex] = True
        # vertex is the lowest representative in its isomorphism class
        Class[vertex] = vertex
        v_not_visited = [True] * N
        v_not_visited[vertex] = False
        in_v_component = [vertex]
        ivc_index = 0
        while ivc_index < len(in_v_component):
            x = in_v_component[ivc_index]
            for a in range(o-1):
                w = nsi[a][x]
                if v_not_visited[w]:
                    in_v_component.append(w)
                    v_not_visited[w] = False
                    visited[w] = True
                    Class[w] = vertex
            for a in range(u-1):
                w = nss[a][x]
                if v_not_visited[w]:
                    in_v_component.append(w)
                    v_not_visited[w] = False
                    visited[w] = True
                    Class[w] = vertex
            ivc_index += 1

        
    # determine unique representatives
    # uses fact that representatives are exactly the i for which Class[i] == i
    reprs = []
    for i in range(N):
        if Class[i] == i:
            reprs.append(i)


    ###############################################################################
    # next: for each representative, determine if there exist valid assignments or not
    # a grid is valid iff there is a valid injective map from items -> slots; digits are 1
    # method: hall's lemma?
    def is_valid(grid):
        # g_bin = grid in binary as an array
        # g_bin[item][slot]
        gg = grid
        g_bin = [0]*o
        for a in range(o):
            g_bin[a] = [0]*u
        for item in range(o):
            for slot in range(u):
                g_bin[item][slot] = gg % 2
                gg = gg // 2

        violating_subset = False
        for i in range(pow(2, o)):
            # a = num ones in i in binary
            # i_bin = i in binary; i[d] = 2^d place
            i_bin = [0]*o
            b_index = 0
            a = 0
            ii = i
            while ii > 0:
                if ii % 2 == 1:
                    a += 1
                    i_bin[b_index] = 1
                ii = ii // 2
                b_index += 1
            # count of # slots available for the subset i
            # recall that by Hall's theorem, this should be >= a
            c = 0
            for slot in range(u):
                for item in range(o):
                    if i_bin[item] == 1 and g_bin[item][slot] == 1:
                        c+= 1
                        break
            if c < a:
                violating_subset = True
                break
        return not(violating_subset)


    valid_reprs = []
    for r in reprs:
        if is_valid(r):
            valid_reprs.append(r)

    dict_vr_to_i = {}
    for i in range(len(reprs)):
        dict_vr_to_i[reprs[i]] = -1
    for i in range(len(valid_reprs)):
        dict_vr_to_i[valid_reprs[i]] = i

    # rewrite Class so that it points to the representative's index, not the representative
    # (smaller numbers)
    for i in range(len(Class)):
        Class[i] = dict_vr_to_i[Class[i]]



    f = open('class'+str(u)+str(o)+'.txt', 'w')
    json.dump(Class, f)
    
    #for i in range(len(Class)):
    #    f.write(str(Class[i]) + " ")
    f.close()

    f = open('vr'+str(u)+str(o)+'.txt', 'w')
    json.dump(valid_reprs, f)
    
    #for i in range(len(valid_reprs)):
    #    f.write(str(valid_reprs[i]) + " ")
    f.close()



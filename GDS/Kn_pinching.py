## Date 5.12
## Author: Thomas B

# Objective:
# compute a upper bound for the triangle number for Kn using the pinching operation.


#two following imports are likely to install on your computer
import igraph
import imageio  

import copy
import math

N = [i for i in range(5,27)]
duration = 0.1 #for gifs
old_color = 'black'
new_color = 'red'
msg = 'execution is to be made from ORCO21 folder. Try changing cmd location or file_loc parameter if you have any problem.\n'
method = 'Rule used for pinching is the following: say we have two X_i, X_j \in S such that exactly one edge of them is of multiplicity 1, and one vertex in common.\nThen denote by a_i,b_i,c_i their vertices, a_i being the one with two edges of multiplicity != 1, b_i = b_j = b.\nThen it means that these two groups are covering only bc_i and bc_j. So, remove them and add X = b,c_i, c_j.\n'
bad_K6_Sol =   [[1, 2, 6],  #R
                [1, 3, 5],  #RP
                [1, 4, 6],  #VP
                [2, 3, 4],  #B
                [2, 4, 5],  #BP
                [2, 5, 6],  #V
                [2, 3, 6]]  #N
file_loc ='GDS/images/'
file_loc_gif = 'GDS/gif/'

def main():
    print(msg)
    print('*'*60)
    print(method)
    print('\n\n')
    for n in N:
        name = 'K_'+str(n)
        print('*'*15 + ' K_' + str(n) + ' ' + '*'*15)
        S = initial_solution(n)
        lowerbound(n)

        print('\nGreedy solution gives '+ str(len(S)))
        modif = True
        while modif:
            S, modif = pinching(S)
            print('modification: ' + str(modif))
            if modif:
                print('size reduced to:' + str(len(S)))
            else:
                print("can't do further pinching operation.\n")
        
        print('*'*15 )
        print('Now saving the solution.')
        filename_list =custom_print(S, n, name)
        print("Making a gif...")

        images = []
        for fname in filename_list:
            images.append(imageio.imread(fname))
        imageio.mimsave(file_loc_gif + str(name)+'.gif', images, duration = duration)



### Functions
# A solution S is a list of list of three vertices. 


def custom_print(S,n, graph_name):
    """
    does a printing group/group of the solution S.    
    does a printing group/group of the solution S.    
    """
    g = igraph.Graph(n)
    layout = g.layout('circle')
    color_dict = {'old' : old_color, 'new' : new_color }
    thick_dict = {'old': 1, 'new' : 3}
    filename_list = []
    
    for iS in range(len(S)):

        L = S[iS]
        v1, v2, v3 = L[0], L[1], L[2]

        for e in g.es:  #all existing edges are set to "old"
            e["type"] = 'old'
        
        if not(g.neighbors(v1).count(v2) != 0):  # litterally: if v2 do not appears among the neighbors of v1
            g.add_edge(v1, v2)
            g.es[-1]["type"] = 'new'
        
        if not(g.neighbors(v1).count(v3) != 0):  # litterally: if v2 do not appears among the neighbors of v1
            g.add_edge(v1, v3)
            g.es[-1]["type"] = 'new'

        if not(g.neighbors(v2).count(v3) != 0):  # litterally: if v2 do not appears among the neighbors of v1
            g.add_edge(v2, v3)
            g.es[-1]["type"] = 'new'
        
        filename = file_loc + graph_name + '_'+ str(iS) + '.png'
        filename_list.append(filename)
        print('saving:' + str(iS) + '/' + str(len(S)))
        igraph.plot(g, filename,layout = layout,vertex_color= ["black" for v in g.vs],edge_width = [thick_dict[etype] for etype in g.es["type"]], edge_color = [color_dict[e_type] for e_type in g.es["type"]])
    return filename_list

def lowerbound(n):
    """
    print lowerboudn informations (|E|/3) for n.
    """
    E = n*(n-1)/2
    print('lowerbound at ' +str(math.ceil(E/3)))

def initial_solution(n):
    """
    Generates an initial solution for Kn.
    It goes this way: start by an edge ij that is not covered by S yet. put i,j inside. Then find z such that it maximizes the covering power of i,j,z.
    """
    M = [[0 for i in range(n)] for j in range(n)]
    S = []

    for i in range(n):
        M[i][i] = 1

    validity, i, j = check_M_validity(M)

    while validity == False:
        group = [i, j]
        z = max_power(group, M)
        group.append(z)

        for e1 in group:
            for e2 in group:
                M[e1][e2] = 1
        S.append(group)
        validity, i, j = check_M_validity(M)
    return S

def max_power(group, M):
    '''
    returns a z of max stoppping power for group.
    '''
    best_z = -1
    best_pow = 0
    for z in range(len(M)):

        #print(group, z, z != group[0] and z != group[1], stopping_power(group, z, M), best_pow, best_z)  
        if z != group[0] and z != group[1]:
            pow = stopping_power(group, z, M)
            if pow == 3:

                return z
            elif pow >= best_pow:       # >= bc in the eventuality all z have the same value (1) we can't allow the alg to pick -1 as best z.
                best_pow = pow
                best_z = z
    #print(best_z, best_pow)
    return best_z

def stopping_power(group, z, M):
    '''
    computes how much the addition of group u z would be good for M. (it is at least 1.)
    '''
    i,j = group[0], group[1]
    return (M[i][j] == 0) + (M[i][z] == 0) + (M[j][z]==0)
    
def check_M_validity(M):
    """
    returns True iff M is composed of 1s.
    """
    n=len(M)
    for i in range(n):
        for j in range(n):
            if M[i][j] == 0:
                return False, i, j
    return True, -1, -1

def pinching(S):
    """
    does the pinching operation. 
    Returns an updated solution S' of f of smaller size, and a boolen (False iff the pinching was impossible.)
    """
    # Scheme:
    # First, creates a list M1 of all groups that avec exactly one edge of multiplicity 1. 
    # then, run this list M1 with a double loop and detect two element A, B that are different but return True to intersectionX(A,B)
    # copies S into Sp, then delete A and B from S. 

    M1 = []
    for L in S:
        if multiplicity1(S,L) <= 1:
            M1.append(L)

    A, B = [], []

    for iA in range(len(M1)):
        for iB in range (iA):
            inter, c = intersectionX(S, M1[iA], M1[iB])
            if inter:
                A, B = M1[iA], M1[iB]
                break

    #stopping condition: could not find a proper candidate.
    if A == []:
        return S, False

    #otherwise we need to retain the 'good edges' similarly as for intersectionX function.
    Acopy = A.copy()
    Bcopy = B.copy()
    Acopy.remove(c)
    Bcopy.remove(c)

    v1A , v2A = Acopy[0], Acopy[1] #remaining vertices of A, B
    v1B , v2B = Bcopy[0], Bcopy[1]

    if multiplicity(S, c, v1A)==1:
        vA = v1A
    else:
        vA = v2A
    
    if multiplicity(S, c, v1B)==1:
        vB = v1B
    else:
        vB = v2B

    # Packing up
    Sp = S.copy()
    Sp.remove(A)
    Sp.remove(B)
    Sp.append([c, vA, vB])
    return Sp, True


def intersectionX(S, A, B):
    """
    returns True iff A, B have a vertex in common, and the vertex they have in common (say c) have to have at least one edge (in A and in B) that contains c which is of degree 1. 
    Also return c, that 'good' vertex.
    """
    flag = False
    for a in A:
        for b in B:
            if a == b:
                c = a
                Acopy, Bcopy = A.copy(), B.copy()
                Acopy.remove(c)
                Bcopy.remove(c)

                v1A , v2A = Acopy[0], Acopy[1] #remaining vertices of A, B
                v1B , v2B = Bcopy[0], Bcopy[1]

                AGOOD = ( multiplicity(S, c, v1A)==1 or multiplicity(S, c, v2A)==1 ) 
                BGOOD = ( multiplicity(S, c, v1B)==1 or multiplicity(S, c, v2B)==1 ) 
                if AGOOD and BGOOD:
                    return True, c
    return flag, -1



def multiplicity1(S, L):
    """
    returns the number of edges of multiplicity exactly 1 in L.
    """
    answer = 0
    a,b,c = L[0], L[1], L[2]
    answer += (multiplicity(S, a,b) ==1)
    answer += (multiplicity(S, a,c) ==1)
    answer += (multiplicity(S, b,c) ==1)
    return answer

def multiplicity(S, u,v):
    """
    returns an integer corresponding to the multiplicity of uv in S.
    u,v has to be different.
    """
    m_uv = 0
    for L in S:
        m_uv += isIn(u,v,L)
    return m_uv

def isIn(u,v,L):
    """
    returns a boolean wether u,v are in L or not.
    Each element of L is supposed unique.
    """
    count=0
    for elt in L:
        count += ( (elt == u) or (elt ==v) )
    return count >= 2






### MAIN

main()

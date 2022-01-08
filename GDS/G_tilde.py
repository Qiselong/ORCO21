## Date 10.12
## Author Thomas B

# Objective: Compute the adjacency matrix of G tilde from the adjacency matrix of G. 
# G tilde is a bipartite graph with parties VE, VT. VE are edges of G, VT are triangles of G. 

#imports
import igraph           # if the import of igraph does not work: put this line in comment and turn igraph_use to False.
import math
import random
import imageio

from igraph import layout

# Parameters:
n = 18       # size of G
d = 0.5  # density of G
nTry = 1000             # max number of try at generating a graph without 
igraph_use = True
word_warp = False       # if the G_tilde has too much lines turn this to False
duration = 0.5

# file section
data_loc = 'GDS/txt/G_tilde.txt'
sol_loc = 'GDS/txt/G_tilde_solution.txt'
G_tilde_plot_loc = 'GDS/G_tilde/G_tilde.png'
G_tilde_sol_loc = 'GDS/G_tilde/G_tilde_solution.png'
G_loc = 'GDS/G_tilde/G.png'


# main definition

def main():

    Edges_list = generation(n,d)
    G = Adjacency(Edges_list, n)
    try_index = 0

    while solitary_edge(Edges_list, G) == True and try_index < nTry:
        Edges_list = generation(n,d)
        G = Adjacency(Edges_list, n)
        try_index +=1

    if try_index == nTry:
        print("number of tries allowed exceeded; try raising the density parameter.")
        return None

    layout1 = print_G(Edges_list, G_loc, n)


    nE = len(Edges_list)
    T_set = triangle_count(G)
    nT = len(T_set)

    print('Parameters of the graph:\n|V|      ' + str(n) +'\n|E|      '+str(nE) +'\nnT       '+str(nT) +'\nVtilde   '+str(nT+nE) + '\nEtilde   ' + str(3*(nT+nE)) )

    G_t = G_tilde(T_set, Edges_list)

    save_for_cplex(G_t, data_loc)

    layout_g_tilde, g_tilde = plot_Gtilde(G_t, T_set, Edges_list,G_tilde_plot_loc )

    input("Save result from MILP into G_tilde_solution.txt")

    Sol_Gtilde = read_sol(sol_loc)

    gtilde_print_sol(Sol_Gtilde, g_tilde, layout_g_tilde, G_tilde_sol_loc, len(Edges_list), G_t)

    S = group_extraction(T_set, Sol_Gtilde)
    print(S)

    animation_optimal_solution(S, layout1)




   




    


# Functions
def animation_optimal_solution(S, layout1):
    """
    uses the layout1 and g1 (for vnames) to create a gif out of the solution S.
    """

    g = igraph.Graph(n)
    name = 'GDS/images/solution_'
    col_dict = {'old' : 'black', 'new' : 'red'}
    thick_dict = {'old' : 2, 'new' : 3}

    for i in range(len(S)):
        name_i = name + str(i) + '.png'
        u,v,w = S[i][0], S[i][1], S[i][2]

        if g.neighbors(u).count(v) == 0:
            g.add_edge(u,v)
            g.es[-1]['type'] = 'new'
        if g.neighbors(u).count(w) == 0: 
            g.add_edge(u,w)
            g.es[-1]['type'] = 'new'
        if g.neighbors(v).count(w) == 0:
            g.add_edge(v,w)
            g.es[-1]['type'] = 'new'

        igraph.plot(g, name_i, layout = layout1, edge_color = [col_dict[e['type']] for e in g.es], edge_width = [thick_dict[e['type']] for e in g.es], vertex_color = ['black' for v in g.vs] )

        for e in g.es:
            e['type'] = 'old'

    filename_list = [name + str(i) +'.png' for i in range(len(S)-1)] + [name + str(len(S)-1) +'.png']*10
    images = []
    for fname in filename_list:
        images.append(imageio.imread(fname))
    imageio.mimsave('GDS/gif/aa_final_solution.gif', images, duration = duration)



def group_extraction(T_set, Gt_sol):
    """
    from the triangle set T_set and Gt_sol, returns the list of the groups of an optimal solution.
    """

    S = []
    for i in range(len(Gt_sol)):
        if Gt_sol[i] == 1:
            S.append(T_set[i])
    return S

def generation(n, d):
    """
    generates as a list of edges (tuples) a random graph of size n with density d. 
    """
    nE = min(math.ceil((n*(n-1))*d/2), n*(n-1)/2)
    L = []
    while len(L) < nE:
        i,j = random.randint(0, n-1), random.randint(0, n-1)
        i,j = min(i,j), max(i,j)            # sort useful for next line
        if L.count((i,j)) == 0 and i != j:  # if i,j is not selected yet, and i,j is a valid edge (not a self loop)
            L.append((i,j)) 
    return L

def Adjacency(L, n):
    """
    computes and return the adjacency matrix of G from the list of edges.
    """
    M = [ [0 for i in range(n)] for j in range(n) ]
    for (i,j) in L:
        M[i][j] = 1
        M[j][i] = 1
    return M

def solitary_edge(L, M):
    """
    given the list of edges and the adjacendy matrix of G, figures out if G has a solitary edge; namely an edge that can't be in any triangle.
    """

    for (i,j) in L:
        ij_solitary = True
        for z in range(len(M)):
            if M[z][j] and M[z][i]:
                ij_solitary = False
        if ij_solitary:
            return True
    return False



def triangle_count(M):
    """
    computes the triangle number of a graph given it's adjacency matrix, and a list of tuples corresponding of all the triangles.
    """
    Triangles = []
    n = len(M)
    for i in range(n):
        for j in range(i):
            for z in range(j):
                if M[i][j] and M[j][z] and M[i][z]:
                    Triangles.append((z, j, i))
    return Triangles

def in_tuple(t1, t2):
    """
    decides in tuple t1 is a subtuple of t2.
    """
    a, b = t1[0], t1[1]
    c, d, e = t2[0], t2[1], t2[2]
    return ( a==c and ( b==d or b==e ) ) or ( a==d and b==e ) #every shit is sorted so i can do that

def G_tilde(triangles, edges):
    """
    print into file_loc the data of G_tilde.
    """
    nE = len(edges)
    n_tilde = len(triangles) + nE
    G_tilde = [ [0 for i in range(n_tilde)] for j in range(n_tilde) ]

    for i_edge in range(len(edges)):
        for i_triangle in range(len(triangles)):
            e_i, t_i = edges[i_edge], triangles[i_triangle]
            if in_tuple(e_i, t_i):
                G_tilde[i_edge][i_triangle + nE] = 1
                G_tilde[i_triangle + nE][i_edge] = 1  
    return G_tilde


def save_for_cplex(M, file_loc):
    """
    save the content of M into file_loc.
    """
    f = open(file_loc, 'w')
    strline = '['
    for i_line in range(len(M)):
        line = M[i_line]
        strline += '['
        for i_elt in range(len(line)):
            if i_elt !=0:
                strline += ','
            strline += str(line[i_elt])
        strline += ']'
        if word_warp:
            strline +='\n'
        f.write(strline)
        strline = ''
    f.close()


def plot_Gtilde(M, Triangles, Edges, file_loc):
    """
    uses the igraph library to plot Gtilde (save it)
    """
    nT, nE = len(Triangles), len(Edges)
    g = igraph.Graph(nT + nE)
    layout1 = g.layout('rt', 2) #whatever you put inside layout, objective is to revamp it to have a "good plot"

    # on X : 10 for NT points, 90 for NE Points
    # suppose nT > nE : nT_0 at 10, nT_nT (lol) at 90; one every 10 + epsilon1, epsilon1 = 80/nT 
    #                   for nE: start at 20, end 80; one every 20 + epsilon2, epsilon2 = 60/NE

    if nT == nE:
        epsilon1 = 80/nT
        epsilon2 = 80/nE
        sT, sE = 10, 10
    elif nT > nE:
        epsilon1 = 80/nT
        epsilon2 = 80/nE
        sT, sE = 10, 10
    else:
        epsilon1 = 80/nT
        epsilon2 = 80/nE
        sT, sE = 10, 10

    for i_e in range(nE):
        g.vs[i_e]['type'] = 'edge'
        g.vs[i_e]['name'] = str(Edges[i_e][0]) + ','+str(Edges[i_e][1])
        layout1[i_e] = (10, sE + i_e*epsilon1 )
    
    for i_t in range(nT):
        i = i_t + nE    #'true' index
        g.vs[i]['type'] = 'triangle'
        T = Triangles[i_t]
        g.vs[i]['name'] = str(T[0]) + ',' + str(T[1]) + ',' + str(T[2])
        layout1[i] = (90, sT + i_t*epsilon2 )

    for i in range(len(M)):
        for j in range(i):
            if M[i][j]:
                g.add_edge(i,j)

    igraph.plot(g, file_loc,layout = layout1, vertex_label = [v['name'] for v in g.vs]) 
    return layout1, g


    

            
def read_sol(file_loc):
    """
    read the solution offered by the MILP and returns it as a boolean vector corresponding to triangles composing an optimal solution. 
    """
    ## A solution is of the form [0 1 0 ... 0 0 1]
    ## 0 means a triangle is not in the solution, 1 means it is
    f = open(file_loc)
    entry = f.readline()
    entry = entry[1:len(entry)-1]
    Sol = [int(elt) for elt in entry.split(' ')]
    return Sol
    
def gtilde_print_sol(S, Gt, layoutGt, fileloc, nE, M):
    """
    Using S, print an optimal solution for the problem defined by Gtilde.
    """
    for edge_count in range(len(Gt.es)):
        Gt.delete_edges(0)

    for i in range(len(S)):
        i_real = i + nE
        if S[i] == 1:
            for j in range(len(M)):
                if M[i_real][j]:
                    Gt.add_edge(i_real, j)
                    

    igraph.plot(Gt, fileloc,layout = layoutGt, vertex_label = [v['name'] for v in Gt.vs]) 

def print_G(Edges, fileloc, n):
    '''
    save G that is defined by edges at fileloc and return it's layout.
    '''

    g = igraph.Graph(n)
    for (i,j) in Edges:
        g.add_edge(i,j)

    layout1 = g.layout_circle()

    igraph.plot(g, fileloc, layout = layout1)
    print("G saved succesfully.")
    return layout1







#main
main()
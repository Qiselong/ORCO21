## Date         9.12    
## Author       Thomas b

# Objective     Do the "superline graph" operation.
#
# Let G be a graph. We define G' := SL(G) this way:
# V(G') are the edges of G.
# for two vertices of G', a, b, there exists an edge if it is possible to draw a triangle in G using the two corresponding edges. 

# We want the following things in this script:
#       1. Generate a random graph G given it's size & some density parameter
#       2. Compute the adjacendy matrix of SL(G)
#       3. Some image generation thing:
#           a. generate both images
#           b. generate on the same image the two graphs (union graph style)
#           c. generate G layout, and using the complex (a+b)/2 arcanes, draw on top of it the superline (using nice colors.)

# imports
import igraph
import random
import math
import numpy as np
from numpy.lib.type_check import imag

# File location stuff
image_loc = 'GDS/images/'

## Parameters
n = 5
d = 1
color_dict = {"edge_G": "blue", "vertex_G" : "black", "edge_Gp" : "red", "vertex_Gp" : "red"}


# main definition

def main():
    Edges = generation(n,d)
    simple_print(Edges)
    SLG = SuperLine(Edges)
    print(SLG)
    nameSLG = image_loc + 'SLG.png'
    igraph.plot(SLG, nameSLG, vertex_label = [v['name'] for v in SLG.vs])

# function definition

def generation(n, d):
    """
    generates as a list of edges (tuples) a random graph of size n with density d. 
    """
    nE = math.ceil((n*(n-1))*d/2)
    L = []
    while len(L) < nE:
        i,j = random.randint(0, n-1), random.randint(0, n-1)
        i,j = min(i,j), max(i,j)            # sort useful for next line
        if L.count((i,j)) == 0 and i != j:  # if i,j is not selected yet, and i,j is a valid edge (not a self loop)
            L.append((i,j)) 
    return L

def simple_print(L, name = 'coucou.png'):
    """
    given a list of edges, does a fast plot of it as a graph.
    """
    ## Note for later: it may be possible that some vertices end up alone. 
    ## Some solve for this would be to look at all vertices of G, get their degree and delete them accordingly.
    g = igraph.Graph(n)

    g.add_edges(L)
    file_name = image_loc+name
    igraph.plot(g, file_name, vertex_label = [i for i in range(len(g.vs))])

def SuperLine(L):
    """
    given the list of edges of G, returns as an igraph graph object the superline graph.
    """
    ## Note that edges are represented as (i,j) , i<j.
    # Observe that (a,b) and (c,d) may have an edge iff a=c or a = d or b = c or b=d. Done by abcd(e1, e2) function.
    # if we can find three edges x, y, z, st any pair put into abcd() return true, it's not sufficient: indeed they could share a common unique vertex.
    # we need an other function to compute that: xyz()

    gp = igraph.Graph(len(L))
    for i in range(len(L)):
        gp.vs[i]['name'] = str(L[i][0]) +',' +str(L[i][1])

    for i in range(len(L)):
        for j in range(i):
            if abcd(L[i], L[j]):
                for k in range(j):
                    if abcd(L[i], L[k]) and abcd(L[j], L[k]):
                        if xyz(L[i], L[j], L[k]):
                            gp.add_edge(i,j)
                            gp.add_edge(j,k)
                            gp.add_edge(i,k)
    gp.simplify(multiple = True)
    return gp


def abcd(e1, e2):
    """
    returns True or False, depending if e1 and e2 may be candidate to have an edge between them.
    """
    a, b, c, d = e1[0], e1[1], e2[0], e2[1]
    return a==c or a==d or b==c or b==d

def xyz(x, y, z):
    """
    return True or False, depending if xyz is a true triangle or not.
    """ 
    #lexico sort: see https://numpy.org/doc/stable/reference/generated/numpy.lexsort.html#numpy.lexsort
    L1 = [x[0], y[0], z[0]]
    L2 = [x[1], y[1], z[1]]
    ind = np.lexsort((L2, L1))

    TMP = [(L1[i], L2[i]) for i in ind]
    x, y, z = TMP[0], TMP[1], TMP[2]

    ##  1,2      1,3      2,3
    return x[0] == y[0] and y[1] == z[1] and x[1] == z[0]










# main execution

main()

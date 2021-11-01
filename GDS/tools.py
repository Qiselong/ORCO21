import igraph

def main():
    g = igraph.Graph.Full(3)
    igraph.plot(g)
    print(comp_3k(g))
    print(g.neighbors(0))
    return None

def T_detection(g, i,j):
    '''
    for a graph g and vertices i, j, detects if \exists k different than i,j that is a neighbour of both i and j.
    returns a list of such k. 
    '''

    K = []
    nI = g.neighbors(i)
    nJ = g.neighbors(j)
    for k1 in nI:
        for k2 in nJ:
            if k1==k2:
                K.append(k1)
    return K

def comp_3k(g):
    '''
    computes the number of triangles of g. 
    '''
    n = g.vcount()

    r = 0
    for i in range(n):
        for j in range(n):
            if i!=j:
                r+=len(T_detection(g,i,j))

    #as all triangles have been counted 3 times
    return r/3

        













main()
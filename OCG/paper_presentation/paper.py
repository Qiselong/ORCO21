# Date 19.11
# Version 1

import igraph
import random
import numpy as np
import os
 


# Parameters
n = 50 # size 
d = 0.2 # density  
max_tries = 5 
dir = 'OCG/images/'
message='Recall execution must be done from ORCO21 folder.'


## main definition

def main():
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    print("*"*80)
    isBP= True
    try_lol = 0
    while isBP and try_lol < max_tries:
        G, Perfect_matchings = generation(n, d)
        layout1 = G.layout("dh")
        isBP = is_BP(G)
        try_lol +=1
    if isBP:
        print("Failed to generate a non BP graph. Can you believe it?")
        return None

    print("Graph generated.")
    igraph.plot(G, dir+"G.png", layout = layout1)
    show_matchings(Perfect_matchings, layout1)


## functions definition

def generation(n, d):
    """
    generate randomly a matching covered graph with n vertices with density ~d. 
    If the result is bipartite, tries up to max_tries times. 
    returns the graph (igraph.Graph), the matchings (list of lists fo tuples)
    """
    graph = igraph.Graph(n)

    cardE = graph.ecount()

    Ms =[] #list of the matchings
    while cardE < d*0.5*n**2:
        M = []                                  # one pm (perfect matching)
        pick_one = [i for i in range( n)]   # pick two elements of this list to get our pm
        


        while len(pick_one) != 0:
            a = random.choice(pick_one)
            pick_one.remove(a)
            b = random.choice(pick_one)
            pick_one.remove(b)
            M.append((min(a,b), max(a,b)))

        Ms.append(M)
        for (a,b) in M:
            if not(graph.are_connected(a, b)): # litteraly: if there are no edge between a and b.
                graph.add_edge(a, b)
        cardE = graph.ecount()

    return graph, Ms

def is_BP(G):
        """
        return True or False depending if G (igraph.Graph) is bipartite or not
        Method used: greedy coloring over the vertices of G
        No i'm kidding we're gonna multiply matrices
        """
        M = np.array(G.get_adjacency()._get_data())
        M2 = np.matmul(M, M)
        
        k = 1
        while k < n:
            TMP = np.matmul(M, M2)
            k +=2
            for i in range(n):
                if TMP[i,i] != 0: 
                    return False
        return True
    
def show_matchings(PMS, layout1):
    """
    Using PMS (list of list of tuples), generates images that are the different perfect matchings.
    """
    for i in range(len(PMS)):
        Mi = PMS[i]
        Gi = igraph.Graph(n)
        for (a,b) in Mi:
            Gi.add_edge(a,b)
        igraph.plot(Gi, dir+'M'+str(i)+'.png', layout = layout1)
            


       




## Main
main()
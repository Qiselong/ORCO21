## Date 21.01
## Author Thomas B

# Objective:
# First version of the project is rather slow as it needs to handle a lot of variables. We propose -for the special case of n = 9- a better model that will use a presolve system; ie some basic solving rules. 

#imports
from z3 import *
import os
import math
from project import *


#locations
puzzle_loc = 'SAT_SMT/txt/puzzle_v2.txt'
solution_loc = 'SAT_SMT/txt/solution_v2.txt'

#parameters
warning = 'For execution & file locations: check the execution folder and the locations (puzzle_loc) variables makes sense.\n'


def main():
    clearConsole()
    print(warning)
    size, C = read_puzzle(puzzle_loc)

    ts = time.perf_counter_ns()
    print("Generating model..")

    X = variables_solve(size)
       
    Cp = presolve(C)
    square = square_constraints(size, X)
    integrity = integrity_constraints(size, X)
    lines = line_constraints(size, X)
    clues = clues_constraints(Cp, X)
    
    print("Model successfully generated.\nSolving..")

    s = Solver()
    s.add(square + integrity + lines + clues)
    s.check() 
    m = s.model()

    te = time.perf_counter_ns()
    print("Model successfully solved. Saving the solution.")
    print("Elapsed time: {0} µs".format((te-ts)//1000))

    save_solution(m, solution_loc, size, X)



## presolve:

def square_values(i,j,C):
    """
    return all the values known in the clues in the square of the case (i,j).
    """

    val = []
    for (k,l,clue) in C:
        if l//3 == j//3 and k//3 == i//3:
            val.append(clue)
    return val

def line_values(i,j,C):
    """
    return all values known in the clues in the line of (i,j)
    """

    val = []
    for (k,l,clue) in C:
        if k == i:
            val.append(clue)
    return val

def collumn_values(i,j,C):
    """
    return all values known in the clues in the collumn of (i,j)
    """

    val = []
    for (k,l,clue) in C:
        if l == j:
            val.append(clue)
    return val  

def value_pointing(i,j, C):
    """
    uses values function at (i,j) to look if exactly one value is missing at (i,j). 
    If not, return (False, C)
    If so, return (True, C + [new clue])
    
    Important: we first check that (i,j) is not a known clue. If it is, just return False, C.
    """

    for (k,l, val) in C:
        if k==i and l == j:
            return False, C

    valSq, valLi, valCo = square_values(i,j,C), line_values(i,j,C), collumn_values(i,j,C)
    Existing_values = union(valSq, union(valLi, valCo))
    if len(Existing_values) == 8:
        print("({0},{1}) -> ".format(i,j), end = "")
        for val in '123456789':
            if Existing_values.count(val) == 0:
                C.append( (i,j,val) )
                print("{0} ;".format(val), end=" ")
                return True, C
    return False, C

#I imagine the following function is likely to give nightmares to a computer scientist, which I am not. I just find it very funny
def union(A,B):         
    """
    union-style merge of A, B.
    """
    for elt in B:
        if A.count(elt) == 0:
            A.append(elt) 
    return A        

def presolve(C):
    """
    use value_pointer until it cannot any longer. 
    """
    print("Starting presolve. Initial number of clues: {0}".format(len(C)))

    change = False
    while change == False:
        for i in range(10):
            for j in range(10):
                change, C = value_pointing(i,j,C)
        if change == False:
            print("\nNothing modified on last loop. Ending presolve.\nNumber of clues: {0}".format(len(C)))
            return C
        if change:      # if we did at least one change and end up here, we run again every i,j.
            change = False
    return C

main()
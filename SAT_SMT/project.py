## Date 13.12
## Author Thomas B

# Objective: 
#   1. create a solver for sudoku using Z3 solver
#       sudokus are of sizes n.n    n \in {4, 9, 16, 25}
#       a file is to be read (puzzle.txt) and the solution is saved in an other file (solution.txt)
#   2. creates a generator of sudokus having a unique solution (later...)

#imports
from z3 import *
import os
import math





#locations
puzzle_loc = 'ORCO21/SAT_SMT/txt/puzzle.txt'

#parameters
warning = 'For execution & file locations: check the execution folder and the locations (puzzle_loc) variables makes sense.\n'

#main definition
def main():
    clearConsole()
    print(warning)
    size, C = read_puzzle(puzzle_loc)


    X = variables_solve(size)

    square = square_constraints(size, X)
    print(square)



#functions definition

def line_constraints(size, X):
    """
    returns line constraints for a puzzle with given number of elements
    """
    lines = [ [ [ If (i1 != i2, X[i1][j] != X[i2][j], True) for i1 in range(size)] for i2 in range(size) ]for j in range(size)] 
    return lines

def coll_constraints(size, X):
    """
    returns collumns constraints for a puzzle with given number of elements
    """
    colls = [ [ [ If (i1 != i2, X[j][i1] != X[j][i1], True) for i1 in range(size)] for i2 in range(size) ]for j in range(size)]  
    return colls

def square_constraints(size, X):
    """
    returns unicity constraints for a puzzle with given number of elements.
    """
    np = int(math.sqrt(size))
    square =[ [ [ [ If(j1//np == j2//np and i1//np == i2//np, X[i1][j1] != X[i2][j2], True ) for j2 in range(size)] for j1 in range(size)] for i2 in range(size)] for i1 in range(size)]
    return square
    
   


def variables_solve(size):
    """
    return the variables necessary to __solve__ a puzzle with given number of elements.
    """

    X =  [ [Int(f"X_{(i,j)}") for j in range(size)] for i in range(size)]
    return X

def read_puzzle(fileloc):
    """
    given a file name, returns the size n of it & the content as a list of constraints.
    constraints are of the form (i, j, val)
    """

    f = open(fileloc, 'r')
    file_content = f.readlines()   
    n = int(file_content[0])
    puzzle_content = file_content[1:len(file_content)]

    # ' ' deletion:
    for i in range(len(puzzle_content)):
        entry = puzzle_content[i] 
        copy = ''
        for elt in entry:
            if not(elt == ' '):
                copy += elt
        puzzle_content[i] = copy
    
    Constraints = []
    for i_line in range(n):
        for i_col in range(n):
            if puzzle_content[i_line][i_col] !='X' :
                value = int(puzzle_content[i_line][i_col])
                Constraints.append( (i_line, i_col, value) )

    return n, Constraints


def clearConsole(): #collectivized code from https://www.delftstack.com/howto/python/python-clear-console/
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

        


# main
main()
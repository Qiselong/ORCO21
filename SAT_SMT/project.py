## Date 13.12
## Author Thomas B
## Last update 21.01

# Objective: 
#   1. create a solver for sudoku using Z3 solver
#       sudokus are of sizes n.n    n \in {4, 9, 16, 25}
#       a file is to be read (puzzle.txt) and the solution is saved in an other file (solution.txt)
#   2. creates a generator of sudokus having a unique solution (later...)


#imports
from z3 import *
import os
import math
import time

#locations
puzzle_loc = 'SAT_SMT/txt/puzzle_v2.txt'
solution_loc = 'SAT_SMT/txt/solution_v2.txt'

#parameters
warning = 'For execution & file locations: check the execution folder and the locations (puzzle_loc) variables makes sense.\n'

#main definition
def main():
    clearConsole()
    print(warning)
    size, C = read_puzzle(puzzle_loc)

    ts = time.perf_counter_ns()
    print("Generating model..")

    X = variables_solve(size)
    square = square_constraints(size, X)
    integrity = integrity_constraints(size, X)
    lines = line_constraints(size, X)
    clues = clues_constraints(C, X)
    
    print("Model successfully generated.)")


    s = Solver()
    s.add(square + integrity + lines + clues)
    s.check() 
    m = s.model()

    te = time.perf_counter_ns()
    print("Model successfully solved. Saving the solution.")
    print("Elapsed time: {0} µs".format((te-ts)//1000))
    save_solution(m, solution_loc, size, X)

    
#functions definition
def str_conversion(elt):
    """
    converts an int into an str. 
    """
    A = '0123456789abcdefABCDEF'
    #print(elt, A[int(str(elt))])
    return A[int(str(elt))]

def int_conversion(elt):
    """
    convert a str into an int
    """
    A = [str(i) for i in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f' , 'A', 'B', 'C', 'D', 'E', 'F']
    return A.index(elt)

def save_solution(m, fileloc, size, X):
    """
    save the solution computed in fileloc
    """
    f = open(fileloc, 'w')
    for i in range(size):
        line = ''
        for j in range(size):
            line+= str_conversion(m[X[i][j]])
        line = save_format(line, size)
        line += '\n'
        f.write(line)
    f.close()
    print('saved successfully in ' + fileloc )

def save_format(line, size):
    """
    given a line and a size, reform the line in "correct" format
    """
    np = int(math.sqrt(size))
    l = ''
    for i in range(size):
        l+=line[i]
        if (i+1)%np == 0:
            l+=' '
    return l

def clues_constraints(C, X):
    """
    given C (list of tuples corresponding to a clue) returns the clues constraints.
    when n>9, it's a bit more complicated: see int_conversion
    """
    clues = []
    for (i,j,val) in C:
        value = int_conversion(val)
        clues.append(X[i][j] == value)
    return clues


def line_constraints(size, X):
    """
    returns line&colls constraints for a puzzle with given number of elements
    """
    lines = []
    for i in range(size):
        for j1 in range(size):
            for j2 in range(size):
                if j1 != j2:
                    lines.append(X[i][j1] != X[i][j2])
                    lines.append(X[j1][i] != X[j2][i])
    return lines


def square_constraints(size, X):
    """
    returns unicity constraints for a puzzle with given number of elements.
    """
    np = int(math.sqrt(size))
    square = []
    for i1 in range(size):
        for i2 in range(size):
            for j1 in range(size):
                for j2 in range(size):
                    if j1//np == j2//np and i1//np == i2//np and (i1,j1) != (i2,j2):
                        square.append(X[i1][j1] != X[i2][j2])
    return square
    
def integrity_constraints(size, X):
    """
    return integrity constraints.
    """   
    integrity = [  And(X[i][j] >= 1, X[i][j] <= size ) for j in range(size) for i in range(size)]
    return integrity


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
    f.close()

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
                value = puzzle_content[i_line][i_col]
                Constraints.append( (i_line, i_col, value) )

    return n, Constraints


def clearConsole(): #collectivized code from https://www.delftstack.com/howto/python/python-clear-console/
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


# main: uncomment following line to run the first version of the project. 
main()
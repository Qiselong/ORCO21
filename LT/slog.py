from scipy.optimize import linprog
import numpy

### parameters
mode= 'default'
k = 3
global D
D = [
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],
     [],    
    ]


def main():
    obj=[1] + [0]*132
    lhs = D

main()

####
# the equaion is : 
# min lambda
# st    DijXij <= lambda forall ij      (1)
#       sum_j Xij = 1                   (2)
#       sum_j Y_j = k                   (3)
#       forall j, sum_i Xij <= nYj      (4)

# vars:=[lambda, X00, X01, ... X011, X10, ... , X1111, Y1, Y2, ... Y11]
# thus |vars| = 1 + 11^2 + 11 = 133
# 

def c_1():
    '''
    returns table corresponding to the first constraint
    '''
    rhs_1 = [[1] + [0]*132]*121
    lhs_1 = []
    for i in range(11):
        for j in range(11):
            tmp = 0
            tmp += D[i][j] #Xkj
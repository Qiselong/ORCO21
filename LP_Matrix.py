#main objective: handle the shit of LP from the matrices pov.
#obj 1: allow to write sum_j Xij <= b
#obj2: allow sum_i Xij <= b_j (trivial when 1 done)
#obj3: allow to write DijXij <= A 
def main():
    '''
    test function.
    '''
    X= [[0]*5]*3
    print("X: ", X, end="\n")
    b = [0]*3
    print(c_sum(X, axis = 'c'))



def c_sum(X, axis= 'l'):
    '''
    returns all necessary tables to handle sum_i Xij comp b_j
    axis : 'l' -default- or 'c'. 'l' is summing over a line, so it's considering sum_j Xij <= b_i.
    If the dimensions of X and b do not match bc of the axis or whatever, an error message is displayed.
    '''
    n , m =  len(X), len(X[0])

    #error case:
    if not(axis == 'l' or axis == 'c'):
        print("c_sum error encountered: axis parameter (" + axis + ") invalid.")
        return None

    LHS = []
    #one constraint should look like [0]*m*k + [1]*m + [0]*m*(n-k)
    if axis == 'l':
        for i in range(n+1):
            LHS_TMP =[0]*(m*i) + [1]*m + [0]*m*(n-i)
            LHS.append(LHS_TMP)
    
    if axis == 'c':
        for j in range(m+1):
            LHS_TMP =[0]*(n*j) + [1]*n + [0]*n*(m-j)
            LHS.append(LHS_TMP)

    return LHS


main()

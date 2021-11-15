# Date: 5 Nov 21
# Auth: Thomas Boudier (M2 ORCO)
# Last update: 12 Nov 21

# there's nothing to do beyond simply executing this file. 
# theres a section parameters that may be changed to get different results.

# imports
import numpy as np


# paramteres
seed = 999      
S = 3           # nb. of possible states/arm // size of tables
verbose = True  # True for as much details as possible, False for just the necessary.
lam = 0.95      # discount parameter
n = 4           # nb. of arms
mu = 5          # gain vector: mean (all gain vectors have similar generation: normal distribution)
sigma = 2       # gain vector: standard deviation


### MAIN
def main():

    np.random.seed(seed)

    if verbose:
        print("*"*60)
        print("Generation with seed", seed)
        print(n, "arms will be generated, with", S, "possible states each.\nThe reward vectors follow a normal law of parameters (", mu, ",", sigma,").")
   
    R_i = [0]*n
    P_i = [0]*n

    for i in range(n):
        R_i[i] = r()
        P_i[i] = P()
        if verbose:
            print("*"*60, "\n     Arm ", i, "\n", "*"*15)
            print("reward vector is" ,R_i[i])
            print("stochastic table is\n", P_i[i], end="\n")
            print("*"*60)

    if verbose:
        print("P_pi generation...")
    Ppi = P_pi(R_i, P_i, S, n)
    if verbose:
        print("R_pi generation...")
    Rpi = R_pi(R_i, P_i, S, n)

    if verbose:
        print("Tables generated.\nComputation of V...")

    print()
    V = np.matmul(Rpi, np.linalg.inv(np.eye(n**S) - lam*Ppi ))
    print("Value of index policy is: ", V)


## Useful functions:
######################## Instances generation ########################
def P():
    '''
    figure out a probability table.
    '''
    #I could not figure a nice way to do it as for the reward vector, so it will be a biased vector.
    P = np.zeros((S,S))
    for i in range(S):
        rest = 1
        for j in range(S-1):
            P[i,j] = np.random.random()*rest        #np.random.random() finds a float in [0,1].
            rest = rest-P[i,j]
        P[i, S-1] =1-  sum(P[i, :])
    return P


def r():
    '''
    figure out a gain table. 
    '''
    R = np.zeros((S))
    for i in range(S):
        R[i] = np.random.normal(mu, sigma)
    return R

######################## Other useful things ########################

def L(W, Ploc = P):     #The only purpose of this function is its existence
    '''
    Bellman operator. LW(s) := r(s) + lambda sum_u p(u|s) W(u)
    LW = r + lambda P W
    '''
    return r + lam*np.matmul(Ploc, W)

def W(s, M, fixed_point, r, lamloc):
    '''
    computes the value of W(s,M).
    '''
    if M < min(r)/(1-lamloc):
        return fixed_point(s)
    
    if M > max(r)/(1-lamloc):
        return M
     
    # what is in comments is useless but i keep it bc it may be useful somewhere else 
    #index_argsort = np.argsort(fixed_point)
    #M = [fixed_point[index_argsort[i]] for i in range(S) but I don't need this
    # I also did not to do a (hidden) sort of the values of the fixed point
    #Ms = fixed_point[index_argsort[s]]

    return max(M, fixed_point(s))


######################## Q5. Functions ########################
def conv_P(s,S, n):
    """
    convert the state s = (s_0, ... s_n-1) in a natural number.
    s correspond to a list of integers. the first element correspond to the state of the first arm, in the sense that conv_P([0,1]) > conv_P([1,0]).
    """
    p = 0
    for i in range(len(s)):
        p += s[i]*S**(i)

    return p

def conv_S(p,S,n):
    """
    convert a state in p (natural number) into a state s.
    an exemple of s with S = 4 is:
    s = [0, 2, 3, 1, 0 , 0, ..]
    """

    #the algorithm is the classical one, then we reverse s before the output to make it consistent with definition of conv_P 

    s= np.zeros((n))
    i = 0
    while p > 0:
        s[i] = p % S
        p = p //S
        i +=1
    return np.flip( np.array(s) )

def diff_p(pi, pj):
    """
    returns a boolean depending wether it's possible to go from pi to pj.
    A similar operation is trivial when dealing directly with states: diff_s(si,sj) = 1 iff si and sj have at most one 'bit' of difference.
    """
    si, sj = conv_S(pi, S, n), conv_S(pj, S, n)
    diff_count = 0
    for i in range(len(si)):
        diff_count += (si[i] == sj[i])
    return (diff_count <= 1)

def Ii(s, Ris, Pis,i):
    """
    i: arm number
    s: s-state considered
    Ris, Pis: Reward/Stochastic tables (of all arms, we only need Ris[i] here for instance.)
    Returns the index of the arm i; ie the minimum value of M such that W_i(s,M)=M
    We know it is the min of the fixed point. 
    """

    return min( np.matmul(Ris[i], np.linalg.inv( np.eye(S)-lam*Pis[i] ) ) )

def I(s, Ris, Pis):
    """
    computes which are has the largest index. Uses extensively the Ii function. Is widely used to fill P_pi and R_pi.
    """
    max_index = Ii(s, Ris, Pis, 0)
    index_index = 0
    for i in range(1,S):
        tmp = Ii(s,Ris,Pis,i)
        if tmp > max_index:
            max_index = tmp
            index_index = i
    return index_index

def R_pi(Ris, Pis, S, n):
    """
    Given all the datas, generates the vector R_pi according to the method discussed in the .tex file.
    """

    R = np.zeros((n**S))
    for p in range(n**S):
        s = conv_S(p, S, n)
        arm_to_pull = I(s, Ris, Pis)
        R[p] = Ris[arm_to_pull][ int(s[arm_to_pull])]
    return R

def P_pi(Ris, Pis, S, n):
    """
    Given all the datas, generates the matrix P_pi according to the method discussed in the .tex file.
    """

    P = np.zeros((n**S, n**S))
    for p1 in range(n**S):
        for p2 in range(n**S):
            if not(diff_p(p1, p2)):
                s1 = conv_S(p1, S, n)
                s2 = conv_S(p2, S, n)
                index_in_s1 = I(s1, Ris, Pis)
                flag = True
                for i in range(len(s1)):
                    if i != index_in_s1 and s1[i] != s2[i]:
                        flag = False
                P[p1, p2] = flag and Pis[index_in_s1][ int(s2[index_in_s1])] [ int(s1[index_in_s1]) ]  
                                        #               ^ here is a casting in int that could have been avoid (and that could be fixed) but I won't take the time to do it. Anyway the instances are not too big so "it's ok".
                                        # theres an other casting on line 184; i figured that one later.
    return P        

######################## Main ########################

main()

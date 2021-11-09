# Date: 5 Nov 21
# Auth: Thomas Boudier (M2 ORCO)

# imports
import numpy as np

# paramteres
seed = 999
S = 3      # nb. of possible states/arm // size of tables
verbose = True
lam = 0.95
epsilon = 0.1

#parameters of normal law (gain vector)
mu = 5      
sigma = 2

def main():

    np.random.seed(seed)

    reward_vector = r()
    Probability_table = P()
    rmin = min(reward_vector)
    rmax = max(reward_vector)

    if verbose:
        print("seed is", seed)
        print("reward vector is" ,reward_vector)
        print("stochastic table is\n", Probability_table)
        print("rmin, rmax:", rmin, rmax)

    M0 = rmin/(1-lam)

    #fixed point of L: W -> R + lam*P*W is: Wf = R(I-lam*P)^-1
    Wf = np.matmul(reward_vector, np.linalg.inv( np.eye(S)-lam*Probability_table ) )

    if verbose:
        print("Fixed point of W:", Wf)


    Mi = np.zeros((S+1))
    Mi[0] = M0
    i = 1

    
    print(Mi)


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



def L(W, Ploc = P):
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
     
    index_argsort = np.argsort(fixed_point)
    #M = [fixed_point[index_argsort[i]] for i in range(S) but I don't need this
    # I also did not to do a (hidden) sort of the values of the fixed point
    Ms = fixed_point[index_argsort[s]]
    
    return max(Ms, fixed_point(s))










    return 

main()

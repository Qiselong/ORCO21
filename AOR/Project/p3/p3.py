p = []
W = []


def c1( A, Y, i, k):
    if Y[i,k] == 0:
        return 0
    
    res = 0
    for j in range(1, n):
        cumul_time = 0 
        for s in range(1, j):
            cumul_time += A[k,j] * p[i,j] 
        res += A[k, j]

def c_2( A, Y, i, k):
    if Y[i,k] == 0:
        return 0

    res = 0
    cumul_time = 0

    for j in range(1, n):
        cumul_time += A[k,j] * p[i,j]
        res += A[k,j * cumul_time * W[j]



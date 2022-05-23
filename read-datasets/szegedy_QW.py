import numpy as np
import scipy.sparse as sp
# transition matrix (copied from entropy.py)
def transmatrix(A):
    n = len(A)
    outdeg = np.zeros(n)
    for i in range(n):
        outdeg[i] = np.sum(A[i,:])
        
    T = np.zeros((n,n))
    for j in range(n):
        if outdeg[j] > 0:
            T[j,:] = A[j,:]/outdeg[j]
        else:
            T[j,j] = 1
    return T.T


def SQW_unitary(P):
    '''
    P is the stochastic matrix representing the Markov Chain
    Returns: Unitary matrix corresponding to the Szegedy Quantum Walk operator
    '''
    N = len(P)

    b_vec = [] #canonical basis vectors

    for i in range(N):
        b_vec.append(sp.csr_matrix(([1],([i],[0])),shape = (N,1)))

    psi = []
    sqrt_edges = np.sqrt(P).T@(b_vec)
    for j in range(N):
        psi.append(sp.kron(b_vec[:,j],P_sqr[j,:].T))

    N2 = N*N
    PI = sp.csr_matrix((N2,N2))
    for j in range(N):
        PI += psi[j]*psi[j].T

    S = sp.csr_matrix((N2,N2))
    for j in range(N):
        for k in range(N):
            S += sp.kron(b_vec[j],b_vec[k])*sp.kron(b_vec[k],b_vec[j]).T

    return S*(2*PI-sp.eye(N2))
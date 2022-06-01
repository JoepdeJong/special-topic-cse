import numpy as np
import scipy.sparse as sp
# transition matrix (copied from entropy.py)
def transmatrix(A):
    n = A.shape[0]
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


def SQW_unitary(A):
    '''
    A is the adjacency matrix of a graph

    Returns: Unitary matrix corresponding to the Szegedy Quantum Walk operator
    '''

     
    P = sp.csr_matrix(transmatrix(A)) # P is the stochastic matrix representing the Markov Chain

    N = P.shape[0]

    b_vec = sp.csr_matrix((N,N)) #canonical basis vectors

    for i in range(N):
        b_vec[:,i] = (sp.csr_matrix(([1],([i],[0])),shape = (N,1)))

    psi = []
    P_sqr = np.sqrt(P)
    for j in range(N):
        psi.append(sp.kron(b_vec[:,j],P_sqr[j,:].T))

    N2 = N*N 
    PI = sp.csr_matrix((N2,N2))
    for j in range(N):
        PI += psi[j]*psi[j].T
      
    S = sp.csr_matrix((N2,N2))
    for j in range(N):
        for k in range(N):
            S += sp.kron(b_vec[:,j],b_vec[:,k])*sp.kron(b_vec[:,k],b_vec[:,j]).T


    return S*(2*PI-sp.eye(N2))
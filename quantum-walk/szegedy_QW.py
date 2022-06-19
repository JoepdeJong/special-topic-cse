import numpy as np
import scipy.sparse as sp
import networkx as nx


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
'''
def transmatrix_new(A):
    n = A.shape[0]
    outdeg = sp.csr_matrix((n,1))
    for i in range(n):
        outdeg[i,0] = sp.csr_matrix.sum(A.getcol(i))

    T = sp.csr_matrix((n,n))
    for j in range(n):
        if outdeg[j,0] > 0:
            T[j,:] = A.getrow(j)/outdeg[j,0]
        else:
            T[j,j] = 1
    return T.T
'''

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
        psi.append(sp.kron(b_vec[:,j],P_sqr[:,j]))

    N2 = N*N 
    PI = sp.csr_matrix((N2,N2))
    for j in range(N):
        PI += psi[j]*psi[j].T
      
    S = sp.csr_matrix((N2,N2))
    for j in range(N):
        for k in range(N):
            S += sp.kron(b_vec[:,j],b_vec[:,k])*sp.kron(b_vec[:,k],b_vec[:,j]).T


    return S*(2*PI-sp.eye(N2)),b_vec,psi

def SQW_unitary_new(A):
    '''
    A is the adjacency matrix of a graph

    Returns: Unitary matrix corresponding to the Szegedy Quantum Walk operator
    '''

     
    P = sp.csr_matrix(transmatrix(A)) # P is the stochastic matrix representing the Markov Chain

    N = P.shape[0]

    b_vec = sp.csr_matrix((N,N)) #canonical basis vectors

    for i in range(N):
        b_vec[:,i] = (sp.csr_matrix(([1],([i],[0])),shape = (N,1)))

    N2 = N*N
    psi = sp.csr_matrix((N2,N))
    P_sqr = np.sqrt(P)
    for j in range(N):
        psi[:,j] = sp.kron(b_vec[:,j],P_sqr[:,j])

     
    PI = sp.csr_matrix((N2,N2))
    for j in range(N):
        PI += psi[:,j]*psi[:,j].T
      
    S = sp.csr_matrix((N2,N2))
    for j in range(N):
        for k in range(N):
            S += sp.kron(b_vec[:,j],b_vec[:,k])*sp.kron(b_vec[:,k],b_vec[:,j]).T


    return S*(2*PI-sp.eye(N2)),b_vec,psi

def average_dist(G,N_steps):

    A = nx.adjacency_matrix(G).todense()

    N = G.number_of_nodes()

    U , b_vec , psi = SQW_unitary_new(A) # unitary that sets the evolution of the QW
    

    # set initial state to uniform one
    n = U.shape[0]

    #alpha = sp.csr_matrix(np.ones(n)/np.sqrt(n)).T
    alpha = sp.csr_matrix(sp.csr_matrix.sum(psi,1)/np.sqrt(psi.shape[1]))

    # set initial distribution from initial state
    p_sum = sp.csr_matrix((N,1))

    for k in range(N):
        p_sum += (sp.kron(b_vec,b_vec[:,k]).T*alpha).power(2)

    projectors = [sp.kron(b_vec,b_vec[:,k]).T for k in range(N)]

    #perform N_steps of the SQW and calculate temportal average of p(j,t) = sum_k |<jk|alpha(t)>|^2
    for i in range(N_steps):
        alpha = U*alpha
        p_sum += np.sum(np.array([(projectors[k]*alpha).power(2) for k in range(N)]))

    return p_sum/N_steps

# use U² to preserve graph's directedness 
def average_dist2(G,N_steps):

    A = nx.adjacency_matrix(G).todense()

    N = G.number_of_nodes()

    U, b_vec , psi = SQW_unitary(A) # unitary that sets the evolution of the QW
    U2 = U*U

    b_vec = sp.csr_matrix((N,N)) #canonical basis vectors

    for i in range(N):
        b_vec[:,i] = (sp.csr_matrix(([1],([i],[0])),shape = (N,1)))

    # set initial state to uniform one
    n = U.shape[0]

    alpha = sp.csr_matrix(np.ones(n)/np.sqrt(n)).T

    # set initial distribution from initial state
    p_sum = sp.csr_matrix((N,1))

    for k in range(N):
        p_sum += (sp.kron(b_vec,b_vec[:,k]).T*alpha).power(2)

    #perform N_steps of the SQW and calculate temportal average of p(j,t) = sum_k |<jk|alpha(t)>|^2
    for i in range(N_steps):
        alpha = U2*alpha
        for k in range(N):
            p_sum += (sp.kron(b_vec,b_vec[:,k]).T*alpha).power(2)

    return p_sum/N_steps

# remove final loop to perform summation un numpy, faster
# use U² to preserve graph's directedness 
def average_dist_U2(G,N_steps):

    A = nx.adjacency_matrix(G).todense()

    N = G.number_of_nodes()

    U , b_vec , psi = SQW_unitary_new(A) # unitary that sets the evolution of the QW
    U2 = U*U

    # set initial state to uniform one
    n = U.shape[0]

    #alpha = sp.csr_matrix(np.ones(n)/np.sqrt(n)).T
    alpha = sp.csr_matrix(sp.csr_matrix.sum(psi,1)/np.sqrt(psi.shape[1]))

    # set initial distribution from initial state
    p_sum = sp.csr_matrix((N,1))

    for k in range(N):
        p_sum += (sp.kron(b_vec,b_vec[:,k]).T*alpha).power(2)

    projectors = [sp.kron(b_vec,b_vec[:,k]).T for k in range(N)]

    #perform N_steps of the SQW and calculate temportal average of p(j,t) = sum_k |<jk|alpha(t)>|^2
    for i in range(N_steps):
        alpha = U2*alpha
        p_sum += np.sum(np.array([(projectors[k]*alpha).power(2) for k in range(N)]))

    return p_sum/N_steps

#########################################
#########################################
# translate everyting to np.arrays instead of scipy.sparse
# (crashes, memory requirements too high for large graphs)
def SQW_unitary2(A):
    '''
    A is the adjacency matrix of a graph

    Returns: Unitary matrix corresponding to the Szegedy Quantum Walk operator
    '''

     
    P = transmatrix(A) # P is the stochastic matrix representing the Markov Chain

    N = P.shape[0]

    b_vec = np.eye(N) #canonical basis vectors

    psi = []
    P_sqr = np.sqrt(P)
    for j in range(N):
        psi.append(np.kron(b_vec[:,j],P_sqr[:,j]))

    N2 = N*N 
    PI = np.zeros((N2,N2))
    for j in range(N):
        PI += psi[j].T@psi[j]
      
    S = np.zeros((N2,N2))
    for j in range(N):
        for k in range(N):
            S += np.kron(b_vec[:,j],b_vec[:,k]).T@np.kron(b_vec[:,k],b_vec[:,j])


    return S@(2*PI-sp.eye(N2)),b_vec

def average_dist_no_sparse(G,N_steps):

    A = nx.adjacency_matrix(G).todense()

    N = G.number_of_nodes()

    U,b_vec = SQW_unitary(A) # unitary that sets the evolution of the QW
    U = U.todense()
    b_vec = b_vec.todense()
    U2 = U@U

    # set initial state to uniform one
    n = U.shape[0]

    alpha = (np.ones(n)/np.sqrt(n)).reshape(n,1)

    # set initial distribution from initial state
    p_sum = np.zeros((N,1))

    for k in range(N):
        p_sum += np.power(np.kron(b_vec,b_vec[:,k]).T@alpha,2)

    projectors = [np.kron(b_vec,b_vec[:,k]).T for k in range(N)]

    #perform N_steps of the SQW and calculate temportal average of p(j,t) = sum_k |<jk|alpha(t)>|^2
    for i in range(N_steps):
        alpha = U2@alpha
        p_sum += np.sum(np.array([np.power(projectors[k]@alpha,2) for k in range(N)]),1)

    return p_sum/N_steps
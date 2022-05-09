from import_siouxroads import *

A = import_draw_roads(draw=False)

### compute normalized Henrici departure from normality d_f
def Henrici(A):
    lambdas = np.square(np.abs(np.linalg.eig(A)[0]))
    frob = np.linalg.norm(A, 'fro')
    return np.sqrt(frob**2 - np.sum(lambdas))/frob

df = Henrici(A)

### compute entropy using a random walk
# first compute transition rates T_ij and transition matrix T
def transmatrix(A):
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

# find stationary distribution qstar

def stationarydistr(T, tol, A):
    q0 = np.ones(n)/n
    #perform step 1 outside of while loop such that condition is met the first iteration
    qold = q0
    qnew = T @ qold
    while np.sum(np.abs(qnew - qold)) > tol:
        qold = qnew
        qnew = T @ qold
    return qnew
        

# compute entropy
def entropy(tol, A):
    h = 0
    T = transmatrix(A)
    qstar = stationarydistr(T, tol, A)
    for i in range(n):
        for j in range(n):
            if T[i,j] > 0:
                h = h - T[i,j]*qstar[j]*np.log(T[i,j])
    return h

tol = 1e-10

h = entropy(tol, A)

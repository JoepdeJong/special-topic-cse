from import_literature1976 import *


### compute normalized Henrici departure from normality d_f
def Henrici(A):
    lambdas = np.square(np.abs(np.linalg.eig(A)[0]))
    frob = np.linalg.norm(A, 'fro')
    return np.sqrt(frob**2 - np.sum(lambdas))/frob

### compute entropy using a random walk
# first compute transition rates T_ij and transition matrix T
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

# find stationary distribution qstar

def stationarydistr(T, tol):
    n = len(T)
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
    n = len(A)
    h = 0
    T = transmatrix(A)
    qstar = stationarydistr(T, tol)
    for i in range(n):
        for j in range(n):
            if T[i,j] > 0:
                h = h - T[i,j]*qstar[j]*np.log(T[i,j])
    return h

# compute weighted sum of eigenvectors with eigenvalue 1
def weightedev(T):
	indices = np.where(np.linalg.eig(T)[0] == 1)
	ev = np.zeros(len(T))
	for i in indices[0]:
		ev = ev + np.linalg.eig(T)[1][:,i]
	return ev/indices[0].size

def entropy2(A):
	h = 0
	T = transmatrix(A)
	ev = weightedev(T)
	n = len(A)
	for i in range(n):
		for j in range(n):
			if T[i,j] > 0:
				h = h - T[i,j]*ev[j]*np.log(T[i,j])
	return h

if __name__ == '__main__':
	G = import_draw_literature(draw=False)
	A = nx.adjacency_matrix(G)
	A = A.todense()
	tol = 1e-10
	h1 = entropy(tol, A)
	h2 = entropy2(A)
	print(h2)
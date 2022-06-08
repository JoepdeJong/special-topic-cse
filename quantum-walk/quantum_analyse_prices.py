from szegedy_QW import average_dist_U2
import os
import networkx as nx
import numpy as np
import scipy.sparse as sp
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def graph_data_list(n_iteration):
	'''
	Creates a list with the names of the files corresponding to 
	our dataset and a specific iteration
	'''
	filt = str(n_iteration)+'.txt'
	return [f for f in os.listdir('../dataset') if f[-5:]==filt]

def get_dist(n_iteration,N_steps):

	datasets = graph_data_list(n_iteration)

	count = 0; total = '/'+str(len(datasets))
	print(str(count)+total,end='\r')

	for f in datasets:

		#Build graph
		G = nx.DiGraph()

		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))

		p_av = average_dist_U2(G,N_steps)

		np.save(os.path.join('results_'+str(N_steps)+'_steps_it'+str(n_iteration),str(f[:-4])),p_av)

		#track progress in simulation
		print(str(count+1)+total,end='\r')
		count+=1
	
	return

def transmatrix(A):
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


def eval_entropy(T,p_dist):

def get_entropy(n_iteration):

	datasets = graph_data_list(n_iteration)

	#Build graph
	for f in datasets:
		G = nx.DiGraph()

		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))





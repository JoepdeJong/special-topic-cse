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

		np.save(os.path.join('new_results_'+str(N_steps)+'_steps_it'+str(n_iteration),str(f[:-4])),p_av.todense())

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
	n = T.shape[0]
	h = 0
	for i in range(n):
		for j in range(n):
			if T[i,j] > 0:
				h -= T[i,j]*p_dist[j]*np.log(T[i,j])
	return h


def get_entropy(n_iteration):

	datasets = graph_data_list(n_iteration)

	#assemble folder name
	foldername_p_dist = 'results_650_steps_it'+str(n_iteration)+'/'

	#build array to store entropies
	# first row for 20 node graphs
	# second row for 50 node graphs
	# third row for 100 node graphs
	entropy_array = np.zeros((3,25))

	#build array to store reciprocal thresholds
	# first row for 20 node graphs
	# second row for 50 node graphs
	# third row for 100 node graphs
	rec_threshold_array = np.zeros((3,25))


 
	i20 = 0
	i50 = 0
	i100 = 0
	for f in tqdm(datasets):
		#Build graph
		G = nx.DiGraph()

		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))

		T = transmatrix(nx.adjacency_matrix(G))

		#load prob dist, but it got stored in a weird
		p_dist = np.load(foldername_p_dist+f[:-4]+'.npy')

		if f[14:17] == '100':
			entropy_array[2,i100] = eval_entropy(T,p_dist)
			
			try:
				rec_threshold_array[2,i100] = float(f[-19:-15])
			except ValueError:
				rec_threshold_array[2,i100] = float(f[-18:-15])

			i100 += 1

		elif f[14:16] == '50':
			entropy_array[1,i50] = eval_entropy(T,p_dist)
			
			try:
				rec_threshold_array[1,i50] = float(f[-19:-15])
			except ValueError:
				rec_threshold_array[1,i50] = float(f[-18:-15])

			i50 += 1

		else:
			entropy_array[0,i20] = eval_entropy(T,p_dist)
			
			try:
				rec_threshold_array[0,i20] = float(f[-19:-15])
			except ValueError:
				rec_threshold_array[0,i20] = float(f[-18:-15])

			i20 += 1

	np.save('entropy_array_it'+str(n_iteration),entropy_array)
	np.save('rec_threshold_array_it'+str(n_iteration),rec_threshold_array)

def get_normalized_entropy(n_iteration):

	datasets = graph_data_list(n_iteration)

	#assemble folder name
	foldername_p_dist = 'new_results_650_steps_it'+str(n_iteration)+'/'

	#build array to store entropies
	# first row for 20 node graphs
	# second row for 50 node graphs
	# third row for 100 node graphs
	entropy_array = np.zeros((3,25))

	#build array to store reciprocal thresholds
	# first row for 20 node graphs
	# second row for 50 node graphs
	# third row for 100 node graphs
	rec_threshold_array = np.zeros((3,25))


 
	i20 = 0
	i50 = 0
	i100 = 0
	for f in tqdm(datasets):
		#Build graph
		G = nx.DiGraph()

		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))

		A = nx.adjacency_matrix(G)

		T = transmatrix(A)

		T_sim = transmatrix((A+A.T)/2)

		#load prob dist
		p_dist = np.load(foldername_p_dist+f[:-4]+'.npy')

		if f[14:17] == '100':
			p_dist_sim = 1/100*np.ones(100)
			entropy_array[2,i100] = eval_entropy(T,p_dist)/eval_entropy(T_sim,p_dist_sim)

			i100 += 1

		elif f[14:16] == '50':
			p_dist_sim = 1/50*np.ones(50)
			entropy_array[1,i50] = eval_entropy(T,p_dist)/eval_entropy(T_sim,p_dist_sim)

			i50 += 1

		else:
			p_dist_sim = 1/20*np.ones(20)
			entropy_array[0,i20] = eval_entropy(T,p_dist)/eval_entropy(T_sim,p_dist_sim)
	
			i20 += 1

	np.save('new_normalized_entropy_array_it'+str(n_iteration),entropy_array)

	return 








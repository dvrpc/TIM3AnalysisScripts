from scipy.sparse import csr_matrix, csgraph
import numpy as np

i =     np.array([1, 2, 2, 5, 1, 3, 3, 4, 3, 5, 4, 5])
j =     np.array([2, 1, 5, 2, 3, 1, 4, 3, 5, 3, 5, 4])
cost =  np.array([5, 5, 6, 6, 2, 2, 1, 1, 2, 2, 2, 2])

cutoff = 100

network = csr_matrix((cost, (i, j)), shape = (6, 6), dtype = 'int')
for i in range(5):
    result = csgraph.dijkstra(network, indices = i+1, limit = cutoff)
    print(i+1, result)
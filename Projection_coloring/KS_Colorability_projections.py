import numpy as np

import scipy as sp
from scipy.optimize import milp, LinearConstraint

import networkx as nx
import itertools as it

import copy
import math

#==================================================
"Constructing the KS System"

def projections_to_color(d):
    """Produce all projection matrices of order d over F_2
    """

    old_set = []
    for i in range(2**(d*d)):
        # Produce the set of all binary d x d matrices using the hack found at https://stackoverflow.com/a/54393156 
        old_set.append(np.matrix([int(k) for k in "{0:b}".format(i).zfill(d*d)]).reshape(d, d))

    zero_matrix = np.zeros((d,d))
    identity_matrix = np.identity(d)

    new_set = []
    for m in old_set:
        # Check for all of the binary matrices to find the symmetric idemptotents (i.e., projections).
        if (np.array_equal(m, m.transpose()) and np.array_equal(m, np.mod(np.matmul(m, m), 2))):
            new_set.append(m)

    # Remove the zero matrix.
    del new_set[0]
    return new_set

def projection_coloring(d):
    """Return True if the set of all projections in projections_to_color(d) is KS colorable
       and False if we do not identify a coloring.
    """
    matrix_set = projections_to_color(d)
    num_of_matrices = len(matrix_set)

    # Print the list of matrices; this can be commented out if we do not want to see them.
    for i in range(0, num_of_matrices):
        print(f"Matrix ", i, ":\n", matrix_set[i])
    # print(matrix_set)
    
    # Generate the orthogonality graph of our projections.
    G = nx.Graph()
    G.add_nodes_from(range(0, num_of_matrices)) 

    zero_matrix = np.zeros((d, d), int)

    for i in range(0, num_of_matrices):
        for j in range(i, num_of_matrices):
            # If the product of the ith and jth matrices yields a matrix whose entries are all 0 mod 2,
            # we add an edge between their corresponding vertices in our graph.
            if np.array_equal(np.mod(np.matmul(matrix_set[i], matrix_set[j]), 2), zero_matrix):
                G.add_edge(i,j)
    
    # Determine the cliques in G as a list of lists of vectors in the clique.
    clqs = list(nx.find_cliques(G))
    num_of_clqs = len(clqs)

    # Create the matrix for the integer linear programming problem.
    M = np.zeros((num_of_clqs,num_of_matrices))

    for i in range(0, num_of_clqs):
        for j in range(1, num_of_matrices):
            if j in clqs[i]:
                M[i, j] = 1
    
    # Create the upper bounds and lower bounds of 1 to require that every maximal clique has a unique projection colored 1.
    upper_bound = np.ones(num_of_clqs)  
    lower_bound = upper_bound           # For projection coloring, all maximal cliques need to sum to one, not just those of largest order.


    coloring_result = milp(c = np.zeros(num_of_matrices), integrality = np.ones(num_of_matrices), constraints = LinearConstraint(M, lower_bound, upper_bound))

    # Print the result of the attempted coloring. Different lines can be commented or uncommented as desired.

    print(G)
    print(coloring_result.message)
    print(f"Dimension =", d)
    print(f"Orthogonality graph:", G)
    # print(clqs)
    # print(M)
    print(f"Number of maximal cliques = ", num_of_clqs)
    print(f"Number of nonzero projections = ", num_of_matrices)
    print(f"KS coloring: ", coloring_result.x)

    if coloring_result.success == True:
        print(f"A coloring was found.")
        return True
    else:
        print(f"The set is uncolorable.")
        return False

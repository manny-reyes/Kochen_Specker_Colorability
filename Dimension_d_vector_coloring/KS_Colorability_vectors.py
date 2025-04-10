from sympy import diophantine
import numpy as np

import scipy as sp
from scipy.optimize import milp, LinearConstraint
import networkx as nx

import copy
import math

#==================================================
# Defining Helper Functions to Construct KS Systems

# Since we are working up to dimension d = 6, we import 6 symbols to act as variables.
from sympy.abc import u, v, w, x, y, z


def sum_of_squares_solutions(d,n):
    """For d between 3 and 6, return a set of solutions to diophantine equations
       of the form (x_1)^2 + ... + (x_d)^2 = n, where n is any nonnegative
       integer.
    """
    vec_sol = {tuple(np.zeros(d, int))}
    if n != 0: # This is for nontrivial solutions.
        if d == 3:
            vec_sol = diophantine(x**2 + y**2 + z**2 - n, permute = True)

        elif d == 4:
            vec_sol = diophantine(w**2 + x**2 + y**2 + z**2 - n, permute = True)

        elif d == 5:
            vec_sol = diophantine(v**2 + w**2 + x**2 + y**2 + z**2 - n, permute = True)
            
        elif d == 6:
            vec_sol = diophantine(u**2 + v**2 + w**2 + x**2 + y**2 + z**2 - n, permute = True)
        else:
            raise TypeError("The dimension must be between 3 and 6.")
            
    return vec_sol

def basis_vectors(d):
    """Return a list of basis vectors in R^{d}.
    """
    # We initialize a variable to access values in a list corresponding to
    # the index position.
    index = 0

    # Initialize the zero vector so we can change its entries.
    zero_vector_list = list(np.zeros(d, int))

    # Initialize a list where we will add our basis vectors.
    basis_vector_list = []

    # Iterate through the entries of the zero vector, updating the 0 in the
    # index position to 1.
    while index < d:
        # Make a copy to avoid referencing issues.
        basis_vector_i = copy.deepcopy(zero_vector_list)

        basis_vector_i[index] = 1
        basis_vector_list += [tuple(basis_vector_i)]
        index += 1

    return basis_vector_list

def factorization(N):
    """Given a positive integer, N, return a set of integers representing the
       factors of N.
    """
    divisors = {1, N}
    for m in range(2, N):
        if N % m == 0:
            divisors.add(m)
    return divisors

#==================================================
# Constructing the KS System

def primitive(int_vec):
    """Given a tuple, int_vec, return True if the corresponding integer vector is primative, 
       i.e. its entries have a greatest common divisor equal to 1, and False otherwise.
    """
    int_list = list(int_vec)
    return math.gcd(*int_list) == 1

# This function helps us access the nonzero elements of a vector without having to iterate
# through all of its elements later on.
def nonzero_tuple(int_vec):
    """Given a tuple, int_vec, return a new tuple whose entries are the nonzero elements
       of int_vec in the order that they appear.
    """
    nonzero_int_list = []
    for x in int_vec:
        if x != 0:
            nonzero_int_list += [x]
    return tuple(nonzero_int_list)

def count_positive_entries(int_vec):
    """Given a tuple, int_vec, return how many positive entries it contains.
    """
    # We'll construct a list whose binary entries represent whether a corresponding
    # element in int_vec is positive (1) or zero/negative (0).
    entries_list = [1 if x > 0 else 0 for x in int_vec]

    return sum(entries_list)


def positive_first_nonzero_entry(int_vec):
    """Given a tuple, int_vec, return True if the first nonzero entry is positive.
    """
    # A tuple containing the nonzero entries of int_vec.
    nonzero_int_vec = nonzero_tuple(int_vec)

    if nonzero_int_vec[0] > 0:
        return True
    else:
        return False

# d = 3, then we can just look at the well_signed vectors our
# sum_of_squares_solutions function generates. It is not used in this code, but
# is left for exploratory purposes.
def well_signed(int_vec):
    """Given a tuple, int_vec, return True if it is well-signed in Z^{3}and False
       otherwise. That is, determine whether one of the following is true:
       1. int_vec has only one nonzero entry which is positive
       2. int_vec has three nonzero entries, two of which are positive
       3. int_vec has two nonzero entries and its first nonzero entry is positive
    """
     # A tuple containing the nonzero entries of int_vec.
    nonzero_int_vec = nonzero_tuple(int_vec)

    # The number of nonzero entries in int_vec.
    nonzero_entry_count = len(nonzero_int_vec)

    # The number of positive entries in int_vec.
    positive_entry_count = count_positive_entries(int_vec)

    if nonzero_entry_count == 1 and positive_entry_count == 1:
        return True
    elif nonzero_entry_count == 3 and positive_entry_count >= 2:
        return True
    elif nonzero_entry_count == 2 and nonzero_int_vec[0] > 0:
        return True
    else:
        return False

def primitive_well_signed_solutions(d,n):
    """Compute solutions to the diophantine equation with d variables squared equaling
       n, where n is any nonnegative integer. Return a set of tuples that represent primitive, 
       well-signed solutions in Z^{d} to the previous equation.
    """
    vec_sol = sum_of_squares_solutions(d,n)

    # Create a deep copy of vec_sol to ensure the for-loop remains consistent.
    new_vec_sol = copy.deepcopy(vec_sol)

    for v in vec_sol:
        if not(primitive(v) and positive_first_nonzero_entry(v)):
            new_vec_sol.remove(v)
    return new_vec_sol


#==================================================
# Coloring the Vectors in our KS System

def basis_vector_coloring(d):
    """Color the bases vectors in R^{d}.
    """
    list_of_bases = basis_vectors(d)

    # We assign the first basis vector in list_of_bases the value 1.
    color_dict = {list_of_bases[0] : 1}

    # We assign the remaining basis vectors in list_of_bases the value 0.
    for u in list_of_bases[1:]:
        color_dict[u] = 0
    return color_dict

def vectors_to_color(d,N):
    """Return a list of tuples (vectors) we want to color. The entries of these vectors will be
       solutions to the diophantine equation with d variables squared equaling n, where n
       is a factor of N.
    """
    # We first use set() so that every vector is unique up to scaling.
    set_of_vectors = set()
    set_of_divisors = factorization(N)
    for n in set_of_divisors:
        if n > 1:
            set_of_vectors.update(primitive_well_signed_solutions(d,n))
    return list(set_of_vectors)

def vector_coloring(d,N):
    """Return True if all vectors (and those generated) from vectors_to_color(N) is KS colorable
       and False if we identify a contradiction in the coloring of our vectors.
    """
    # color_dict = basis_vector_coloring(d)

    set_of_vectors = vectors_to_color(d,N)
    set_of_all_vectors = basis_vectors(d) + set_of_vectors

    num_of_vectors = len(set_of_all_vectors)

    # Generate the orthogonality graph of our vectors.
    G = nx.Graph()

    # Note, we index the first vector in set_of_all_vectors with 0.
    G.add_nodes_from(range(0, num_of_vectors))
    
    # If the the ith and jth vectors are orthogonal, we add an edge between their corresponding
    # vertices in our graph.
    for i in range(0, num_of_vectors):
        for j in range(i, num_of_vectors):
            if np.dot(set_of_all_vectors[i], set_of_all_vectors[j]) == 0:
                G.add_edge(i, j)
    
    # Determine the cliques in G as a list of lists of vectors in the clique.
    clqs = list(nx.find_cliques(G))
    num_of_clqs = len(clqs)

    # Create the matrix for the integer linear programming problem.
    M = np.zeros((num_of_clqs, num_of_vectors))

    for i in range(0, num_of_clqs):
        for j in range(0, num_of_vectors):
            if j in clqs[i]:
                M[i, j] = 1
    
    #Create the upper bounds of 1 and lower bounds on coloring values to force a 
    # single 1 in each orthogonal basis and at most one 1 in smaller cliques.
    upper_bound = np.ones(num_of_clqs)
    lower_bound = np.zeros(num_of_clqs)

    for i in range(0, num_of_clqs):
        current_clique = clqs[i][:]

        # If the clique contains as many vectors as the dimension of the vector space,
        # we require exactly one vector to be colored 0.
        if len(current_clique) == d:
            lower_bound[i] = 1


    coloring_result = milp(c = np.zeros(num_of_vectors), integrality = np.ones(num_of_vectors), constraints = LinearConstraint(M, lower_bound, upper_bound))

    print(coloring_result.message)
    print(f"Dimension =", d)
    print(f"Orthogonality graph:", G)
    print(f"Lower bound vector ", lower_bound)
    # print(clqs)
    # print(M)
    print(f"Number of maximal orthogonal sets =", sum(upper_bound))
    print(f"Number of bases = ", sum(lower_bound))
    print(f"Number of vectors we are consider = ", num_of_vectors)
    print(f"Number of cliques = ", num_of_clqs)
    # print(coloring_result.x)
    # print(set_of_all_vectors)
    print(f"The divisors are", factorization(N))


    if coloring_result.success == True:
        print(f"A coloring was found.")
        return True
    else:
        print(f"The set is uncolorable.")
        return False
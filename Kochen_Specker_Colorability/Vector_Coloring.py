from sympy import diophantine
from sympy.abc import i, j, k
from functools import reduce
import math
import copy
import numpy as np
from Factors_or_N import *

def sum_of_squares_solutions(n):
    """Return a set of i, j, and k solutions to diophantine equations of the form i^2 + j^2 + k^2 = n, 
       where n is any nonnegative integer.
    """
    vec_sol = {(0, 0, 0)}
    if n != 0: # This is for nontrivial solutions.
        vec_sol = diophantine(i**2 + j**2 + k**2 - n, permute = True)
    return vec_sol

def primitive(int_vec):
    """Given a tuple, int_vec, return True if the corresponding the integer vector 
       is primative, i.e. its entries have greatest common divisor equal to 1, and 
       False otherwise.
    """
    int_list = list(int_vec)
    return math.gcd(*int_list) == 1

# def nonzero_entry(int_vec):
#     """Given a tuple, int_vec, return True if it contains a nonzero entry and False otherwise.
#     """
#     # We cast the tuple as a list to more efficiently add it's elements.
#     int_vec_list = list(int_vec)
#     return sum(int_vec_list) != 0

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
    # We'll construct a list whose binary entries represent whether a corresponding element 
    # in int_vec is positive (1) or negative (0).
    entries_list = [1 if x > 0 else 0 for x in int_vec]

    # print(entries_list)
    return sum(entries_list)

def well_signed(int_vec):
    """Given a tuple, int_vec, return True if it is well-signed and False otherwise. That is, 
       determine whether one of the following is true:
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

def primative_well_signed_solutions(n):
    """Compute i, j, and k solutions to diophantine equations of the form i^2 + j^2 + k^2 = n, 
       where n is any nonnegative integer. Return a set of tuples that represent primitive, 
       well-signed integer vector solutions in R^3 to the previous equation.
    """
    vec_sol = sum_of_squares_solutions(n)
    new_vec_sol = copy.copy(vec_sol)    # Create a shallow copy of vec_sol to ensure the for-loop remains consistent.
    for v in vec_sol:
        if not(primitive(v) and well_signed(v)):
            new_vec_sol.remove(v)
    return new_vec_sol

def pairwise_orthogonal(v, vec_set):   # v is a tuple and vec_set is a set of tuples (vectors)
    """Return True if the primitive, well-signed integer vector v is orthogonal to all other vectors
       in the set vec_list and False otherwise.
    """
    for vec in vec_set:
        if v != vec and np.dot(v, vec) != 0: 
            print(f"The vector {v} and {vec} are not orthogonal, since their dot product is {np.dot(v, vec)}.")
            return False
    return True

def orthogonal_set(vec_set):
    """Return True if the set of primitive, well-signed integer vectors, vec_set, is an orthogonal set and
       False otherwise.
    """
    for v in vec_set:
        if not(pairwise_orthogonal(v, vec_set)):
            return False
    return True

def set_of_values(N):
    """Given a positive integer, N, return a set of integers representing the factors of N and pairwise products 
       of these factors.
    """
    set_values = {1, N}
    for x in range(2, N):
        # if N % x == 0 and is_prime(x):
        if  N % x == 0:
            set_values.add(x)

    return set_values

def set_up_for_color_assignment(N):
    set_to_color = set()
    vals_to_iterate = set_of_values(N)
    for v in vals_to_iterate:
        if v > 2:
            # print(v)
            set_to_color.update(primative_well_signed_solutions(v))
    return set_to_color

def color_assignment(N):
    """Return True if all vectors (constructed) from primative_well_signed_solutions(N) has been designated 
       either a 1 or 0.
    """
    # white = 1 and black = 0
    color_dict = {(1, 0, 0): 1, (0, 0, 1): 0, (0, 1, 0): 0} # Q_{1} is a subset of S_{n} (N) for all n and N in Z
    if N % 2 == 0:
        color_dict[(1, 0, -1)] = 1  # Now, we add vectors from Q_{2} that form an orthogonal set with (0, 1, 0) in Q_{1}
        color_dict[(1, 0, 1)] = 0
        color_dict[(1, 1, 0)] = 0   # Add vectors from Q_{2} that form an orthogonal set with (0, 0, 1) in Q_{1}
        color_dict[(1, -1, 0)] = 1
        color_dict[(0, 1, 1)] = 0   # Finally, add vectors from Q_{2} that form an orthogonal set  with (1, 0, 0) in Q_{1}
        color_dict[(0, 1, -1)] = 0

    # vec_set = primative_well_signed_solutions(N)
    vec_set = set_up_for_color_assignment(N)

    for_loop_color_dict = copy.copy(color_dict) # Create a shallow copy of color_dict to ensure the for-loop remains consistent.

    for vec_sol_to_N in vec_set:
        for key_vec in for_loop_color_dict.keys():
            if np.dot (vec_sol_to_N, key_vec) == 0 and for_loop_color_dict[key_vec] == 1:
                color_dict[vec_sol_to_N] = 0

                # print(f"The dot product of {vec_sol_to_N} and {key_vec} is {np.dot(vec_sol_to_N, key_vec)}!")

    # print("We'll now be considering the cross product of 2 black vectors!")

    new_for_loop_color_dict = copy.copy(color_dict) # Create a shallow copy of an updated color_dict to ensure the for-loop remains consistent.

    for key_vec_1 in new_for_loop_color_dict.keys():
        for key_vec_2 in new_for_loop_color_dict.keys():
            if new_for_loop_color_dict[key_vec_1] == 0 and new_for_loop_color_dict[key_vec_2] == 0 and np.dot (key_vec_1, key_vec_2) == 0:
                cross_product = np.cross(key_vec_1, key_vec_2)
                normalized_cp = cross_product / math.gcd(*cross_product)
                new_vec = tuple(normalized_cp)
                # print(f"The cross product of {key_vec_1} and {key_vec_2} is {tuple(np.cross(key_vec_1, key_vec_2))}!")
                if new_vec in color_dict.keys() and color_dict[new_vec] != 1:
                    return False
                else:
                    color_dict[new_vec] = 1

    return color_dict
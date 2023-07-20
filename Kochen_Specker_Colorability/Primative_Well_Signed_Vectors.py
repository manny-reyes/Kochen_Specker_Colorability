import math
import copy
from Sum_of_Squares_and_Divisibility import sum_of_squares_solutions

def primitive(int_vec):
    """Given a tuple, int_vec, return True if the corresponding integer vector is primative, 
       i.e. its entries have a greatest common divisor equal to 1, and False otherwise.
    """
    int_list = list(int_vec)
    return math.gcd(*int_list) == 1

# This function helps up access the nonzero elements of a vector without having to iterate
# through all of its elements.
def nonzero_tuple(int_vec):
    """Given a tuple, int_vec, return a new tuple whose entries are the nonzero elements of 
       int_vec in the order that they appear.
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

def primitive_well_signed_solutions(n):
    """Compute i, j, and k solutions to diophantine equations of the form i^2 + j^2 + k^2 = n, 
       where n is any nonnegative integer. Return a set of tuples that represent primitive, 
       well-signed integer vector solutions in R^3 to the previous equation.
    """
    vec_sol = sum_of_squares_solutions(n)

    # Create a shallow copy of vec_sol to ensure the for-loop remains consistent.
    new_vec_sol = copy.copy(vec_sol)

    for v in vec_sol:
        if not(primitive(v) and well_signed(v)):
            new_vec_sol.remove(v)
    return new_vec_sol
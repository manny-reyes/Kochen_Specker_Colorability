from Sum_of_Squares_and_Divisibility import *
from Primitive_Well_Signed_Vectors import *
import numpy as np
import math

def vectors_to_color(N):
    """Return a set of tuples (vectors) we want to color. The entries of these vectors will be
       i, j, and k solutions to the diophantine equation i^2 + j^2 + k^2 = n, where n is a factor
       of N.
    """
    vec_set = set()
    set_of_divisors = factorization(N)
    for n in set_of_divisors:
        if n > 2:
            vec_set.update(primitive_well_signed_solutions(n))
    return vec_set

def vector_coloring(N):
    """Return True if all vectors (and those generated) from vec_set is KS colorable and False 
       if we identify a contradiction in the coloring of our vectors.
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

    vec_set = vectors_to_color(N)

    return is_KS_colorable_set(vec_set, color_dict)

def is_KS_colorable_set(vec_set, color_dict):
    """Return True if the set of all vectors (and those generated) from vec_set is KS colorable 
       or assumptions had to be made to continue the coloring process and False if we identify 
       a contradiction in the coloring.
    """
    for_loop_color_dict = copy.deepcopy(color_dict) # Create a deep copy of color_dict to ensure the for-loop remains consistent.

    for v in vec_set:
        for key_vec in for_loop_color_dict.keys():
            if np.dot(v, key_vec) == 0 and for_loop_color_dict[key_vec] == 1:
                if not(v in for_loop_color_dict.keys()):
                    color_dict[v] = 0
                elif for_loop_color_dict[v] != 0:
                    print(f"A contradiction has been identified from coloring {v} after taking the dot product of {v} and {key_vec}.")
                    return False

    new_for_loop_color_dict = copy.deepcopy(color_dict) # Create a deep copy of an updated color_dict to ensure the for-loop remains consistent.

    for key_vec_1 in new_for_loop_color_dict.keys():
        for key_vec_2 in new_for_loop_color_dict.keys():
            if new_for_loop_color_dict[key_vec_1] == 0 and new_for_loop_color_dict[key_vec_2] == 0 and np.dot (key_vec_1, key_vec_2) == 0:
                cross_product = np.cross(key_vec_1, key_vec_2)
                normalized_cp = cross_product / math.gcd(*cross_product)
                new_vec = tuple(np.array(normalized_cp, dtype = int))
                if new_vec in color_dict.keys() and color_dict[new_vec] != 1:
                    print(f"A contradiction has been identified from coloring {new_vec}, the cross product of {key_vec_1} and {key_vec_2}.")
                    return False
                elif well_signed(new_vec):
                # else: # Uncomment this line of code (and comment out the previous line) if you'd like to consider vectors that are not well-signed
                    color_dict[new_vec] = 1

    # If color_dict stayed the same, we must make an assumption.
    if set(color_dict.keys()) - set(for_loop_color_dict.keys()) == set():
        uncolored_vec_set = vec_set - set(color_dict.keys())

        return assumption(vec_set, uncolored_vec_set, color_dict)

    # Otherwise, run this function again.
    return is_KS_colorable_set(vec_set, color_dict)

def assumption(vec_set, uncolored_vec_set, color_dict):
    """Return True if the set of all vectors (and those generated) from vec_set is KS colorable 
       or assumptions had to be made to continue the coloring process and False if we identify 
       a contradiction in the coloring.

       This is an extension of is_KS_colorable_set(...)
    """
    if uncolored_vec_set == set():
        print(f"Every vector in our original finite set of vectors has been colored: {color_dict}")
        return False
    else:
        first_uncolored_vec = uncolored_vec_set.pop()
        # You'll have to manually tell Python what assumption your want the first uncolored vector to take on.
        color_dict[first_uncolored_vec] = 0
        print(f"We'll assume that {first_uncolored_vec} is colored 0.")

        return is_KS_colorable_set(vec_set, color_dict)

# Miscellaneous functions for testing.
def pairwise_orthogonal(v, vec_set):   # v is a tuple and vec_set is a set of tuples (vectors)
    """Return True if the primitive, well-signed integer vector v is orthogonal to all other 
       vectors in the set vec_list and False otherwise.
    """
    for vec in vec_set:
        if v != vec and np.dot(v, vec) != 0: 
            print(f"The vector {v} and {vec} are not orthogonal, since their dot product is {np.dot(v, vec)}.")
            return False
    return True

def orthogonal_set(vec_set):
    """Return True if the set of primitive, well-signed integer vectors, vec_set, is an orthogonal 
       set and False otherwise.
    """
    for v in vec_set:
        if not(pairwise_orthogonal(v, vec_set)):
            return False
    return True
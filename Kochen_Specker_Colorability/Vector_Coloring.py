import numpy as np
from Primitive_Well_Signed_Vectors import *
from Sum_of_Squares_and_Divisibility import *
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
            # vec_set.update(sum_of_squares_solutions(n))
    return vec_set

def color_assignment(N):
    """Return True if all vectors (constructed) from primative_well_signed_solutions(N) has been designated 
       either a 1 or 0 and False if we identify a contradiction.
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
    vec_set = vectors_to_color(N)

    return identify_contradiction(vec_set, color_dict)

def identify_contradiction(vec_set, color_dict):
    """Return True if all vectors (and those generated) from vec_set has been designated either a 1 
       or 0 and False if we identify a contradiction.
    """
    for_loop_color_dict = copy.copy(color_dict) # Create a shallow copy of color_dict to ensure the for-loop remains consistent.

    for v in vec_set:
        for key_vec in for_loop_color_dict.keys():
            if np.dot(v, key_vec) == 0 and for_loop_color_dict[key_vec] == 1:
                if not(v in for_loop_color_dict.keys()):
                    color_dict[v] = 0
                elif for_loop_color_dict[v] != 0:
                    print(f"A contradiction has been identified from taking the dot product of {v} and {key_vec}.")
                    print(f"We colored the other vectors as follows: {color_dict}")
                    return False

            # print(f"The dot product of {v} and {key_vec} is {np.dot(v, key_vec)}!")

    # print("We'll now be considering the cross product of 2 black vectors!")

    new_for_loop_color_dict = copy.copy(color_dict) # Create a shallow copy of an updated color_dict to ensure the for-loop remains consistent.

    for key_vec_1 in new_for_loop_color_dict.keys():
        for key_vec_2 in new_for_loop_color_dict.keys():
            if new_for_loop_color_dict[key_vec_1] == 0 and new_for_loop_color_dict[key_vec_2] == 0 and np.dot (key_vec_1, key_vec_2) == 0:
                cross_product = np.cross(key_vec_1, key_vec_2)
                normalized_cp = cross_product / math.gcd(*cross_product)
                # new_vec = tuple(normalized_cp)
                new_vec = tuple(np.array(normalized_cp, dtype = int))
                if new_vec in color_dict.keys() and color_dict[new_vec] != 1:
                    print(f"A contradiction has been identified from coloring {new_vec}, the cross product of {key_vec_1} and {key_vec_2}.")
                    print(f"We colored the other vectors as follows: {color_dict}")
                    return False
                # elif primitive(new_vec) and well_signed(new_vec):
                else:
                    color_dict[new_vec] = 1

    if set(color_dict.keys()) - set(for_loop_color_dict.keys()) == set():
        # print("The vectors that were colored in our previous iteration are:")
        # print(for_loop_color_dict)

        # print("The vectors we just colored are:")
        # print(color_dict)

        print("The vectors we have left to color are:")
        print(vec_set - set(color_dict.keys()))
        uncolored_vec_set = vec_set - set(color_dict.keys())

        return assumption(vec_set, uncolored_vec_set, color_dict)

    return identify_contradiction(vec_set, color_dict)

def assumption(vec_set, uncolored_vec_set, color_dict):
    if uncolored_vec_set == set():
        print("Every element in our original finite set of vectors has been colored.")
        return False
    else:
        first_uncolored_vec = uncolored_vec_set.pop()
        color_dict[(1, 4, -1)] = 0
        print(f"Let's assume {first_uncolored_vec} is colored 0.")

        return identify_contradiction(vec_set, color_dict)

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
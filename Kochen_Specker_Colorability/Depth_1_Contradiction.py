from Sum_of_Squares_and_Divisibility import *
from Primitive_Well_Signed_Vectors import *
import numpy as np
import math
import copy

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

def identify_contradiction(N):
    """Return True if we identify a contradiction after at most 1 assumption and False otherwise.
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

    # This is the set of vectors we will color.
    vec_set = vectors_to_color(N)

    return identify_depth_1_assumption_contradiction(vec_set, color_dict)

def is_KS_colorable_set(vec_set, color_dict):
    """Return a dictionary whose entries are as follows:
       1. a boolean value where True indicates that either the set of vectors (and those generated) 
          from vec_set is KS colorable or assumptions must be made to continue the coloring process 
          and False if we identify a contradiction in the coloring
       2. an updated color dictionary.
    """
    for_loop_color_dict = copy.deepcopy(color_dict) # Create a deep copy of color_dict to ensure the for-loop runs w/o error.

    for v in vec_set:
        for key_vec in for_loop_color_dict.keys():
            if np.dot(v, key_vec) == 0 and for_loop_color_dict[key_vec] == 1:
                if not(v in for_loop_color_dict.keys()):
                    color_dict[v] = 0
                elif for_loop_color_dict[v] != 0:
                    print(f"A contradiction has been identified from coloring {v} after taking the dot product of {v} and {key_vec}.")
                    return {1: False, 2: color_dict}

    new_for_loop_color_dict = copy.deepcopy(color_dict) # Create a deep copy of an updated color_dict to ensure the for-loop runs w/o error.

    for key_vec_1 in new_for_loop_color_dict.keys():
        for key_vec_2 in new_for_loop_color_dict.keys():
            if new_for_loop_color_dict[key_vec_1] == 0 and new_for_loop_color_dict[key_vec_2] == 0 and np.dot (key_vec_1, key_vec_2) == 0:
                cross_product = np.cross(key_vec_1, key_vec_2)
                normalized_cp = cross_product / math.gcd(*cross_product)
                new_vec = tuple(np.array(normalized_cp, dtype = int))
                if new_vec in new_for_loop_color_dict.keys() and new_for_loop_color_dict[new_vec] != 1:
                    print(f"A contradiction has been identified from coloring {new_vec}, the cross product of {key_vec_1} and {key_vec_2}.")
                    return {1: False, 2: color_dict}
                elif well_signed(new_vec):
                # else: # Uncomment this line of code (and comment out the previous line) if you'd like to consider vectors that are not well-signed
                    color_dict[new_vec] = 1

    if set(color_dict.keys()) - set(for_loop_color_dict.keys()) == set():
        return {1: True, 2: color_dict}

    return is_KS_colorable_set(vec_set, color_dict)

def identify_depth_1_assumption_contradiction(vec_set, color_dict):
    """Return True if we identify a contradiction after at most 1 assumption and False otherwise.
    """
    no_assumption_return_dict = is_KS_colorable_set(vec_set, color_dict)
    updated_color_dict = no_assumption_return_dict[2]
    original_updated_color_dict = copy.deepcopy(no_assumption_return_dict[2])
    uncolored_vec_set = vec_set - set(updated_color_dict.keys())

    # If a contradiction was reached without making any assumptions, return True.
    if not(no_assumption_return_dict[1]):
        return True

    # Otherwise, we'll consider each uncolored vector in vec_set and run an updated color_dict
    # through is_KS_colorable_set(...) assuming each uncolored vector is assigned 0 and 1 separately
    elif uncolored_vec_set != set():
        print("We'll need need to make assumptions!")
        for v in uncolored_vec_set:
            # The following line of code will yield a lot of information in the terminal. Feel free to comment it out.
            print(f"We'll assume that {v} is colored 0 then 1.")
            
            # Let's assume v is colored 0.
            updated_color_dict[v] = 0

            assumption_0_return_dict = is_KS_colorable_set(vec_set, updated_color_dict)

            # We must revert the changes made to updated_color_dict.
            updated_color_dict = copy.deepcopy(original_updated_color_dict)
            assert updated_color_dict == original_updated_color_dict

            # Now, let's assume v is colored 1.
            updated_color_dict[v] = 1

            assumption_1_return_dict = is_KS_colorable_set(vec_set, updated_color_dict)

            # Again, we must revert the changes made to updated_color_dict.
            updated_color_dict = copy.deepcopy(original_updated_color_dict)
            assert updated_color_dict == original_updated_color_dict

            # If at any point both assumptions yield a contradiction, return True.
            if not(assumption_0_return_dict[1]) and not(assumption_1_return_dict[1]):
                return True

            # If at any point our assumptions yield a KS colorable set of vectors, print them.
            elif vec_set - set(assumption_0_return_dict[2].keys()) == set():
               print(f"Every vector in our original finite set of vectors has been colored by assuming {v} was colored 0: {assumption_0_return_dict[2]}")
            elif vec_set - set(assumption_1_return_dict[2].keys()) == set():
               print(f"Every vector in our original finite set of vectors has been colored by assuming {v} was colored 1: {assumption_1_return_dict[2]}")
        
        return False
    
    # If the set of vectors (and those generated) from vec_set is KS colorable, return False
    else:
        print(f"Every vector in our original finite set of vectors has been colored: {color_dict}")
        return False
import numpy as np
from Primitive_Well_Signed_Vectors import *
from Sum_of_Squares_and_Divisibility import *
import math

def 1_step_assumption(uncolored_vec_set, color_dict, depth):
    """Return...
    """
    if 

    
    if result_of_1st_coloring[1]:
        vec_set = copy.copy(result_of_1st_coloring[2])
        color_dict = copy.copy(result_of_1st_coloring[3])
        uncolored_vec_set = vec_set - set(color_dict.keys())
        for v in uncolored_vec_set:
            # print(f"The assumption we are making is on the vector {v}.")
            color_dict[v] = 0
            # print(f"The dictionary assuming 0 is {color_dict}.")
            result_of_2nd_coloring_0 = identify_contradiction(vec_set, color_dict)

            vec_set = copy.copy(result_of_1st_coloring[2])
            color_dict = copy.copy(result_of_1st_coloring[3])
            color_dict[v] = 1
            # print(f"The dictionary assuming 1 is {color_dict}.")
            result_of_2nd_coloring_1 = identify_contradiction(vec_set, color_dict)

            if not(result_of_2nd_coloring_0[1]) and not(result_of_2nd_coloring_1[1]):
                return True
            vec_set = copy.copy(result_of_1st_coloring[2])
            color_dict = copy.copy(result_of_1st_coloring[3])
            # print(f"Let's make sure the dictionary is reverted to the original dictionary: {color_dict}.")
            print("-----NEXT ITERATION-----")
        return False
    else:
        return True

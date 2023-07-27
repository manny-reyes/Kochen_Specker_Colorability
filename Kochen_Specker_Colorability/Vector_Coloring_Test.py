from Vector_Coloring import *

# This testing suite will primarily focus on tracing color_assignment(6**3):
vec_sol_for_6 = vectors_to_color(6**3)

# We'll first ensure that vector solutions to all divisors of 6**3 are contained in vec_sol_for_6:
v_3 = primitive_well_signed_solutions(3)
v_4 = primitive_well_signed_solutions(4)
v_6 = primitive_well_signed_solutions(6)
v_8 = primitive_well_signed_solutions(8)
v_9 = primitive_well_signed_solutions(9)
v_12 = primitive_well_signed_solutions(12)
v_18 = primitive_well_signed_solutions(18)
v_24 = primitive_well_signed_solutions(24)
v_27 = primitive_well_signed_solutions(27)
v_36 = primitive_well_signed_solutions(36)
v_54 = primitive_well_signed_solutions(54)
v_72 = primitive_well_signed_solutions(72)
v_108 = primitive_well_signed_solutions(108)
v_216 = primitive_well_signed_solutions(216)

vec_sol_list = [v_3, v_4, v_6, v_8, v_9, v_12, v_18, v_24, v_27, v_36, v_54, v_72, v_108, v_216]

def subset(A, B):
    """Return True if A is a subset of B and false otherwise.
    """
    for a in A:
        if not(a in B):
            return False
    return True

vec_sol_for_6_copy = copy.copy(vec_sol_for_6)

for vec_set in vec_sol_list:
    if subset(vec_set, vec_sol_for_6):
        vec_sol_for_6_copy -= vec_set
assert vec_sol_for_6_copy == set()
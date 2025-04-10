from Primitive_Well_Signed_Vectors import *

true_list_1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
true_list_2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1)]
true_list_3 = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]

true_list = true_list_1 + true_list_2 + true_list_3

false_list_1 = list(sum_of_squares_solutions(1) - set(true_list_1))
false_list_2 = list(sum_of_squares_solutions(2) - set(true_list_2))
false_list_3 = list(sum_of_squares_solutions(3) - set(true_list_3))

false_list = false_list_1 + false_list_2 + false_list_3

for true_v in true_list:
    assert well_signed(true_v)

for false_v in false_list:
    assert not(well_signed(false_v))
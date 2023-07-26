from Sum_of_Squares_and_Divisibility import *

# The entries of the dictonary are given as follows: {n : the sum of the divisors of n}, where
# n is a positive integer
sum_of_divisors = {1 : 1, 2 : 3, 4 : 7, 6 : 12, 16 : 31, 12 : 28, 64 : 127, 24 : 60}

for n in sum_of_divisors.keys():
    assert sum(factorization(n)) == sum_of_divisors[n]

# The entries of the dictonary are given as follows: {n : the number of divisors of n}, where
# n is a positive integer
num_of_divisors = {1 : 1, 2 : 2, 4 : 3, 6 : 4, 16 : 5, 12 : 6, 64 : 7, 24 : 8}

for n in num_of_divisors.keys():
    assert number_of_divisors(n) == num_of_divisors[n]

first_10_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
non_prime_list = [-1, 0, 0.5, 1]

for p in first_10_prime_list:
    assert is_prime(p)

for non_p in non_prime_list:
    assert not(is_prime(non_p))
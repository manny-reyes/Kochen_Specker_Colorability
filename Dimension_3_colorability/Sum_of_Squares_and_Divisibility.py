from sympy import diophantine
from sympy.abc import i, j, k
import copy
import math

def sum_of_squares_solutions(n):
    """Return a set of i, j, and k solutions to diophantine equations of the form i^2 + j^2 + k^2 = n, 
       where n is any nonnegative integer.
    """
    vec_sol = {(0, 0, 0)}
    if n != 0: # This is for nontrivial solutions.
        vec_sol = diophantine(i**2 + j**2 + k**2 - n, permute = True)
    return vec_sol

def factorization(N):
    """Given a positive integer, N, return a set of integers representing the factors of N.
    """
    divisors = {1, N}
    for d in range(2, N):
        if N % d == 0:
            divisors.add(d)
    return divisors

# Miscellaneous functions for testing.
def number_of_divisors(N):
    """Return the number of positive divisors that a positive integer, N, has.
    """
    init_val = N
    n = copy.copy(init_val)

    count_divisors = 1
    index = 2
    while index**2 <= init_val:
        power = 0
        while n % index == 0:
            n = n / index
            power += 1
        count_divisors *= (power + 1)
        index += 1
    
    if n > 1:
        count_divisors *= 2

    return count_divisors

def is_prime(n):
    """Return True if the positive integer n is prime and False otherwise.
    """
    if n > 1:
        # We only need to check up to the sqrt(n) – consider if n wasn't prime, i.e. it can be
        # expressed as n = a * b, and suppose a AND b were greater than sqrt(n)...
        for divisor in range(2, int(math.sqrt(n)) + 1):
            if n % divisor == 0:
                return False
        return True
    return False
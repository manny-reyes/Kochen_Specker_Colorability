import copy

def num_factors(N):
    init_val = N
    n = copy.copy(init_val)

    factors_counter = 1
    index = 2
    while index^2 <= init_val:
        power = 0
        while n % index == 0:
            n = n / index
            power += 1
        factors_counter *= (power + 1)
        index += 1
    
    if n > 1:
        factors_counter *= 2

    return factors_counter

def is_prime(n):
    if n > 1:
        for divisor in range(2, (n // 2) + 1):
            if n % divisor == 0:
                return False
        return True
    return False
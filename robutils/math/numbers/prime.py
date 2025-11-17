# mypackage/math/numbers/prime.py

"""Module for prime number related functions."""

def is_prime(n):
    """Checks if a positive integer is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_primes_up_to(limit):
    """Generates a list of prime numbers up to a given limit using a basic sieve."""
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes
# mypackage/math/numbers/fibonacci.py

"""Module for Fibonacci sequence-related calculations."""

def get_nth_fibonacci(n):
    """
    Calculates the n-th Fibonacci number (F_n).

    Args:
        n (int): The position in the sequence (n >= 0).

    Returns:
        int: The n-th Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def is_fibonacci(num):
    """
    Checks if a number is a Fibonacci number.
    A number N is Fibonacci if 5*N^2 + 4 or 5*N^2 - 4 is a perfect square.
    """
    def is_perfect_square(n):
        s = int(n**0.5)
        return s * s == n
    
    return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)
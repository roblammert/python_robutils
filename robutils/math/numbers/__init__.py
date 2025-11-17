# mypackage/math/numbers/__init__.py

from .fibonacci import get_nth_fibonacci, is_fibonacci
from .prime import is_prime, get_primes_up_to

# Define what happens during a 'from mypackage.math.numbers import *'
__all__ = [
    "get_nth_fibonacci",
    "is_fibonacci",
    "is_prime",
    "get_primes_up_to",
]
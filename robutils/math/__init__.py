"""Math utilities package for measurements, numbers, and containers."""

# Import subpackages for easy access
from . import measurements
from . import numbers
from . import containers

# Also expose the Hashtable class for convenience
from .containers import Hashtable

# Import all numbers functions at math level
from .numbers import (
    get_nth_fibonacci,
    is_fibonacci,
    is_prime,
    get_primes_up_to,
    is_integer,
    is_float,
    is_positive,
    is_non_negative,
    is_in_range,
    is_perfect_square,
    is_power_of_two,
    is_scientific_notation,
    is_currency,
    is_percentage,
    is_hexadecimal,
    is_binary,
    is_octal,
    is_roman_numeral,
    is_uuid,
    is_ipv4,
    is_ipv6,
    is_phone_number,
    is_isbn10,
    is_isbn13
)

# Import all measurements functions at math level
from .measurements import (
    convert_area,
    calculate_triangle_area,
    calculate_circle_area,
    convert_distance,
    convert_temperature,
    convert_volume,
    convert_weight,
    AREA_UNITS,
    DISTANCE_UNIT,
    TEMPERATURE_UNITS,
    VOLUME_UNITS,
    WEIGHT_UNIT
)

__all__ = [
    # subpackages
    'measurements',
    'numbers',
    'containers',
    # containers
    'Hashtable',
    # numbers - fibonacci
    'get_nth_fibonacci',
    'is_fibonacci',
    # numbers - prime
    'is_prime',
    'get_primes_up_to',
    # numbers - validate
    'is_integer',
    'is_float',
    'is_positive',
    'is_non_negative',
    'is_in_range',
    'is_perfect_square',
    'is_power_of_two',
    'is_scientific_notation',
    'is_currency',
    'is_percentage',
    'is_hexadecimal',
    'is_binary',
    'is_octal',
    'is_roman_numeral',
    'is_uuid',
    'is_ipv4',
    'is_ipv6',
    'is_phone_number',
    'is_isbn10',
    'is_isbn13',
    # measurements - area
    'convert_area',
    'calculate_triangle_area',
    'calculate_circle_area',
    'AREA_UNITS',
    # measurements - distance
    'convert_distance',
    'DISTANCE_UNIT',
    # measurements - temperature
    'convert_temperature',
    'TEMPERATURE_UNITS',
    # measurements - volume
    'convert_volume',
    'VOLUME_UNITS',
    # measurements - weight
    'convert_weight',
    'WEIGHT_UNIT'
]
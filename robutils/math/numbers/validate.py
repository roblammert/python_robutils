import math # Added for number theory checks
from typing import Union, Optional


def _to_number(value: Union[str, int, float]) -> Optional[Union[int, float]]:
    """
    Internal utility to safely convert input to int or float.
    Returns None if conversion fails.
    """
    if isinstance(value, (int, float)):
        return value

    if not isinstance(value, str):
        return None # Input is not a string, int, or float

    # Attempt to clean and convert string
    try:
        # Try integer conversion (handles inputs like "100")
        return int(value)
    except ValueError:
        try:
            # Then, try float conversion (handles inputs like "100.5" or "1e3")
            return float(value)
        except ValueError:
            return None


def is_integer(value: Union[str, int, float]) -> bool:
    """Checks if the input represents a valid integer."""
    num = _to_number(value)
    if num is None:
        return False
    # Check if the number is exactly equal to its integer representation
    # This handles floats that are conceptually integers (e.g., 5.0)
    return num == int(num)


def is_float(value: Union[str, int, float]) -> bool:
    """Checks if the input represents a valid floating-point number (or integer)."""
    num = _to_number(value)
    # Any successful conversion results in a valid number (int or float)
    return num is not None


def is_positive(value: Union[str, int, float]) -> bool:
    """Checks if the input is a positive number (> 0)."""
    num = _to_number(value)
    return num is not None and num > 0


def is_non_negative(value: Union[str, int, float]) -> bool:
    """Checks if the input is a non-negative number (>= 0)."""
    num = _to_number(value)
    return num is not None and num >= 0


def is_in_range(value: Union[str, int, float], min_val: Union[int, float], max_val: Union[int, float]) -> bool:
    """Checks if the number is within the inclusive range [min_val, max_val]."""
    num = _to_number(value)
    if num is None:
        return False
    return min_val <= num <= max_val


def is_prime(value: Union[str, int, float]) -> bool:
    """Checks if the input is a positive integer and a prime number (using trial division)."""
    num = _to_number(value)
    # Must be a positive integer
    if num is None or not is_integer(num) or num <= 1:
        return False

    n = int(num)

    # Handle small primes
    if n in (2, 3):
        return True
    # Optimization: Exclude multiples of 2 and 3
    if n % 2 == 0 or n % 3 == 0:
        return False

    # Check divisors up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def is_perfect_square(value: Union[str, int, float]) -> bool:
    """Checks if the input is a non-negative integer that is a perfect square."""
    num = _to_number(value)
    if num is None or not is_non_negative(num) or not is_integer(num):
        return False

    # Calculate the integer square root
    root = int(math.sqrt(num))
    # Check if the square of the root equals the number
    return root * root == num


def is_power_of_two(value: Union[str, int, float]) -> bool:
    """Checks if the input is a positive integer that is a power of two (e.g., 1, 2, 4, 8...)."""
    num = _to_number(value)
    if num is None or not is_positive(num) or not is_integer(num):
        return False
    
    n = int(num)
    # Use bitwise operation: A power of two has only one bit set.
    return (n & (n - 1)) == 0


def is_scientific_notation(value: str) -> bool:
    """Checks if a string represents a number in scientific/E notation (e.g., '1.2e+3', '1E6')."""
    import re
    if not isinstance(value, str):
        return False
    
    # Regex: optional sign, digits, optional decimal part, mandatory 'e' or 'E', optional sign, digits
    sci_pattern = r'^[+-]?\d+(\.\d*)?([eE][+-]?\d+)?$'
    # Ensure it matches the pattern AND can be converted to a number
    return bool(re.match(sci_pattern, value)) and _to_number(value) is not None


def is_currency(value: str, allow_symbol: bool = True) -> bool:
    """
    Validates if a string represents a standard currency format (e.g., 1,000.50 or $10.00).
    """
    import re
    if not isinstance(value, str):
        return False

    # Pre-clean: Remove common currency symbols and optional spaces
    clean_value = value.strip()
    if allow_symbol:
        # Regex to find optional currency symbol at the start or end
        currency_pattern = r'^\s*[\$£€¥]?\s*(.*?)\s*[\$£€¥]?\s*$'
        match = re.match(currency_pattern, clean_value)
        if match:
            clean_value = match.group(1)

    try:
        # Remove all commas and try to convert to float. This handles the numeric part validity.
        num_str = clean_value.replace(',', '')
        float(num_str)
        return True
    except ValueError:
        return False


def is_percentage(value: Union[str, int, float], allow_symbol: bool = True) -> bool:
    """
    Checks if the input is a valid number, optionally followed by a '%' symbol.
    """
    if isinstance(value, str) and allow_symbol:
        # Remove the percentage symbol if present
        cleaned_value = value.strip().rstrip('%').strip()
    else:
        cleaned_value = value

    num = _to_number(cleaned_value)
    return num is not None


def is_hexadecimal(value: str) -> bool:
    """Checks if a string is a valid hexadecimal number (e.g., '1A3F', '0xAF4B')."""
    import re
    if not isinstance(value, str) or not value:
        return False
    # Optional '0x' or '0X' prefix, followed by one or more hex digits
    hex_pattern = r'^(?:0x|0X)?[0-9a-fA-F]+$'
    return bool(re.match(hex_pattern, value))


def is_binary(value: str) -> bool:
    """Checks if a string is a valid binary number (0s and 1s, optionally prefixed with '0b')."""
    import re
    if not isinstance(value, str) or not value:
        return False
    # Optional '0b' or '0B' prefix, followed by one or more 0/1 digits
    binary_pattern = r'^(?:0b|0B)?[01]+$'
    return bool(re.match(binary_pattern, value))


def is_octal(value: str) -> bool:
    """Checks if a string is a valid octal number (digits 0-7, optionally prefixed with '0o')."""
    import re
    if not isinstance(value, str) or not value:
        return False
    # Optional '0o' or '0O' prefix, followed by one or more 0-7 digits
    octal_pattern = r'^(?:0o|0O)?[0-7]+$'
    return bool(re.match(octal_pattern, value))


def is_roman_numeral(value: str) -> bool:
    """Checks if a string is a valid Roman numeral (I through MMMCMXCIX, 1 to 3999)."""
    import re
    if not isinstance(value, str):
        return False
    # Regex for Roman numerals 1 to 3999 (case-insensitive check)
    roman_pattern = r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    return bool(re.match(roman_pattern, value.upper().strip()))


def is_uuid(value: str) -> bool:
    """Checks if a string is a valid UUID (Universally Unique Identifier)."""
    import uuid
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def is_ipv4(value: str) -> bool:
    """Checks if a string is a valid IPv4 address."""
    import ipaddress
    if not isinstance(value, str):
        return False
    try:
        ipaddress.IPv4Address(value)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def is_ipv6(value: str) -> bool:
    """Checks if a string is a valid IPv6 address."""
    import ipaddress
    if not isinstance(value, str):
        return False
    try:
        ipaddress.IPv6Address(value)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def is_phone_number(value: str) -> bool:
    """
    Checks if a string looks like a basic international phone number.
    """
    import re
    if not isinstance(value, str):
        return False
    # Allows optional '+' at start, optional grouping/separators (parentheses, spaces, hyphens, dots).
    # Requires at least 7 digits total.
    phone_pattern = r'^\+?\s*(\(\d{1,3}\))?\s*[\d\s\-\.]{7,}$'
    return bool(re.match(phone_pattern, value.strip()))


def is_isbn10(value: str) -> bool:
    """Checks if a string is a valid ISBN-10 with correct checksum."""
    import re
    if not isinstance(value, str): return False
    isbn = re.sub(r'[\s\-]', '', value).upper()
    if len(isbn) != 10: return False

    checksum = 0
    for i in range(9):
        if not isbn[i].isdigit(): return False
        checksum += int(isbn[i]) * (10 - i)

    last_char = isbn[9]
    if last_char.isdigit():
        checksum += int(last_char) * 1
    elif last_char == 'X':
        checksum += 10 * 1
    else:
        return False

    return checksum % 11 == 0


def is_isbn13(value: str) -> bool:
    """Checks if a string is a valid ISBN-13 with correct checksum."""
    import re
    if not isinstance(value, str): return False
    isbn = re.sub(r'[\s\-]', '', value)
    if len(isbn) != 13 or not isbn.isdigit(): return False

    checksum = 0
    # Weights: 1, 3, 1, 3, 1, 3, ...
    for i in range(12):
        digit = int(isbn[i])
        weight = 1 if (i + 1) % 2 != 0 else 3
        checksum += digit * weight

    last_digit = int(isbn[12])
    total = checksum + last_digit
    return total % 10 == 0


import re
import ipaddress
import uuid
from typing import Optional, List, Union, Set

# --- 1. Presence/Null/Empty Checks ---

def is_not_none(text: Optional[str]) -> bool:
    """Ensures the string is not None (i.e., present)."""
    return text is not None

def is_not_empty(text: Optional[str]) -> bool:
    """Ensures the string is not None and has a length greater than zero (not "")."""
    return text is not None and len(text) > 0

def is_not_whitespace_only(text: Optional[str]) -> bool:
    """Ensures the string is not None and is not composed solely of whitespace characters."""
    return text is not None and text.strip() != ""

# --- 2. Length Constraints ---

def has_min_length(text: str, min_len: int) -> bool:
    """Ensures the string meets a minimum length requirement (inclusive)."""
    if not isinstance(text, str) or min_len < 0:
        return False
    return len(text) >= min_len

def has_max_length(text: str, max_len: int) -> bool:
    """Ensures the string does not exceed a maximum length requirement (inclusive)."""
    if not isinstance(text, str) or max_len < 0:
        return False
    return len(text) <= max_len

def has_length_in_range(text: str, min_len: int, max_len: int) -> bool:
    """Ensures the string's length falls within a specified range (inclusive)."""
    if not isinstance(text, str) or min_len < 0 or max_len < min_len:
        return False
    length = len(text)
    return min_len <= length <= max_len

# --- 3. Content Restrictions ---

def contains_only_allowed_chars(text: str, allowed_chars: Union[str, Set[str]]) -> bool:
    """
    Ensures the string only contains characters from a permitted set.
    
    :param allowed_chars: A string or set of allowed characters.
    """
    if not isinstance(text, str):
        return False
    
    allowed_set = set(allowed_chars) if isinstance(allowed_chars, str) else allowed_chars
    return all(c in allowed_set for c in text)

def contains_no_disallowed_chars(text: str, disallowed_chars: Union[str, Set[str]]) -> bool:
    """
    Ensures the string does not contain characters from a forbidden set.
    
    :param disallowed_chars: A string or set of forbidden characters.
    """
    if not isinstance(text, str):
        return False
    
    disallowed_set = set(disallowed_chars) if isinstance(disallowed_chars, str) else disallowed_chars
    return all(c not in disallowed_set for c in text)

def is_in_allowed_list(text: str, allowed_values: List[str]) -> bool:
    """Checks if the string is present in a predefined list of allowed values (case-sensitive)."""
    if not isinstance(text, str):
        return False
    return text in allowed_values

def is_not_in_forbidden_list(text: str, forbidden_values: List[str]) -> bool:
    """Checks if the string is NOT present in a predefined list of forbidden values (case-sensitive)."""
    if not isinstance(text, str):
        return False
    return text not in forbidden_values

# --- 4. Core Validation Functions (Original) ---

def is_valid_email(email: str) -> bool:
    """
    Validates if the provided string is a basic, common email format.
    Covers the vast majority of real-world emails.
    """
    if not isinstance(email, str):
        return False
    # Extended pattern allowing for longer TLDs and common subdomain structures
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$"
    return re.match(email_regex, email) is not None

def is_valid_phone_e164(phone: str) -> bool:
    """
    Validates if the string conforms to the E.164 standard for international
    phone numbers, which includes country code and allows 7 to 15 digits.
    Format: +[country code][number].
    """
    if not isinstance(phone, str):
        return False
    cleaned_phone = re.sub(r'[^\d\+]', '', phone)
    e1164_regex = r"^\+\d{7,15}$"
    return re.match(e1164_regex, cleaned_phone) is not None

def is_alphanumeric_or_spaces(text: str) -> bool:
    """Checks if a string contains only letters, numbers, and spaces."""
    if not isinstance(text, str):
        return False
    return bool(re.fullmatch(r"[\w\s]+", text))

# --- 5. Advanced Structured Data Validation (Original) ---

def is_valid_ip_address(ip_string: str) -> bool:
    """
    Validates if a string is a valid IPv4 or IPv6 address.
    Uses the standard library 'ipaddress' module for reliability.
    """
    if not isinstance(ip_string, str):
        return False
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def is_valid_uuid(uuid_str: str, version: Optional[int] = None) -> bool:
    """
    Validates if a string is a well-formed UUID (version 1-5).
    """
    if not isinstance(uuid_str, str):
        return False
    try:
        val = uuid.UUID(uuid_str)
        if version is not None and val.version != version:
            return False
        # Check if the generated string representation matches the input (canonical form)
        return str(val) == uuid_str.lower()
    except ValueError:
        return False

def is_valid_url(url: str) -> bool:
    """
    Validates a string as a basic, non-local HTTP/HTTPS URL.
    Checks for scheme (http/https), domain, and a path/query structure.
    """
    if not isinstance(url, str):
        return False
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(url_regex, url) is not None

# --- 6. Formatting & Transformation Functions (Original) ---

def normalize_whitespace(text: str) -> str:
    """Replaces all sequences of whitespace with a single space and strips leading/trailing space."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# --- 7. Sanitization Functions (Original) ---

def sanitize_for_url(text: str, separator: str = '-') -> str:
    """
    Sanitizes a string for use in a URL slug (kebab-case-like).
    Removes special characters and replaces separators with the defined separator.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', separator, text)

    return text.strip(separator)

def remove_html_tags(text: str) -> str:
    """Removes basic HTML tags from a string using regex."""
    if not isinstance(text, str):
        return ""
    return re.sub(r'<[^>]+>', '', text)

# --- Example Usage (Demonstrates all features) ---
if __name__ == '__main__':
    print("--- Advanced Text Utility Module Usage Examples ---")

    # 1. Presence Checks
    print("\n## 1. Presence Checks")
    test_str = "   "
    print(f"is_not_none(None): {is_not_none(None)}")
    print(f"is_not_empty(''): {is_not_empty('')}")
    print(f"is_not_whitespace_only('{test_str}'): {is_not_whitespace_only(test_str)}")
    print(f"is_not_whitespace_only('Hello'): {is_not_whitespace_only('Hello')}")

    # 2. Length Constraints
    print("\n## 2. Length Constraints")
    test_len_str = "Python" # Length 6
    print(f"has_min_length('{test_len_str}', 5): {has_min_length(test_len_str, 5)}")
    print(f"has_max_length('{test_len_str}', 5): {has_max_length(test_len_str, 5)}")
    print(f"has_length_in_range('{test_len_str}', 4, 8): {has_length_in_range(test_len_str, 4, 8)}")

    # 3. Content Restrictions
    print("\n## 3. Content Restrictions")
    test_content = "user123"
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789"
    disallowed = "!@#$%^&"
    allowed_list = ["admin", "guest", "editor"]
    
    print(f"contains_only_allowed_chars('{test_content}', alphanumeric): {contains_only_allowed_chars(test_content, allowed)}")
    print(f"contains_no_disallowed_chars('{test_content}', special chars): {contains_no_disallowed_chars(test_content, disallowed)}")
    print(f"is_in_allowed_list('admin'): {is_in_allowed_list('admin', allowed_list)}")
    print(f"is_not_in_forbidden_list('root'): {is_not_in_forbidden_list('root', ['root', 'administrator'])}")

    # 4. Core Validation
    print("\n## 4. Core Validation")
    print(f"Valid Email: {is_valid_email('user.name@company.co.uk')}")
    print(f"Valid E.164 Phone: {is_valid_phone_e164('+16505550123')}")

    # 5. Advanced Structured Validation
    print("\n## 5. Advanced Structured Validation")
    test_uuid_v4 = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    print(f"Valid UUID v4: {is_valid_uuid(test_uuid_v4, version=4)}")
    print(f"Valid IPv6: {is_valid_ip_address('2001:db8::1')}")
    print(f"Valid URL: {is_valid_url('https://www.google.com/search')}")

    # 6. Formatting & Sanitization
    print("\n## 6. Formatting & Sanitization")
    print(f"sanitize_for_url('100% Fun & Games'): {sanitize_for_url('100% Fun & Games')}")
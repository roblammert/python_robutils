# mypackage/text/manipulate.py

"""Module for various text manipulation utilities."""

def reverse_string(text):
    """Reverses the order of characters in a string."""
    return text[::-1]

def slugify(text, separator='-'):
    """Converts a string into a URL-friendly slug."""
    import re
    # Convert to lowercase
    text = text.lower()
    # Replace non-alphanumeric characters with the separator
    text = re.sub(r'[^a-z0-9\s-]', '', text).strip()
    # Collapse consecutive separators
    text = re.sub(r'[-\s]+', separator, text)
    return text

def truncate(text, max_length, suffix='...'):
    """Truncates a string after max_length and adds a suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
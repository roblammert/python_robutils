# mypackage/text/manipulate.py

"""Module for various text manipulation utilities."""

def reverse_string(text: str):
    """Reverses the order of characters in a string."""
    return text[::-1]

def slugify(text: str, separator='-'):
    """Converts a string into a URL-friendly slug."""
    import re
    # Convert to lowercase
    text = text.lower()
    # Replace non-alphanumeric characters with the separator
    text = re.sub(r'[^a-z0-9\s-]', '', text).strip()
    # Collapse consecutive separators
    text = re.sub(r'[-\s]+', separator, text)
    return text

def truncate(text: str, max_length, suffix='...'):
    """Truncates a string after max_length and adds a suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def to_upper(text: str):
    """Convert text to uppercase."""
    return text.upper()

def to_lower(text: str):
    """Convert text to lowercase."""
    return text.lower()

def capitalize_first(text: str):
    """Capitalize the first character of the text."""
    return text.capitalize()

def replace_substring(text: str, old: str, new: str):
    """Replace occurrences of a substring with a new substring."""
    return text.replace(old, new)

def split(text: str, delimiter=None):
    """Split the text into a list of substrings based on a delimiter."""
    return text.split(delimiter)

def join(text: str, iterable):
    """Join an iterable of strings into a single string with the text as the delimiter."""
    return text.join(iterable)

def strip(text: str):
    """Strip leading and trailing whitespace from the text."""
    return text.strip()

def to_title_case(text: str):
    """Capitalizes the first letter of every word based off of built-in title() method"""
    return text.title()

def to_snake_case(text: str):
    """Converts text (e.g., 'CamelCase', 'kebab-case', 'Sentence') to snake_case."""
    import re
    # 1. Replace all non-alphanumeric/underscore to space
    temp_text = re.sub(r'[^\w\s]', ' ', text)
    # 2. Convert CamelCase to snake_case (e.g. 'AString' -> 'A String')
    temp_text2 = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', temp_text)
    # 3. Replace all whitepace and hyphens with a single underscore
    temp_text3 = re.sub(r'[\s-]+', '_', temp_text2).lower()
    return temp_text3

def to_camel_case(text: str, upper: bool = False):
    """
    Converts text (e.g., 'snake_case', 'kebab-case', 'Sentence') to camelCase
    
    Args:
        text (str): Text to manipulate.
        upper (bool): If True, converts to PascalCase (e.g., 'HelloWorld').
                      If False, (default), converts to camelCase (e.g., 'helloWorld').
    """
    import re
    
    # 1. Convert any separators (hyphens, underscores) to spaces
    temp_text = re.sub(r'[_\-\s]+', ' ', text.strip())
    # 2. Capitalize the first letter of every word
    capitalized_text = temp_text.title()
    # 3. Remove all spaces to join the words
    joined_text = capitalized_text.replace(' ', '')
    # 4. Apply lower/upper camel case rule
    if upper:
        #PascalCase (Upper Camel Case): First letter is capitalized
        return joined_text
    else:
        # camelCase (Lower Camel Case): First letter is lowercased
        # 'HelloWorld' -> 'helloWorld'
        if joined_text:
            return joined_text[0].lower() + joined_text[1:]
        else:
            return '' # handle empty input gracefully
        
def to_pascal_case(text: str):
    return to_camel_case(text,True)

def to_kebab_case(text: str):
    """Converts text to kebab-case (e.g., 'hello-world')."""
    import re
    # 1. Insert space before captial letters (for CamelCase)
    temp_text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    # 2. Replace all non-alphanumeric/underscore to space
    temp_text2 = re.sub(r'[^\w\s]', ' ', temp_text)
    # 3. Replace any sequence of separators/spaces with a single space
    temp_text3 = re.sub(r'[\s-]+', ' ', temp_text2).strip()
    # 4. Replace any space with hyphen and lowercase all letters
    return temp_text3.replace(' ', '-').lower()

def to_sentence_case(text: str):
    """
    Converts text to sentence case (e.g., 'Hello world.').
    Makes the first letter uppercase and the rest lowercase.
    """
    if not text:
        return text
    
    # 1. Convert everything to lowercase first
    lower_text = text.lower()
    
    # 2. Capitalize the first letter
    return lower_text[0].upper() + lower_text[1:]

def strip_whitespace(text: str):
    """
    Removes leading and trailing whitespace, including spaces, newlines, and tabs.
    """
    return text.strip()

def remove_extra_spaces(text: str):
    """
    Replaces all sequences of whitespace (multiple spaces, newlines, tabs) with a single space.
    """
    import re
    clean = re.sub(r'\s+', ' ', text).strip()
    return clean

def remove_punctuation(text: str):
    """
    Removes all standard punctuation marks (.,!?- etc.) from the text.
    """
    import string
    translator = str.maketrans('','', string.punctuation)
    clean = text.translate(translator)
    return clean

def clean(text: str, to_lower: bool = False, remove_punct: bool = True):
    """
    Performs a sequence of common cleaning operations.
    
    Args:
        text (str): Text to manipulate.
        to_lower (bool): If True, converts the entire text to lowercase.
        remove_punct (bool): If True, removes all punctuation.
    """
    # 1. Strip leading/trailing whitespace
    text = strip_whitespace(text)
    
    # 2. Remove extra spaces within the text
    text = remove_extra_spaces(text)
    
    # 3. Remove punctuation
    if remove_punct:
        text = remove_punct(text)
        
    # 4. Convert to lowercase
    if to_lower:
        text = text.lower()
        
    return text

def pad(text: str, length: int, fillchar: str = ' ', direction: str = 'right'):
    """
    Pads the text to the specified length with a fill character.
    Used in fixed-width file formats or log outputs.
    
    Args:
        text (str): Text to manipulate.
        length (int): The final desired length of the string.
        fillchar (str): The character to use for padding.
        direction (str): 'left, 'right', or 'center'
    """
    
    if direction == 'left':
        text = text.rjust(length, fillchar)
    elif direction == 'center':
        text = text.center(length, fillchar)
    else: # Default is 'right'
        text = text.ljust(length, fillchar)
        
    return text

def url_encode(text: str):
    """
    URL-encodes the text, replacing reserved and unsafe characters
    (like spaces) with %xx hexadecimal codes.
    """
    from urllib.parse import quote_plus
    text = quote_plus(text)
    return text

def url_decode(text: str):
    """
    URL-decodes the text.
    """
    from urllib.parse import unquote_plus
    text - unquote_plus(text)
    return text



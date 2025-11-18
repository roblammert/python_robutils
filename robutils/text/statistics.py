# mypackage/text/statistics.py

"""Module for calculating statistical properties of text."""

def word_count(text: str):
    """Count the number of words in the text."""
    return len(text.split())

def words(text: str):
    """Return a list of words in the text."""
    return text.split()

def char_count(text: str):
    """Count the number of characters in the text."""
    return len(text)

def is_palindrome(text: str):
    """Check if the text is a palindrome."""
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

def sentence_count(text: str):
    """Count the number of sentences in the text."""
    import re
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def sentence_list(text: str):
    """Return a list of sentences in the text."""
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

def paragraph_count(text: str):
    """Count the number of paragraphs in the text."""
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def paragraphs(text: str):
    """Return a list of paragraphs in the text."""
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

def is_empty(text: str):
    """Check if the text is empty."""
    return len(text) == 0

def byte_length(text: str):
    """Get the byte length of the text."""
    return len(text.encode('utf-8'))

def average_word_length(text: str):
    """Calculates the average length of words in the text."""
    words = text.split()
    if not words:
        return 0.0
    
    # Strip common punctuation before calculating length
    lengths = [len(w.strip('.,!?"\'')) for w in words]
    return sum(lengths) / len(lengths)

def character_count(text: str, include_spaces=True):
    """Counts the total number of characters."""
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', ''))
    
def starts_with(text: str, prefix: str):
    """Check if the text starts with a given prefix."""
    return text.startswith(prefix)

def ends_with(text: str, suffix: str):
    """Check if the text ends with a given suffix."""
    return text.endswith(suffix)

def contains_only(text: str, chars):
    """Check if the text contains only the specified characters."""
    return all(c in chars for c in text)

def count_substring(text: str, substring: str):
    """Count occurrences of a substring in the text."""
    return text.count(substring)
    
def word_frequency(text) -> list[str]:
    """Return a dictionary with word frequency counts."""
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


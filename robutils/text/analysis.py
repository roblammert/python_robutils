# mypackage/text/analysis.py

"""Module for basic text analysis functions."""

def count_words(text):
    """Returns the number of words in a string."""
    words = text.split()
    return len(words)

def get_unique_words(text):
    """Returns a set of unique words in the string (case-insensitive)."""
    words = text.lower().split()
    # Filter out common punctuation if necessary
    return set(w.strip('.,!?"\'') for w in words if w)

def get_word_frequency(text):
    """Returns a dictionary with word counts."""
    from collections import Counter
    words = text.lower().split()
    return Counter(w.strip('.,!?"\'') for w in words if w)
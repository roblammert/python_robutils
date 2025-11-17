# mypackage/text/statistics.py

"""Module for calculating statistical properties of text."""

def average_word_length(text):
    """Calculates the average length of words in the text."""
    words = text.split()
    if not words:
        return 0.0
    
    # Strip common punctuation before calculating length
    lengths = [len(w.strip('.,!?"\'')) for w in words]
    return sum(lengths) / len(lengths)

def character_count(text, include_spaces=True):
    """Counts the total number of characters."""
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', ''))
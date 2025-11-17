# mypackage/text/__init__.py

from .markdown import bold, italic, heading, link
from .analysis import count_words, get_unique_words, get_word_frequency
from .statistics import average_word_length, character_count
from .manipulate import reverse_string, slugify, truncate

# Define what happens during a 'from mypackage.text import *'
__all__ = [
    "bold",
    "italic",
    "heading",
    "link",
    "count_words",
    "get_unique_words",
    "get_word_frequency",
    "average_word_length",
    "character_count",
    "reverse_string",
    "slugify",
    "truncate",
]
# mypackage/text/markdown.py

"""Module for generating common Markdown elements."""

def bold(text):
    """Returns the text enclosed in Markdown bold syntax."""
    return f"**{text}**"

def italic(text):
    """Returns the text enclosed in Markdown italic syntax."""
    return f"*{text}*"

def heading(text, level=1):
    """Returns the text formatted as a Markdown heading."""
    if 1 <= level <= 6:
        prefix = "#" * level
        return f"{prefix} {text}"
    else:
        raise ValueError("Heading level must be between 1 and 6.")

def link(text, url):
    """Returns a Markdown link."""
    return f"[{text}]({url})"
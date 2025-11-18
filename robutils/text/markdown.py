# mypackage/text/markdown.py

"""Module for generating common Markdown elements."""

def bold(text: str):
    """Returns the text enclosed in Markdown bold syntax."""
    return f"**{text}**"

def italic(text: str):
    """Returns the text enclosed in Markdown italic syntax."""
    return f"*{text}*"

def heading(text: str, level: int = 1):
    """Returns the text formatted as a Markdown heading."""
    if 1 <= level <= 6:
        prefix = "#" * level
        return f"{prefix} {text}"
    else:
        raise ValueError("Heading level must be between 1 and 6.")

def link(text: str, url: str):
    """Returns a Markdown link."""
    return f"[{text}]({url})"

def to_plain_text(text: str):
    """Convert markdown text to plain text."""
    # Remove markdown syntax for a simple plain text conversion
    import re
    text1 = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
    text2 = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text1)    # Convert links to text
    text3 = re.sub(r'[#>*_`~\-]', '', text2)             # Remove other markdown chars
    return text3.strip()

def heading_count(text: str, min: int = 1, max: int = 6):
    """Count the number of headings in the markdown text."""
    import re
    return len(re.findall(r'^(#{'+min+','+max+'})\s', text, re.MULTILINE))

def bold_count(text: str):
    """Count the number of bold text occurrences in the markdown text."""
    import re
    return len(re.findall(r'\*\*(.*?)\*\*', text))

def italic_count(text: str):
    """Count the number of italic text occurrences in the markdown text."""
    import re
    return len(re.findall(r'\*(.*?)\*', text))

def link_count(text: str):
    """Count the number of links in the markdown text."""
    import re
    return len(re.findall(r'\[(.*?)\]\((.*?)\)', text))

def list_count(text: str):
    """Count the number of list items in the markdown text."""
    import re
    return len(re.findall(r'^\s*[-*+]\s', text, re.MULTILINE))

def code_block_count(text: str):
    """Count the number of code blocks in the markdown text."""
    import re
    return len(re.findall(r'```(.*?)```', text, re.DOTALL))

def inline_code_count(text: str):
    """Count the number of inline code occurrences in the markdown text."""
    import re
    return len(re.findall(r'`(.*?)`', text))

def image_count(text: str):  
    """Count the number of images in the markdown text."""
    import re
    return len(re.findall(r'!\[(.*?)\]\((.*?)\)', text))  


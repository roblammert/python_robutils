# mypackage/text/markdown.py

"""Module for generating common Markdown elements."""

import re
from typing import List, Dict, Any, Optional

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
    text1 = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
    text2 = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text1)    # Convert links to text
    text3 = re.sub(r'[#>*_`~\-]', '', text2)             # Remove other markdown chars
    return text3.strip()

def heading_count(text: str, min: int = 1, max: int = 6):
    """Count the number of headings in the markdown text."""
    return len(re.findall(r'^(#{'+min+','+max+'})\s', text, re.MULTILINE))

def bold_count(text: str):
    """Count the number of bold text occurrences in the markdown text."""
    return len(re.findall(r'\*\*(.*?)\*\*', text))

def italic_count(text: str):
    """Count the number of italic text occurrences in the markdown text."""
    return len(re.findall(r'\*(.*?)\*', text))

def link_count(text: str):
    """Count the number of links in the markdown text."""
    return len(re.findall(r'\[(.*?)\]\((.*?)\)', text))

def list_count(text: str):
    """Count the number of list items in the markdown text."""
    return len(re.findall(r'^\s*[-*+]\s', text, re.MULTILINE))

def code_block_count(text: str):
    """Count the number of code blocks in the markdown text."""
    return len(re.findall(r'```(.*?)```', text, re.DOTALL))

def inline_code_count(text: str):
    """Count the number of inline code occurrences in the markdown text."""
    return len(re.findall(r'`(.*?)`', text))

def image_count(text: str):  
    """Count the number of images in the markdown text."""
    return len(re.findall(r'!\[(.*?)\]\((.*?)\)', text))  

def parse_markdown_table(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Parses a standard GitHub-flavored Markdown table string into a list of 
    dictionaries.

    It handles tables with or without the leading/trailing pipe characters on 
    each row. It skips the mandatory separator line (---|---).

    Args:
        markdown_text: A string containing the Markdown table.

    Returns:
        A list of dictionaries, where each dict is a row and keys are 
        column headers. Returns an empty list if the input is not a valid 
        multi-line table.
    """
    lines = markdown_text.strip().split('\n')

    # Need at least a header and a separator line
    if len(lines) < 2:
        return []

    # 1. Extract and clean the Header Row
    header_line = lines[0].strip()
    # Remove surrounding pipes and split
    if header_line.startswith('|') and header_line.endswith('|'):
        header_line = header_line[1:-1]
    
    headers = [h.strip() for h in header_line.split('|')]
    
    # 2. Skip the Separator Line (lines[1])
    
    # 3. Process Data Rows (lines[2] onwards)
    data = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue

        # Clean the row: remove outer pipes if present
        if line.startswith('|') and line.endswith('|'):
            line = line[1:-1]
        
        # Split by pipe. 
        cells = [c.strip() for c in line.split('|')]

        # Ensure the number of cells matches the number of headers
        if len(cells) == len(headers):
            row_dict = dict(zip(headers, cells))
            data.append(row_dict)
        else:
            # Optional: Log a warning about a row with mismatched columns
            print(f"Warning: Skipping row with {len(cells)} cells, expected {len(headers)}: {line}")
            
    return data


def generate_markdown_table(
    data: List[Dict[str, Any]], 
    alignment: Optional[Dict[str, str]] = None
) -> str:
    """
    Generates a Markdown table string from a list of dictionaries, with 
    optional column alignment control. 
    
    It automatically calculates column widths for clean alignment.

    Args:
        data: A list of dictionaries, where each dict is a row.
        alignment: An optional dictionary mapping header names to alignment 
                   strings ('left', 'center', or 'right'). Defaults to 'left'.

    Returns:
        A multiline string representing the Markdown table.
    """
    if not data:
        return ""

    if alignment is None:
        alignment = {}

    # Define alignment symbols for the separator line
    ALIGNMENT_SYMBOLS = {
        'left': ':',
        'center': ':',
        'right': ':'
    }

    # 1. Get all unique headers (column names)
    headers = list(data[0].keys())

    # 2. Calculate the maximum content width for each column
    column_widths = {}
    for header in headers:
        # Start with the header's length as the minimum width
        max_width = len(header)
        
        # Check the width of all data values in that column
        for row in data:
            value_str = str(row.get(header, ''))
            max_width = max(max_width, len(value_str))
            
        # The separator requires 3 hyphens minimum, so adjust max_width if needed
        column_widths[header] = max(3, max_width)

    # 3. Build the Markdown string
    markdown_lines = []

    # A. Header Row: | Header 1 | Header 2 | ... |
    header_cells = []
    for header in headers:
        width = column_widths[header]
        # Left-align the header text and pad it to the calculated width
        header_cells.append(f" {header:<{width}} ") 
    markdown_lines.append("|" + "|".join(header_cells) + "|")

    # B. Separator Row: |:---|:---:|---:|
    separator_cells = []
    for header in headers:
        # Determine alignment (default to 'left')
        align_type = alignment.get(header, 'left').lower()
        width = column_widths[header]
        
        # Calculate the required number of hyphens
        # The total separator string width is 'width' + 2 spaces from the header row, 
        # but we only need to match the 'width' of the content part.
        
        if align_type == 'center':
            # Example: :------: (width + 2 colons)
            hyphens_count = width
            separator_cell = f":{'-' * hyphens_count}:"
        elif align_type == 'right':
            # Example: ------: (width + 1 colon)
            hyphens_count = width + 1
            separator_cell = f"{'-' * hyphens_count}:"
        else: # 'left' or any other value
            # Example: :------ (width + 1 colon)
            hyphens_count = width + 1
            separator_cell = f":{'-' * hyphens_count}"
        
        # We need to pad the separator cell to match the total visual width 
        # of the column for perfect visual alignment (optional, but clean)
        # Note: The separator is padded with spaces to match the header/data length
        separator_cells.append(f" {separator_cell:<{width}} ")

    # We need to simplify the separator logic to match standard Markdown alignment rules
    # and just use the minimal symbols, which is much safer for compatibility.

    separator_cells = []
    for header in headers:
        align_type = alignment.get(header, 'left').lower()
        min_hyphens = column_widths[header] # Already min 3
        
        # Generate the separator string based on alignment
        if align_type == 'center':
            sep = f":{'-' * min_hyphens}:"
        elif align_type == 'right':
            sep = f"{'-' * (min_hyphens + 1)}:"
        else: # 'left' or default
            sep = f":{'-' * (min_hyphens + 1)}"

        # The separator itself is padded to match the header/data cell padding
        separator_cells.append(f" {sep:<{column_widths[header]}} ")
        
    markdown_lines.append("|" + "|".join(separator_cells) + "|")
    
    # C. Data Rows: | Data 1 | Data 2 | ... |
    for row in data:
        data_cells = []
        for header in headers:
            width = column_widths[header]
            value_str = str(row.get(header, ''))
            # Left-align the data cell content
            data_cells.append(f" {value_str:<{width}} ")
        markdown_lines.append("|" + "|".join(data_cells) + "|")
        
    return "\n".join(markdown_lines)


# --- Example Usage ---

# 1. GENERATE Markdown Table with Alignment
print("--- GENERATING MARKDOWN TABLE ---")
data_to_save = [
    {'Product': 'Laptop', 'Price': 1200.99, 'Units Sold': 150},
    {'Product': 'Mousepad', 'Price': 15.00, 'Units Sold': 9800},
    {'Product': 'Keyboard', 'Price': 75.50, 'Units Sold': 320},
]

# Define alignment: center product, right-align numbers
alignments = {
    'Product': 'center',
    'Price': 'right',
    'Units Sold': 'right'
}

markdown_output = generate_markdown_table(data_to_save, alignments)
print(markdown_output)


# 2. PARSE Markdown Table back into a Data Structure
print("\n--- PARSING MARKDOWN TABLE ---")
markdown_input = """
| Name       | Role        | Salary (K) |
|:----------:|:-----------|-----------:|
| Jane Doe   | Manager     | 95         |
| John Smith | Developer   | 110        |
| Alan Turing| Cryptogrpher| 120        |
"""

parsed_data = parse_markdown_table(markdown_input)
print(parsed_data)
print("-------------------------------")

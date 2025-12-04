"""RobUtils - A comprehensive Python utilities library with math, text, tools, and container utilities."""

__version__ = "0.1.0"

# Import subpackages for easy access
from . import math
from . import text
from . import tools
from . import containers

__all__ = [
    'math',
    'text',
    'tools',
    'containers',
    '__version__'
]
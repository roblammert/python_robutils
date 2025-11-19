# mypackage/math/containers/__init__.py

from .hashtable import get, put, remove, contains_key 

# Define what happens during a 'from mypackage.containers import *'
__all__ = [
    "get",
    "put",
    "remove",
    "contains_key",
]
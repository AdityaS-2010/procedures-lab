"""
Utility procedures student implement and test.
"""

# This import is important later to understand what's going on
from typing import Dict, Optional

def add(a: float, b: float) -> float:
    """
    Return a + b.
    """
    # TODO: Implement
    raise NotImplementedError

def fib(n: int) -> int:
    """
    Return the n-th Fibonacci number with fib(0) == 0, fib(1) == 1.
    """
    # TODO: implement
    raise NotImplementedError

"""
Simple "database"
Hi again! We imported `typing.Dict` because it's more readable type wise.
That is, so you can tell what we types of variables (string, integer, etc.) we want to use in our dictionary.
"""
_DB: Dict[str, Dict] = {}

def create_item(key: str, value: Dict) -> None:
    """
    Create or replace an item at key with value.
    """
    # TODO: implement
    raise NotImplementedError

def read_item(key: str) -> Optional[Dict]:
    """
    Return the stored value or None if missing.
    """
    # TODO: implement
    raise NotImplementedError

def update_item(key: str, patch: Dict) -> bool:
    """
    Update a stored dictionary item with the keys/values from path.
    Return True if item exists and was updated, False if item missing.
    """
    # TODO: implement
    raise NotImplementedError

def delete_item(key: str) -> bool:
    """
    Delete item at key. Return True if deleted, False if item missing.
    """
    # TODO: implement
    raise NotImplementedError

def clear_db() -> None:
    """Helper for tests (remove all items)."""
    global _DB
    _DB = {}
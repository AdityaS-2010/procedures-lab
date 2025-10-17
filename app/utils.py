"""
Utility procedures student implement and test.
"""

# This import is important later to understand what's going on
from typing import Dict, Optional
import copy

def add(a: float, b: float) -> float:
    """
    Return a + b.
    """
    return a + b

def fib(n: int) -> int:
    """
    Return the n-th Fibonacci number with fib(0) == 0, fib(1) == 1.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    # iterative implementation to avoid recursion limits
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

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
    # store a shallow copy to avoid caller mutations affecting the DB
    _DB[key] = copy.deepcopy(value)

def read_item(key: str) -> Optional[Dict]:
    """
    Return the stored value or None if missing.
    """
    v = _DB.get(key)
    if v is None:
        return None
    # return a deep copy so callers can't mutate internal state
    return copy.deepcopy(v)

def update_item(key: str, patch: Dict) -> bool:
    """
    Update a stored dictionary item with the keys/values from path.
    Return True if item exists and was updated, False if item missing.
    """
    if key not in _DB:
        return False
    existing = _DB[key]
    if not isinstance(existing, dict):
        # replace non-dict values with a copy of patch
        _DB[key] = copy.deepcopy(patch)
        return True
    # merge patch into existing dict (existing.update(patch) semantics)
    existing.update(copy.deepcopy(patch))
    return True

def delete_item(key: str) -> bool:
    """
    Delete item at key. Return True if deleted, False if item missing.
    """
    if key in _DB:
        del _DB[key]
        return True
    return False

def clear_db() -> None:
    """Helper for tests (remove all items)."""
    global _DB
    _DB = {}
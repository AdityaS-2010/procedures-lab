import pytest
from app import utils

def setup_function():
    utils.clear_db()

def test_add_simple():
    assert utils.add(2, 3) == 5
    assert utils.add(-1, 2.5) == 1.5

def test_fib_basic():
    # Fibonacci: 0,1,1,2,3,5,8,...
    seq = [utils.fib(i) for i in range(10)]
    assert seq[:7] == [0,1,1,2,3,5,8]

def test_db_crud():
    utils.create_item("k1", {"x": 1})
    assert utils.read_item("k1") == {"x": 1}
    assert utils.update_item("k1", {"y": 2}) is True
    assert utils.read_item("k1") == {"x": 1, "y": 2}
    assert utils.delete_item("k1") is True
    assert utils.read_item("k1") is None

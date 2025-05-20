import pytest
from ..src.add import addf
def test_addition():
    print("测试1+1")
    assert addf(1,1) == 2
def test_addition2():
    print("测试1+2")
    assert addf(1,2) == 3
def test_addition3():
    print("测试1+4")
    assert addf(1,3) == 3

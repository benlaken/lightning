import os
import sys
from ..storm import Storm


def test_reading_function():
    """Example of how to run a test. In this case to see if reading
    is a function. """
    def foo(): pass
    assert type(Storm.read_data) == type(foo)

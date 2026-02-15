"""
Basic tests for the Flappy Bird game package.
"""
import pytest
from flappy_bird.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def test_constants():
    """Test that game constants are properly defined."""
    assert SCREEN_WIDTH > 0
    assert SCREEN_HEIGHT > 0
    assert SCREEN_WIDTH != SCREEN_HEIGHT  # Not a square game


if __name__ == "__main__":
    test_constants()
    print("All tests passed!")
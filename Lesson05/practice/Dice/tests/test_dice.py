import pytest
from dice import Dice

def test_create_dice():
    dice6 = Dice()
    assert dice6.sides == 6


def test_roll():
    dice6 = Dice()
    for _ in range(100):
        assert 1 <= dice6.roll() <= 6

# __init__.py
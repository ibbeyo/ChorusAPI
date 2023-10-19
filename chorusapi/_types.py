from typing import Literal
from enum import Enum

TierType = Literal['gt1', 'gt2', 'gt3', 'gt4', 'gt5']

class DifficultyType(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 4
    EXPERT = 8
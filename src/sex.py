import enum
import random


class Sex(enum.Enum):
    F = 0
    M = 1

    @classmethod
    def random_sex(cls) -> 'Sex':
        return cls.F if random.choice([True, False]) else cls.M

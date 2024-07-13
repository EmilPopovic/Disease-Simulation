import random

from sex import Sex


class Individual:

    id = 0
    year = 0

    #region parameters

    MINIMUM_MATING_AGE = 0
    MAXIMUM_MATING_AGE = 0
    OLD_AGE_LIMIT = 0
    MAXIMUM_AGE = 0
    INFECTION_KILL_AGE = 0
    MATING_PROBABILITY = 0
    OLD_AGE_DEATH_PROBABILITY = 0
    RANDOM_DEATH_PROBABILITY = 0
    BREAKUP_PROBABILITY = 0

    #endregion

    def __init__(
            self,
            age: int,
            sex: Sex,
            infected: bool,
            first_gen: bool = False,
            parent1: 'Individual' = None,
            parent2: 'Individual' = None,
            year_of_birth: int = None) -> None:
        self.age = age
        self.sex = sex
        self.infected = infected

        self.id = Individual.id
        Individual.id += 1

        self.first_gen = first_gen

        self.parent1 = parent1
        self.parent2 = parent2

        self.alive = True

        self.children: list['Individual'] = []

        self.partner: 'Individual' = None

        self.year_of_birth: int = None

    #region behaviour

    def can_mate(self) -> bool:
        return self.alive and Individual.MINIMUM_MATING_AGE <= self.age <= Individual.MAXIMUM_MATING_AGE

    @classmethod
    def mate(cls, a: 'Individual', b: 'Individual') -> 'Individual':
        if a.sex == b.sex:
            raise ValueError("same sex individuals cannot mate")

        if not a.can_mate() or not b.can_mate():
            raise ValueError("either individual is dead")

        child = Individual(
            age=0,
            sex=Sex.random_sex(),
            infected=a.infected or b.infected,
            parent1=a,
            parent2=b,
            year_of_birth=cls.year
        )

        a.children.append(child)
        b.children.append(child)

        return child

    def mate_with_partner(self) -> list['Individual']:
        if self.partner is None:
            return []

        try:
            child = self.mate(self, self.partner)
        except ValueError as _:
            return []

        return [child]

    def infect(self) -> None:
        self.infected = True

    def kill(self) -> None:
        self.alive = False
        self.break_up()

    def live_year(self, pop: list['Individual']) -> dict:
        result = {
            'child_count': 0,
            'broke_up': False
        }

        if not self.alive:
            return result

        if self.partner and random.random() < self.MATING_PROBABILITY:
            children = self.mate_with_partner()
            pop.extend(children)
            result['child_count'] = len(children)

        if random.random() < Individual.BREAKUP_PROBABILITY:
            broke_up = self.break_up()
            result['broke_up'] = broke_up

        return result

    def break_up(self) -> bool:
        if self.partner:
            self.partner.partner = None
            self.partner = None
            return True
        return False

    def increase_age(self) -> dict:
        result = {
            'died': False
        }

        if not self.alive:
            return result

        self.age += 1

        if self.infected and self.age > Individual.INFECTION_KILL_AGE:
            self.kill()
            result['died'] = True

        if self.age > Individual.OLD_AGE_LIMIT and random.random() < self.OLD_AGE_DEATH_PROBABILITY:
            self.kill()
            result['died'] = True

        if random.random() < self.RANDOM_DEATH_PROBABILITY:
            self.kill()
            result['died'] = True

        if self.age > Individual.MAXIMUM_AGE:
            self.kill()
            result['died'] = True

        return result

    def __repr__(self) -> str:
        return f'Individual {self.id}: age {self.age}, sex: {self.sex}, infected: {self.infected}'

    def __eq__(self, other: 'Individual') -> bool:
        return self.id == other.id

    def __hash__(self):
        return self.id.__hash__()

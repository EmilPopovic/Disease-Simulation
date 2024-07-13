import random

from sex import Sex


class Individual:

    id = 0

    #region parameters

    MINIMUM_MATING_AGE = 0
    MAXIMUM_MATING_AGE = 0
    MAXIMUM_AGE = 0
    INFECTION_KILL_AGE = 0
    MATING_PROBABILITY = 0
    DEATH_PROBABILITY_AFTER_MAX_AGE = 0
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
        self.id += 1

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

    @staticmethod
    def mate(a: 'Individual', b: 'Individual') -> 'Individual':
        if a.sex == b.sex:
            raise ValueError("same sex individuals cannot mate")

        if not a.can_mate() or not b.can_mate():
            raise ValueError("either individual is dead")

        child = Individual(
            age=0,
            sex=Sex.random_sex(),
            infected=a.infected or b.infected,
            parent1=a,
            parent2=b
        )

        a.children.append(child)
        b.children.append(child)

        return child

    def mate_with_partner(self) -> bool:
        if self.partner is None:
            return False

        self.mate(self, self.partner)

        return True

    def infect(self) -> None:
        self.infected = True

    def kill(self) -> None:
        self.alive = False
        self.break_up()

    def live_year(self) -> None:
        if not self.alive:
            return

        if self.partner is not None and random_percent() < self.MATING_PROBABILITY:
            self.mate_with_partner()

        if random_percent() < Individual.BREAKUP_PROBABILITY:
            self.break_up()

    def break_up(self) -> None:
        if self.partner is not None:
            self.partner.partner = None
            self.partner = None

    def increase_age(self) -> None:
        self.age += 1

        if self.infected and self.age > Individual.INFECTION_KILL_AGE:
            self.kill()

        if self.age > Individual.MAXIMUM_AGE and random_percent() < self.DEATH_PROBABILITY_AFTER_MAX_AGE:
            self.kill()

        if random_percent() < self.RANDOM_DEATH_PROBABILITY:
            self.kill()


    def __repr__(self) -> str:
        return f'Individual {self.id}: age {self.age}, sex: {self.sex}, infected: {self.infected}'


def random_percent():
    return random.randint(0, 100)
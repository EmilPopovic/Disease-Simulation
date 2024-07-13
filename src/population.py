import random

from collections import deque

from src.individual import Individual
from src.sex import Sex


class Population:

    year = 0

    #region parameters

    INITIAL_POPULATION = 0
    INITIAL_INFECTIONS = 0

    MINIMUM_INITIAL_AGE = 0
    MAXIMUM_INITIAL_AGE = 0

    MINIMUM_INCEST_DISTANCE = 0

    #endregion

    def __init__(self):
        self.population: list[Individual] = []

    #region auto-populating
    @classmethod
    def auto_populated(cls) -> 'Population':
        def random_individual():
            return Individual(
                random.randint(cls.MINIMUM_INITIAL_AGE, cls.MAXIMUM_INITIAL_AGE),
                Sex.random_sex(),
                False,
                True
            )

        population: 'Population' = Population()
        population.population = [random_individual() for _ in range(cls.INITIAL_POPULATION)]

        for i in range(cls.INITIAL_INFECTIONS):
            population.population[i].infect()

        return population

    #endregion

    @staticmethod
    def distance(ind1: Individual, ind2: Individual, max_depth: int = -1) -> int:
        if ind1 == ind2:
            return 0

        queue = deque([(ind1, 0)])
        visited = set()
        visited.add(ind1)

        while queue:
            current, distance = queue.popleft()

            for parent in [ind1.parent1, ind1.parent2]:
                if parent and parent not in visited:
                    if parent == ind2:
                        return distance + 1

                    visited.add(parent)

                    if max_depth < 0 or distance + 1 <= max_depth:
                        queue.append((parent, distance + 1))

            for child in ind1.children:
                if child not in visited:
                    if child == ind2:
                        return distance + 1

                    visited.add(child)

                    if max_depth < 0 or distance + 1 <= max_depth:
                        queue.append((child, distance + 1))

        return -1

    def advance_sim(self):
        self.year += 1

        single: list[Individual] = self.filter_pop(
            lambda
                x: x.alive and x.partner is None and Individual.MINIMUM_MATING_AGE <= x.age <= Individual.MAXIMUM_MATING_AGE
        )
        single.sort(key=lambda x: x.age, reverse=False)

        for i, first in enumerate(single):
            for j, second in enumerate(single):
                if i == j or first.partner or second.partner:
                    continue

                if self.distance(first, second, self.MINIMUM_INCEST_DISTANCE) == -1 and first.sex != second.sex:
                    ...



        for individual in self.population:
            individual.live_year()

        for individual in self.population:
            individual.increase_age()

    #region collection-stream-esque stuff

    def count_in_pop(self, criteria) -> int:
        return self.count(self.population, criteria)

    def filter_pop(self, criteria) -> list[Individual]:
        return self.filter(self.population, criteria)

    def average_in_pop(self, attribute) -> float:
        return self.average(self.population, attribute)

    @staticmethod
    def count(pop: list[Individual], criteria) -> int:
        return sum(1 for individual in pop if criteria(individual))

    @staticmethod
    def filter(pop: list[Individual], criteria) -> list[Individual]:
        return [individual for individual in pop if criteria(individual)]

    @staticmethod
    def average(pop: list[Individual], attribute) -> float:
        return sum(attribute(individual) for individual in pop) / len(pop) if pop else 0

    #endregion

    #region stats and printing

    def print_stats(self, title: str = 'Population statistics') -> None:
        alive: list[Individual] = self.filter_pop(lambda x: x.alive)

        size = len(alive)
        male_count = self.count(alive, lambda x: x.sex == Sex.M)
        female_count = self.count(alive, lambda x: x.sex == Sex.F)
        mf_ratio = male_count / female_count if female_count else 0
        avg_age = self.average(alive, lambda x: x.age)
        infections = self.count(alive, lambda x: x.infected)
        infection_ratio = infections / len(self.population)
        infected_males = self.count(alive, lambda x: x.infected and x.sex == Sex.M)
        infected_females = self.count(alive, lambda x: x.infected and x.sex == Sex.F)

        print(title)
        print(f'  size: {size}')
        print(f'  males: {male_count}')
        print(f'  females: {female_count}')
        print(f'  m/f ratio: {mf_ratio:.2f}')
        print(f'  average age: {avg_age:.2f}')
        print(f'  infections: {infections}')
        print(f'  infected males: {infected_males}')
        print(f'  infected females: {infected_females}')
        print(f'  infection ratio: {infection_ratio * 100:.2f}%')

    def __repr__(self):
        return f'Population:\n{'\n'.join([f'  {individual}' for individual in self.population])}'

    def print(self) -> None:
        print(self.__repr__())

    #endregion



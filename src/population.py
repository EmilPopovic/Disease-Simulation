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
    MEAN_INITIAL_AGE = 0
    STD_DEV_INITIAL_AGE = 0

    POTENTIAL_PARTNER_COUNT = 0
    MAXIMUM_AGE_DIFFERENCE = 0
    RELATIONSHIP_PROBABILITY = 0

    MINIMUM_INCEST_DISTANCE = 0

    #endregion

    def __init__(self):
        self.population: list[Individual] = []
        self.yearly_info = {
            0: {
                'born_count': 0,
                'new_relationships': 0,
                'breakup_count': 0,
                'death_count': 0,
                'count_by_age_bin': {
                    '0-19': 0,
                    '20-39': 0,
                    '40-59': 0,
                    '60-79': 0,
                    '80-99': 0,
                    '100+': 0,
                }
            }
        }

    #region auto-populating
    @classmethod
    def auto_populated(cls) -> 'Population':

        def random_age():
            age = -1
            while age < cls.MINIMUM_INITIAL_AGE or age > cls.MAXIMUM_INITIAL_AGE:
                age = int(random.gauss(cls.MEAN_INITIAL_AGE, cls.STD_DEV_INITIAL_AGE))
            return age

        def random_individual():
            return Individual(
                random_age(),
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

    #region simulation logic

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
        Population.year += 1

        single: list[Individual] = self.filter_pop(
            lambda
                x: x.alive and x.partner is None and Individual.MINIMUM_MATING_AGE <= x.age <= Individual.MAXIMUM_MATING_AGE
        )
        single.sort(key=lambda x: x.age, reverse=False)

        Individual.year = self.year

        self.yearly_info[self.year] = {
            'born_count': 0,
            'new_relationships': 0,
            'breakup_count': 0,
            'death_count': 0,
            'count_by_age_bin': {}
        }

        for i, first in enumerate(single):
            for j, second in enumerate(random.sample(single, min(Population.POTENTIAL_PARTNER_COUNT, len(single)))):
                if i == j or first.partner or second.partner:
                    continue

                distance = self.distance(first, second, Population.MINIMUM_INCEST_DISTANCE)

                if distance < 0 or distance > Population.MINIMUM_INCEST_DISTANCE and first.sex != second.sex:
                    age_difference = abs(first.age - second.age)
                    age_diff_factor = max(0.1, 1 - age_difference / Population.MAXIMUM_AGE_DIFFERENCE)

                    if random.random() < age_diff_factor * Population.RELATIONSHIP_PROBABILITY:
                        first.partner = second
                        second.partner = first
                        self.yearly_info[self.year]['new_relationships'] += 1


        for individual in self.population:
            result = individual.live_year(self.population)

            self.yearly_info[self.year]['born_count'] += result['child_count']
            self.yearly_info[self.year]['breakup_count'] += 1 if result['broke_up'] else 0

        for individual in self.population:
            result = individual.increase_age()

            self.yearly_info[self.year]['death_count'] += 1 if result['died'] else 0

        self.yearly_info[self.year]['count_by_age_bin']['0-19'] = self.count_in_pop(lambda x: 0 <= x.age < 20)
        self.yearly_info[self.year]['count_by_age_bin']['20-39'] = self.count_in_pop(lambda x: 20 <= x.age < 40)
        self.yearly_info[self.year]['count_by_age_bin']['40-59'] = self.count_in_pop(lambda x: 40 <= x.age < 60)
        self.yearly_info[self.year]['count_by_age_bin']['60-79'] = self.count_in_pop(lambda x: 60 <= x.age < 80)
        self.yearly_info[self.year]['count_by_age_bin']['80-99'] = self.count_in_pop(lambda x: 80 <= x.age < 100)
        self.yearly_info[self.year]['count_by_age_bin']['100+'] = self.count_in_pop(lambda x: x.age > 100)

    #endregion

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
        print()

    def print_yearly_stats(self, year: int, title: str = f'Yearly stats for year {year}') -> None:
        print(title)
        print(f'  born count: {self.yearly_info[year]['born_count']}')
        print(f'  death count: {self.yearly_info[year]['death_count']}')
        print(f'  new relationships: {self.yearly_info[year]['new_relationships']}')
        print(f'  breakup count: {self.yearly_info[year]['breakup_count']}')
        print()

    def __repr__(self):
        return f'Population:\n{'\n'.join([f'  {individual}' for individual in self.population])}'

    def print(self) -> None:
        print(self.__repr__())

    #endregion



from src.individual import Individual
from src.population import Population


Individual.MINIMUM_MATING_AGE = 18
Individual.MAXIMUM_MATING_AGE = 50
Individual.MAXIMUM_AGE = 70
Individual.INFECTION_KILL_AGE = 40
Individual.MATING_PROBABILITY = 5
Individual.DEATH_PROBABILITY_AFTER_MAX_AGE = 10
Individual.RANDOM_DEATH_PROBABILITY = 1
Individual.BREAKUP_PROBABILITY = 5

Population.INITIAL_POPULATION = 1000
Population.INITIAL_INFECTIONS = 0
Population.MINIMUM_INITIAL_AGE = 14
Population.MAXIMUM_INITIAL_AGE = 60
Population.MINIMUM_INCEST_DISTANCE = 6

ITERATIONS = 20


# todo https://plotly.com/python/network-graphs/


def main():
    pop: Population = Population.auto_populated()
    pop.print_stats('Initial population stats')

    for i in range(ITERATIONS):
        pop.advance_sim()
        pop.print_stats(f'Stats in year {i}')


if __name__ == '__main__':
    main()

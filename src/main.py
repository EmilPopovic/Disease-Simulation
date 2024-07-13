from src.individual import Individual
from src.population import Population


Individual.MINIMUM_MATING_AGE = 18
Individual.MAXIMUM_MATING_AGE = 50
Individual.OLD_AGE_LIMIT = 70
Individual.MAXIMUM_AGE = 120
Individual.INFECTION_KILL_AGE = 40

Individual.MATING_PROBABILITY = 0.11
Individual.OLD_AGE_DEATH_PROBABILITY = 0.05
Individual.RANDOM_DEATH_PROBABILITY = 0.01
Individual.BREAKUP_PROBABILITY = 0.02

Population.INITIAL_POPULATION = 1000
Population.INITIAL_INFECTIONS = 10

Population.MINIMUM_INITIAL_AGE = 0
Population.MAXIMUM_INITIAL_AGE = 120
Population.MEAN_INITIAL_AGE = 40
Population.SD_INITIAL_AGE = 20

Population.POTENTIAL_PARTNER_COUNT = 30
Population.MAXIMUM_AGE_DIFFERENCE = 10
Population.RELATIONSHIP_PROBABILITY = 0.05

Population.MINIMUM_INCEST_DISTANCE = 2

ITERATIONS = 200


# todo https://plotly.com/python/network-graphs/


def main():
    pop: Population = Population.auto_populated()

    #pop.print()

    pop.print_stats('Initial population stats')

    for i in range(ITERATIONS):
        pop.advance_sim()
        pop.print_yearly_stats(pop.year)

    pop.print_stats('Final population stats')


if __name__ == '__main__':
    main()

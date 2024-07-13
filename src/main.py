import numpy as np
import pylab as plt

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
Population.SD_INITIAL_AGE = 30

Population.POTENTIAL_PARTNER_COUNT = 30
Population.MAXIMUM_AGE_DIFFERENCE = 10
Population.RELATIONSHIP_PROBABILITY = 0.05

Population.MINIMUM_INCEST_DISTANCE = 2

ITERATIONS = 1000


def main():
    pop: Population = Population.auto_populated()

    #pop.print()

    pop.print_stats('Initial population stats')

    for i in range(ITERATIONS):
        pop.advance_sim()
        #pop.print_yearly_stats(pop.year)

    pop.print_stats('Final population stats')


    x = np.arange(0, ITERATIONS + 1, 1)

    pop_data = pop.yearly_population_to_ndarray().T

    total_population = pop_data

    plt.subplot(2, 2, 1)
    plt.stackplot(
        x,
        *total_population,
        baseline='zero',
        labels=['0-19', '20-39', '40-59', '60-79', '80-99', '100+']
    )
    plt.title('Total population by age bin')
    plt.axis('tight')
    plt.legend(loc='upper right')

    norm_population = pop_data / pop_data.sum(axis=0, keepdims=True) * 100

    plt.subplot(2, 2, 2)
    plt.stackplot(
        x,
        *norm_population,
        baseline='zero',
        labels=['0-19', '20-39', '40-59', '60-79', '80-99', '100+']
    )
    plt.title('Normalized population by age bin')
    plt.axis('tight')
    plt.ylim(0, 100)
    plt.legend(loc='upper right')


    plt.show()

if __name__ == '__main__':
    main()

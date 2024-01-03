import numpy as np
import random

def find_indices(arr1, arr2):
    return [i for i, item in enumerate(arr1) if item in arr2]


def crossover(new_population, p_crossover):
    # Get the size of the population
    n = len(new_population)
    # Check if the size is odd
    parity = n % 2
    # Initialize the new population
    new_population_1 = []

    # Iterate over pairs of individuals in the population
    for i in range(0, n-1, 2):
        # Extract the current and next individuals
        parent_1 = np.array(new_population[i])
        parent_2 = np.array(new_population[i+1])

        # Check for common elements between the two individuals
        commons = find_indices(parent_1, parent_2)
        # Perform crossover with a certain probability
        # len(commons) > 2 Every path has the same start and end so must have at least 3 points in common
        
        if random.random() < p_crossover and len(commons) > 2:
            # Select a random crossover point (exclude the first and last)
            crossover_point_in_parent_1 = random.choice(commons[1:-1])   
            crossover_point_in_parent_2 = np.where(parent_2 == parent_1[crossover_point_in_parent_1])[0][0]

            # swapping genetic material
            new_population_1.append(list(parent_1[:crossover_point_in_parent_1 + 1]) + list(parent_2[crossover_point_in_parent_2+1:]))
            new_population_1.append(list(parent_2[:crossover_point_in_parent_2 + 1]) + list(parent_1[crossover_point_in_parent_1+1:]))
        else:
            # If no crossover, keep the individuals unchanged
            new_population_1.append(parent_1.tolist())
            new_population_1.append(parent_2.tolist())

    # If the population size is odd, append the last individual as is
    if parity == 1:
        new_population_1.append(np.array(new_population[-1]).tolist())

    return new_population_1


if __name__ == '__main__':
    new_population_data = [
        np.array([0, 2, 13, 35, 46, 57, 68, 78, 89, 99]),
        np.array([0, 1, 2, 3, 13, 24, 35, 46, 57, 68, 78, 89, 99]),å
    ]
    p_crossover_value = 1

    result = crossover(new_population_data, p_crossover_value)
    print(result)

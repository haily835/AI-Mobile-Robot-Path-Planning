import numpy as np
import random
# Set a seed for reproducibility
random.seed(42)

def truncation_selection(population, fitness_values, top_percentage=0.9):
    # Sort individuals based on fitness values
    sorted_pairs = sorted(zip(population, fitness_values), key=lambda x: x[1], reverse=True)

    # Select the top individuals
    selected_count = int(len(sorted_pairs) * top_percentage)
    selected_individuals = [pair[0] for pair in sorted_pairs[:selected_count]]
    random.shuffle(selected_individuals)
    return selected_individuals

def selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fitness / total_fitness for fitness in fitness_values]

    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]

    new_population = []

    while len(new_population) < len(population):
        for _ in range(2):  # Do this twice to create offspring
            random_number = random.uniform(0, 1)

            selected_individual = None
            for i in range(len(population)):
                if i == 0 and random_number <= cumulative_probabilities[0]:
                    selected_individual = population[0]
                    break
                elif cumulative_probabilities[i-1] < random_number <= cumulative_probabilities[i]:
                    selected_individual = population[i]
                    break

            # Create offspring (you can replace this with your own logic)
            new_population.append(selected_individual)

    return new_population

if __name__ == '__main__':
    new_population_data = [np.array([1, 2, 9]), np.array([4, 5, 9]), np.array([7, 8, 9])]
    fit_value_data = [10, 20, 30]

    result = selection(new_population_data, fit_value_data)
    print(result)

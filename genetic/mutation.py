import numpy as np
from grid_number_to_xy import grid_number_to_xy
import random

def mutation(new_population, p_mutation, G):
    n = len(new_population)
    rows, cols = G.shape[0], G.shape[1]
    next_population = []
    
    for i in range(n):
        path = new_population[i]
        
        if np.random.rand() < p_mutation and len(path) > 3:
            possible_mutations = []
            
            for i in range(1, len(path) - 1):
                
                r, c = grid_number_to_xy(path[i], cols)

                actions = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),           (0, 1),
                        (1, -1), (1, 0), (1, 1)]
                
                prev = grid_number_to_xy(path[i - 1], cols)
                after = grid_number_to_xy(path[i + 1], cols)
                for action in actions:
                    end = (r + action[0], c + action[1])

                    # Check if the end position is within the grid bounds and is not an obstacle
                    if 0 <= end[0] < rows and 0 <= end[1] < cols and G[end[0], end[1]] == 0 \
                        and end[0] != prev[0] and end[0] != prev[1] \
                        and end[0] != after[0] and end[0] != after[1]:
                        mutated = np.copy(path)
                        mutated[i] = end[0] * cols + end[1]
                        possible_mutations.append(mutated.tolist())

            
            if len(possible_mutations):
                mutation = random.choice(possible_mutations)
                next_population.append(mutation)
            else: 
                next_population.append(path)

        else:
            next_population.append(path)

    return next_population


if __name__ == '__main__':
    new_population_data = [
        np.array([1, 2, 99]),
        np.array([4, 5, 99]),
        np.array([7, 8, 99]),
        np.array([10, 411, 99]),
        np.array([1, 141, 99]),
        np.array([2, 4, 99]),
        np.array([10, 11, 99]),
    ]
    p_mutation_value = 0.2
    G_data = np.zeros((20, 20)) # Adjaciency matrix
    r_data = 20

    result = mutation(new_population_data, p_mutation_value, G_data)
    print(result)

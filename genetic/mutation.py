import numpy as np
from .grid_number_to_yx import grid_number_to_yx
import random
import concurrent.futures
# Set a seed for reproducibility
random.seed(42)

# check if the line connected pass through obstacle
def check_path(a, b, G):
    a1, b1 = a
    a3, b3 = b
    valid = False
    # Check if the path can be smoothed by removing a middle point
    if a1 < a3 and b1 < b3 and np.all(G[a1:a3+1, b1:b3+1] == 0): valid = True
    elif a1 < a3 and b1 > b3 and np.all(G[a1:a3+1, b3:b1+1] == 0): valid = True
    elif a1 > a3 and b1 < b3 and np.all(G[a3:a1+1, b1:b3+1] == 0): valid = True
    elif a1 > a3 and b1 > b3 and np.all(G[a3:a1+1, b3:b1+1] == 0): valid = True

    return valid

def mutate_path(path, p_mutation, G):
    rows, cols = G.shape[0], G.shape[1]
    if random.random() < p_mutation and len(path) > 3:
        possible_mutations = []
        
        for i in range(1, len(path) - 1):
            r, c = grid_number_to_yx(path[i], cols)

            actions = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),           (0, 1),
                        (1, -1), (1, 0), (1, 1)]
            
            prev = grid_number_to_yx(path[i - 1], cols)
            after = grid_number_to_yx(path[i + 1], cols)
            for action in actions:
                end = (r + action[0], c + action[1])

                # Check if the end position is 
                # within the grid bounds and is not an obstacle
                # not repeated the previous path
                # the connected not passing obstacle
                if 0 <= end[0] < rows and 0 <= end[1] < cols and G[end[0], end[1]] == 0 \
                    and end[0] != prev[0] and end[0] != prev[1] \
                    and end[0] != after[0] and end[0] != after[1] \
                    and check_path(end, prev, G) and check_path(end, after, G):
                    mutated = np.copy(path)
                    mutated[i] = end[0] * cols + end[1]
                    possible_mutations.append(mutated.tolist())

        
        if len(possible_mutations):
            mutation = random.choice(possible_mutations)
            return mutation
        else:
            return path

    else:
        return path

def mutation(new_population, p_mutation, G):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(mutate_path, individual, p_mutation, G) for individual in new_population]

        # Wait for all tasks to complete and retrieve results
        return [future.result() for future in concurrent.futures.as_completed(futures)]

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
    p_mutation_value = 1
    G_data = np.zeros((20, 20)) # Adjaciency matrix
    r_data = 20

    result = mutation(new_population_data, p_mutation_value, G_data)
    print(result)

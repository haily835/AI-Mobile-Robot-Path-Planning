import numpy as np
from .distance import distance

def cal_path_value(new_population, grid_size):
    # Get the number of populations in the new_population list
    n = len(new_population)
    
    # Initialize an array to store path values for each population
    path_value = np.zeros(n)

    # Iterate over each population in new_population
    for i in range(n):
        # Get a single population from the list
        single_population = new_population[i]
        
        # Get the number of points in the single_population
        m = len(single_population)

        # Iterate over each point in the population (except the last one)
        for j in range(m - 1):
            # Calculate the distance between consecutive points
            dis = distance(single_population[j], single_population[j + 1], grid_size)
            
            # Accumulate the distance to the path_value for the current population
            path_value[i] += dis

    return path_value


# population_data = [
# ]

# result = cal_path_value(population_data)

# print(result)

import numpy as np

def selection(new_population, fit_value):
    ## Calculate total fitness value and normalize fitness values
    total_fit_value = np.sum(fit_value)

    
    normal_fit_value = fit_value / total_fit_value
    
    # Calculate cumulative normalized fitness values
    cum_normal_fit_value = np.cumsum(normal_fit_value)
    
    # Generate sorted random values
    random_values = np.sort(np.random.rand(len(new_population)))
    
    # Initialize the new population list
    new_population_selected = []
    
    # Perform roulette wheel selection
    for random_value in random_values:
        # Find the index where the random value is less than cumulative normalized fitness
        fit_index = np.searchsorted(cum_normal_fit_value, random_value)
        
        # Select the individual
        new_population_selected.append(new_population[fit_index])
    
    return new_population_selected

if __name__ == '__main__':
    new_population_data = [np.array([1, 2, 9]), np.array([4, 5, 9]), np.array([7, 8, 9])]
    fit_value_data = [10, 20, 30]

    result = selection(new_population_data, fit_value_data)
    print(result)

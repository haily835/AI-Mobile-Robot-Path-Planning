import numpy as np
from grid_number_to_xy import grid_number_to_xy

def deletion(population, G):
    new_population_1 = []
    rows, cols = G.shape[0], G.shape[1]
    for path in population:
        long = len(path)
        j = 0

        while j != long - 2:
            # Get coordinates for the current and next grid points
            a1, b1 = grid_number_to_xy(path[j], cols)
            a3, b3 = grid_number_to_xy(path[j + 2], cols)
            skip = False
            # Check if the path can be smoothed by removing a middle point
            if a1 < a3 and b1 < b3 and np.all(G[a1:a3+1, b1:b3+1] == 0): skip = True
            elif a1 < a3 and b1 > b3 and np.all(G[a1:a3+1, b3:b1+1] == 0): skip = True
            elif a1 > a3 and b1 < b3 and np.all(G[a3:a1+1, b1:b3+1] == 0): skip = True
            elif a1 > a3 and b1 > b3 and np.all(G[a3:a1+1, b3:b1+1] == 0): skip = True
            
            if skip: 
                path = np.delete(path, j + 1)
            else:
                j += 1
            long = len(path)

        new_population_1.append(path)

    return new_population_1

if __name__ == '__main__':
    path_data = [[1, 2, 3, 4, 10], [6, 7, 8, 9, 10]]
    G_data = np.zeros((20, 20))  

    result = deletion(path_data, G_data, 20)
    print(result)
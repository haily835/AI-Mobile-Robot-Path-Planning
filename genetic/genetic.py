import numpy as np
from selection import selection
from crossover import crossover
from deletion import deletion
from cal_path_value import cal_path_value
from cal_smooth_value import cal_smooth_value
from mutation import mutation
import numpy as np
from grid_number_to_xy import grid_number_to_xy
import matplotlib.pyplot as plt
from insertion import insertion
from aco import aco


def convert_path_to_xy(path, cols):
    return [grid_number_to_xy(grid, cols) for grid in path]


def plot_path(G, path_coordinates):
    # Create a heatmap plot with 1 as white and 0 as black
    plt.imshow(G, cmap='gray_r', interpolation='nearest', vmin=0, vmax=1)

    # Plot the path on top of the heatmap
    path_x, path_y = zip(*path_coordinates)
    plt.plot(path_y, path_x, color='red', marker='o')

    plt.title('Visualization of Grid Matrix with Path')
    plt.show()


def genetic(G, start, end, max_generation = 100, p_crossover = 0.2, 
            p_mutation = 0.05, weight_length = 20, weight_smooth = 20):
    
    rows, cols = G.shape[0], G.shape[1]

    new_population = aco(G, start, end, m=50, NC_max=100)

    print("Finish Ant colony optimization")

    path_value = cal_path_value(new_population, cols)
    sort1, index = np.sort(path_value), np.argsort(path_value)
    new_population = [new_population[i] for i in index]
    # print('new_population: ', new_population)
    path_value = cal_path_value(new_population, cols)
    smooth_value = cal_smooth_value(new_population, cols)
    fit_value = (weight_length / path_value) + (weight_smooth / smooth_value)

    mean_path_value = np.zeros(max_generation)
    min_path_value = np.zeros(max_generation)
    min_path = []

    for i in range(max_generation):
        new_population = selection(new_population, fit_value)
        new_population = crossover(new_population, p_crossover)

        # print(f'before mutation: {new_population[0]}')
        new_population = mutation(new_population, p_mutation, G)
        # print(f'after mutation: {new_population[0]}')

        # end_change(new_population_1, position_e)
        new_population = insertion(new_population, G)

        new_population = deletion(new_population, G)

        path_value = cal_path_value(new_population, cols)

        smooth_value = cal_smooth_value(new_population, cols)

        # fit_value = []
        # for i in range(len(path_value)):
        #     fit_value.append(
        #         weight_length / (path_value or np.Inf) + (weight_smooth / smooth_value)
        #     )
        
        fit_value = 10 ** cols - (weight_length * path_value) - (weight_smooth * path_value)

        mean_path_value[i] = np.mean(path_value)
        ma = np.argmax(fit_value)
        min_path_value[i] = path_value[ma]
        min_path.append(new_population[ma])
    
    return convert_path_to_xy(min_path[-1], cols)

if __name__ == '__main__':
    G = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    path = genetic(G, [0,0], [9,9])
    plot_path(G, path)

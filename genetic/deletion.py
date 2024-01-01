import numpy as np
from .grid_number_to_yx import grid_number_to_yx
import concurrent.futures
from path_smooth.path_smooth import delete_nodes
from matplotlib.patches import Rectangle

def convert_path_to_xy(path, cols):
    xy_path = []
    for grid in path:
        y, x = grid_number_to_yx(grid, cols)
        xy_path.append((x, y))
    return xy_path

def delete_nodes(path, G):
    rows, cols = G.shape[0], G.shape[1]
    long = len(path)
    j = 0

    while j != long - 2:
        # Get coordinates for the current and next grid points
        a1, b1 = grid_number_to_yx(path[j], cols)
        a3, b3 = grid_number_to_yx(path[j + 2], cols)
        skip = False
        # Check if the path can be smoothed by removing a middle point
        if a1 <= a3 and b1 <= b3 and np.all(G[a1:a3+1, b1:b3+1] == 0): skip = True
        elif a1 <= a3 and b1 >= b3 and np.all(G[a1:a3+1, b3:b1+1] == 0): skip = True
        elif a1 >= a3 and b1 <= b3 and np.all(G[a3:a1+1, b1:b3+1] == 0): skip = True
        elif a1 >= a3 and b1 >= b3 and np.all(G[a3:a1+1, b3:b1+1] == 0): skip = True
        
        if skip: path = np.delete(path, j + 1)
        else: j += 1
        
        long = len(path)
    return path




def delete_slow(path, cols, obstacle_rectangles, grid_size):
    path_xy = convert_path_to_xy(path, cols)
    smoothed = delete_nodes(path_xy, obstacle_rectangles, grid_size)
    return [(p[1] * cols + p[0]) for p in smoothed]

def deletion(population, map):
    G = map.get_grid_matrix()

    # # those information is needed once
    # cols = G.shape[1]
    # obstacles = map.obstacles
    # grid_size = map.grid_size
    # obstacle_rectangles = []
    # for o in obstacles:
    #     x, y = o
        
    #     rect_coords = (x * grid_size, y * grid_size)
    #     rect = Rectangle(rect_coords, grid_size, grid_size, linewidth=1)
    #     rect_points = rect.get_corners()

    #     obstacle_rectangles.append(rect_points)
    
    # return [delete_slow(individual, cols, obstacle_rectangles, grid_size) for individual in population]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(population)) as executor:
        futures = [executor.submit(delete_nodes, individual, G) for individual in population]
        return [future.result() for future in concurrent.futures.as_completed(futures)]
    

if __name__ == '__main__':
    path_data = [[1, 2, 3, 4, 10], [6, 7, 8, 9, 10]]
    G_data = np.zeros((20, 20))

    result = deletion(path_data, G_data, 20)
    print(result)
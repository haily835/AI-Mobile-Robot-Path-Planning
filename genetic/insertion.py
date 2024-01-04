import numpy as np
from .grid_number_to_yx import grid_number_to_yx
import random
import concurrent.futures
# Set a seed for reproducibility
random.seed(42)

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

def insert_path(path, G):
    i = 0
    rows, cols = G.shape[0], G.shape[1]
    while i < (len(path) - 1):
        p1 = grid_number_to_yx(path[i], cols)
        p2 = grid_number_to_yx(path[i + 1], cols)
        delta = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))
        # print(f'delta {i} ', delta)
        # Delta = 1 => discontinuos
        if delta > 1:
            p_alt = ((p2[0] + p1[0]) // 2, (p2[1] + p1[1]) // 2)
            
            if G[p_alt[0], p_alt[1]] == 0 \
                and check_path(p_alt, p1, G) and check_path(p_alt, p2, G):
                insert_grid = p_alt[0] * cols + p_alt[1]
                path = path[:i+1] + [insert_grid] + path[i+1:]
                i += 2
            else:
                # find nearest grid
                actions = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),           (0, 1),
                        (1, -1), (1, 0), (1, 1)]
                
                alternatives = []

                for action in actions:
                    end = (p_alt[0] + action[0], p_alt[1] + action[1])

                    # Check if the end position is within the grid bounds and is not an obstacle
                    if 0 <= end[0] < rows and 0 <= end[1] < cols and G[end[0], end[1]] == 0 \
                        and end[0] != p1[0] and end[0] != p1[1] \
                        and end[0] != p2[0] and end[0] != p2[1] \
                        and check_path(end, p1, G) and check_path(end, p2, G):
                        alternatives.append(end)

                if len(alternatives):
                    # print('insert')
                    alt = random.choice(alternatives)
                    path = path[:i+1] + [alt[0] * cols + alt[1]] + path[i+1:]
                    i += 2
                else:
                    i += 1
        else:
            i += 1
        
    return path

def insertion(population, G):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(insert_path, individual, G) for individual in population]

        # Wait for all tasks to complete and retrieve results
        return [future.result() for future in concurrent.futures.as_completed(futures)]

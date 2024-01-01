import numpy as np
from grid_number_to_xy import grid_number_to_xy
import random

def insertion(population, G):
    next_population = []
    rows, cols = G.shape[0], G.shape[1]

    for path in population:
        i = 0
        while i < (len(path) - 1):
            p1 = grid_number_to_xy(path[i], cols)
            p2 = grid_number_to_xy(path[i + 1], cols)
            delta = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))

            # Delta = 1 => discontinuos
            if delta != 1:
                p_alt = ((p2[0] + p1[0]) // 2, (p2[1] + p1[1]) // 2)
                
                if G[p_alt[0], p_alt[1]] == 0:
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
                            and end[0] != p2[0] and end[0] != p2[1]:
                            mutated = np.copy(path)
                            mutated[i] = end[0] * cols + end[1]
                            alternatives.append(mutated.tolist())

                    if len(alternatives):
                        alt = random.choice(alternatives)
                        path = path[:i+1] + [alt[0] * cols + alt[1]] + path[i+1:]
                        i += 2
                    else:
                        i += 1
            else:
                i += 1
        
        next_population.append(path)

    return next_population
import numpy as np
from genetic.deletion import delete_nodes
from genetic.genetic import plot_path, convert_path_to_xy
from genetic.grid_number_to_yx import grid_number_to_yx
# Import necessary custom-built classes and methods
# from utils.obstacle_space import Map
from obstacle.obstacle_map import Map
from a_star.explorer import Explorer
from a_star.search import astar_search, path_states, dynamic_weighted_astar_search
import time

map = Map(image_path='./obstacle/o3.png', grid_size=40)



G = map.get_grid_matrix()
path = [0, 38, 74, 111, 148, 185, 222, 259, 296, 334, 374, 337, 493, 569, 695, 733, 734, 772, 887]
map.draw_path_found(convert_path_to_xy(path, G.shape[1]), (0,0), (32,26))


modified = delete_nodes(path, G)
print('modified: ', modified)


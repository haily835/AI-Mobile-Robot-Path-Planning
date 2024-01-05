import time
from a_star.search import astar_search, path_states, dynamic_weighted_astar_search
from path_smooth.path_smooth import simplify_path
from math import sqrt

def cal_runtime(explorer):
    a_runtime = 0
    
    for i in range(100):
        start_time = time.time()
        node = astar_search(explorer)
        end_time = time.time()
        # Calculate the elapsed time
        a_runtime += (end_time - start_time)

    b_runtime = 0
    
    goal = explorer.goal
    
    def h(node):
        h1 = abs(goal[0] - node.state[0])
        h2 = abs(goal[1] - node.state[1])
        return h1 + h2 + (sqrt(2) - 2) * min(h1, h2)
    for i in range(100):
        start_time = time.time()
        node = dynamic_weighted_astar_search(explorer, h=h)
        end_time = time.time()
        # Calculate the elapsed time
        b_runtime += (end_time - start_time)

    c_runtime = 0
    
    for i in range(100):
        start_time = time.time()
        node = dynamic_weighted_astar_search(explorer, h=h)
        path = path_states(node)
        simplified_path = simplify_path(path, explorer.map)
        end_time = time.time()
        # Calculate the elapsed time
        c_runtime += (end_time - start_time)

    
    print('a_runtime: ', a_runtime/100)
    print('b_runtime: ', b_runtime/100)
    print('c_runtime: ', c_runtime/100)
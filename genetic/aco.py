import numpy as np
from distance import distance
import numpy as np
from grid_number_to_xy import grid_number_to_xy

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

def calc_distance_matrix(G, end_coord):
    # Initialize the distance matrix D
    rows, cols = G.shape[0], G.shape[1]
    D = np.zeros((rows, cols))
    end_r, end_c = end_coord
    # Calculate distances for each pair of points
    for i in range(rows):
        for j in range(cols):
            if G[i, j] == 0:
                D[i, j] = ((i - end_r) ** 2 + (j - end_c) ** 2) ** 0.5
            else:
                # If there is no path, set distance to infinity
                D[i, j] = np.inf  # When i = j, the distance is not calculated; it should be 0, but the reciprocal is taken later, using eps for floating-point relative precision

    # Set a small distance for the destination point
    D[end_r, end_c] = 0.05
    return D
    
def calc_heuristic_factor(D):
    """
    Parameters:
        - D is the distance matrix

    Return: 
        - The heuristic factor (Eta) as the reciprocal of the distance to the destination
    """
    # Calculate the heuristic factor (Eta) as the reciprocal of the distance to the destination
    Eta = 1 / D
    return Eta

def calc_pheromone(Eta):
    # Initialize the pheromone matrix (Tau) with a multiplier for innovation
    Tau = 10 * Eta  # Innovative point
    return Tau


# Calculate the movement matrix
# The 8 columns is associated with different directions or moves in a grid,
def calc_movement_matrix(G):
    rows, cols = G.shape[0], G.shape[1]
    D_move = []
    for i in range(rows * cols):
        D_move.append([])
        for j in range(8):
            D_move[i].append('')

    for point in range(rows * cols):
        r, c = grid_number_to_xy(point, cols)
        if G[r, c] == 0:
            actions = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),           (0, 1),
                        (1, -1), (1, 0), (1, 1)]
            for i, action in enumerate(actions):
                end_r, end_c = r + action[0], c + action[1]
                if 0 <= end_r < rows \
                    and 0 <= end_c < cols \
                    and G[end_r, end_c] == 0:
                    
                    D_move[point][i] = end_r * cols + end_c

    return D_move


# Checkpoint: Movement matrix and adjacency matrix calculations completed without errors
# Start iteration
# number of ants = 2, NC_max = 10 => each elements in the route array have 2 paths

# m = 50  # m is the number of ants
# NC_max = 5  # maximum number of iterations
# Alpha = 2  # Alpha is the parameter representing the importance of pheromones
# Beta = 6  # Beta is the parameter representing the importance of the heuristic factor
# Rho = 0.1  # Rho is the pheromone evaporation coefficient
# Q = 1  # pheromone strength coefficient
# Tau = np.ones((n, n))  # Tau is the pheromone matrix
# NC = 0  # current iteration counter
# s = 0  # starting point coordinates in the matrix
# position_e = 99  # destination coordinates in the matrix
# r_e, c_e = grid_number_to_xy(position_e, n)


# min_PL_NC_ant = float('inf')  # minimum path length among ants
# min_ant = 0  # ant index with the minimum path
# min_NC = 0  # iteration index with the minimum path
def aco(G, start, end, m, NC_max, Alpha=2, Beta=6, Rho=0.1, Q=1, min_PL_NC_ant=float('inf')):
    rows, cols = G.shape[0], G.shape[1]

    D_move = calc_movement_matrix(G)
    start_grid_num = start[0] * cols + start[1]
    end_grid_num = end[0] * cols + end[1]
    D = calc_distance_matrix(G=G, end_coord=end)

    Eta = calc_heuristic_factor(D)
    Tau = calc_pheromone(Eta=Eta)

    routes = [[] for _ in range(NC_max)]  # Store the path of each ant for each iteration
    PL = np.zeros((NC_max, m))  # Store the path lengths of each ant for each iteration
    NC = 1
    while NC < NC_max:
        for ant in range(m):
            current_position = start_grid_num  # Current position is the starting point
            path = [start_grid_num]  # Initialize the path
            visited = [start_grid_num]

            PL_NC_ant = 0  # Initialize the path length
            D_D = D_move.copy()  # D_D is an intermediate matrix to avoid modifying D_move directly
            D_work = D_D[current_position]  # Send information about the next possible nodes from the current point to D_work

            # Exclude the visited
            next_nodes = [node for node in D_work if (node != '' and not (node in visited))]

            while current_position != end_grid_num and len(next_nodes) >= 1:
                p = np.zeros(len(next_nodes))

                # Calculate the probability to move to each reachable node
                for i in range(len(next_nodes)):
                    r, c = grid_number_to_xy(next_nodes[i], cols)  # Calculate the row and column of the reachable point
                    p[i] = (Tau[r, c] ** Alpha) * (Eta[r, c] ** Beta) # Probability to move to each reachable node
                
                p /= np.sum(p)  # Normalize the probabilities
                pcum = np.cumsum(p)  # Cumulative probabilities
                select = np.where(pcum >= np.random.rand())[0]  # Roulette wheel selection for the next node
                
                to_visit = next_nodes[select[0]]  # Move to the selected next node

                # Arrive at the next node
                path.append(to_visit)
                dis = distance(current_position, to_visit, cols)  # Calculate the distance to the next node
                PL_NC_ant += dis  # Accumulate the distance
                current_position = to_visit  # Update the current position
                
                visited.append(current_position)
                D_work = D_D[int(current_position)]  # Send information about the next reachable node from the current node to D_work

                next_nodes = [node for node in D_work if (node != '' and not (node in visited))]

            #### END Path finding
            # Iterate all ants in one iteration
            routes[NC].append(path)  # Record the path of the ant
            
            if path[-1] == end_grid_num:
                PL[NC, ant] = PL_NC_ant  # Record the distance traveled by ants reaching the destination
                if PL_NC_ant < min_PL_NC_ant:
                    min_PL_NC_ant = PL_NC_ant  # Record the iteration and ant with the shortest path
            else:
                PL[NC, ant] = 0

        delta_Tau = np.zeros((rows, cols))  # Initialize the pheromone variable

        for j3 in range(m):
            if PL[NC, ant]:
                rout = routes[NC][ant]
                tiaoshu = len(rout) - 1  # Find the number of times ants reach the destination
                value_PL = PL[NC, ant]  # Distance traveled by ants reaching the destination
                for u in range(0, tiaoshu):
                    r3, c3 = grid_number_to_xy(rout[u], cols)
                    delta_Tau[r3, c3] += Q / value_PL  # Calculate the value of the pheromone variable

        Tau = (1 - Rho) * Tau + delta_Tau  # Update the pheromone
        NC += 1


    ### END Ant colony optimization

    ## Generate initial population from routes found by all ants
    new_population = []
    for NC in range(NC_max):
        for i in range(m):
            if PL[NC, i]:
                new_population.append(routes[NC][i])
    
    return new_population


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

    print(aco(
        G, start=[0,0], end=[9,9], m=5, NC_max=3
    ))
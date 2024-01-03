import numpy as np
from .grid_number_to_yx import grid_number_to_yx

def calculate_angle(A, B, C):
    BA = A - B
    BC = C - B

    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    cosine_theta = dot_product / (norm_BA * norm_BC)

    # Use arccosine to get the angle in radians
    angle_radians = np.arccos(cosine_theta)

    degrees = angle_radians * (180 / np.pi)
    return degrees

def cal_smooth_value(new_population, grid_size, verbose=False):
    # Get the number of populations in the new_population list
    n = len(new_population)
    smooth_value = np.zeros(n)

    for i in range(n):
        if verbose: print(f'Path {i+1}')
        path = new_population[i]
        m = len(path)

        # Iterate over each point in the population starting from the third point
        for j in range(2, m):
            a = np.array(grid_number_to_yx(path[j - 2], grid_size))[::-1]
            b = np.array(grid_number_to_yx(path[j - 1], grid_size))[::-1]
            c = np.array(grid_number_to_yx(path[j], grid_size))[::-1]
            
            angle = calculate_angle(np.array(a), np.array(b), np.array(c))
            if verbose: print(f'Angle {j-2} {j-1} {j}: ', angle)
            if angle < 90:
                smooth_value[i] += 500
            elif angle == 90:
                smooth_value[i] += 20
            else:
                smooth_value[i] += 4
        
    return smooth_value


# population_data = [
   
# ]

# # Call the calculation_smooth_value function with the example data
# result = cal_smooth_value(population_data)

# # Print the result
# print(result)

import numpy as np


def calculate_angle(A, B, C):
    AB = B - A
    BC = C - B

    dot_product = np.dot(AB, BC)
    norm_AB = np.linalg.norm(AB)
    norm_BC = np.linalg.norm(BC)

    cosine_theta = dot_product / (norm_AB * norm_BC)

    # Use arccosine to get the angle in radians
    angle_radians = np.arccos(cosine_theta)

    # Express the angle in terms of pi
    angle_in_pi = angle_radians / np.pi

    return angle_in_pi

def cal_smooth_value(new_population, grid_size):
    # Get the number of populations in the new_population list
    n = len(new_population)
    smooth_value = np.zeros(n)

    for i in range(n):
        path = new_population[i]
        m = len(path)

        # Iterate over each point in the population starting from the third point
        for j in range(2, m):
            a = path[j - 2]
            b = path[j - 1]
            c = path[j]

            angle = calculate_angle(np.array(a), np.array(b), np.array(c))
            if angle < np.pi / 2:
                smooth_value[i] += 500
            elif angle == np.pi / 2:
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

import numpy as np

def calculate_angle(A, B, C):
    BA = A - B
    BC = C - B

    dot_product = np.dot(BA, BC)
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    cosine_theta = dot_product / (norm_BA * norm_BC + 0.000001)

    # Use arccosine to get the angle in radians
    angle_radians = np.arccos(cosine_theta)

    degrees = angle_radians * (180 / np.pi)
    return degrees


def cal_path_length(path):
    sum_len = 0
    for j in range(len(path) - 1):
        p1 = path[j]
        p2 = path[j + 1]
        dis = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
        sum_len += dis
    return sum_len


def cal_bend(path):
    bend = 0
    for j in range(2, len(path)):
        a = np.array(path[j - 2])
        b = np.array(path[j - 1])
        c = np.array(path[j])
        
        angle = calculate_angle(np.array(a), np.array(b), np.array(c))
        
        if angle < 179:
            bend += 1
    return bend

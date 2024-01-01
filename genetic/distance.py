from .grid_number_to_yx import grid_number_to_yx

def distance(w, to_visit, n):

    r1, c1 = grid_number_to_yx(w, n)
    r2, c2 = grid_number_to_yx(to_visit, n)
    
    # Calculate Euclidean distance
    dis = ((r1 - r2)**2 + (c1 - c2)**2)**0.5

    return dis


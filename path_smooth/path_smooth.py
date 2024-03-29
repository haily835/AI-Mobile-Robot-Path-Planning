import matplotlib.pyplot as plt
from obstacle.obstacle_map import Map
from shapely.geometry import LineString, Polygon
from matplotlib.patches import Rectangle

def is_line_through_rectangle(x1, y1, x2, y2, rectangle_vertices):
    line = LineString([(x1, y1), (x2, y2)])
    rectangle = Polygon(rectangle_vertices)

    return line.intersects(rectangle)

def find_next_turn(path_center_points, obstacle_rectangles, start_index, verbose=True):
    p1 = path_center_points[start_index]
    # print('p1: ', p1)
    # print('current node: ', start_index)
    i = start_index + 1

    while i < len(path_center_points) - 2:
        p2 = path_center_points[i]
        necessary_turn = False

        for rec in obstacle_rectangles:
            necessary_turn = is_line_through_rectangle(p1[0], p1[1], p2[0], p2[1], rec)
            if necessary_turn: break

        # If it is a neccessary turn => the prev nodes must be added
        if necessary_turn:
            # print('necessary_turn: ', i - 1)
            return i - 1
        else:
            # print('skip: ', i)
            i += 1
    return i

def simplify_path(path, map: Map):
    simplified_path = [path[0]]  # Start with the initial node
    obstacles = map.obstacles
    grid_size = map.grid_size
    
    obstacle_rectangles = []
    for o in obstacles:
        x, y = o
        
        rect_coords = (x * grid_size, y * grid_size)
        rect = Rectangle(rect_coords, grid_size, grid_size, linewidth=1)
        rect_points = rect.get_corners()

        obstacle_rectangles.append(rect_points)

    path_center_points = []
    for coords in path:
        x, y = coords
        center_coords = (x * grid_size + 0.5 * grid_size, y * grid_size + 0.5 * grid_size)
        path_center_points.append(center_coords)
    

    i = 0
    while i < len(path_center_points) - 2:
        next_turn_index = find_next_turn(path_center_points, obstacle_rectangles, i)
        simplified_path.append(path[next_turn_index])
        if i != next_turn_index:
            i = next_turn_index
        else:
            i += 1

    # Add the target node
    simplified_path.append(path[-1])

    return simplified_path

def plot_path(path, obstacles):
    fig, ax = plt.subplots()

    # Plot obstacles
    for obstacle in obstacles:
        poly = Polygon(list(obstacle.exterior.coords))
        ax.add_patch(plt.Polygon(poly.exterior.coords, edgecolor='gray', facecolor='gray'))

    # Plot the original path
    ax.plot(*zip(*path), marker='o', label='Original Path')

    # Simplify the path
    simplified_path = simplify_path(path, obstacles)
    ax.plot(*zip(*simplified_path), marker='o', label='Simplified Path', linestyle='dashed')

    ax.legend()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    plt.show()


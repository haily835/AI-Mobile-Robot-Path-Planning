import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString, Point, Polygon
from obstacle.obstacle_map import Map

def is_valid_edge(start, end, obstacles):
    edge = LineString([start, end])

    # Check if any point on the line segment intersects with any obstacles
    for obstacle in obstacles:
        if obstacle.intersects(edge):
            return False
    return True

def find_turning_point(start, end, obstacles):
    # Split the line segment between start and end into smaller segments
    num_segments = 10
    intermediate_points = np.linspace(start, end, num_segments)

    # Find the first point that intersects with an obstacle
    for point in intermediate_points:
        point = Point(point)
        for obstacle in obstacles:
            if obstacle.contains(point):
                return tuple(point.coords[0])

    # If no turning point is found, return the original end point
    return end


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

# Example usage with the new path
# path = [(1, 1), (1, 4), (3, 4), (5, 7), (9, 1)]
# obstacle = [(4, 2), (6, 2), (6, 4), (4, 4)]  # Example obstacle as a list of vertices
# obstacles = [Polygon(obstacle)]

# plot_path(path, obstacles)
from shapely.geometry import LineString, Polygon
from matplotlib.patches import Rectangle

def is_line_through_rectangle(x1, y1, x2, y2, rectangle_vertices):
    line = LineString([(x1, y1), (x2, y2)])
    rectangle = Polygon(rectangle_vertices)

    return line.intersects(rectangle)

def find_next_turn(path_center_points, obstacle_rectangles, start_index):
    p1 = path_center_points[start_index]
    print('p1: ', p1)
    i = start_index + 1

    while i < len(path_center_points) - 2:
        p2 = path_center_points[i]
        necessary_turn = False

        for rec in obstacle_rectangles:
            necessary_turn = is_line_through_rectangle(p1[0], p1[1], p2[0], p2[1], rec)
            if necessary_turn: break

        # If it is a neccessary turn;
        #   then add it to the simplified_path
        #   start searching for next node from it
        if necessary_turn: 
            print(f'{p2} is added')
            return i - 1
        else:
            # print(f'{p2} is skipped')
            # Else skip this node and start search the next node
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
        # rectangles_vertices = [
        #     [x, y],             [x + grid_size, y],
        #     [y, y + grid_size], [x + grid_size, y + grid_size]
        # ]
        # print(rect_points)
        # obstacle_rectangles.append(rectangles_vertices)
        # if x==1 and y ==8:
        #     print(rect_points.tolist())
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

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import random

class Map:
    def __init__(self, image_path, grid_size):
        """
        Initialize the ImageGrid object with the specified image, grid size, and padding size.

        Parameters:
        - image_path (str): The path to the black-and-white image file.
        - grid_size (int): The size of each grid cell in pixels.
        """
        # Load the black-and-white image
        self.image = plt.imread(image_path)

        # Set the grid size
        self.grid_size = grid_size

        # Calculate the number of rows and columns in the grid
        self.y_lim = math.ceil(self.image.shape[0] / self.grid_size)
        self.x_lim = math.ceil(self.image.shape[1] / self.grid_size)
        self.obstacles = []
        
        for y in range(self.y_lim):
            for x in range(self.x_lim):
                if self.is_obstacle_in_grid(x, y):
                    self.obstacles.append((x, y))

    def get_grid_matrix(self):
        G = np.zeros((self.y_lim, self.x_lim))
        
        for y in range(self.y_lim):
            for x in range(self.x_lim):
                if self.is_obstacle_in_grid(x, y):
                    G[y][x] = 1
                else:
                    G[y][x] = 0
        return G
    
    def is_obstacle_in_grid(self, x, y):
        """
        Check whether a small grid at the specified row and column contains a black portion.

        Parameters:
        - row: Row index of the grid
        - col: Column index of the grid

        Returns:
        - True if the grid contains a black portion (obstacle), False otherwise.
        """
        # Check whether the current node lies within the map
        if y > (self.y_lim - 1) or x > (self.x_lim - 1): return True
        if y < 0 or x < 0: return True
        grid_size = self.grid_size
        
        start_y, end_y = y * grid_size, (y + 1)* grid_size
        start_x, end_x = x * grid_size, (x + 1) * grid_size

        if np.any(self.image[start_y:end_y , start_x:end_x] == 0):
            return True
        
        return False  # If none of the surrounding grids contains an obstacle, consider the main grid as obstacle
    
    def draw_rect(self, ax, coords, edgecolor='r', facecolor='none', plot_center_point=False):
        
        x, y = coords

        # Calculate the coordinates of the rectangle
        rect_coords = (x * self.grid_size, y * self.grid_size)

        # Create and add the rectangle patch
        rect = Rectangle(rect_coords, self.grid_size, self.grid_size,
                         linewidth=1, edgecolor=edgecolor, facecolor=facecolor)
        ax.add_patch(rect)

        if plot_center_point:
            # Calculate the coordinates of the center point
            center_coords = (rect_coords[0] + 0.5 * self.grid_size, rect_coords[1] + 0.5 * self.grid_size)

            # Plot the center point
            ax.plot(*center_coords, marker='o', color='black')


    def draw_grid(self, ax):
        # Draw mesh grid
        for i in range(1, self.x_lim):
            x = i * self.grid_size
            ax.axvline(x, color="#E5E4E2", linestyle="--", linewidth=0.5)

        for i in range(1, self.y_lim):
            y = i * self.grid_size
            ax.axhline(y, color="#E5E4E2", linestyle="--", linewidth=0.5)

        # Draw obstacles
        for o in self.obstacles:
            self.draw_rect(ax, o, edgecolor='r', facecolor='none')
        ax.invert_yaxis()
        
        # Draw x and y axes
        ax.axhline(0, color="blue", linewidth=2)
        ax.axvline(0, color="blue", linewidth=2)
        ax.imshow(self.image, origin="upper", cmap='gray')
        

        # Draw arrows on x and y axes
        # ax.arrow(self.cols * self.grid_size, 0, 0.5 * self.grid_size, 0, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
        # ax.arrow(0, self.rows * self.grid_size, 0, 0.5 * self.grid_size, head_width=0.2, head_length=0.2, fc='blue', ec='blue')

        # Draw axis ticks and labels
        if self.y_lim < 40 and self.x_lim < 40:
            ax.set_xticks(np.arange(0, (self.x_lim + 1) * self.grid_size, self.grid_size))
            ax.set_yticks(np.arange(0, (self.y_lim + 1) * self.grid_size, self.grid_size))
            ax.set_xticklabels(np.arange(0, self.x_lim + 1), fontsize=8)
            ax.set_yticklabels(np.arange(0, self.y_lim + 1), fontsize=8)
        else:
            ax.set_xticks([0, self.x_lim * self.grid_size])
            ax.set_yticks([0, self.y_lim * self.grid_size])
            ax.set_xticklabels([0, self.x_lim])
            ax.set_yticklabels([0, self.y_lim])

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Set grid
        ax.grid(True, linestyle='--', linewidth=0.5)
    

    def draw_coordinate_system(self, fig=None, ax=None):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        
        if fig and ax:
            self.draw_grid(ax)
        else:
            fig, ax = plt.subplots()
            self.draw_grid(ax)
            plt.show()
        

    def plot_center_points(self, ax, rectangle_coords_list, color='blue'):
        center_points = []

        for coords in rectangle_coords_list:
            x, y = coords
            center_coords = (x * self.grid_size + 0.5 * self.grid_size, y * self.grid_size + 0.5 * self.grid_size)
            center_points.append(center_coords)
        for center_point in center_points:
            ax.scatter(center_point[0], center_point[1], color=color, s=23, label='Path')
        # Connect the center points with lines
        for i in range(len(center_points) - 1):
            ax.plot([center_points[i][0], center_points[i + 1][0]],
                    [center_points[i][1], center_points[i + 1][1]], color=color, linestyle='-', linewidth=1)
                
                
    def draw_path_found(self, states, initial, goal, reached = [], fig=None, ax=None):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        if not (fig or ax):
            fig, ax = plt.subplots()
            self.draw_grid(ax)
        
        # Draw reached states
        for r in reached:
            self.draw_rect(ax, r, edgecolor='#D9D9D9', facecolor='#D9D9D9')
        
        self.plot_center_points(ax, states)
        self.draw_rect(ax, initial, edgecolor='green', facecolor='green')
        self.draw_rect(ax, goal, edgecolor='orange', facecolor='orange')

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Reached Node'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Start'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Path'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Goal')
        ]

        # Add legend
        ax.legend(handles=legend_elements, loc='upper right')

        if not (fig or ax): 
            plt.show()

    def draw_multiple_path_found(self, paths, initial, goal, reached = [], fig=None, ax=None):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        if not (fig or ax):
            fig, ax = plt.subplots()
            self.draw_grid(ax)
        
        # Draw reached states
        for r in reached:
            self.draw_rect(ax, r, edgecolor='#D9D9D9', facecolor='#D9D9D9')
        
        legend_elements = []

        for path in paths:
            nodes, color, label = path
            self.plot_center_points(ax, nodes, color)
            
            legend = Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
            legend_elements.append(legend)
        
        self.draw_rect(ax, initial, edgecolor='green', facecolor='green')
        self.draw_rect(ax, goal, edgecolor='orange', facecolor='orange')

        legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Start'))
        legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='Goal'))
        
        # Add legend
        ax.legend(handles=legend_elements, loc='upper right')

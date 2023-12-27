import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Rectangle

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
        self.rows = math.ceil(self.image.shape[0] / self.grid_size)
        self.cols = math.ceil(self.image.shape[1] / self.grid_size)
        self.obstacles = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_obstacle_in_grid(row, col):
                    self.obstacles.append((row,col))

    def is_obstacle_in_grid(self, y, x):
        """
        Check whether a small grid at the specified row and column contains a black portion.

        Parameters:
        - row: Row index of the grid
        - col: Column index of the grid

        Returns:
        - True if the grid contains a black portion (obstacle), False otherwise.
        """
        # Check whether the current node lies within the map
        if y > (self.rows - 1) or x > (self.cols - 1): return True
        if y < 0 or x < 0: return True
        grid_size = self.grid_size
        
        start_y, end_y = y * grid_size, (y + 1)* grid_size
        start_x, end_x = x * grid_size, (x + 1) * grid_size

        if np.any(self.image[start_y:end_y , start_x:end_x] == 0):
            return True
        
        return False  # If none of the surrounding grids contains an obstacle, consider the main grid as obstacle
    
    def draw_rect(self, ax, coords, edgecolor='r', facecolor='none', plot_center_point=False):
        row, col = coords

        # Calculate the coordinates of the rectangle
        rect_coords = (col * self.grid_size, row * self.grid_size)

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
        for i in range(1, self.cols):
            x = i * self.grid_size
            ax.axvline(x, color="#E5E4E2", linestyle="--", linewidth=0.5)

        for i in range(1, self.rows):
            y = i * self.grid_size
            ax.axhline(y, color="#E5E4E2", linestyle="--", linewidth=0.5)

        # Draw obstacles
        for o in self.obstacles:
            self.draw_rect(ax, o, edgecolor='r', facecolor='none')
        ax.invert_yaxis()
        
        # Draw x and y axes
        ax.axhline(0, color="blue", linewidth=2)
        ax.axvline(0, color="blue", linewidth=2)
        ax.imshow(self.image, origin="upper")
        
        height, width = self.image.shape[:2]
        rect = Rectangle((0, 0), width, height, linewidth=2, edgecolor='pink', facecolor='none')
        ax.add_patch(rect)

        # Draw arrows on x and y axes
        # ax.arrow(self.cols * self.grid_size, 0, 0.5 * self.grid_size, 0, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
        # ax.arrow(0, self.rows * self.grid_size, 0, 0.5 * self.grid_size, head_width=0.2, head_length=0.2, fc='blue', ec='blue')

        # Draw axis ticks and labels
        if self.cols < 30 and self.rows < 30:
            ax.set_xticks(np.arange(0, (self.cols + 1) * self.grid_size, self.grid_size))
            ax.set_yticks(np.arange(0, (self.rows + 1) * self.grid_size, self.grid_size))
            ax.set_xticklabels(np.arange(0, self.cols + 1))
            ax.set_yticklabels(np.arange(0, self.rows + 1))
        else:
            ax.set_xticks([0, self.cols * self.grid_size])
            ax.set_yticks([0, self.rows * self.grid_size])
            ax.set_xticklabels([0, self.cols])
            ax.set_yticklabels([0, self.rows])

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Set grid
        ax.grid(True, linestyle='--', linewidth=0.5)
    

    def draw_coordinate_system(self):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        fig, ax = plt.subplots()
        self.draw_grid(ax)
        plt.show()

    def plot_center_points(self, ax, rectangle_coords_list):
        center_points = []

        for coords in rectangle_coords_list:
            row, col = coords
            center_coords = (col * self.grid_size + 0.5 * self.grid_size, row * self.grid_size + 0.5 * self.grid_size)
            center_points.append(center_coords)
        
        # Connect the center points with lines
        for i in range(len(center_points) - 1):
            ax.plot([center_points[i][0], center_points[i + 1][0]],
                    [center_points[i][1], center_points[i + 1][1]], color='blue', linestyle='-', linewidth=2)
                
                
    def draw_path_found(self, states, initial, goal, reached = []):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        fig, ax = plt.subplots()
        self.draw_grid(ax)
        
        # Draw path
        
        for r in reached:
            self.draw_rect(ax, r, edgecolor='#D9D9D9', facecolor='#D9D9D9')
        
        # for s in states:
        #     self.draw_rect(ax, s, edgecolor='blue', facecolor='green', plot_center_point=True)
        
        self.plot_center_points(ax, states )
        self.draw_rect(ax, initial, edgecolor='green', facecolor='green')
        self.draw_rect(ax, goal, edgecolor='orange', facecolor='orange')

        
        plt.show()


    
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

class Map:
    def __init__(self, image_path, grid_size):
        # Load the black-and-white image
        self.image = plt.imread(image_path)
        self.flipped_image = np.flipud(self.image)

        # Set the grid size
        self.grid_size = grid_size

        # Calculate the number of rows and columns in the grid
        self.rows = self.image.shape[0] // self.grid_size
        self.cols = self.image.shape[1] // self.grid_size

    def is_obstacle_in_grid(self, row, col):
        """
        Check whether a small grid at the specified row and column contains a black portion.

        Parameters:
        - row: Row index of the grid
        - col: Column index of the grid

        Returns:
        - True if the grid contains a black portion (obstacle), False otherwise.
        """
        # Calculate the coordinates of the bottom-left corner of the grid
        bottom_left_x = col * self.grid_size
        bottom_left_y = (self.rows - row - 1) * self.grid_size  # Flip the row index

        # Extract the region corresponding to the grid
        grid_region = self.flipped_image[bottom_left_y:bottom_left_y + self.grid_size, bottom_left_x:bottom_left_x+self.grid_size]

        # Check if any pixel in the grid is black (value = 0)
        return np.any(grid_region == 0)

    def visualize_coordinate_system(self):
        """
        Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows.
        """
        fig, ax = plt.subplots()

        # Draw mesh grid
        for i in range(1, self.cols):
            x = i * self.grid_size
            ax.axvline(x, color="black", linestyle="--", linewidth=0.5)

        for i in range(1, self.rows):
            y = i * self.grid_size
            ax.axhline(y, color="black", linestyle="--", linewidth=0.5)


        ax.imshow(self.image, extent=[0, self.cols * self.grid_size, 0, self.rows * self.grid_size])

        # Draw obstacles
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_obstacle_in_grid(row, col):
                    rect = Rectangle((col * self.grid_size, (self.rows - row - 1) * self.grid_size), self.grid_size, self.grid_size,
                                     linewidth=1, edgecolor='r', facecolor='none')
                    ax.add_patch(rect)

        # Draw x and y axes
        ax.axhline(0, color="blue", linewidth=2)
        ax.axvline(0, color="blue", linewidth=2)

        # Draw arrows on x and y axes
        ax.arrow(self.cols * self.grid_size, 0, 0.5 * self.grid_size, 0, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
        ax.arrow(0, self.rows * self.grid_size, 0, 0.5 * self.grid_size, head_width=0.2, head_length=0.2, fc='blue', ec='blue')

        # Draw axis ticks and labels
        ax.set_xticks(np.arange(0, (self.cols + 1) * self.grid_size, self.grid_size))
        ax.set_yticks(np.arange(0, (self.rows + 1) * self.grid_size, self.grid_size))
        ax.set_xticklabels(np.arange(0, self.cols + 1))
        ax.set_yticklabels(np.arange(0, self.rows + 1))

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Set grid
        ax.grid(True, linestyle='--', linewidth=0.5)

        plt.show()

# Example usage:
image_path = "./obstacle.png"
grid_size = 300

# Create a Map instance
my_map = Map(image_path, grid_size)

# Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows
my_map.visualize_coordinate_system()

import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Rectangle

class Map:
    def __init__(self, image_path, grid_size, padding_size):
        # Load the black-and-white image
        self.image = plt.imread(image_path)
        self.flipped_image = np.flipud(self.image)

        # Set the grid size
        self.grid_size = grid_size

        # Set the padding size
        self.padding_size = padding_size

        # Calculate the number of rows and columns in the grid
        self.rows = math.ceil(self.image.shape[0] / self.grid_size)
        self.cols = math.ceil(self.image.shape[1] / self.grid_size)

    def is_obstacle_in_grid(self, row, col):
        """
        Check whether a small grid at the specified row and column contains a black portion.

        Parameters:
        - row: Row index of the grid
        - col: Column index of the grid

        Returns:
        - True if the grid contains a black portion (obstacle), False otherwise.
        """
        # Iterate over the surrounding grids with padding
        for i in range(-self.padding_size, self.padding_size + 1):
            for j in range(-self.padding_size, self.padding_size + 1):
                # Calculate the coordinates of the bottom-left corner of the surrounding grid
                surround_bottom_left_x = (col + j) * self.grid_size
                surround_bottom_left_y = (self.rows - row - 1 - i) * self.grid_size  # Flip the row index

                # Check if the surrounding grid is within the image boundaries
                if (surround_bottom_left_x >= 0 and surround_bottom_left_y >= 0 and
                        surround_bottom_left_x + self.grid_size <= self.image.shape[1] and
                        surround_bottom_left_y + self.grid_size <= self.image.shape[0]):
                    # Check if any pixel in the surrounding grid is black (value = 0)
                    if np.any(self.flipped_image[surround_bottom_left_y:surround_bottom_left_y+self.grid_size,
                                                surround_bottom_left_x:surround_bottom_left_x+self.grid_size] == 0):
                        return True  # If any surrounding grid contains an obstacle, consider the main grid as obstacle

        return False  # If none of the surrounding grids contains an obstacle, consider the main grid as obstacle
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

        print(self.rows)
        print(self.cols)
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

if __name__ == "main":
    # Example usage:
    image_path = "./images/final_path.png"
    grid_size = 25
    padding_size = 2  # Set the desired padding size

    # Create a Map instance
    my_map = Map(image_path, grid_size, padding_size)

    # Visualize the coordinate system with labeled axes, mesh grid, obstacles, and arrows
    my_map.visualize_coordinate_system()

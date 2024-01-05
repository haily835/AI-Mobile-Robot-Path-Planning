# AI Path Planning Problem - A Comparision of A star search and Genetic algorithm

### Project descriptions:
The report of the project can be found here
https://www.overleaf.com/project/6597318ab7308c7fecfecce3




### Project structure and File Descriptions

#### Grid / Map implementation
- **obstacle/obstacle_map.py**: A Map class with function to convert the **gray scale** image file to a mesh grid. An image is divided into smaller cells of size "grid_size". A cell contain "grid_size" pixels in it. Cells that contains obstacle will be marked as red rectange. This class also contains functions to plot the path found by different algorithms.

- **obstacle/random_map.py**: In case we want to generate random map with obstacles we can use this script to generate images. The images generated will be stored in **generated_images** folder.


#### A Star algorithm
- **a_star/explorer.py**: Path finding as a search problem (Follow the provided code from An Introduction to AI text book)
- **a_star/search.py**: Search algorithm, including traditional A star (with Euclidian/ Proposed heurisics) and the dynamic weighted a star. (Follow the suggestion in the paper https://ieeexplore.ieee.org/document/8397830). 


#### Genetic algorithm implemenation
- **genetic/grid_number_to_yx.py**: the grids are number from top left corner (left -> right, top -> bottom). The grid at the top left is numbered as 0. This file contains the functions to convert the grid number to the y,x coordinates. y = floor(position // number_of_columns), x = position mod number_of_columns
- **genetic/aco.py**: Ant colony optimization algorithm to generate the initial population (Follow X.LDai, S Long,Z.W Zhang and D.  Gong, “Mobile Robot Path Planning Based on Ant Colony Algorithm With A* Heuristic Method” paper)
- Note: The following implemenations are based on the paper Yibo Li ,Dingguang Dong ,Xiaonan Guo, "Mobile Robot Path Planning based on Improved Genetic Algorithm With A-star Heuristic Method" 
- **genetic/cal_path_value.py**: calculation of the sum  Euclidean distance of a path
- **genetic/cal_smooth_value.py**: calculate the sum of path smooth value based on the angle that the robot need to turn at each node on path.
- **genetic/selection.py**: select the parents based on the fitness value = Inf - w1 * path_length - w2 * path_smooth. (roulette wheel selection)
- **genetic/crossover.py**: single point crossover with probability
- **genetic/mutation.py**: select the random grid with probability, replace it with its nearby grid. Ensure that the new grid is valid - within the boundary, the lines connect with the previous and after grids dont cross the obstacles, etc... 
- **genetic/insertion.py**: insert some additional grids to lower the turn angles.
- **genetic/deletion.py**: delete grids to smoother the path. Ensure that the grids along 2 points can be removed and the 2 points can be connected without passing the ostacles.
- **genetic/distance.py**: calculate the Euclidean distance between 2 points (grid number).


#### Path smoothing
**path_smooth/path_smooth.py**: Connect consecutive grids to provide better path.


#### Sample maps
-  **generated_images**: This folder contains the manually created images and auto generated images. Note that the U_shape maps, o1 => o4 are used to test for experiments.


### Notebooks
- 10_grid_size: Test all algorthms with **generated_images/o3.png**. The cell size is small (10 pixels per cell). The complexity of the problem will be increased as this means that the search space is much more bigger, however the path return will be better.

- 40_grid_size: Test all algorthms with **generated_images/o3.png**. The cell size is big (40 pixels per cell). The complexity of the problem will be decrease.

- u_shape: Test all algorthms with **generated_images/u_shape.png**. This one is used to test a scenerio when the robot may be stuck inside the U obstacles and can not get out.


### Commands
- **UI**: Contains options for the map (such as importing images or generating random images). User can choose the algorithm with configuration to find the path.

  ```bash
    python ui.py
  ```

- **Clone the Repository:**
  ```bash
  git clone https://github.com/haily835/AI-Mobile-Robot-Path-Planning
  ```

- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

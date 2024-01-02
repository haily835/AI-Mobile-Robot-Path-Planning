import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QFormLayout, \
    QRadioButton, QSpinBox, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox, QLCDNumber, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from obstacle.obstacle_map import Map
from obstacle.random_map import generate_image
from a_star.explorer import Explorer
from a_star.search import astar_search, path_states, dynamic_weighted_astar_search
from path_smooth.path_smooth import simplify_path
from genetic.genetic import genetic
import time
from math import sqrt
import random

# Set a seed for reproducibility
random.seed(42)

class MatplotlibWidget(QWidget):
    def __init__(self):
        super(MatplotlibWidget, self).__init__()

        self.initUI()

    def initUI(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plotImage(self, image_path, grid_size):
        self.ax.clear()
        # img = mpimg.imread(image_path)
        # self.ax.imshow(img)
        self.map = Map(image_path=image_path, grid_size=grid_size)
        self.map.draw_coordinate_system(self.figure, self.ax)
        # Refresh canvas
        self.canvas.draw()
        return self.map

    def plotStartGoalPoints(self, start_pos, goal_pos):
        # Plot start and goal points
        self.ax.clear()
        self.map.draw_coordinate_system(self.figure, self.ax)
        self.map.draw_rect(self.ax, start_pos, edgecolor='green', facecolor='g')
        self.map.draw_rect(self.ax, goal_pos, edgecolor='orange', facecolor='orange')
        # self.ax.plot(start_pos[0], start_pos[1], 'go', markersize=10, label='Start')
        # self.ax.plot(goal_pos[0], goal_pos[1], 'ro', markersize=10, label='Goal')

        # Refresh canvas
        # self.ax.legend()
        self.canvas.draw()

    def draw_path_found(self, path, initial, goal, reached = []):
        self.ax.clear()
        self.map.draw_coordinate_system(self.figure, self.ax)
        self.map.draw_path_found(path, initial, goal, reached, self.figure, self.ax)
        self.canvas.draw()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.matplotlib_widget = MatplotlibWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pathfinding Algorithm Configuration')
        self.setGeometry(100, 100, 1000, 500)

        self.createFormGroupBox()

        hbox = QHBoxLayout()
        hbox.addWidget(self.formGroupBox)
        hbox.addWidget(self.matplotlib_widget)

        self.setLayout(hbox)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox('Algorithm Configuration')
        layout = QFormLayout()

        # Image Form
        self.image_button = QPushButton('Select Image')
        self.image_button.clicked.connect(self.selectImage)
        self.random_image_button = QPushButton('Generate Random Map')
        self.random_image_button.clicked.connect(self.generateImage)

        self.image_label = QLabel('Image:')
        layout.addRow(self.image_button, self.random_image_button)
        layout.addRow(self.image_label)
        
        # Grid size
        self.grid_size_spinbox = QSpinBox()
        self.grid_size_spinbox.setValue(40)
        layout.addRow(QLabel('Grid size:'))
        layout.addRow(self.grid_size_spinbox)

        # Create map
        self.apply_button = QPushButton('Create map')
        self.apply_button.clicked.connect(self.plotImage)
        layout.addRow(self.apply_button)

        # Start Position Form
        self.start_x_edit = QSpinBox()
        self.start_y_edit = QSpinBox()
        startBox = QHBoxLayout()
        startBox.addWidget(self.start_x_edit)
        startBox.addWidget(self.start_y_edit)
        layout.addRow(QLabel('Start Position (x, y):'), startBox)
        
        # Goal Position Form
        self.end_x_edit = QSpinBox()
        self.end_y_edit = QSpinBox()
        endBox = QHBoxLayout()
        endBox.addWidget(self.end_x_edit)
        endBox.addWidget(self.end_y_edit)
        layout.addRow(QLabel('Goal Position (x, y):'), endBox)

        # Show Start Goal Button
        self.show_sg_button = QPushButton('Show Start Goal Point')
        self.show_sg_button.clicked.connect(self.plotStartGoalPoints)
        layout.addRow(self.show_sg_button)

        # Algorithm Selection Form

        # A star
        self.astar_euclidian_radio = QPushButton('A* Search (Euclidian Heuristic)')
        layout.addRow(self.astar_euclidian_radio)
        self.astar_euclidian_radio.clicked.connect(self.selectAStarEuclidian)
        
        
        
        self.astar_improved_radio = QPushButton('A* Search (Proposed Heuristic Dynamic Weight)')
        layout.addRow(self.astar_improved_radio)
        self.astar_improved_radio.clicked.connect(self.selectProposedAstar)
        
        self.astar_improved_smooth_radio = QPushButton('A* Search (Proposed Heuristic Dynamic Weight) + Smooth Path')
        layout.addRow(self.astar_improved_smooth_radio)
        self.astar_improved_smooth_radio.clicked.connect(self.selectProposedAstarPathSmooth)
        
        
        # Genetic
        layout.addRow(QLabel('<b>Genetic Algorithm</b>'))
        self.genetic_generation_spinbox = QSpinBox()
        self.genetic_generation_spinbox.setValue(100)
        layout.addRow(QLabel('Generations:'), self.genetic_generation_spinbox)

        self.genetic_init_pop_spinbox = QSpinBox()
        self.genetic_init_pop_spinbox.setValue(20)
        layout.addRow(QLabel('Number of ants:'),self.genetic_init_pop_spinbox)

        self.genetic_crossover_prob = QLineEdit()
        self.genetic_crossover_prob.setText('0.2')
        layout.addRow(QLabel('Crossover probability:'), self.genetic_crossover_prob)

        self.genetic_mutation_prob = QLineEdit()
        self.genetic_mutation_prob.setText('0.05')
        layout.addRow(QLabel('Mutation probability:'), self.genetic_mutation_prob)

        self.genetic_btn = QPushButton('Run Genetic')
        layout.addRow(self.genetic_btn)
        self.genetic_btn.clicked.connect(self.runGenetic)
        
        # Add everything to the form group box
        layout.addRow(QLabel('<b>Execution details:</b>'))
        self.execution = QLabel('.....')
        layout.addRow(self.execution)

        self.formGroupBox.setLayout(layout)

    def selectImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if fileName:
            self.image_label.setText(fileName)
            # Add logic to handle the selected image
            # self.matplotlib_widget.plotImage(fileName)

    def generateImage(self):
        fileName = generate_image()
        self.image_label.setText(fileName)

    def plotImage(self):
        # Add logic to plot the image using MatplotlibWidget
        image_path = self.image_label.text()
        grid_size = self.grid_size_spinbox.value()
        map = self.matplotlib_widget.plotImage(image_path, grid_size)
        self.map = map
        self.start_x_edit.setMinimum(0)
        self.start_x_edit.setMaximum(map.x_lim - 1)
        self.start_y_edit.setMinimum(0)
        self.start_y_edit.setMaximum(map.y_lim - 1)

        self.end_x_edit.setMinimum(0)
        self.end_x_edit.setMaximum(map.x_lim - 1)
        self.end_x_edit.setValue(map.x_lim - 1)
        self.end_y_edit.setMinimum(0)
        self.end_y_edit.setMaximum(map.y_lim - 1)
        self.end_y_edit.setValue(map.y_lim - 1)

    def plotStartGoalPoints(self):
        # Add logic to plot start and goal points on the image
        image_path = self.image_label.text()
        start_pos = (float(self.start_x_edit.text()), float(self.start_y_edit.text()))
        goal_pos = (float(self.end_x_edit.text()), float(self.end_y_edit.text()))
        self.matplotlib_widget.plotStartGoalPoints(start_pos, goal_pos)

    def selectAStarEuclidian(self):
        initial = (int(self.start_x_edit.text()), int(self.start_y_edit.text()))
        goal = (int(self.end_x_edit.text()), int(self.end_y_edit.text()))
        map = self.map
        if map.is_obstacle_in_grid(initial[0], initial[1]):
            QMessageBox.information(self, 'Invalid', 'Start point lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            print('Start point lie in obstacle space!!\nPlease try again')
            return
        if map.is_obstacle_in_grid(goal[0], goal[1]):
            QMessageBox.information(self, 'Invalid', 'Goal lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            return
        
        explorer = Explorer(map=map, initial=initial, goal=goal)
        start_time = time.time()
        node = astar_search(explorer)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.execution.setText(f"A* Search (Euclidian Heuristic)\nReached nodes: {len(explorer.reached.keys())}\nElapsed Time: {round(elapsed_time, 5)} seconds")
        
        # Plot path
        path = path_states(node)
        self.matplotlib_widget.draw_path_found(path, initial, goal, explorer.get_reached())
        
    def selectProposedAstar(self):
        initial = (int(self.start_x_edit.text()), int(self.start_y_edit.text()))
        goal = (int(self.end_x_edit.text()), int(self.end_y_edit.text()))
        map = self.map
        
        if map.is_obstacle_in_grid(initial[0], initial[1]):
            QMessageBox.information(self, 'Invalid', 'Start point lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            print('Start point lie in obstacle space!!\nPlease try again')
            return
        if map.is_obstacle_in_grid(goal[0], goal[1]):
            QMessageBox.information(self, 'Invalid', 'Goal lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            return
        
        def h(node):
            h1 = abs(goal[0] - node.state[0])
            h2 = abs(goal[1] - node.state[1])
            return h1 + h2 + (sqrt(2) - 2) * min(h1, h2)
        
        
        explorer = Explorer(map=map, initial=initial, goal=goal)
        start_time = time.time()
        node = dynamic_weighted_astar_search(explorer, h=h)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.execution.setText(f"A* Search (Proposed Heuristic Dynamic Weight)\nReached nodes: {len(explorer.reached.keys())}\nElapsed Time: {round(elapsed_time, 5)} seconds")
        
        # Plot path
        path = path_states(node)
        self.matplotlib_widget.draw_path_found(path, initial, goal, explorer.get_reached())
        
    def selectProposedAstarPathSmooth(self):
        initial = (int(self.start_x_edit.text()), int(self.start_y_edit.text()))
        goal = (int(self.end_x_edit.text()), int(self.end_y_edit.text()))
        map = self.map
        
        if map.is_obstacle_in_grid(initial[0], initial[1]):
            QMessageBox.information(self, 'Invalid', 'Start point lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            print('Start point lie in obstacle space!!\nPlease try again')
            return
        if map.is_obstacle_in_grid(goal[0], goal[1]):
            QMessageBox.information(self, 'Invalid', 'Goal lie in obstacle space!!\nPlease try again', QMessageBox.Ok)
            return
        
        def h(node):
            h1 = abs(goal[0] - node.state[0])
            h2 = abs(goal[1] - node.state[1])
            return h1 + h2 + (sqrt(2) - 2) * min(h1, h2)
        
        
        explorer = Explorer(map=map, initial=initial, goal=goal)
        start_time = time.time()
        node = dynamic_weighted_astar_search(explorer, h=h)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.execution.setText(f"A* Search (Proposed Heuristic Dynamic Weight) + Smooth Path\nReached nodes: {len(explorer.reached.keys())}\nElapsed Time: {round(elapsed_time, 5)} seconds")
        
        # Plot path
        path = path_states(node)
        simplified_path = simplify_path(path, map)
        self.matplotlib_widget.draw_path_found(simplified_path, initial, goal, explorer.get_reached())
    
    def runGenetic(self):
        max_generation, initial_population_size = self.genetic_generation_spinbox.value(), self.genetic_init_pop_spinbox.value()
        p_crossover, p_mutation = (float(self.genetic_crossover_prob.text()), float(self.genetic_mutation_prob.text()))
        
        initial = (int(self.start_x_edit.text()), int(self.start_y_edit.text()))
        goal = (int(self.end_x_edit.text()), int(self.end_y_edit.text()))
        # G = self.map.get_grid_matrix()
        # print(G)
        path = genetic(self.map, start=initial, end=goal,
                       max_generation=max_generation, initial_population_size=initial_population_size, 
                       p_crossover=p_crossover, p_mutation=p_mutation)
        print(path)
        self.matplotlib_widget.draw_path_found(path, initial, goal, [])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

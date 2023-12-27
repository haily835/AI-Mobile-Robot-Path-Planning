import numpy as np
from math import sqrt
from obstacle.obstacle_map import Map
from .search import Problem, Node

class Explorer(Problem):
    def __init__(self, map: Map, initial: tuple[int,int], goal: tuple[int,int]): 
        self.map = map
        self.initial = initial
        self.goal = goal
        
    def actions(self, state: tuple[int,int]):
        neighbors = []
        for move in [(1,0), (0,1), (1,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]:
            neighbors.append(np.array(state) + np.array(move))
        valid_neighbors = [n for n in neighbors if not self.map.is_obstacle_in_grid(n[0], n[1])]
        # print('valid_neighbors: ', valid_neighbors)
        return valid_neighbors
    
    def result(self, state, action):
        return action
    
    def is_goal(self, state):
        return (self.goal[0] == state[0]) and (self.goal[1] == state[1])
    
    def action_cost(self, s, a, s1): return 1
    
    def h(self, node: Node):
        # h1 = abs(self.goal[0] - node[0])
        # h2 = abs(self.goal[1] - node[1])
        return sqrt((self.goal[0] - node.state[0])**2 + (self.goal[1] - node.state[1])**2)
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    

    def get_reached(self):
        return [[int(coord) for coord in r.split(',')] for r in list(self.reached)]
        
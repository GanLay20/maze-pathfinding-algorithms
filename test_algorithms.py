"""
Filename: main.py
Author: Yan Myo Aung
Email: ayn174@uregina.ca
Date Created: 2023-07-03
Description:
    This script provides implementations of various maze-solving algorithms and tools to visualize and
    compare their performance.

    Algorithms Implemented:
    1. Branch and Bound
    2. Branch and Bound with Heuristics
    3. A*

    Features:
    - Visualization of the path found by each algorithm using the pyamaze library.
    - Timing utilities to measure and compare the performance of the implemented algorithms.
    - A bar chart representation to visually compare the average runtime of the algorithms.

    External Libraries Used:
    - pyamaze: For maze generation, rendering, and path visualization.
    - queue.PriorityQueue: For managing nodes during the search in the algorithms.
    - matplotlib: For plotting performance comparisons.
    - numpy: For statistical calculations on the algorithm runtimes.
    - os & glob: For file operations, especially related to saving and renaming maze configurations.

    Note:
    Before running the script, ensure all dependencies are installed, and you've set the appropriate paths
    and filenames. The script concludes by checking if all the implemented algorithms find the same solution path
    for the given maze.

Usage:
    python main.py

"""

#Import required libraries
from pyamaze import maze, agent, textLabel,COLOR
from queue import PriorityQueue
import time
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import random

# Check if a given cell is within the bounds of the maze
def is_in_bounds(cell, rows, cols):
    row, col = cell
    return 1 <= row <= rows and 1 <= col <= cols

# Define the standard Branch and Bound algorithm
class BranchAndBound:
    def __init__(self, m):
        # Initialize maze, starting position, goal position, and possible directions of movement
        self.m = m
        self.rows = self.m.rows
        self.cols = self.m.cols
        self.start = (self.rows, self.cols)
        self.goal = (1, 1)
        self.directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

    # Find the shortest path using the Branch and Bound algorithm
    def find_shortest_path(self):
        """
                Implement the Branch and Bound algorithm to find the shortest path
                from the start to the goal in the given maze.

                Returns:
                    A list representing the shortest path from the start to the goal.
        """


        queue = PriorityQueue()                     # Initialize priority queue and variables to track progress

        # Start the queue with the starting cell and a path length of 0.
        queue.put((0, self.start, [self.start]))    # Cost, current_cell, path
        best_path_length = float('inf')             # Initialize the shortest path length found so far to infinity.
        best_path = []
        visited = set()                              # Keep track of cells that have already been visited.

        while not queue.empty():
            # Get the cell in the queue with the shortest path length.
            current_length, current_cell, path = queue.get()

            # Skip if already visited
            if current_cell in visited:
                continue

            visited.add(current_cell)


            # Bounding step: If we've reached the goal and the path is shorter than
            # any previously found path, update our shortest path.
            if current_cell == self.goal and current_length < best_path_length:
                best_path_length = current_length
                best_path = path

            # Branching step: Explore all neighboring cells.
            for d, (dx, dy) in self.directions.items():
                neighbor = (current_cell[0] + dx, current_cell[1] + dy)

                # If the neighbor is within the maze bounds, the path to the neighbor
                # is shorter than our best path length, and we haven't visited the neighbor yet,
                # add the neighbor to our queue.
                if (is_in_bounds(neighbor, self.m.rows, self.m.cols)
                        and self.m.maze_map[current_cell][d]
                        and current_length + 1 < best_path_length
                        and neighbor not in visited):
                    queue.put((current_length + 1, neighbor, path + [neighbor]))

        return best_path

    # Visualize the path found by the algorithm
    def visualize_path(self, path):
        """
                Visualize the path found by the Branch and Bound algorithm on the maze.

                Parameters:
                    path: The path to visualize, represented as a list.
        """
        bb_robot = agent(self.m, footprints=True)
        self.m.tracePath({bb_robot: path.copy()})
        l = textLabel(self.m, 'Branch and Bound Path Length', len(path))
        self.m.run()

# Define the Branch and Bound algorithm with heuristics
class BranchAndBound_With_Heuristics:
    def __init__(self, m):
        self.m = m
        self.rows = self.m.rows
        self.cols = self.m.cols
        self.start = (self.rows, self.cols)
        self.goal = (1, 1)
        self.directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

    def heuristic(self, cell):

        # Euclidean distance heuristic
        return ((cell[0] - self.goal[0]) ** 2 + (cell[1] - self.goal[1]) ** 2) ** 0.5

    def find_shortest_path(self):
        """
                Implement the Branch and Bound algorithm with heuristics to find the shortest path
                from the start to the goal in the given maze.

                Returns:
                    A list representing the shortest path from the start to the goal.
        """
        queue = PriorityQueue()
        queue.put((0, 0, self.start, [self.start])) # Heuristic cost, path cost, current_cell, path
        best_path_length = float('inf')
        best_path = []
        visited = set()

        while not queue.empty():
            _, current_length, current_cell, path = queue.get()

            if current_cell in visited:
                continue

            visited.add(current_cell)

            if current_cell == self.goal and current_length < best_path_length:
                best_path_length = current_length
                best_path = path

            for d, (dx, dy) in self.directions.items():
                neighbor = (current_cell[0] + dx, current_cell[1] + dy)

                # If the neighbor is within the maze bounds, the path to the neighbor
                # is shorter than our best path length, and we haven't visited the neighbor yet,
                # add the neighbor to our queue.
                if (is_in_bounds(neighbor, self.m.rows, self.m.cols)
                    and self.m.maze_map[current_cell][d]
                    and current_length + 1 < best_path_length
                    and neighbor not in visited):

                    # Calculate the total cost as path length + heuristic.
                    total_cost = current_length + 1 + self.heuristic(neighbor)
                    queue.put((total_cost, current_length + 1, neighbor, path + [neighbor]))

        return best_path


    def visualize_path(self, path):
        bbh_robot = agent(self.m, footprints=True)
        self.m.tracePath({bbh_robot: path.copy()})
        l = textLabel(self.m, 'Branch and Bound with Heuristic Path Length', len(path))
        self.m.run()


class AStar:
    def __init__(self, maze):
        self.maze = maze
        # Define the start and goal coordinates.
        # Start is assumed to be the bottom-right of the maze while goal is top-left.
        self.start_coord = (self.maze.rows, self.maze.cols)
        self.goal_coord = (1, 1)
        # Define possible directions and their corresponding movements in terms of rows and columns.
        self.directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

    def calculate_heuristic(self, current, target):
        """
                Calculate the Manhattan distance between the current cell and target cell.
                This serves as our heuristic in the A* algorithm.
        """

        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    def find_shortest_path(self):
        """
                Implement the A* algorithm to find the shortest path from start to goal in the given maze.

                Returns:
                    A dictionary representing the path from the start to the goal.
        """
        # Initialize the cost from the start to every position as infinity.
        # The cost to get from start to start is obviously 0.
        actual_cost = {coord: float('inf') for coord in self.maze.grid}
        actual_cost[self.start_coord] = 0

        # Initialize the total estimated cost of a cheapest path from start to goal
        # that goes through each position.
        estimated_cost = {coord: float('inf') for coord in self.maze.grid}
        estimated_cost[self.start_coord] = self.calculate_heuristic(self.start_coord, self.goal_coord)

        # Priority queue for positions with their estimated cost as priority.
        open_set = PriorityQueue()
        open_set.put((estimated_cost[self.start_coord], self.start_coord))  # estimated cost, position
        # Dictionary to store where we came from for each position.
        came_from = {}

        while not open_set.empty():
            # Get the position in open set with the lowest estimated cost.
            current_coord = open_set.get()[1]

            # If this position is the goal, we are done.
            if current_coord == self.goal_coord:
                break
            # Consider all neighbors of the current position.
            for direction, (dx, dy) in self.directions.items():
                # If this direction is valid in the maze.
                if self.maze.maze_map[current_coord][direction]:
                    neighbor_coord = (current_coord[0] + dx, current_coord[1] + dy)

                    # Calculate the actual cost if we move to this neighbor from the current position.
                    tentative_actual_cost = actual_cost[current_coord] + 1

                    # If this new path to the neighbor is shorter than any previously known path,
                    # update our path and costs.
                    if tentative_actual_cost < actual_cost[neighbor_coord]:
                        came_from[neighbor_coord] = current_coord
                        actual_cost[neighbor_coord] = tentative_actual_cost
                        estimated_cost[neighbor_coord] = (tentative_actual_cost + \
                                                          self.calculate_heuristic(neighbor_coord, self.goal_coord))
                        open_set.put((estimated_cost[neighbor_coord], neighbor_coord))

        # Reconstruct the path from the goal back to the start.
        path = {}
        current_coord = self.goal_coord
        while current_coord != self.start_coord:
            path[came_from[current_coord]] = current_coord
            current_coord = came_from[current_coord]

        return path

    def visualize_path(self, path):
        """
                Visualize the path found by the A* algorithm on the maze.

                Parameters:
                    path: The path to visualize, represented as a dictionary.
        """
        # Create an agent to visualize the path.
        astar_robot = agent(self.maze, footprints=True)
        # Trace the path in the maze.
        self.maze.tracePath({astar_robot: path.copy()})
        path_length_label = textLabel(self.maze, 'A* Path Length', len(path) + 1)
        # Run the maze visualization.
        self.maze.run()


# Function to time how long each algorithm takes to run
def time_algorithm(algorithm, maze, num_trials=100):
    # Time how long the algorithm takes to run
    times = []
    for _ in range(num_trials):
        start_time = time.time()
        algorithm(maze).find_shortest_path()
        times.append(time.time() - start_time)
    return np.mean(times), np.std(times)

# Compare the performance of different algorithms
def compare_algorithms(algorithms, maze, num_trials=100):
    # Map full names to short names
    name_map = {
        'BranchAndBound': 'BB',
        'BranchAndBound_With_Heuristics': 'BBH',
        'AStar': 'AS'
    }
    means = []
    stds = []
    labels = []
    for algorithm in algorithms:
        mean, std = time_algorithm(algorithm, maze, num_trials)
        means.append(mean)
        stds.append(std)
        # Use the short name from the name_map
        labels.append(name_map[algorithm.__name__])

    return means, stds, labels

# Plot the comparison results
def plot_comparison(means, stds, labels):
    plt.bar(labels, means, yerr=stds)
    plt.ylabel('Time taken (seconds)')
    plt.title('Comparison of Maze Solving Algorithms')
    plt.show()


if __name__ == '__main__':
    # Create a maze
    rows, cols = 20, 20
    m = maze(rows, cols)
    m.CreateMaze(theme=COLOR.light,loopPercent=100, saveMaze=True)

    # Rename the saved maze files
    directory = os.getcwd()

    csv_files = sorted(glob.glob(os.path.join(directory, 'maze--*.csv')),
                       key=os.path.getmtime)[-1:]

    # Loop through the files
    for old_file_path in csv_files:
        directory, old_file_name = os.path.split(old_file_path)
        new_file_name = 'maze.csv'
        new_file_path = os.path.join(directory, new_file_name)
        os.replace(old_file_path, new_file_path)

    # Test the Branch and Bound algorithm
    bb = BranchAndBound(m)
    start_time = time.time()
    path = bb.find_shortest_path()
    end_time = time.time()
    print(f"Time taken for Branch and Bound algorithm: {end_time - start_time} seconds")
    bb.visualize_path(path)

    # Test the Branch and Bound algorithm with heuristics
    m.CreateMaze(theme=COLOR.light,loopPercent=100,loadMaze="maze.csv")
    bbh = BranchAndBound_With_Heuristics(m)
    start_time = time.time()
    path1 = bbh.find_shortest_path()
    end_time = time.time()
    print(f"Time taken for Branch and Bound with Heuristics algorithm: {end_time - start_time} seconds")
    bbh.visualize_path(path1)

    # Test the A* algorithm
    m.CreateMaze( theme=COLOR.light,loopPercent=100,loadMaze="maze.csv")
    astar = AStar(m)
    start_time = time.time()
    path2 = astar.find_shortest_path()
    end_time = time.time()
    print(f"Time taken for A* algorithm: {end_time - start_time} seconds")
    astar.visualize_path(path2)

    # Compare all three algorithms
    algorithms = [BranchAndBound, BranchAndBound_With_Heuristics, AStar]
    means, stds, labels = compare_algorithms(algorithms, m)
    plot_comparison(means, stds, labels)

    # Check if all algorithms found paths with the same length
    if len(path) == len(path1) == len(path2) + 1:
        print("All three algorithms found paths with the same length.")
    else:
        print("The algorithms found paths with different lengths.")

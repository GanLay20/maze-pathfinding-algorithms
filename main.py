from pyamaze import maze, agent, textLabel,COLOR
from queue import PriorityQueue
import time

class BranchAndBound:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.m = maze(self.rows, self.cols)
        self.m.CreateMaze(theme=COLOR.light,loopPercent=100)
        self.start = (self.rows, self.cols)
        self.goal = (1, 1)
        self.directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

    def find_shortest_path(self):
        queue = PriorityQueue()
        queue.put((0, self.start, [self.start])) # Cost, current_cell, path
        best_path_length = float('inf') # Initialize the best path length
        visited = set() # Keep track of visited cells

        while not queue.empty():
            current_length, current_cell, path = queue.get()

            # Skip if already visited
            if current_cell in visited:
                continue

            visited.add(current_cell)

            # If we reached the goal and the path is shorter than the best path, update the best path length
            if current_cell == self.goal and current_length < best_path_length:
                best_path_length = current_length
                best_path = path

            # Explore neighbors
            for d, (dx, dy) in self.directions.items():
                neighbor = (current_cell[0] + dx, current_cell[1] + dy)

                # If the path to this neighbor is shorter than the best path length and it's a valid move
                if self.m.maze_map[current_cell][d] and current_length + 1 < best_path_length and neighbor not in visited:
                    queue.put((current_length + 1, neighbor, path + [neighbor]))

        return best_path

    def visualize_path(self, path):
       # a = agent(self.m, footprints=True)
       ##  l = textLabel(self.m, 'Branch and Bound Path Length', len(path))
        self.m.run()

if __name__ == '__main__':
    rows, cols = 20, 20
    bb = BranchAndBound(rows, cols)

    start_time = time.time()
    path = bb.find_shortest_path()
    end_time = time.time()

    print(f"Time taken for Branch and Bound algorithm: {end_time - start_time} seconds")
    bb.visualize_path(path)
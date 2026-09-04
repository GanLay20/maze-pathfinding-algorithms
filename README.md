Maze Pathfinding Algorithm Comparison

This project compares three algorithms for solving the same randomly generated maze: Branch and Bound, Branch and Bound with a Euclidean-distance heuristic, and A* search with a Manhattan-distance heuristic. I used pyamaze to generate the maze and show the path found by each algorithm. The program also checks whether they find paths of the same length and compares their average running times over several trials.

Features
-Generates a configurable two-dimensional maze.
-Solves the same maze using three algorithms.
-Visualizes each solution with animated footprints.
-Reports the path length and execution time.
-Benchmarks each algorithm over 100 trials.
-Displays the average runtime and standard deviation in a bar chart.
-Checks whether all algorithms return paths of equal length.

Project Structure
├── images/
│   ├── a-star.png
│   ├── branch-and-bound.png
│   └── branch-and-bound-heuristic.png
├── tests/
│   └── test_algorithms.py
├── LICENSE
├── README.md
├── main.py
├── requirements-dev.txt
└── requirements.txt
Requirements
Python 3
pyamaze
NumPy
Matplotlib

Install the required packages with:

python -m pip install -r requirements.txt

Alternatively, install them directly:

python -m pip install pyamaze numpy matplotlib
Running the Project

Run the program with:

python main.py

Each visualization window must be closed before the next algorithm starts. After all three visualizations finish, the program runs the benchmark and displays the runtime comparison chart.

Example Results

In the example below, all three algorithms solved the same 20 × 20 maze using paths containing 41 cells, equivalent to 40 moves.

![Branch and Bound](images/branch-and-bound.png)

![Branch and Bound with Heuristic](images/branch-and-bound-heuristic.png)

![A-star Search](images/a-star.png)


The algorithms may choose different optimal routes when multiple routes have the same cost. Equal path costs therefore demonstrate optimality even if the visual paths are not identical.

Configuration

The maze dimensions can be changed in main.py:
  -rows, cols = 20, 20

The number of timing trials can also be changed:
-means, stds, labels = compare_algorithms(algorithms, m, num_trials=100)

Reducing the animation delay makes the agent move faster:
-self.m.tracePath({robot: path}, delay=50)

Notes
The graphical interface requires a desktop environment with Tkinter support.
Execution times depend on the maze, computer, operating system, and Python environment.
Setting loopPercent=100 allows the maze to contain multiple possible routes.
License

This project is licensed under the MIT License.

Author

Yan Myo Aung

This project is licensed under the MIT License.

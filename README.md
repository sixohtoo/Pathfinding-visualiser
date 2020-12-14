# Pathfinding-visualiser
A shortest path visualiser using pygame.

# Features
Contains both Dijkstra's algorithm and A-star pathfinding algorithm.

Abilty to draw barriers/obstacles for pathfinder to go around.

Basic Maze Generator can be used to generate a Randomised Prim's algorithm maze
which acts as barriers for the pathfinding algorithm.

3 different speed options for algorithms.

2 different reset options for the board.

# Controls
run `python3 astar.py` to open program (Name is now inaccurate - I will change this).

**Left click** on any square in the grid to place the 'Starting Node'.

**Left click** on any other square in the grid to place the 'Finishing Node'.

Any other squares that are left clicked will show as barriers.

**Right click** to 'reset' a square (Removes start, finish and barrier nodes).

**C** clears the entire board.

**R** removes any path nodes. Leaves start, finish and barrier nodes untouched.

**1, 2, 3** sets the algorithm speed (fastest to slowest).

**M** creates a maze starting at the 'Start Node'.

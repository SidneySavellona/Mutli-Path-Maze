# Mutli-Path-Maze

# A* Maze Pathfinder with Multiple Shortest Routes (Tkinter GUI)

This project is a Python application that visualizes the **A\*** pathfinding algorithm on a maze using a GUI built with **Tkinter**. It supports:

- Generating **easy** and **complicated** mazes
- Finding the **1st**, **2nd**, and **3rd shortest non-colliding paths**
- Displaying all shortest paths simultaneously with **distinct colors**
- Showing the **number of blocks** in each path
- Allowing manual maze editing and start/end positioning

---

## Features

- **Pathfinding**: Uses the A* algorithm to find the shortest path from the start to the end.
- **Multiple Paths**: Finds up to 3 unique non-overlapping paths.
- **Color-Coded Paths**: 
  - 1st path → Yellow  
  - 2nd path → Orange  
  - 3rd path → Blue  
- **Dynamic Maze Generation**:
  - Easy: Random sparse walls
  - Complicated: Generated using Recursive Backtracking (perfect maze)
- **Path Details Panel**: Displays how many blocks each path uses on the right side of the interface.

## GControls

- **Left Click**: Toggle walls on the grid manually.
- **Right Click**: Set Start and End points.
- **Find Paths**: Finds and displays all 3 shortest paths simultaneously.
- **Reset**: Clears the grid and paths.
- **Maze Buttons**: Auto-generate an easy, hard, or complicated maze.
- **Dropdown**: Optionally highlight only 1st, 2nd, or 3rd path.



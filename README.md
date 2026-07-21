*This project has been created as part of the 42 curriculum by <login1>.*

# Fly-In Drone Simulator

## Description

Fly-In is a drone traffic simulation project developed as part of the 42 curriculum.
The goal of the project is to simulate multiple drones moving through a network of
hubs while respecting different constraints such as path availability, hub capacity,
restricted zones, and movement scheduling.

The project reads a custom map description file, parses and validates the data,
creates a graph representation of the drone network, calculates efficient paths,
and simulates the movement of multiple drones turn by turn.

The simulator includes a graphical visualization using Pygame, allowing users to
observe the drone movements, paths, hubs, and network structure in real time.

Main features:

- Custom map parser with validation
- Graph construction from hubs and connections
- Pathfinding algorithms (BFS and Dijkstra)
- Multi-drone simulation
- Turn-based movement scheduling
- Capacity handling
- Restricted zone management
- Interactive Pygame visualization
- Menu system for selecting different maps


# Instructions

## Requirements

The project requires:

- Python 3.10+
- pygame
- flake8
- mypy

Dependencies are listed in:

requiremnts.text

## Installation

Create the virtual environment and install dependencies:

```bash
make install
```
#### other make comands

```bash

make run # Running the project

make clean # Clean temporary files

make debug # Debug mode

make lint # Code quality

make lint-strict # strict Code quality
```

## Algorithm Choices and Implementation Strategy
### Graph Representation

The drone network is represented as a graph.

Each hub is represented as a node:

Node:
    - Hub information
    - List of connected neighbors

Connections between hubs create edges in the graph.

The graph structure allows efficient traversal and path searching.

### Breadth First Search (BFS)

BFS is implemented to find the shortest path based on the number of connections.
The algorithm explores the graph level by level:


Start from the initial hub
Add neighboring hubs to a queue
Mark visited nodes
Continue until the destination is reached

BFS is useful when all connections have the same cost.
in this Project it also confirms if there is a path or not. 

### Dijkstra Algorithm

Dijkstra's algorithm is used to find the lowest-cost path.

Unlike BFS, Dijkstra considers different hub costs.

Each node stores:

Current minimal distance
Previous node in the optimal path

A priority queue (heapq) is used to always process the cheapest available path first.

This allows the simulator to prefer efficient routes through the network.

## Simulation Strategy

The simulation runs turn by turn.

During each turn:

Each drone checks its next possible movement
Capacity restrictions are evaluated
Conflicts between drones are prevented
Valid movements are executed
The next turn begins

Each drone keeps track of:

Current position
Target path
Finished state
Visualization

## The graphical interface is implemented using Pygame.


The visualization makes the simulation easier to understand by:

Showing the complete network structure
Making drone collisions and waiting behavior visible
Allowing users to follow individual drones
Providing immediate feedback about pathfinding decisions

Colors are used to distinguish different hub types and drone states.

### Resources

-https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
-https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/

Artificial Intelligence was used as a learning and documentation aid.

AI was used for:

- Explaining algorithms such as BFS and Dijkstra
- Debugging Python errors and understanding mypy errors
- README.md structure

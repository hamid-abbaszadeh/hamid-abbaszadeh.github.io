---
title: Pathfinding project in c++
description: >-
  BFS, DFS(Recursive & Iterative), Dijkstra, Greedy, & A* Algorithms. These
  algorithms are used to search the tree and find the shortest path from
  starting node to goal node in the tree.
layout: project_page
published: true
---

[![Benjamin Bannekat ](https://raw.githubusercontent.com/hamid-abbaszadeh/hamid-abbaszadeh.github.io/master/images/path.gif)](https://hamid-abbaszadeh.github.io/projects/Shortest-path-Algorithm)

> BFS, DFS(Recursive & Iterative), Dijkstra, Greedy, & A* Algorithms. These algorithms are used to search the tree and find the shortest path from starting node to goal node in the tree.

For the corresponding Github repository click [here](https://gist.github.com/hamid-abbaszadeh/ca8555a0f5cfc2cb09e78b96dedd25c8).


    
  
# Introduction

Blind search algorithms such as breadth-first and depth-first exhaust all possibilities; starting from the given node, they iterate over all possible paths until they reach the goal node. These algorithms run in O(V+E), or linear time, where V is the number of vertices, and E is the number of edges between vertices.

However, it is not necessary to examine all possible paths. Algorithms such as Greedy, Dijkstra’s algorithm, and A* eliminate paths either using educated guesses(heuristics) or distance from source to node V to find the optimal path. By eliminating impossible paths, these algorithms can achieve time complexities as low as O(E log(V)).

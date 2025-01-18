#include "p8c2_robot_in_grid.h"

/*
Robot in a Grid: Imagine a robot sitting on the upper left corner of grid with r
rows and c columns. The robot can only move in two directions, right and down,
but certain cells are "off limits" such that the robot cannot step on them.
Design an algorithm to find a path for the robot from the top left to the bottom
right.
*/

Path find_path(Maze maze) {
  int rows = maze.size();
  int cols = maze[0].size();
  Position end = {rows - 1, cols - 1};
  Path path;

  if (find_path(maze, end, path)) {
    std::cout << "path found" << std::endl;
    return path;
  } else {
    std::cout << "path NOT found" << std::endl;
    return {};
  }
}

bool find_path(Maze maze, Position candidate, Path &path) {
  if (candidate[0] < 0 || candidate[1] < 0 ||
      maze[candidate[0]][candidate[1]]) {
    return false;
  }
  Position left = {0,0};
  Position up = {0,0};
  left[0] = candidate[0];
  left[1] = candidate[1] - 1;
  up[0] = candidate[0] - 1;
  up[1] = candidate[1];
  if ((candidate[0] == 0 && candidate[1] == 0) || find_path(maze, left, path) ||
      find_path(maze, up, path)) {
    path.push_back(candidate);
    return true;
  }
  return false;
}
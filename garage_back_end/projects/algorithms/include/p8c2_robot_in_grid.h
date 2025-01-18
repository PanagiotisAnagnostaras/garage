#include "common_headers.h"

typedef std::vector<int> Position;
typedef std::vector<std::vector<int>> Path;
typedef std::vector<std::vector<bool>> Maze;

Path find_path(Maze maze);

bool find_path(Maze maze, Position candidate, Path &path);
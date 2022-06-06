"""
ingest.py, written as part of Blob_Traffic project (https://github.com/antholuo/Blob_Traffic)
---------------------------------------
January 2022
Anthony Luo (antholuo@gmail.com), Christina Zhang (christinaytzhangroxs@gmail.com)
---------------------------------------
    This file is designed to take a line-by-line entry (cin) or a text file (preferred) and parse it into either a
numpy array or a python list.
Todo: The rest of our pathfinding code needs to be updated to accept numpy arrays.
"""

import numpy as np

# list of characters that are recognized as "walls" when we ingest from .txt files
WALL_CHARACTERS = ["X", "x", "#", "9"] # these will correlate with 9
BLOB_START = "@" # this will correlate with 1
BLOB_GOAL = "$"  # this will correlate with 2
# empty space will corelate with 0

def yx_to_xy(yx_grid):
    """Turns a y/x grid (row, column) into an x/y grid.
    Iterates through the yx grid keeping track of the current location, and maps that value to the corresponding
    position within the xy grid
    :param map: int[][], a typical ingested y/x grid
    :return: int[][], a RHR cartesian x,y grid
    ------------------------------------------------
    yx_style_grid:
      0 1 2
    0 a b c     ==  [[a,b,c],
    1 d e f          [d,e,f]]

    xy_style_grid:
    1 a b c     ==  [[d, a],
    0 d e f          [e, b],
      0 1 2          [f, c]]
    """
    len_x = len(yx_grid[0])  # any index works, grid should be same length anywhere.
    len_y = len(yx_grid)  # how many y indices there are.
    xy_grid = []
    # note that the above may change as we edit our code. I will think of a solution.

    # generate locations for us to follow (relative to yx)
    x_loc = 0
    y_loc = 0  # note that the y direction is flipped

    while x_loc < len_x:
        temp = []
        y_loc = 0
        while y_loc < len_y:
            temp.append(yx_grid[len_y - y_loc - 1][x_loc])  # need to flip the y
            y_loc += 1
        xy_grid.append(temp)
        x_loc += 1

    return xy_grid


def txt_to_np(filepath):
    # print("converting txt to np")
    lines = []
    with open(filepath, "r") as file:
        lines = file.readlines()

    yx_grid = []

    y = 0
    x = 0
    for line in lines:
        yx_grid.append([])
        line = line.rstrip()
        line = line.replace(" ", "")
        for char in line:
            if char in WALL_CHARACTERS:
                yx_grid[y].append(9)
            elif char == BLOB_START:
                yx_grid[y].append(1)  # todo: confirm if this is correct
            elif char == BLOB_GOAL:
                yx_grid[y].append(2)
            else:
                yx_grid[y].append(0)
        y += 1
    return list_to_np(yx_grid)


# simple visualization of the maze and the path A* takes
def visualize(maze, path=[]):
    for coordinate in path:
        maze[coordinate[0]][coordinate[1]] = "#"

    x = 0
    y = 0
    max_x = len(maze)
    max_y = len(maze[1])
    while y < max_y:
        x = 0
        print()
        while x < max_x:
            print(maze[x][max_y - y - 1], end=" ")
            x += 1
        y += 1


def _visualize_np(np_grid):
    """
    internal function to print out entire np_grid
    :param np_grid:
    :return:
    """
    print("printing RAW numpy array. NOTE that this will be transformed with regard to our actual array.")
    with np.printoptions(threshold=np.inf):
        print(np_grid)


def list_to_np(grid):
    return np.array(grid, dtype=np.byte)


def write_to_file(np_grid):
    """Converts numpy.ndarray to strings and then writes to file"""
    with open("../Test(ing)/np_maze_out.txt", "w") as file:
        for row in np_grid:
            for cell in row:
                file.write(str(cell))
            file.write("\n")


def testfunc1():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    xy_grid = yx_to_xy(maze)
    visualize(xy_grid)
    print()
    np_grid = list_to_np(xy_grid)
    _visualize_np(np_grid)
    # write_to_file(np_grid)


def testfunc2():
    np_grid = txt_to_np("../Test(ing)/maze.txt")
    with np.printoptions(threshold=np.inf):
        print(np_grid)
    # print(np_grid.dtype)
    write_to_file(np_grid)


if __name__ == "__main__":
    testfunc2()

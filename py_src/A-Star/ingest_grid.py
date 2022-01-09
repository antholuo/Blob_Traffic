"""
ingest_grid.py, written as part of Blob_Traffic project (https://github.com/antholuo/Blob_Traffic)
---------------------------------------
January 2022
Anthony Luo (antholuo@gmail.com), Christina Zhang (christinaytzhangroxs@gmail.com)
---------------------------------------
    This file is designed to take a line-by-line entry (cin) or a text file (preferred) and parse it into a workable
format for the rest of our code.
"""


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


if __name__ == "__main__":
    print("running ingest_grid.py")
    testfunc1()

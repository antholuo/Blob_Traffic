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
    xy_grid = []
    len_x = len(yx_grid[0]) # any index works, grid should be same length anywhere.


if __name__ == "__main__":
    print("running ingest_grid.py")

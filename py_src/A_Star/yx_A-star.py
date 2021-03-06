"""
A-Star function, revision 1.

====================================
g: distance between current node and start node
h: heuristic, estimated * cost * between current node to end node
f: total cost of the node.
"""

# blep

import logging
import os
import sys
import time
import platform

print(sys.version, sys.version_info)
print(
    platform.python_implementation(),
    platform.python_version(),
    platform.python_compiler(),
)


def setup_custom_logger(name):
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = logging.FileHandler("log.txt", mode="w")
    handler.setFormatter(formatter)
    # screen_handler = logging.StreamHandler(stream=sys.stdout)
    # screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    # logger.addHandler(screen_handler)
    return logger


logger = setup_custom_logger("a-star")


class Node:
    def __init__(self, parent, position, g=0, h=0, f=0):
        self.parent = parent
        self.position = position

        # g/h/f default to 0
        self.g = g
        self.h = h
        self.f = f

    def __eq__(self, other):
        """
        Equals function within our Node to allow us to do comparisons on the node.
        :param other:
        :return:
        """
        return (
            self.position == other.position
        )  # a lot simpler than going through the list in a convoluted way


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        logger.info("backtrace path is: " + str(current.position))
        path.append(current.position)
        current = current.parent
    return path[::-1]  # returns traversed path


def astar(maze, start, end, allow_diag=False):
    """
    Main function for searching astar.
    :param maze: Maze is defined as an nxm grid (array) with passable grid values as 0 and "walls" as 1. # TODO: add difficulty of traversing different grid blocks
    :param start: row, column start position? (or is it x,y)
    :param end: row, column end position? (or is it x,y)
    :param allow_diag: 0 = no diag, 1 = diag.
    :return: list from given start to given end
    """

    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    # gives us the direction of motion to reach the next squares from our current square
    if not allow_diag:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    else:
        adjacent_squares = (
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        )

    logger.debug(msg="starting while loop")
    while len(open_list) > 0:

        # do we need to set this if we are prioq later?
        current_node = open_list[0]  # get the first node in the open list.
        current_index = 0

        logger.info("currently on position:" + str(current_node.position))
        # priority q (check the one with the shortest list).
        # todo: replace this with a proper queue
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # remove this node from the open list and put it into the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # we have reached a solution, return the path.
        if current_node.position == end_node.position:
            return return_path(current_node)

        children = []

        # checks to see if neighbouring squares are valid places to move, if so, add it to the children of the current node
        for next_position in adjacent_squares:

            # node position is the position of the current node plus which ever direction we are going in
            node_position = (
                current_node.position[0] + next_position[0],
                current_node.position[1] + next_position[1],
            )

            # checks to see if position is inside grid
            if (
                node_position[0] < 0
                or node_position[0] > (len(maze[0]) - 1)
                or node_position[1] < 0
                or node_position[1] > (len(maze) - 1)
            ):
                continue

            # checks to see if position is a wall/impassable
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            # Child is on the closed list
            if child in closed_list:
                # print("child in closed list")
                continue

            # Create the f, g, and h values
            child.g = (
                current_node.g
                + (
                    ((child.position[0] - child.parent.position[0]) ** 2)
                    + ((child.position[1] - child.parent.position[1]) ** 2)
                )
                ** 0.5
            )
            child.h = (
                ((child.position[0] - end_node.position[0]) ** 2)
                + ((child.position[1] - end_node.position[1]) ** 2)
            ) ** 0.5
            child.f = child.g + child.h

            # if child is already on the open list
            if child in open_list:
                # print("child in open list")
                idx = open_list.index(child)
                if child.g < open_list[idx].g:
                    # print ("code reached")
                    # update the node in the open list
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                # todo: verify if this is the correct way to push child into open_list
                # push child to open_list
                open_list.append(child)


def run_astar():
    maze = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    """
    Here we define MAZE #2, which is going to be written in x,y (column, row) format, but should look as such:
        0 1 2 3 4 5 6 7 8 9
        -------------------
    0 | 0 0 0 0 0 0 1 0 0 1
    1 | 0 0 0 0 0 1 1 0 1 0
    2 | 0 0 0 0 0 1 0 0 1 0
    3 | 0 0 0 0 0 0 0 1 1 0
    4 | 0 0 1 0 0 1 0 0 0 0
    5 | 0 0 1 1 1 1 0 0 0 0
    6 | 0 0 0 0 1 0 0 0 1 0, 
    """

    maze2 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0],
    ]

    start = (0, 0)
    end = (0, 7)

    path = astar(maze, start, end)
    return [path, maze]


# simple visualization of the maze and the path A* takes
def visualization(path, maze):
    print(path)
    for coordinate in path:
        maze[coordinate[0]][coordinate[1]] = "#"

    for i in range(len(maze)):
        for j in maze[i]:
            print(j, end=" ")
        print("")


if __name__ == "__main__":
    print("entering main function for A-Star main")

    visualization(run_astar()[0], run_astar()[1])

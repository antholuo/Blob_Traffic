"""
A-Star_main.py
================================
re-written a-star search algorithm to support searching in x,y (column, row) format for better compatibility with the rest of our code.
"""

import logging
import os
import sys
import time
import platform

print(sys.version, sys.version_info)
print(platform.python_implementation(), platform.python_version(), platform.python_compiler())

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    # screen_handler = logging.StreamHandler(stream=sys.stdout)
    # screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    # logger.addHandler(screen_handler)
    return logger


logger = setup_custom_logger("xy_a-star")

class Node:
    def __init__(self, parent, position, g=0, h=0, f=0):
        self.parent     = parent
        self.position   = position

        self.g = g
        self.h = h
        self.f = f

    def __eq__(self, other):
        """Overrides the bulitin == function to compare position instead of actual node classes."""
        return self.position == other.position

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        logger.info("backtrace path is: " + str(current.position))
        path.append(current.position)
        current = current.parent
    return path[::-1] # returns traversed path

def astar(maze, start, end, allow_diag=False):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    # starting node added to open list
    open_list.append(start_node)

    # gives us the direction of motion to reach the next squares from our current square
    if not allow_diag:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    else:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

    logger.debug(msg="starting while loop")

    # loop until empty
    while len(open_list) > 0:
        current_node = open_list[0]
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

        for next_position in adjacent_squares:
            node_position = (current_node.position[0] + next_position[0], current_node.position[1] + next_position[1])

            # this is different because of flipped x and y
            if node_position[0] < 0 or node_position[0] > (len(maze) -1) or node_position[1]<0 or node_position[1] > (len(maze[0])-1):
                continue

            # check for wall/impassable
            if maze[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + (((child.position[0] - child.parent.position[0]) ** 2) + (
                        (child.position[1] - child.parent.position[1]) ** 2)) ** 0.5
                child.h = (((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)) ** 0.5
                child.f = child.g + child.h

                # if child is already on the open list
                if child in open_list:
                    idx = open_list.index(child)
                    if child.g < open_list[idx].g:
                        # update the node in the open list
                        open_list[idx].g = child.g
                        open_list[idx].f = child.f
                        open_list[idx].h = child.h
                else:
                    # todo: verify if this is the correct way to push child into open_list
                    # push child to open_list
                    open_list.append(child)

def run_astar():
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
    6 | 0 0 0 0 1 0 0 0 1 0
    """

    maze2 = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1, 1],
             [0, 1, 1, 0, 1, 1, 0],
             [1, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0],
             [0, 1, 1, 1, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9, 2)
    print("start = ", start)
    print("end = ", end)
    path = astar(maze2, start, end)
    return [path, maze2]

# simple visualization of the maze and the path A* takes
def visualization(path, maze):
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
            print(maze[x][y], end = " ")
            x += 1
        y += 1

if __name__ == "__main__":
    print("entering main function for A-Star main")

    path, maze = run_astar()
    print(path)

    visualization(path, maze)


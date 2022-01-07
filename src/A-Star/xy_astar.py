"""
xy_astar.py
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

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        logger.info("backtrace path is: " + str(current.position))
        path.append(current.position)
        current = current.parent
    return path[::-1] # returns traversed path

def astar(map, start, end, allow_diag=False):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    # gives us the direction of motion to reach the next squares from our current square
    if not allow_diag:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    else:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

    logger.debug(msg="starting while loop")
    
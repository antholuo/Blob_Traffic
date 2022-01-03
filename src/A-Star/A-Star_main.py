"""
A-Star function, revision 1.

====================================
g: distance between current node and start node
h: heuristic, estimated * cost * between current node to end node
f: total cost of the node.
"""

# blep

class Node:
    def __init__(self, parent, position, g=0, h=0, f=0):
        self.parent = parent
        self.position = position

        # g/h/f default to 0
        self.g = g
        self.h = h
        self.f = f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current=current.parent
    return path[::-1] # returns traversed path

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
        next_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
    else:
        next_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))

    while len(open_list) > 0:

        # do we need to set this if we are prioq later?
        current_node = open_list[0] # get the first node in the open list.
        current_index = 0

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
        if current_node == end_node:
            return return_path(current_node)

        children = []

        for next_position in next_squares:
            node_position = (current_node.position[0] + next_position[0], current_node.position[1] + next_position[1])

            if node_position[0] < 0 or node_position[0] > len(maze[0]) or node_position[1] < 0 or node_position[1] > len(maze):
                continue
            if maze[node_position[0]][node_position[1]] == 1:
                continue

        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
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



if __name__ == "__main__":
    print("main start")
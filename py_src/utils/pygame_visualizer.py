"""
pygame_visualizer.py
-------------------
Anthony Luo (antholuo@gmail.com), Christina Zhang (christinaytzhangroxs@gmail.com)
-------------------
This file is a visualizer class for our Blob traffic.
"""

import sys

import numpy as np
import pygame


class Visualizer:
    # possible directions for the blob to travel in
    DIRECTIONS = {
        "N": np.array([0, -1]),
        "S": np.array([0, 1]),
        "E": np.array([1, 0]),
        "W": np.array([-1, 0]),
        "NE": np.array([1, -1]),
        "NW": np.array([-1, -1]),
        "SE": np.array([1, 1]),
        "SW": np.array([-1, 1])
    }

    # colours of the paths, walls, blob and goal
    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)
    BLUE = (52, 167, 201)
    PINK = (207, 56, 124)

    def __init__(self, grid, block_size=None, enable_render=True):
        self.game_over = False
        self.reward = 0
        self.block_size = block_size
        self.enable_render = enable_render

        # import the grid from a text file
        self.grid = grid

        # set grid_size and screen_size
        self.grid_size = self.grid.shape
        self.screen_size = (block_size * self.grid_size[0], block_size * self.grid_size[1])

        # get the blob and goal locations from the grid
        # recall that blob is where there is a 1
        # goal is where there is a 2
        self.blob = np.where(self.grid == 1)
        self.goal = np.where(self.grid == 2)

        if self.enable_render:
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode(self.screen_size)
            self.render()

    # recall that walls are where there is a 9
    def is_valid_loaction(self, location):
        # check if the location is in the grid
        if (location[0] >= 0 and location[0] < self.grid_size[0]) and (
                location[1] >= 0 and location[1] < self.grid_size[1]):
            # check if the location is not a wall
            if self.grid[location[0]][location[1]] != 9:
                return True
            else:
                return False
        else:
            return False

    # move the blob
    def move_blob(self, direction):
        # get the direction vector
        direction_vector = self.DIRECTIONS[direction]

        # get the new blob location
        new_blob = self.blob + direction_vector

        # if the new blob location is valid, update the blob location
        if self.is_valid_location(new_blob):
            self.grid[self.blob[1]][self.blob[0]] = 0
            self.blob += np.array(self.DIRECTIONS[direction])
            self.grid[self.blob[1]][self.blob[0]] = 1

        if self.enable_render:
            self.render()

    def reset_blob(self):
        self.blob = np.zeros(2, dtype=int)
        self.goal = self.grid_size - np.ones(2, dtype=int)
        self.grid[self.blob[1]][self.blob[0]] = 1
        self.grid[self.goal[1]][self.goal[0]] = 2

        if self.enable_render:
            self.screen = pygame.display.set_mode(self.screen_size)
            pygame.time.delay(1000)
            self.render()

    # quit_game
    # called when environment is to be deleted
    def quit_game(self):
        if self.game_over is True:
            if self.enable_render is True:
                pygame.display.quit()
            pygame.quit()
            sys.exit()

    def render(self):
        # draw the grid
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, self.BLACK, [j * self.block_size, i * self.block_size,
                                                               self.block_size, self.block_size])
                elif self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, self.BLUE, [j * self.block_size, i * self.block_size,
                                                              self.block_size, self.block_size])
                elif self.grid[i][j] == 2:
                    pygame.draw.rect(self.screen, self.PINK, [j * self.block_size, i * self.block_size,
                                                              self.block_size, self.block_size])
                elif self.grid[i][j] == 9:
                    pygame.draw.rect(self.screen, self.WHITE, [j * self.block_size, i * self.block_size,
                                                               self.block_size, self.block_size])

        # update the screen
        pygame.display.update()
        self.clock.tick(60)

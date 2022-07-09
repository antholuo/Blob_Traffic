"""
blob_env_view

this file controls and updates the movement of the blob as well as visualizing the grid if needed
"""

"""
BETTER VERSION FOUND IN UTILS/PYGAME_VISUALIZER.PY
"""

import pygame
import random
import numpy as np
import os
import sys
from ingest_grid import txt_to_np

# BlobEnvView class
class BlobEnvView:

    # possible directions for the blob to travel
    COMPASS = {"N": [0, 1], "S": [0, -1], "E": [1, 0], "W": [-1, 0]}

    # colours of the paths, walls, blob and goal
    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)
    BLUE = (52, 167, 201)
    PINK = (207, 56, 124)

    # init
    def __init__(self, grid_file_path=None, block_size=None, enable_render=False):

        # yes uwu
        self.game_over = False
        self.reward = 0
        self.block_size = block_size
        self.enable_render = False

        # import the grid from a text file
        self.grid = txt_to_np(grid_file_path)

        self.min_reward = -5 * self.grid.size

        # set grid_size and screen_size
        self.grid_size = self.grid.shape
        self.screen_size = (
            block_size * self.grid_size[0],
            block_size * self.grid_size[1],
        )

        # determine location of walls, blob start and goal based on the text file
        blob_start = np.where(self.grid == 0.1)
        goal = np.where(self.grid == 0.2)
        walls = np.where(self.grid == 0.9)
        self.blob = np.array(list(zip(blob_start[0], blob_start[1])))[0]
        self.goal = np.array(list(zip(goal[0], goal[1])))[0]
        self.walls = np.array(list(zip(walls[0], walls[1])))

        # if we want to visualize it, initialize pygame and call the render method
        if self.enable_render is True:
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode(self.screen_size)
            self.render()

    def location_type(self, location):
        # if location is on the grid
        if (location[0] >= 0 and location[0] < self.grid_size[0]) and (
            location[1] >= 0 and location[1] < self.grid_size[1]
        ):
            # if location is a wall
            if self.grid[location[1]][location[0]] == 0.9:
                return False, -0.75
            # if location has been travelled to before
            elif self.grid[location[1]][location[0]] == 0.3:
                return True, -0.25
            # otherwise
            else:
                return True, -0.05
        else:
            return False, -0.75

    # move_blob
    # called for each step
    def move_blob(self, action):
        # set new_loc to be the new location of the blob
        new_loc = self.blob + np.array(self.COMPASS[action])

        is_valid_location, reward = self.location_type(new_loc)

        # check if new_loc is a valid location for the blob to be, if it is
        # set self.blob to that location and update the grid
        if is_valid_location:
            self.grid[self.blob[1]][self.blob[0]] = 0.3
            self.blob += np.array(self.COMPASS[action])
            self.grid[self.blob[1]][self.blob[0]] = 0.1

        # visualization
        if self.enable_render is True:
            self.render()

        return reward

    # reset_blob
    # called everytime environment is reset
    def reset_blob(self, grid_file_path):
        # resetting grid, blob and goal loaction
        self.grid = txt_to_np(grid_file_path)
        blob_start = np.where(self.grid == 0.1)
        self.blob = np.array(list(zip(blob_start[0], blob_start[1])))[0]

        # visualize
        if self.enable_render is True:
            self.screen = pygame.display.set_mode(self.screen_size)
            self.render()

    # quit_game
    # called when environment is to be deleted
    def quit_game(self):
        if self.game_over is True:
            if self.enable_render is True:
                pygame.display.quit()
            pygame.quit()
            sys.exit()

    # render
    # called if enable_render is True
    # redraws the entire grid - this includes the walkable black blocks, the walls, the blob and the goal
    def render(self):
        # x and y are the location on the screen where the blocks will be drawn
        x, y = 0, 0

        # iterate through each value in self.grid
        for row in self.grid:
            y = 0
            for elem in row:
                rect = pygame.Rect(x, y, self.block_size, self.block_size)

                # based on the number at the location, colour the block a different colour
                if elem == 0.9:
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                if elem == 0 or elem == 0.3:
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                if elem == 0.1:
                    pygame.draw.rect(self.screen, self.BLUE, rect)
                if elem == 0.2:
                    pygame.draw.rect(self.screen, self.PINK, rect)

                y += self.block_size
            x += self.block_size

        # update the display
        pygame.display.update()

    # why this one no work TT ah wtv
    def efficient_render(self, old_loc, new_loc):
        pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(old_loc[1] * self.block_size, old_loc[0] * self.block_size, self.block_size, self.block_size))
        if new_loc is not None:
            pygame.draw.rect(self.screen, self.BLUE, pygame.Rect(new_loc[1] * self.block_size, new_loc[0] * self.block_size, self.block_size, self.block_size))
        pygame.display.update()

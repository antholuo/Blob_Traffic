"""
blob_env_view

this file controls and updates the movement of the blob as well as visualizing the grid if needed
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
    COMPASS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

    # colours of the paths, walls, blob and goal
    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)
    BLUE = (52, 167, 201)
    PINK = (207, 56, 124)

    # init
    def __init__(self, grid_file_path=None, block_size=None, enable_render=True):

        # yes uwu
        self.grid_file_path = grid_file_path
        self.game_over = False
        self.reward = 0
        self.block_size = block_size
        self.enable_render = enable_render

        # import the grid from a text file
        self.grid = txt_to_np(self.grid_file_path)

        # set grid_size and screen_size
        self.grid_size = self.grid.shape[:2]
        self.screen_size = (
            block_size * self.grid_size[0],
            block_size * self.grid_size[1],
        )

        # place the blob at the top left corner and the goal at the bottom right corner
        # we can change this to be decided by the user or text file or wtv in the future
        self.grid = txt_to_np(self.grid_file_path)
        self.blob = []
        self.goal = None
        self.reset_goal = None
        for row_index, row in enumerate(self.grid):
            for col_index, elem in enumerate(row):
                if elem == 1:
                    self.blob.append((col_index, row_index))
                if elem == 2:
                    self.goal = (col_index, row_index)
                    self.reset_goal = (col_index, row_index)

        self.blob = np.array(self.blob, dtype=int)
        self.goal = np.array(self.goal)
        self.reset_goal = np.array(self.reset_goal)

        # if we want to visualize it, initialize pygame and call the render method
        if self.enable_render is True:
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode(self.screen_size)
            self.render()


    # move_blob
    # called for each step
    def move_blob(self, blob, index, action):
        # set new_loc to be the new location of the blob

        new_loc = blob + np.array(self.COMPASS[action])


        # check if new_loc is a valid location for the blob to be, if it is
        # set self.blob to that location and update the grid
        if (
            0 <= new_loc[0] < self.grid_size[0]
            and 0 <= new_loc[1] < self.grid_size[1]
            and self.grid[new_loc[1]][new_loc[0]] != 9
            and self.grid[new_loc[1]][new_loc[0]] != 1
        ):
            self.grid[blob[1]][blob[0]] = 0
            blob += np.array(self.COMPASS[action])
            self.grid[blob[1]][blob[0]] = 1

        if new_loc[0] == 9 and new_loc[1] == 9:
            self.blob = np.delete(self.blob, index, 0)
            self.blob = np.insert(self.blob, index, (-1, -1), axis=0)

        # visualization
        if self.enable_render is True:
            self.render()



    # reset_blob
    # called everytime environment is reset
    def reset_blob(self):
        # resetting grid, blob and goal loaction
        self.grid = txt_to_np(self.grid_file_path)
        self.blob = []
        self.goal = None
        self.reset_goal = None
        for row_index, row in enumerate(self.grid):
            for col_index, elem in enumerate(row):
                if elem == 1:
                    self.blob.append((col_index, row_index))
                if elem == 2:
                    self.goal = (col_index, row_index)
                    self.reset_goal = (col_index, row_index)

        self.blob = np.array(self.blob, dtype=int)
        self.goal = np.array(self.goal)
        self.reset_goal = np.array(self.reset_goal)

        # visualize
        if self.enable_render is True:
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

    # render
    # called if enable_render is True
    # redraws the entire grid - this includes the walkable black blocks, the walls, the blob and the goal
    def render(self):
        # x and y are the location on the screen where the blocks will be drawn
        x, y = 0, 0
        self.grid[self.goal[0]][self.goal[1]] = 2
        # iterate through each value in self.grid
        for row in self.grid:
            y = 0
            for elem in row:
                rect = pygame.Rect(x, y, self.block_size, self.block_size)

                # based on the number at the location, colour the block a different colour
                if elem == 9:
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                if elem == 0:
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                if elem == 1:
                    pygame.draw.rect(self.screen, self.BLUE, rect)
                if elem == 2:
                    pygame.draw.rect(self.screen, self.PINK, rect)

                y += self.block_size
            x += self.block_size

        # update the display
        pygame.display.update()

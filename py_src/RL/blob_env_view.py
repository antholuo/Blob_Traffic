import pygame
import random
import numpy as np
import os
import sys
from ingest_grid import txt_to_np

class BlobEnvView:
    COMPASS = {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "W": (-1, 0)
    }

    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)
    BLUE = (52, 167, 201)
    PINK = (207, 56, 124)
    BLOCKSIZE = 50

    def __init__(self, grid_file_path=None, grid_size=(10,10), screen_size=(800,800), enable_render=True):

        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        self.maze_size = grid_size
        self.game_over = False

        self.block_size = 50

        self.enable_render = enable_render
        self.screen_size = screen_size

        # blob and goal position
        self.grid = txt_to_np(grid_file_path)
        self.blob = np.zeros(2, dtype=int)
        self.goal = np.array([9,7])
        self.grid[self.blob[1]][self.blob[0]] = 1
        self.grid[self.goal[1]][self.goal[0]] = 2

        if self.enable_render is True:
            self.screen = pygame.display.set_mode(self.screen_size)
            self.screen.fill(self.BLACK)
            self.render()

    # action
    def move_blob(self, action):
        new_loc = self.blob + np.array(self.COMPASS[action])


        if self.grid[new_loc[1]][new_loc[0]] != 9 and new_loc[0] >= 0 and new_loc[1] >= 0 and new_loc[0] <= self.grid.shape[0] and new_loc[1] <= self.grid.shape[1]:
            self.grid[self.blob[1]][self.blob[0]] = 0
            self.blob += np.array(self.COMPASS[action])
            self.grid[self.blob[1]][self.blob[0]] = 1

    def reset_blob(self):
        self.blob = np.zeros(2, dtype=int)
        self.goal = np.array([9, 7])
        self.grid[self.blob[1]][self.blob[0]] = 1
        self.grid[self.goal[1]][self.goal[0]] = 2

        if self.enable_render is True:
            self.screen = pygame.display.set_mode(self.screen_size)
            self.screen.fill(self.BLACK)
            self.render()


    def quit_game(self):
        if self.game_over is True:
            if self.enable_render is True:
                pygame.display.quit()
            pygame.quit()
            sys.exit()

    # idk what this is for
    def update(self, mode):
        pass

    def render(self):
        x, y = 0, 0
        for row in self.grid:
            y = 0
            for elem in row:
                # we can do this better by just... not drawing the black squares since bg is already black and also only drawing the walls once since they never move
                # but... we would need to cover up the tracks made by the blue blob with black ... hmmm ...
                if elem == 9:
                    rect = pygame.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                    pygame.draw.rect(self.screen, self.WHITE, rect)

                if elem == 0:
                    rect = pygame.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                    pygame.draw.rect(self.screen, self.BLACK, rect)

                if elem == 1:
                    rect = pygame.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                    pygame.draw.rect(self.screen, self.BLUE, rect)

                if elem == 2:
                    rect = pygame.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                    pygame.draw.rect(self.screen, self.PINK, rect)

                y += 50
            x += 50








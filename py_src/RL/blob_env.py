import gym
from gym import spaces
import numpy as np
from ingest_grid import txt_to_np
import pygame
import sys

BLACK = (50, 50, 50)
WHITE = (200, 200, 200)
BLUE = (52, 167, 201)
PINK = (207, 56, 124)
BLOCKSIZE = 50
# in the future we find a way to generate these or smth
DEST_X = 450
DEST_Y = 350
WINDOW_HEIGHT = BLOCKSIZE * 8
WINDOW_WIDTH = BLOCKSIZE * 10

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

def drawDest(x, y):
    rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
    pygame.draw.rect(SCREEN, PINK, rect)


class Wall():
    def __init__(self):
        self.np_grid = txt_to_np("grid.txt")
        print(self.np_grid)
        self.wall_list = []

        # okay so current im flipping it so it matches with the grid.txt file idk what we actually want tho
        for i in range(len(self.np_grid)):
            for j in range(len(self.np_grid[0])):
                if self.np_grid[i][j] == 9:
                    self.wall_list.append((j * BLOCKSIZE, i * BLOCKSIZE))

    def render(self):
        for block in self.wall_list:
            rect = pygame.Rect(block[0], block[1], BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, WHITE, rect)

class Dest():
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def render(self):
        rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, PINK, rect)


class Blob():
    def __init__(self, x_pos, y_pos, wall_list):
        self.x = x_pos
        self.y = y_pos
        self.prev_x = x_pos
        self.prev_y = y_pos
        self.wall_list = wall_list

    def render(self):
        rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, BLUE, rect)

class BlobEnv(gym.Env):
    def __init__(self):

        self.do_render = True

        self.action_space = spaces.Discrete(4)

        self.maze_size = (10, 8)

        low = np.zeros(len(self.maze_size), dtype=int)
        high =  np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)
        self.observation_space = spaces.Box(low, high, dtype=np.int64)


        # elements present inside the environment
        self.walls= Wall()
        self.blob = Blob(0, 0, self.walls.wall_list)
        self.dest = Dest(DEST_X, DEST_Y)
        self.elements = [self.blob, self.dest, self.walls.wall_list]

        self.reward = 0
        self.done = False

        if self.do_render:
            pygame.init()
            SCREEN.fill(BLACK)
            drawGrid()
            self.walls.render()
            self.dest.render()
            self.blob.render()

    def step(self, action):
        if action == 0:
            self.blob.y -= 50
        if action == 1:
            self.blob.y += 50
        if action == 2:
            self.blob.x -= 50
        if action == 3:
            self.blob.x += 50

        if (self.blob.x, self.blob.y) in self.walls.wall_list:
            self.blob.x = self.blob.prev_x
            self.blob.y = self.blob.prev_y
        elif self.blob.x < 0 or self.blob.y < 0 or self.blob.x > WINDOW_WIDTH - 50 or self.blob.y > WINDOW_HEIGHT - 50:
            self.blob.x = self.blob.prev_x
            self.blob.y = self.blob.prev_y

        self.blob.prev_y = self.blob.y
        self.blob.prev_x = self.blob.x

        if (self.blob.x, self.blob.y) == (self.dest.x, self.dest.y):
            self.done = True

        if self.do_render:
            self.blob.render()
            pygame.display.update()

        if self.done == True:
            self.reward += 50
        else:
            self.reward -= 1


        blob_x = self.blob.x
        blob_y = self.blob.y
        wall_list = self.walls.wall_list
        dest_x = self.dest.x
        dest_y = self.dest.y

        self.observation = [blob_x, blob_y, dest_x, dest_y] + wall_list

        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        self.blob.x = 0
        self.blob.y = 0
        self.reward = 0

        blob_x = self.blob.x
        blob_y = self.blob.y
        wall_list = self.walls.wall_list
        dest_x = self.dest.x
        dest_y = self.dest.y

        self.observation = [blob_x, blob_y, wall_list, dest_x, dest_y]

        return self.observation



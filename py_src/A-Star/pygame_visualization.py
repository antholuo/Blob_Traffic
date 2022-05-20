import pygame
import sys
import numpy as np
from ingest_grid import txt_to_np

'''

'''
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

    def update(self):
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.y -= 50
            if event.key == pygame.K_s:
                self.y += 50
            if event.key == pygame.K_a:
                self.x -= 50
            if event.key == pygame.K_d:
                self.x += 50

        if not self.check_valid():
            self.x = self.prev_x
            self.y = self.prev_y

        self.prev_y = self.y
        self.prev_x = self.x

    def check_valid(self):
        if (self.x, self.y) in self.wall_list:
            return False
        if self.x < 0 or self.y < 0 or self.x > WINDOW_WIDTH - 50 or self.y > WINDOW_HEIGHT - 50:
            return False
        return True

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    walls = Wall()
    blob = Blob(0, 0, walls.wall_list)

    while True:
        SCREEN.fill(BLACK)
        drawGrid()
        walls.render()
        blob.update()
        blob.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (blob.x == DEST_X and blob.y == DEST_Y):
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
    drawDest(DEST_X, DEST_Y)

def drawDest(x, y):
    rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
    pygame.draw.rect(SCREEN, PINK, rect)


if __name__ == "__main__":
    main()
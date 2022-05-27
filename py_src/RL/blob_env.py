
import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from blob_env_view import BlobEnvView

class BlobEnv(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    ACTION = ["N", "E", "S", "W"]

    def __init__(self, maze_file=None, maze_size=None, mode=None, enable_render=True):

        self.viewer = None
        self.enable_render = enable_render

        self.maze_view = BlobEnvView(grid_file_path="grid.txt", grid_size=(10,10), screen_size=(500,500), enable_render=True)

        self.maze_size = self.maze_view.maze_size

        self.action_space = spaces.Discrete(2 * len(self.maze_size))

        # not quite sure what is going on here tbh
        low = np.zeros(len(self.maze_size), dtype=int)
        high = np.array(self.maze_size, dtype=int) - np.ones(len(self.maze_size), dtype=int)
        self.observation_space = spaces.Box(low, high, shape=(2,) ,dtype=np.int64)

        self.state = None
        self.steps_beyond_done = None

        self.reward = 0

        # Simulation related variables.
        self.seed()
        self.reset()

        # Just need to initialize the relevant attributes
        self.configure()

    def __del__(self):
        if self.enable_render is True:
            self.maze_view.quit_game()

    def configure(self, display=None):
        self.display = display

    # no clue what this is for
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.maze_view.move_blob(self.ACTION[action])

        # check to see if blob has made it
        if np.array_equal(self.maze_view.blob, self.maze_view.goal):
            self.reward += 1
            self.maze_view.game_over = True
            done = True
        else:
            self.reward += -0.1/(self.maze_size[0]*self.maze_size[1])
            done = False

        self.state = self.maze_view.blob

        info = {}

        return self.state, self.reward, done, info

    def reset(self):
        self.maze_view.reset_blob()
        self.state = np.zeros(2, dtype=int)
        self.steps_beyond_done = None
        self.done = False
        self.reward = 0
        return self.state

    def is_game_over(self):
        return self.maze_view.game_over

    def render(self, mode="human", close=False):
        if close:
            self.maze_view.quit_game()

        return self.maze_view.update(mode)

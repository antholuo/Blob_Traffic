"""
blob_env

this file sets up the environment in which the agent will be trained
calls blob_env_view for the actual movement of the blob and visualization
"""

# imports
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from blob_env_view import BlobEnvView

# BlobEnv
# child class of the gym Env class
class BlobEnv(gym.Env):

    # different kind of modes ... honestly not too sure what this is for i think its just different display modes tho
    # we not using this rn hehe
    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    # possible actions the blob can take (moving N, S, E, W)
    ACTION = ["N", "E", "S", "W"]

    # __init__
    # initializing the environment
    # not quite sure what to do with the mode ... (confusion TT)
    def __init__(self, grid_file=None, block_size=50, mode=None, enable_render=True):

        self.enable_render = enable_render

        self.grid_file = grid_file

        # set up the visualization
        self.grid_view = BlobEnvView(
            grid_file_path=grid_file, block_size=block_size, enable_render=enable_render
        )

        # grid_size is a tuple: (x, y)
        self.grid_size = self.grid_view.grid_size

        # action_space is the number of possible actions - N,E,S,W is 4
        self.action_space = spaces.Discrete(4)

        # honestly not quite sure why we need a low and high ... i think its just to keep the observation (state) in check
        # low is top left corner
        low = np.zeros(len(self.grid_view.grid.flatten()), dtype=np.float)
        low = np.append(low, -1)

        # print("lower boiumd ois", low)

        # high is bottom right corner
        high = np.ones(len(self.grid_view.grid.flatten()), dtype=np.float)
        high = np.append(high, 4)

        # print("upper bound is", high)

        # the shape of observation_space must match self.observation, since what is what is being returned by step and reset
        # for us it has shape of 2 since all we are storing in the state rn is blob location
        self.observation_space = spaces.Box(low = low, high = high, dtype=np.float)

        # initialize state and reward
        self.observation = None
        self.reward = 0

        # reset the environment just because :D
        self.reset()

    # __del__
    # quit the visualization
    def __del__(self):
        if self.enable_render is True:
            self.grid_view.quit_game()

    # step
    # every action of the blob (N,E,S,W)
    def step(self, action):
        # translate a value between 0-3 to a compass direction
        step_reward = self.grid_view.move_blob(self.ACTION[action])

        # check to see if blob has made it to the goal
        if np.array_equal(self.grid_view.blob, self.grid_view.goal):
            self.reward += 1
            self.grid_view.game_over = True
            done = True
        # have a min reward so blob cannot just fail forever
        elif self.reward < self.grid_view.min_reward:
            self.grid_view.game_over = True
            done=True
        else:
            self.reward += step_reward
            done = False

        # the observation space will be the grid and the action taken
        self.observation = np.append(self.grid_view.grid.flatten(), 4)
        # self.observation = np.array(self.observation, dtype=np.float)

        # not sure what info needs to be but it needs to be returned by step bc parent class stuff idek
        info = {}

        return self.observation, self.reward, done, info

    # reset
    # resets the environment everytime a run is over
    def reset(self):
        self.grid_view.reset_blob(self.grid_file)
        self.observation = np.append(self.grid_view.grid.flatten(), -1)
        self.done = False
        self.reward = 0
        return self.observation

    # render
    # not sure what this is for ... changes the mode ig? not used rn maybe good to keep for future idek
    def render(self, mode="human", close=False):
        if close:
            self.grid_view.quit_game()

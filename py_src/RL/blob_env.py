"""
blob_env

this file sets up the environment in which the agent will be trained
calls blob_env_view for the actual movement of the blob and visualization
"""

# todo: our observation space always needs to stay the same size!

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

        # set up the visualization
        self.grid_view = BlobEnvView(
            grid_file_path=grid_file, block_size=block_size, enable_render=enable_render
        )

        # grid_size is a tuple: (x, y)
        self.grid_size = self.grid_view.grid_size

        # action_space is the number of possible actions - N,E,S,W is 4
        self.action_space = spaces.Discrete(4)

        # ! this is for q-table
        # low is top left corner
        low = np.zeros(len(self.grid_view.blob) * 2, dtype=int)
        # high is bottom right corner
        high = np.full(len(self.grid_view.blob) * 2, 9, dtype=int)

        # the shape of observation_space must match self.state, since what is what is being returned by step and reset
        # for us it has shape of 2 since all we are storing in the state rn is blob location
        self.observation_space = spaces.Box(low, high, shape=(len(self.grid_view.blob) * 2,), dtype=np.int64)

        # # ! this is for dqn
        # # low is top left corner
        # low = np.zeros(self.grid_view.grid.shape, dtype=np.uint8)
        # # high is bottom right corner
        # high = np.full(self.grid_view.grid.shape, 255, dtype=np.uint8)
        #
        # # the shape of observation_space must match self.state, since what is what is being returned by step and reset
        # # for us it has shape of 2 since all we are storing in the state rn is blob location
        # self.observation_space = spaces.Box(low, high, shape=self.grid_view.grid.shape, dtype=np.uint8)

        # initialize state and reward
        self.state = None
        self.reward = 0

        # reset the environment just because :D
        self.reset()

    # __del__
    # quit the visualization
    def __del__(self):
        if self.enable_render is True:
            self.grid_view.quit_game()

    # def check_done(self):
    #     for index, blob in enumerate(self.grid_view.blob):
    #         if blob[0] == 9 and blob[1] == 9:
    #             print("99 arrived")
    #         if not np.array_equal(blob, self.grid_view.goal):
    #             return False
    #         else:
    #             self.grid_view.blob = np.delete(self.grid_view.blob, index, 0)
    #             # self.grid_view.goal = self.grid_view.reset_goal
    #             self.grid_view.grid[self.grid_view.goal[0], self.grid_view.goal[1]] = 2
    #     return True

    def check_done(self):
        for val in self.grid_view.blob.flatten():
            if val != -1:
                return False
        return True
    # step
    # every action of the blob (N,E,S,W)
    def step(self, action):
        for index, blob in enumerate(self.grid_view.blob):
            if blob[0] != -1 and blob[1] != -1:
                # translate a value between 0-3 to a compass direction
                self.grid_view.move_blob(blob, index, self.ACTION[action])

        # check to see if blob has made it to the goal
        if self.check_done():
            self.reward += 1
            self.grid_view.game_over = True
            done = True
        else:
            self.reward += -0.1 / (self.grid_size[0] * self.grid_size[1])
            done = False

        # # set the state to the blob location
        self.state = self.grid_view.blob
        self.state = self.state.flatten()

        # not sure what info needs to be but it needs to be returned by step bc parent class stuff idek
        info = {}

        return self.state, self.reward, done, info

    # reset
    # resets the environment everytime a run is over
    def reset(self):
        self.grid_view.reset_blob()
        self.state = np.zeros(len(self.grid_view.blob) * 2, dtype=int)
        self.done = False
        self.reward = 0
        return self.state

    # render
    # not sure what this is for ... changes the mode ig? not used rn maybe good to keep for future idek
    def render(self, mode="human", close=False):
        if close:
            self.grid_view.quit_game()

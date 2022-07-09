"""
check_env

checking and testing our custom blob environment
"""

# imports
from stable_baselines3.common.env_checker import check_env
from blob_env import BlobEnv
import pygame

# checking the environment
env = BlobEnv(grid_file="grid.txt")

# check_env takes a little bit of time so there is a small lag in the first run
# comment this out if you want it already passes but in case we change smth its here :D
check_env(env)

# testing the environment
episodes = 5
done = False

# for each episode in range we run the blob in the environment
for episode in range(episodes):

    # set done to False and reset the environment
    done = False
    obs = env.reset()

    # while the done is False, so when the blob has not yet reached the goal
    while not done:
        # let the blob move in randomly chosen directions
        random_action = env.action_space.sample()
        print("action", random_action)

        # move the blob
        # once the blob reaches the destination, done will be True and the episode will end
        obs, reward, done, info = env.step(random_action)
        print("reward", reward)
    print("goal reached \n\n")
    pygame.time.delay(500)

print("finished running all episodes, exiting program now")

# after we are done running, quit the visualization
env.__del__()

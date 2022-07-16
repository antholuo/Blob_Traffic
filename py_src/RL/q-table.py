"""
https://github.com/MattChanTK/ai-gym/blob/master/maze_2d/maze_2d_q_learning.py :D
"""

import sys
import numpy as np
import math
import random

import gym
from blob_env import BlobEnv

def simulate():

    # Instantiating the learning related parameters
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    discount_factor = 0.99

    num_streaks = 0

    # Render tha maze
    env.render()

    for episode in range(NUM_EPISODES):

        # Reset the environment
        obv = env.reset()

        # the initial state
        state_0 = tuple(obv)
        total_reward = 0

        for t in range(MAX_T):

            # Select an action
            action = select_action(state_0, explore_rate)
            print(action)
            # execute the action
            obv, reward, done, info = env.step(action)

            # Observe the result
            state = tuple(obv)
            total_reward += reward

            # Update the Q based on the result

            # np.amax gets the maximum value of the array`1
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])

            # Setting up for the next iteration
            state_0 = state

            # Render tha maze
            if RENDER_MAZE:
                env.render()

            if done:
                print("Episode %d finished after %f time steps with total reward = %f (streak %d)."
                      % (episode, t, total_reward, num_streaks))

                if t <= SOLVED_T:
                    num_streaks += 1
                else:
                    num_streaks = 0
                break

            elif t >= MAX_T - 1:
                print("Episode %d timed out at %d with total reward = %f."
                      % (episode, t, total_reward))

        # It's considered done when it's solved over 120 times consecutively
        if num_streaks > STREAK_TO_END:
            break

        # Update parameters
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)


def select_action(state, explore_rate):
    # Select a random action
    if random.random() < explore_rate:
        action = env.action_space.sample()
    # Select the action with the highest q
    else:
        action = int(np.argmax(q_table[state]))
    return action


def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))

if __name__ == "__main__":

    # Initialize the "maze" environment
    env = BlobEnv(grid_file="grid.txt")

    print("Action Space {}".format(env.action_space))
    print("State Space {}".format(env.observation_space))

    '''
    Defining the environment related constants
    '''
    # Number of discrete states (bucket) per state dimension
    # one bucket per grid
    MAZE_SIZE = tuple([10, 10])

    # Number of discrete actions
    NUM_ACTIONS = env.action_space.n  # ["N", "S", "E", "W"]

    '''
    Learning related constants
    '''
    MIN_EXPLORE_RATE = 0.001
    MIN_LEARNING_RATE = 0.2
    DECAY_FACTOR = np.prod(MAZE_SIZE, dtype=float) / 10.0

    '''
    Defining the simulation related constants
    '''
    NUM_EPISODES = 50000
    MAX_T = np.prod(MAZE_SIZE, dtype=int) * 100
    STREAK_TO_END = 100
    SOLVED_T = np.prod(MAZE_SIZE, dtype=int)
    DEBUG_MODE = 0
    RENDER_MAZE = True
    ENABLE_RECORDING = True

    '''
    Creating a Q-Table for each state-action pair
    '''
    print(MAZE_SIZE)
    print(NUM_ACTIONS)
    q_table = np.zeros(MAZE_SIZE + (NUM_ACTIONS,), dtype=np.float64)

    '''
    Begin simulation
    '''
    simulate()


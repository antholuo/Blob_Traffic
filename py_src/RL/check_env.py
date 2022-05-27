from stable_baselines3.common.env_checker import check_env
from blob_env import BlobEnv

env = BlobEnv()
episodes = 5
done = False

for episode in range(episodes):
    done = False
    obs = env.reset()

    while not done:
        random_action = env.action_space.sample()
        print("action", random_action)
        obs, reward, done, info = env.step(random_action)
        print("reward", reward)

    print("goal reached \n\n")

print("finished running all episodes, exiting program now")
env.__del__()

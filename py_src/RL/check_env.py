from stable_baselines3.common.env_checker import check_env
from blob_env import BlobEnv

env = BlobEnv()

check_env(env)
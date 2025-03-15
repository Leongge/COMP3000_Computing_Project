"""Uses Stable-Baselines3 to train agents to play the Waterworld environment using SuperSuit vector envs.

For more information, see https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html

Author: Elliot (https://github.com/elliottower)
"""
from __future__ import annotations

import glob
import os
import time

import supersuit as ss
from stable_baselines3 import SAC
from stable_baselines3.sac import MlpPolicy
from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback, EvalCallback

from pettingzoo.sisl import waterworld_v4
# from pettingzoo.butterfly import pistonball_v6
# import marlenv_custom
import marlenv_DM

def train_butterfly_supersuit(
    env_fn, steps: int = 10_000, seed: int | None = 0, **env_kwargs
):
    # Train a single model to play as each agent in a cooperative Parallel environment
    env = env_fn.parallel_env(**env_kwargs)

    env.reset(seed=seed)

    print(f"Starting training on {str(env.metadata['name'])}.")

    env = ss.pettingzoo_env_to_vec_env_v1(env)
    env = ss.concat_vec_envs_v1(env, 1, num_cpus=1, base_class="stable_baselines3")

    # Account for the number of parallel environments
    eval_callback = EvalCallback(
        env,
        best_model_save_path=f"marl/models/bests",
        n_eval_episodes=2,
        log_path="marl",
        eval_freq=2000,
        deterministic=True,
    )

    checkpoint_callback = CheckpointCallback(
        save_freq=20,
        save_path="check_point",
        name_prefix="marl",
        verbose=2
    )

    # Callback list
    callback_list = [
        eval_callback,
        checkpoint_callback
    ]

    # Note: Use stable baselines 3 -> SAC algorithm
    model = SAC(
        MlpPolicy,
        env,
        verbose=2,
        learning_rate=1e-3,
        batch_size=256,
        #need to install cuDNN for cuda version (cuDNN Archive), check cuda driver , pytorch.org
        #find cuba in NVIDIA GPU Computing Toolkit
        #nvidia-msi (in cmd)
        #put the cuDNN into the cuda version(12.1)
        #device="cuda"
    )

    # model_path = r"check_point/marl_49920_steps.zip"
    model_path = r"CUSTOMMARL_20240318-181400.zip"
    model = SAC.load(path=model_path, env=env)

    model.learn(total_timesteps=steps, log_interval=4, callback=callback_list)

    model.save(f"{env.unwrapped.metadata.get('name')}_{time.strftime('%Y%m%d-%H%M%S')}")

    print("Model has been saved.")

    print(f"Finished training on {str(env.unwrapped.metadata['name'])}.")

    env.close()

    # rewards = {agent: 0 for agent in env.possible_agents}

    # Note: We train using the Parallel API but evaluate using the AEC API
    # SB3 models are designed for single-agent settings, we get around this by using he same model for every agent
    # for i in range(1):
    #     env.reset(seed=i)
    #
    #     for agent in env.agent_iter():
    #         obs, reward, termination, truncation, info = env.last()
    #
    #         for a in env.agents:
    #             rewards[a] += env.rewards[a]
    #         if termination or truncation:
    #             break
    #         else:
    #             act = model.predict(obs, deterministic=True)[0]
    #
    #         env.step(act)
    # env.close()
    #
    # avg_reward = sum(rewards.values()) / len(rewards.values())
    # print("Rewards: ", rewards)
    # print(f"Avg reward: {avg_reward}")
    # return avg_reward


#Get check point and put in eval, so that it will just run one time
#change the SAC.load(checkPoint_path, env=env)
#we can define the num_games in main, else it will just take the default value.
def eval(env_fn, num_games: int = 100, render_mode: str | None = None, **env_kwargs):
    # Evaluate a trained agent vs a random agent
    env = env_fn.env(render_mode=render_mode, **env_kwargs)

    print(
        f"\nStarting evaluation on {str(env.metadata['name'])} (num_games={num_games}, render_mode={render_mode})"
    )

    # try:
    #     latest_policy = max(
    #         glob.glob(f"{env.metadata['name']}*.zip"), key=os.path.getctime
    #     )
    # except ValueError:
    #     print("Policy not found.")
    #     exit(0)
    #
    # model = SAC.load(latest_policy)

    model_path = r"check_point/marl_96000_steps.zip"
    model = SAC.load(path=model_path)

    rewards = {agent: 0 for agent in env.possible_agents}

    # Note: We train using the Parallel API but evaluate using the AEC API
    # SB3 models are designed for single-agent settings, we get around this by using he same model for every agent
    for i in range(num_games):
        env.reset(seed=i)

        for agent in env.agent_iter():
            obs, reward, termination, truncation, info = env.last()

            for a in env.agents:
                rewards[a] += env.rewards[a]
            if termination or truncation:
                break
            else:
                act = model.predict(obs, deterministic=True)[0]

            env.step(act)
    env.close()

    avg_reward = sum(rewards.values()) / len(rewards.values())
    print("Rewards: ", rewards)
    print(f"Avg reward: {avg_reward}")
    return avg_reward


if __name__ == "__main__":
    # env_fn = waterworld_v4
    # env_fn = pistonball_v6
    env_fn = marlenv_DM
    env_kwargs = {}

    # Train a marl model
    # train_butterfly_supersuit(env_fn, steps=196_608, seed=0, **env_kwargs)
    eval(env_fn, num_games=1, seed=0, **env_kwargs)

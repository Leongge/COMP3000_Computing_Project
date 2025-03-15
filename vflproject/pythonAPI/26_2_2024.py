import os
import json
from collections import defaultdict
from typing import Callable

import numpy as np
import gymnasium as gym
from gymnasium.utils import EzPickle, seeding

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from pettingzoo.utils.conversions import aec_to_parallel_wrapper
import os
import sys
from ParamAgent import ParamAgent

sys.path.append(os.path.join(os.getcwd(), "hflib"))
from hflib import launch


def env(**kwargs):
    vflenv = MARLEnv(**kwargs)
    vflenv = wrappers.ClipOutOfBoundsWrapper(vflenv)
    vflenv = wrappers.OrderEnforcingWrapper(vflenv)
    return vflenv


def parallel_wrapper_fn(env_fn: Callable) -> Callable:
    def par_fn(**kwargs):
        penv = env_fn(**kwargs)
        penv = aec_to_parallel_wrapper(penv)
        return penv

    return par_fn


parallel_env = parallel_wrapper_fn(env)

class MARLEnv(AECEnv, EzPickle):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "name": "CUSTOMMARL",
        "is_parallelizable": True,
        "has_manual_policy": True,
        "render_mode": None
    }

    def __init__(self, *args, **kwargs):
        EzPickle.__init__(self, *args, **kwargs)

        # Your custom object to be initialize here
        # For example: HFAPI?
        self.hflaunch = launch.HFLaunch()

        self.dictionary_of_all_agents_observations = {}

        # Agent selection
        self.agents = ["Parameter_" + str(r) for r in range(5)]
        self.possible_agents = self.agents[:]
        self.agent_name_mapping = dict(zip(self.agents, list(range(5))))
        self._agent_selector = agent_selector(self.agents)

        # Action spaces
        # Set design parameter range
        n_action = 1  # C1, L1, C2, L2, C3, L3
        # parameter range are between 10-100
        p_min = -1
        p_max = 1
        each_agent_action_space = gym.spaces.Box(low=-p_min, high=p_max, shape=(n_action,),
                                                 dtype=np.float32)  # your normal gym action space
        self.action_spaces = dict(zip(
            self.agents,
            [each_agent_action_space] * self.num_agents,
        ))

        # State spaces
        # Observation S parameter
        n_obs = 4  # S11, S12, S21, S22
        s_min = 0
        s_max = 1
        each_agent_observation_sapce = gym.spaces.Box(low=s_min, high=s_max, shape=(n_obs,),
                                                      dtype=np.float32, )  # your normal gym observation space
        self.observation_spaces = dict(zip(
            self.agents,
            [each_agent_observation_sapce] * self.num_agents,
        ))

        # State (global observation)
        self.state_space = gym.spaces.Box(
            low=s_min,
            high=s_max,
            shape=(n_obs,),
            dtype=np.float32,
        )
        self.state = np.asarray([0 for _ in range(n_obs)], dtype=np.float32)

        # Miscellaneous
        self.render_mode = None

        # set 3 goal
        self.goals = {
            'g0': {'series': 'S11', 'value': -15, 'min': 0.1, 'max': 0.45},
            'g1': {'series': 'S21', 'value': -15, 'min': 0.01, 'max': 0.079},
            'g2': {'series': 'S21', 'value': -15, 'min': 0.554, 'max': 1.0}
        }

        # initialize
        self.design_parameters = [
            {"Name": "c1", "Value": 99.81559268198907, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l1", "Value": 17.71350271999836, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c2", "Value": 19.814235474914312, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l2", "Value": 54.64225618168712, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c3", "Value": 13.813209887593985, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l3", "Value": 95.40046508423984, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0}
        ]

        # dictionary of param agents
        self.param_agents = dict(zip(self.agents, [ParamAgent(idx, self.design_parameters, self.goals) for idx in
                                                   range(len(self.design_parameters))]))

    def observe(self, agent):
        """
        Return individual observation
        """
        return self.param_agents[agent].observe()

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def step(self, action):
        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return

        # Select current agent
        # action = np.asarray(action)
        agent = self.agent_selection

        # Update agent current value
        agent_index = self.agent_name_mapping[agent]
        self.param_agents[agent].update_value(step_size=action)
        self.design_parameters[agent_index]["Value"] = self.param_agents[agent].current_value

        # Your step logic is here (same like gym env step)
        response = self.hflaunch.update_design(variable_list=self.design_parameters)

        # Get S parameter
        s_parameters = self.extract_s_parameters(response)
        frequency_values = self.extract_frequency_values(response)
        self.param_agents[agent].s_parameters = s_parameters
        self.param_agents[agent].frequency_values = frequency_values

        # Since you are treating each design parameter as your agent, reward is calculated
        # after all agents are updated. Thus if the current agent is last agent and finish stepping,
        # design response is then simulated and evaluated.
        if self._agent_selector.is_last():
            # Update the following:
            # 1. self.terminate
            self.terminate = self.check_goals(s_parameters, frequency_values)
            # 2. self.rewards
            all_agents_current_rewards = [self.param_agents[ag].calculate_reward() for ag in self.param_agents]
            self.rewards = dict(zip(self.agents, all_agents_current_rewards))
            # self.rewards = self.calculate_reward(s_parameters, frequency_values)

            all_agents_termination = [self.param_agents[ag].check_goals() for ag in self.param_agents]
            self.terminations = dict(zip(self.agents, all_agents_termination))
            self.truncations = dict(zip(self.agents, [False for _ in self.agents]))

        else:
            self._clear_rewards()

        self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = self._agent_selector.next()  # Here update agent_selection to point to next agent
        self._accumulate_rewards()

        # if self.render_mode == "human":
        #     self.render()

    def reset(self, seed=None, options=None):
        # your reset logic, reset hfapi?
        # initialize
        self.design_parameters = [
            {"Name": "c1", "Value": 99.81559268198907, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l1", "Value": 17.71350271999836, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c2", "Value": 19.814235474914312, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l2", "Value": 54.64225618168712, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c3", "Value": 13.813209887593985, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l3", "Value": 95.40046508423984, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0}
        ]

        # dictionary of param agents
        self.param_agents = dict(zip(self.agents, [ParamAgent(idx, self.design_parameters, self.goals) for idx in
                                                   range(len(self.design_parameters))]))

        # Your step logic is here (same like gym env step)
        response = self.hflaunch.update_design(variable_list=self.design_parameters)

        # Get S parameter
        s_parameters = self.extract_s_parameters(response)
        frequency_values = self.extract_frequency_values(response)
        for agent in self.agents:
            self.param_agents[agent].s_parameters = s_parameters
            self.param_agents[agent].frequency_values = frequency_values

        self.agents = self.possible_agents[:]
        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.next()

        all_agents_current_rewards = [self.param_agents[ag].calculate_reward() for ag in self.param_agents]
        self.rewards = dict(zip(self.agents, all_agents_current_rewards))
        # self.rewards = dict(zip(self.agents, [0 for _ in self.agents]))
        self._cumulative_rewards = dict(zip(self.agents, [0 for _ in self.agents]))
        self.terminations = dict(zip(self.agents, [False for _ in self.agents]))
        self.truncations = dict(zip(self.agents, [False for _ in self.agents]))
        self.infos = dict(zip(self.agents, [{} for _ in self.agents]))

    def extract_s_parameters(self, response):
        # from response get S parameters
        s_parameters = {}
        if "SimulationResult" in response and "Response1" in response["SimulationResult"]:
            series_data = response["SimulationResult"]["Response1"]["Series"]
            for series_name, series_info in series_data.items():
                s_parameters[series_info["Name"]] = series_info["DataY"]

        return s_parameters

    def extract_frequency_values(self, response):
        frequency_values = []
        if "SimulationResult" in response and "Response1" in response["SimulationResult"]:
            series_data = response["SimulationResult"]["Response1"]["Series"]
            if any(series_data.values()):
                first_series = next(iter(series_data.values()))
                if "DataX" in first_series:
                    frequency_values = first_series["DataX"]
        return frequency_values

        # def calculate_reward(self, s_parameters, frequency_values):
        #     reward = 0
        #     for i, goal in enumerate(self.goals.values()):
        #         if goal['series'] in s_parameters and i < len(frequency_values):
        #             if (goal['min'] <= frequency_values[i] <= goal['max']) and (
        #                     s_parameters[goal['series']][i] <= goal['value']):
        #                 reward += 1  # Increase reward for meeting the goal
        #     return reward

        #     def calculate_reward(self, s_parameters, frequency_values):
        #         reward = 0
        #         for i, goal in enumerate(self.goals.values()):
        #             if goal['series'] in s_parameters and i < len(frequency_values):
        #                 # Ensure s_parameter is not less than goal_value
        #                 s_value = max(s_parameters[goal['series']][i], goal['value'])

        #                 if goal['min'] <= frequency_values[i] <= goal['max']:
        #                     # Calculate Euclidean distance for each point
        #                     distances = [np.linalg.norm(
        #                         np.array([0, s_value]) - np.array([0, goal['value']]))]

        #                     # Calculate cost based on Euclidean distance
        #                     cost = np.mean(distances)

        #                     # Convert cost to reward (higher distance -> lower reward)
        #                     reward += 1 - cost

        #         return reward

        # def check_goals(self, s_parameters, frequency_values):
        #     for i, goal in enumerate(self.goals.values()):
        #         if goal['series'] in s_parameters and i < len(frequency_values):
        #             if not ((goal['min'] <= frequency_values[i] <= goal['max']) and (
        #                     goal['min'] <= s_parameters[goal['series']][i] <= goal['max']) and (
        #                             s_parameters[goal['series']][i] <= goal['value'])):
        #                 return False  # Goal not achieved
        #     return True  # Achieved all goals

        #     def make_observation(self, s_parameters, frequency_values):
        #         goal = None
        #         for g, g_info in self.goals.items():
        #             if g_info['series'] == 'S11':
        #                 goal = g_info
        #                 break

        #         if goal is None:
        #             return None

        #         min_frequency = goal['min']
        #         max_frequency = goal['max']

        #         # find the frequency value index between the min max
        #         indices = []
        #         for i, freq_value in enumerate(frequency_values):
        #             if min_frequency <= freq_value <= max_frequency:
        #                 indices.append(i)

        #         # get index per 10
        #         selected_indices = indices[::10]

        #         # get s_parameter based on the index
        #         selected_s_parameters = [s_parameters['S11'][i] for i in selected_indices]
        #         return selected_s_parameters



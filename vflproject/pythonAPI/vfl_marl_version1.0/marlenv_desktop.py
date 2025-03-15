import os
import json
import copy
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
# sys.path.append(r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0")
# sys.path.append(r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0\hflib")
vflproject_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Assuming "vflproject" is a subdirectory
package_root = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0", "hflib")
project_root = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0")

sys.path.append(package_root)
sys.path.append(project_root)


from hflib import launch


def env(c1, l1, c2, l2, c3, l3, c1_O_min, c1_O_max, l1_O_min, l1_O_max,
        c2_O_min, c2_O_max, l2_O_min, l2_O_max, c3_O_min, c3_O_max,
        l3_O_min, l3_O_max, g0_s, g1_s, g2_s, g0_v, g1_v, g2_v,
        g0_mi, g0_ma, g1_mi, g1_ma, g2_mi, g2_ma, **kwargs):
    vflenv = MARLEnv(c1=c1, l1=l1, c2=c2, l2=l2, c3=c3, l3=l3,
                     c1_O_min=c1_O_min, c1_O_max=c1_O_max, l1_O_min=l1_O_min,
                     l1_O_max=l1_O_max, c2_O_min=c2_O_min, c2_O_max=c2_O_max,
                     l2_O_min=l2_O_min, l2_O_max=l2_O_max, c3_O_min=c3_O_min,
                     c3_O_max=c3_O_max, l3_O_min=l3_O_min, l3_O_max=l3_O_max,
                     g0_s=g0_s, g1_s=g1_s, g2_s=g2_s,
                     g0_v=g0_v, g1_v=g1_v, g2_v=g2_v,
                     g0_mi=g0_mi, g1_mi=g1_mi, g2_mi=g2_mi,
                     g0_ma=g0_ma, g1_ma=g1_ma, g2_ma=g2_ma, **kwargs)
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

    def __init__(self,c1, l1, c2, l2, c3, l3, c1_O_min, c1_O_max,
                 l1_O_min, l1_O_max, c2_O_min, c2_O_max, l2_O_min,
                 l2_O_max, c3_O_min, c3_O_max, l3_O_min, l3_O_max,
                 g0_s, g1_s, g2_s,
                 g0_v, g1_v, g2_v,
                 g0_mi, g1_mi, g2_mi,
                 g0_ma, g1_ma, g2_ma, *args, **kwargs):
        EzPickle.__init__(self, *args, **kwargs)

        # Your custom object to be initialize here
        # For example: HFAPI?
        # designpath = r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0\BPF-4-100M-450M.fpx"
        designpath = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0", "BPF-4-100M-450M.fpx")
        self.hflaunch = launch.HFLaunch()
        load_output = self.hflaunch.load_design(design_path=designpath)

        #self.dictionary_of_all_agents_observations = {}

        # Agent selection
        n_vars = 6
        self.agents = ["Parameter_" + str(r) for r in range(n_vars)]
        self.possible_agents = self.agents[:]
        self.agent_name_mapping = dict(zip(self.agents, list(range(n_vars))))
        self._agent_selector = agent_selector(self.agents)

        # Action spaces
        # Set design parameter range
        n_action = 1
        # parameter range are between 10-100
        p_min = 0
        p_max = 1
        each_agent_action_space = gym.spaces.Box(low=p_min, high=p_max, shape=(n_action,),
                                                 dtype=np.float32)  # your normal gym action space
        self.action_spaces = dict(zip(
            self.agents,
            [each_agent_action_space] * self.num_agents,
        ))

        # State spaces
        # Observation S parameter
        n_obs = 8  # 6 design parameter and cost
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

        self.c1 = c1
        self.l1 = l1
        self.c2 = c2
        self.l2 = l2
        self.c3 = c3
        self.l3 = l3
        self.c1_O_min = c1_O_min
        self.c1_O_max = c1_O_max
        self.l1_O_min = l1_O_min
        self.l1_O_max = l1_O_max
        self.c2_O_min = c2_O_min
        self.c2_O_max = c2_O_max
        self.l2_O_min = l2_O_min
        self.l2_O_max = l2_O_max
        self.c3_O_min = c3_O_min
        self.c3_O_max = c3_O_max
        self.l3_O_min = l3_O_min
        self.l3_O_max = l3_O_max
        self.g0_s = g0_s
        self.g1_s = g1_s
        self.g2_s = g2_s
        self.g0_v = g0_v
        self.g1_v = g1_v
        self.g2_v = g2_v
        self.g0_mi = g0_mi
        self.g1_mi = g1_mi
        self.g2_mi = g2_mi
        self.g0_ma = g0_ma
        self.g1_ma = g1_ma
        self.g2_ma = g2_ma

        # set 3 goal
        self.goals = {
            'g0': {'series': self.g0_s, 'value': self.g0_v, 'min': self.g0_mi, 'max': self.g0_ma},
            'g1': {'series': self.g1_s, 'value': self.g1_v, 'min': self.g1_mi, 'max': self.g1_ma},
            'g2': {'series': self.g2_s, 'value': self.g2_v, 'min': self.g2_mi, 'max': self.g2_ma}
        }

        # initialize
        self.optimal_design_parameters = [
            {"Name": "c1", "Value": 20, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l1", "Value": 28, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c2", "Value": 12.36, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l2", "Value": 45.5, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "c3", "Value": 12, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
            {"Name": "l3", "Value": 46.8, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0}
        ]

        self.odp = [v["Value"] for v in self.optimal_design_parameters]

        self.initial_design_parameters = [
            {"Name": "c1", "Value": self.c1, "Unit": "", "Imaginary": False, "Min": self.c1_O_min, "Max": self.c1_O_max},
            {"Name": "l1", "Value": self.l1, "Unit": "", "Imaginary": False, "Min": self.l1_O_min, "Max": self.l1_O_max},
            {"Name": "c2", "Value": self.c2, "Unit": "", "Imaginary": False, "Min": self.c2_O_min, "Max": self.c2_O_max},
            {"Name": "l2", "Value": self.l2, "Unit": "", "Imaginary": False, "Min": self.l2_O_min, "Max": self.c2_O_max},
            {"Name": "c3", "Value": self.c3,"Unit": "", "Imaginary": False, "Min": self.c3_O_min, "Max": self.c3_O_max},
            {"Name": "l3", "Value": self.l3, "Unit": "", "Imaginary": False, "Min": self.l3_O_min, "Max": self.l3_O_max}
        ]

        self.design_parameters = copy.deepcopy(self.initial_design_parameters)

        # dictionary of param agents
        self.param_agents = dict(zip(self.agents, [ParamAgent(idx, self.design_parameters, self.goals) for idx in
                                                   range(len(self.design_parameters))]))
        self.best_parameters = [par["Value"] for par in self.design_parameters]
        self.current_parameters = [par["Value"] for par in self.design_parameters]
        self.best_cost = None
        self.best_reward = None
        self.step_counter = 0
        self.episode = 0
        self.action_pred = []

    def normalize_values(self, values):
        min_value = min(values)
        max_value = max(values)

        normalized_values = [(value - min_value) / (max_value - min_value) for value in values]

        return normalized_values

    def observe(self, agent):
        """
        Return individual observation
        """
        old_min = 1
        old_max = 100

        new_min = 0.01
        new_max = 1

        self.current_parameters = [par["Value"] for par in self.design_parameters]

        observation = self.param_agents[agent].observation
        return observation

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def step(self, action):
        self.step_counter+=1
        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return

        self.action_pred.append(action[0])
        # Select current agent
        # action = np.asarray(action)
        agent = self.agent_selection

        # Update agent current value
        agent_index = self.agent_name_mapping[agent]
        self.param_agents[agent].update_value(action=action[0])
        self.design_parameters[agent_index]["Value"] = self.param_agents[agent].current_value
        x = [v["Value"] for v in self.design_parameters]
        x = np.asarray(x)

        # Your step logic is here (same like gym env step)
        response = self.hflaunch.update_design(variable_list=self.design_parameters)

        # Get S parameter
        s_parameters = self.extract_s_parameters(response)
        frequency_values = self.extract_frequency_values(response)
        self.param_agents[agent].s_parameters = s_parameters
        self.param_agents[agent].frequency_values = frequency_values

        self.param_agents[agent].calculate_reward(x)
        current_agent_cost = self.param_agents[agent].cost
        current_agent_reward = self.param_agents[agent].reward
        if current_agent_cost < self.best_cost:
            self.best_cost = current_agent_cost
            self.best_parameters = [par["Value"] for par in self.design_parameters]

        if current_agent_reward > self.best_reward:
            self.best_reward = current_agent_reward

        self.current_parameters = [par["Value"] for par in self.design_parameters]
            # Since you are treating each design parameter as your agent, reward is calculated
        # after all agents are updated. Thus if the current agent is last agent and finish stepping,
        # design response is then simulated and evaluated.
        if self._agent_selector.is_last():
            # Update the following:
            # 1. self.terminate
            #self.terminate = self.param_agents[agent].check_goals()

            # 2. self.rewards
            all_agents_current_rewards = [self.param_agents[ag].reward for ag in self.param_agents]
            self.rewards = dict(zip(self.agents, all_agents_current_rewards))
            # self.rewards = self.calculate_reward(s_parameters, frequency_values)

            all_agents_termination = [self.check_termination(agent) for _ in self.param_agents]
            self.terminations = dict(zip(self.agents, all_agents_termination))
            self.truncations = dict(zip(self.agents, [False for _ in self.agents]))

            print(
                f"Current Step: {self.step_counter} "
                f"| Best Cost: {self.best_cost}"
                f"| Best Reward: {self.best_reward}"
                f"| Best Parameters: {self.best_parameters}"
                # f"| Current Parameters: {self.current_parameters}"
                # f"| Actions: {self.action_pred}"
                # f"| Current Cost: {current_agent_cost}"
            )

        else:
            self._clear_rewards()

        self.agent_selection = self._agent_selector.next()  # Here update agent_selection to point to next agent
        self._cumulative_rewards[self.agent_selection] = 0
        self._accumulate_rewards()
        #print(f"Parameters: {self.design_parameters}")

        # if self.render_mode == "human":
        #     self.render()

    def reset(self, seed=None, options=None):
        # your reset logic, reset hfapi?
        # initialize
        self.step_counter = 0
        self.episode += 1
        print(f"Current Episode:{self.episode}")

        self.agents = self.possible_agents[:]
        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.next()

        self.design_parameters = copy.deepcopy(self.initial_design_parameters)

        # dictionary of param agents
        self.param_agents = dict(zip(self.agents, [ParamAgent(idx, self.design_parameters, self.goals) for idx in
                                                   range(len(self.design_parameters))]))

        # Your step logic is here (same like gym env step)
        response = self.hflaunch.update_design(variable_list=self.design_parameters)

        # Get S parameter
        s_parameters = self.extract_s_parameters(response)
        frequency_values = self.extract_frequency_values(response)
        x = [v["Value"] for v in self.design_parameters]
        x = np.asarray(x)
        for agent in self.agents:
            self.param_agents[agent].s_parameters = s_parameters
            self.param_agents[agent].frequency_values = frequency_values
            self.param_agents[agent].calculate_reward(x)
        self.best_parameters = [par["Value"] for par in self.design_parameters]
        self.best_cost = np.min([self.param_agents[pa].cost for pa in self.param_agents])
        self.best_reward = np.max([self.param_agents[rw].reward for rw in self.param_agents])

        print(
            f"Current Step: {self.step_counter} "
            f"| Best Cost: {self.best_cost}"
            f"| Best Reward: {self.best_reward}"
            f"| Best Parameters: {self.best_parameters}"
       )

        all_agents_current_rewards = [self.param_agents[ag].reward for ag in self.param_agents]
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

    def check_termination(self, agent):
        max_step = 60
        condition1 = self.param_agents[agent].check_goals()
        condition2 = self.step_counter >= max_step
        return bool(condition1 or condition2)
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

        #return np.array(selected_s_parameters)
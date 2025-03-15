import gym
from gym import spaces
import random
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "hflib"))
from hflib import launch

class MicrowaveFilterEnv(gym.Env):

    def __init__(self):
        # set design parameter range
        self.action_space = spaces.Box(low=-1, high=1, shape=(6,), dtype=float) #C1, L1, C2, L2, C3, L3

        # set response range
        self.observation_space = spaces.Box(low=-20, high=0, shape=(4,), dtype=float) #S11, S12, S21, S22

        # set 3 goal
        self.goals = {
            'g0': {'series': 'S11', 'value': -15, 'min': 0.1, 'max': 0.45},
            'g1': {'series': 'S21', 'value': -15, 'min': 0.01, 'max': 0.079},
            'g2': {'series': 'S21', 'value': -15, 'min': 0.554, 'max': 1.0}
        }

        # initialize
        self.design_parameters = [
            {"Name": "c1","Value": 99.81559268198907,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
            {"Name": "l1","Value": 17.71350271999836,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
            {"Name": "c2","Value": 19.814235474914312,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
            {"Name": "l2","Value": 54.64225618168712,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
            {"Name": "c3","Value": 13.813209887593985,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
            {"Name": "l3","Value": 95.40046508423984,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0}
          ]


    def step(self, action):
        # update design parameters
        for i in range(len(self.design_parameters)):
            self.design_parameters[i]['Value'] = action[i]

        # use api update_deisgn function and get response
        hflaunch = launch.HFLaunch()
        response = hflaunch.update_design(variable_list=self.design_parameters)

        # Get S parameter
        s_parameters =self.extract_s_parameters(response)
        frequency_values=self.extract_frequency_values(response)

        # based on response to calculate reward
        reward = self.calculate_reward(s_parameters, frequency_values)

        # check whether the goal achieve
        done = self.check_goals(s_parameters, frequency_values)

        return s_parameters, reward, done, False,{"design parameter":self.design_parameters }#can put , for more value


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

    def calculate_reward(self, s_parameters, frequency_values):
        reward = 0
        for i, goal in enumerate(self.goals.values()):
            if goal['series'] in s_parameters and i < len(frequency_values):
                if (goal['min'] <= frequency_values[i] <= goal['max']) and (
                        goal['min'] <= s_parameters[goal['series']][i] <= goal['max']) and (
                        s_parameters[goal['series']][i] <= goal['value']):
                    reward += 1  # Increase reward for meeting the goal
        return reward

    def check_goals(self, s_parameters, frequency_values):
        for i, goal in enumerate(self.goals.values()):
            if goal['series'] in s_parameters and i < len(frequency_values):
                if not ((goal['min'] <= frequency_values[i] <= goal['max']) and (
                        goal['min'] <= s_parameters[goal['series']][i] <= goal['max']) and (
                                s_parameters[goal['series']][i] <= goal['value'])):
                    return False  # Goal not achieved
        return True  # Achieved all goals


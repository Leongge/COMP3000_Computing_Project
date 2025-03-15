import copy

import numpy as np


class ParamAgent_DM:
    def __init__(self, index, variable_object, goal_object, design_model):
        # define variable
        self.name = variable_object[index]["Name"]
        self.index = index
        self.current_value = variable_object[index]["Value"]
        self.initial_value = variable_object[index]["Value"]
        self.boundary = [variable_object[index]["Min"], variable_object[index]["Max"]]
        self.step_size = 0.1 * (variable_object[index]["Max"] - variable_object[index]["Min"])
        self.prev_cost = None
        self.cost = None
        self.reward = None
        self.initial_cost = None

        # Response
        self.s_parameters = None
        self.frequency_values = None
        self.observation = None

        # Goal
        self.goals = goal_object
        self.design_model = design_model

    def update_value(self, action):
        # update_value = action * self.step_size
        # self.current_value += update_value
        # self.current_value = np.clip(self.current_value, self.boundary[0], self.boundary[1])
        self.current_value = self.boundary[0] + (action * (self.boundary[1] - self.boundary[0]))
        self.current_value = np.clip(self.current_value, self.boundary[0], self.boundary[1])

    # def observe(self):
    #     goal = self.goals['g0']
    #
    #     min_frequency = goal['min']
    #     max_frequency = goal['max']
    #
    #     # find the frequency value index between the min max
    #     indices = []
    #     for i, freq_value in enumerate(self.frequency_values):
    #         if min_frequency <= freq_value <= max_frequency:
    #             indices.append(i)
    #
    #     # get index per 10
    #     # selected_indices = indices[::10]
    #
    #     # get s_parameter based on the index
    #     selected_s_parameters = [self.s_parameters['S11'][i] for i in indices]
    #     mag_2_params = np.power(10, np.divide(selected_s_parameters, 20))
    #     return mag_2_params

    # def observe(self):
    #     current_value = self.current_value
    #     cost = self.cost
    #     return [current_value, cost]

    def make_observation(self, x):
        # self.observation = x/100
        # self.observation = list(self.observation)
        # self.observation.insert(0, self.index/6)
        if self.initial_cost is None:
            self.initial_cost = copy.deepcopy(self.cost)
        self.observation = [
            self.index / 6,
            # self.current_value / 100,
            np.clip(self.cost / self.initial_cost, 0, 1)
        ]
        for xv in x:
            self.observation.append(xv/100)
        self.observation = np.asarray(self.observation)

    def compute_cost_from_modeler(self, x):
        self.cost = self.design_model.predict(x=x)

        if self.prev_cost is None:
            self.prev_cost = copy.deepcopy(self.cost)

        self.reward = -self.cost
        if self.cost < self.prev_cost:
            self.reward += 10
        self.make_observation(x)

    def calculate_reward(self):
        self.cost = 0
        for i, goal in enumerate(self.goals.values()):
            if goal['series'] in self.s_parameters:
                # Ensure s_parameter is not less than goal_value
                for j in range(len(self.frequency_values)):

                    if goal['min'] <= self.frequency_values[j] <= goal['max']:
                        s_value = self.s_parameters[goal['series']][j]

                        if s_value > goal['value']:
                            # Calculate Euclidean distance for each point
                            self.cost += np.abs(np.linalg.norm(np.array([0, s_value]) - np.array([0, goal['value']])))

        self.reward = -self.cost
        # import matplotlib.pyplot as plt
        # plt.plot(self.frequency_values,self.s_parameters[goal['series']])
        # plt.show()
        # return self.reward

    def check_goals(self):
        # for i, goal in enumerate(self.goals.values()):
        #     if goal['series'] in self.s_parameters and i < len(self.frequency_values):
        #         if not ((goal['min'] <= self.frequency_values[i] <= goal['max']) and (
        #                 goal['min'] <= self.s_parameters[goal['series']][i] <= goal['max']) and (
        #                         self.s_parameters[goal['series']][i] <= goal['value'])):
        #             return False  # Goal not achieved
        # return True  # Achieved all goals\
        if self.cost == 0:
            return True
        else:
            return False

import os
import sys
sys.path.append(os.path.join(os.getcwd(), "hflib"))
import csv
import random
import numpy as np
from hflib import launch

designpath = r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0\BPF-4-100M-450M.fpx"

# set initial value
initial_values = {
    "c1": 20,
    "l1": 28,
    "c2": 12.36,
    "l2": 45.5,
    "c3": 12,
    "l3": 46.8
}

#adjust range
adjustment_range = 3

#iteration
num_iterations = 1000


csv_file_path = "parameters_and_cost.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["c1", "l1", "c2", "l2", "c3", "l3", "cost"])

# loop 1000
for iteration in range(num_iterations):

    goals = {
        'g0': {'series': 'S11', 'value': -14.5, 'min': 0.1e9, 'max': 0.45e9},
        'g1': {'series': 'S21', 'value': -15, 'min': 0.01e9, 'max': 0.079e9},
        'g2': {'series': 'S21', 'value': -15, 'min': 0.554e9, 'max': 1.0e9}
    }
    # random adjust value of c1 until l3
    adjusted_values = {}
    for param, value in initial_values.items():
        adjustment = random.uniform(-adjustment_range, adjustment_range)
        adjusted_values[param] = value + adjustment

    hflaunch = launch.HFLaunch()

    load_output = hflaunch.load_design(design_path=designpath)

    optimal_design_parameters = [
        {"Name": param, "Value": adjusted_values[param], "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0}
        for param in initial_values.keys()
    ]
    response = hflaunch.update_design(variable_list=optimal_design_parameters)

    def extract_s_parameters(response):
        # from response get S parameters
        s_parameters = {}
        if "SimulationResult" in response and "Response1" in response["SimulationResult"]:
            series_data = response["SimulationResult"]["Response1"]["Series"]
            for series_name, series_info in series_data.items():
                s_parameters[series_info["Name"]] = series_info["DataY"]

        return s_parameters


    def extract_frequency_values(response):
        frequency_values = []
        if "SimulationResult" in response and "Response1" in response["SimulationResult"]:
            series_data = response["SimulationResult"]["Response1"]["Series"]
            if any(series_data.values()):
                first_series = next(iter(series_data.values()))
                if "DataX" in first_series:
                    frequency_values = first_series["DataX"]
        return frequency_values

    s_parameters = extract_s_parameters(response)
    frequency_values = extract_frequency_values(response)

    # calculate cost
    def calculate_cost():
        cost = 0
        for goal in goals.values():
            if goal['series'] in s_parameters:
                # Ensure s_parameter is not less than goal_value
                for j in range(len(frequency_values)):
                    if goal['min'] <= frequency_values[j] <= goal['max']:
                        s_value = s_parameters[goal['series']][j]
                        if s_value > goal['value']:
                            cost += np.abs(np.linalg.norm(np.array([0, s_value]) - np.array([0, goal['value']])))

        return cost

    with open('parameters_and_cost.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([adjusted_values[param] for param in initial_values.keys()] + [calculate_cost()])

    print("Iteration:", iteration + 1, "Cost:", calculate_cost())

print("All iterations completed.")

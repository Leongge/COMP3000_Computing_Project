import os
import sys
sys.path.append(os.path.join(os.getcwd(), "hflib"))
from hflib import launch

# Define design path
designpath = r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\BPF-4-100M-450M.fpx"

# Sample of the variable list used to update the design
variablelist = [
    {"Name": "c1","Value": 99.81559268198907,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l1","Value": 17.71350271999836,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "c2","Value": 19.814235474914312,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l2","Value": 54.64225618168712,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "c3","Value": 13.813209887593985,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l3","Value": 95.40046508423984,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0}
  ]

# Initialize
hflaunch = launch.HFLaunch()

# Load design
load_output = hflaunch.load_design(design_path=designpath)

# Update design with variable list
update_output = hflaunch.update_design(variable_list=variablelist)

print(load_output)
print(update_output)


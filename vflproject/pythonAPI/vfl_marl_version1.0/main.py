import os
import sys
sys.path.append(os.path.join(os.getcwd(), "hflib"))
from hflib import launch

# Define design path
designpath = r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0\BPF-4-100M-450M.fpx"

# Sample of the variable list used to update the design
variablelist = [
    {"Name": "c1","Value": 41.09485179185867,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l1","Value": 14.411045610904694,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "c2","Value": 10.687678158283234,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l2","Value": 92.58323073387146,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "c3","Value": 91.27581477165222,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0},
    {"Name": "l3","Value": 29.537899792194366,"Unit": "","Imaginary": False,"Min": 10.0,"Max": 100.0}
  ]

# Initialize
hflaunch = launch.HFLaunch()

# Load design
load_output = hflaunch.load_design(design_path=designpath)

# Update design with variable list
update_output = hflaunch.update_design(variable_list=variablelist)

#print(load_output)
print(update_output)


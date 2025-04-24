import os
import sys

sys.path.append(os.path.join(os.getcwd(), "hflib"))
# sys.path.append(r"C:\Users\leongsheng\source\repos\vflproject\TeamVFL_Project_Prototype\bin\x64\Debug\common\pythonlib")
# sys.path.append(r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0")
vflproject_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Assuming "vflproject" is a subdirectory
package_root = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0", "hflib")
project_root = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0")
python_root = os.path.join(vflproject_dir, "TeamVFL_Project_Prototype", "bin", "x64", "Debug", "common", "pythonlib")

sys.path.append(package_root)
sys.path.append(project_root)
sys.path.append(python_root)

# Define design path
designpath = r"C:\Users\leong\OneDrive\Documents\Peninsula Collegue\Study\Year 3 Sem 2\FYP\FYP_BSSE2309678\vflproject\backend\aiora-metric-vC2\Trainer\EDSHF_designs\2p-EPU2D\2p-EPU2D.fpx"
# designpath = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0", "BPF-4-100M-450M.fpx")

from hflib import launch
# Function to update design with given parameters
def update_design():
    # Sample of the variable list used to update the design
    variablelist = [
        {"Name": "Z12", "Value": 0.78530491 , "Unit": "", "Imaginary": False, "Min": 0.7, "Max": 1.0},
        {"Name": "Z34", "Value": 1.58758221 , "Unit": "", "Imaginary": False, "Min": 1.2, "Max": 1.8},
        {"Name": "Z45", "Value": 1.77645188, "Unit": "", "Imaginary": False, "Min": 1.5, "Max": 2.0},
        {"Name": "Z56", "Value": 1.99591214 , "Unit": "", "Imaginary": False, "Min": 1.5, "Max": 2.0},
        {"Name": "Z67", "Value": 1.7423165, "Unit": "", "Imaginary": False, "Min": 1.5, "Max": 2.0},
        {"Name": "Z78", "Value": 1.25440941, "Unit": "", "Imaginary": False, "Min": 1.0, "Max": 1.5},
        {"Name": "ZL8", "Value": 0.95884651, "Unit": "", "Imaginary": False, "Min": 0.5, "Max": 1.0},
        {"Name": "ZS2", "Value": 1.55458286 , "Unit": "", "Imaginary": False, "Min": 1.2, "Max": 1.7},
        {"Name": "ZS3", "Value": 1.13045791, "Unit": "", "Imaginary": False, "Min": 1.0, "Max": 1.5}
    ]

    # Initialize
    hflaunch = launch.HFLaunch()

    # Load design
    load_output = hflaunch.load_design(design_path=designpath)

    # Update design with variable list
    update_output = hflaunch.update_design(variable_list=variablelist)

    # Return update output
    return update_output


if __name__ == "__main__":
    # # Check if arguments are passed
    # if len(sys.argv) != 6:
    #     print("Usage: python update_graph.py c1 l1 c2 l2 c3 l3")
    #     sys.exit(1)

    # Update design with given parameters
    update_output = update_design()

    # Print update output
    print(update_output)

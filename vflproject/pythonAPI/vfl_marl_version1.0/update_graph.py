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
# designpath = r"C:\Users\leongsheng\source\repos\vflproject\pythonAPI\vfl_marl_version1.0\BPF-4-100M-450M.fpx"
designpath = os.path.join(vflproject_dir, "pythonAPI", "vfl_marl_version1.0", "BPF-4-100M-450M.fpx")

from hflib import launch
# Function to update design with given parameters
def update_design(c1, l1, c2, l2, c3, l3):
    # Sample of the variable list used to update the design
    variablelist = [
        {"Name": "c1", "Value": c1, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
        {"Name": "l1", "Value": l1, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
        {"Name": "c2", "Value": c2, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
        {"Name": "l2", "Value": l2, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
        {"Name": "c3", "Value": c3, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0},
        {"Name": "l3", "Value": l3, "Unit": "", "Imaginary": False, "Min": 10.0, "Max": 100.0}
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

    # Parse arguments
    c1 = float(sys.argv[1])
    l1 = float(sys.argv[2])
    c2 = float(sys.argv[3])
    l2 = float(sys.argv[4])
    c3 = float(sys.argv[5])
    l3 = float(sys.argv[6])

    # Update design with given parameters
    update_output = update_design(c1, l1, c2, l2, c3, l3)

    # Print update output
    print(update_output)

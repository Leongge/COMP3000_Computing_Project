# vflproject
Dear all members this is the repository of VFL team and Filpal team happy collaboration ya

# Team Member
| Name                 | Role            |
| -------------------- | --------------- |
| Khor Chun Leong      | Technical Lead  |
|                      | Scrum Master    |
| Vincent Goh Kah Fung | Client Liaison  |
| Fong Yun Xin         | Product Owner   |

# Configuration
-Visual Studio
Nuget Packages required:
1. pythonnet 3.0.1
2. pythonnet_netstandard_py39_win 2.5.2
3. Newtonsoft.Json 13.0.3
4. OxyPlot.Core 2.1.2
5. OxyPlot.WindowsForms 2.1.2

Debug : x64

-Python 
Version : 3.9.12
Packages required:
1. dm-tree v0.1.8
2. gym v0.15.3
3. gymnasium v0.28.1
4. hfapi v0.1b0
5. importlib-metadata v7.0.1
6. importlib-resources v6.1.1
7. matplotlib v3.8.2
8. numpy v1.24.2
9. openssl v1.1.1w
10. pettingzoo v1.24.2
11. protobuf v3.20.1
12. pygame v2.3.0
13. pymunk v6.2.0
14. pythonnet v3.0.1
15. ray v1.10.0
16. scipy v1.11.4
17. stable-baselines3 v2.2.1
18. supersuit v3.9.1
19. tensorboard v2.16.2
20. torch v2.1.2
21. yarl v1.9.2


# Setup
First, go to vflproject->pythonAPI-> vfl_marl_DM -> Training.py to train own models
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121030.png)

You can define how much step the ai will train
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-122452.png)

After get the check point
<br>
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121111.png)

You can open tensorbaord folder and check the graph by using following step
1. open cmd
2. cd to your current location
3. type "tensorboard --logdir your_tensorboard_folder_name"
4. then you will get a localhost liknk like "http://localhost:6006/"
5. you may check which checkpoint have the best performance
6. for example, in this graph. The best checkpoint will be 14442000
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-124459.png)

Next, move the checkpoint that you would like to observe to pythonAPI -> vfl_marl_version1.0 -> checkpoint
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121138.png)

Edit the vfl_marl_version1.0 -> RunAfterTraining_Desktop.py , update the checkpoint
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121355.png)

Then you may run use the visual studio 2022, open the TeamVFL_Project_Prototype.sln, Start and select the .fpx file in FPX Test File folder
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121624.png)

After import the .fpx file, click on "Optimize" then you will be able to see the optimize design parameter and result graph
![alt text](https://leongge.com/wp-content/uploads/2024/04/Screenshot-2024-04-16-121731.png)


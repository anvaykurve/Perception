Terminal 1
```
cd ~/Perception_Module/ROS2_Bag
python3 cone_centroid_publisher.py --ros-args -p use_sim_time:=true
```

Terminal 2
```
cd ~/Perception_Module/ROS2_Bag
ros2 bag play custom_track_1*/ --clock -r 0.5 -l*
# -l makes it run in an infinite loop
# 0.5 gives it more processing time
```

Terminal 3
```
rviz2
```
# C++

Terminal 1
```
cd ~/Perception_Module
colcon build --packages-select perception_cpp
source install/setup.bash
ros2 run perception_cpp cone_centroid_publisher --ros-args -p use_sim_time:=true
```

Terminal 2
```cd ~/Perception_Module/ROS2_Bag
ros2 bag play custom_track_1*/ --clock -l
```

Terminal 3 
```
rviz2
```
Teminal 4
```
ros2 topic hz /cone_centroids
```


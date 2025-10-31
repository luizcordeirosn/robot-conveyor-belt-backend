#!/usr/bin/env bash

source /opt/ros/melodic/setup.bash
source /catkin_ws/devel/setup.bash
cp /catkin_ws/worlds/empty.world /catkin_ws/src/niryo_robot_gazebo/worlds/niryo_cube_world.world

if [ $# -gt 0 ];then
    # If we passed a command, run it
    exec "$@"
else
    /bin/bash
fi

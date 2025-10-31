#!/usr/bin/env bash
xhost si:localuser:root

docker run -it \
           --rm \
           --privileged \
           --name niryo_simulation \
           --net=host \
           --env="DISPLAY" \
           --volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
           -v "$(pwd)/worlds/":/catkin_ws/worlds/ \
           -e QT_X11_NO_MITSHM=1 \
           niryo_simulation_image \
           bash

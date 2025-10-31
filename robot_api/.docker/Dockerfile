FROM osrf/ros:melodic-desktop-full-bionic

ENV LIBGL_ALWAYS_SOFTWARE=1

RUN apt-get update && apt-get install -y git nano wget build-essential python-pip sqlite3 ffmpeg terminator dbus-x11

RUN mkdir -p catkin_ws/src && cd catkin_ws && git clone --branch v4.0.1 --depth 1 https://github.com/NiryoRobotics/ned_ros.git src

RUN apt-get update && apt-get install -y ros-melodic-catkin  \
                       python-catkin-pkg  \
                       python-pymodbus  \
                       python-rosdistro  \
                       python-rospkg  \
                       python-rosdep-modules  \
                       python-rosinstall  \
                       python-rosinstall-generator  \
                       python-wstool

RUN apt-get update && apt-get install -y ros-melodic-moveit  \
                       ros-melodic-ros-control  \
                       ros-melodic-ros-controllers \
                       ros-melodic-tf2-web-republisher \
                       ros-melodic-rosbridge-server \
                       ros-melodic-joint-state-publisher-gui \
                       ros-melodic-gazebo-ros-control  \
                       ros-melodic-controller-manager

RUN bash -c "source /opt/ros/melodic/setup.bash && cd /catkin_ws && catkin_make"

RUN pip2 install -r /catkin_ws/src/requirements_ned2.txt
RUN apt-get update && apt-get install -y python-opencv
RUN pip2 install numpy enum34
RUN pip2 install --no-dependencies pyniryo==1.1.1

# For run GUI applications in examples
RUN apt-get update && apt-get install -y python-tk

WORKDIR /catkin_ws

#  Source environments
RUN echo 'source /opt/ros/melodic/setup.bash' >> ~/.bashrc
RUN echo 'source /catkin_ws/devel/setup.bash' >> ~/.bashrc

# Entrypoint
ADD .docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
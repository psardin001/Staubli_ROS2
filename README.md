# Staubli ROS 2 driver

This repository provides the ROS 2 driver and robot description for a Staubli
TX2-60L with a CS9 controller. It is based on the ROS 1
[`staubli_val3_driver`](https://github.com/ros-industrial/staubli_val3_driver)
and ROS-Industrial
[`industrial_core`](https://github.com/ros-industrial/industrial_core).

The direct streaming launch provides robot-state feedback, joint-trajectory
execution, IO access, and system services. The default joint configuration is
stored in `staubli_val3_driver/config/tx2_60l_streaming.yaml`.

## Installing the VAL3 components
Copy the contents of the _staubli_val3_driver/val3_ folder to the CS9 controller via USB or an FTP client such as WinScp or the transfer manager found in the Staubli Robotics Suite.

## Configuring the robot

Configure the TCP sockets from the teach pendant home:
1) IO --> Socket --> TCP Servers --> "+"
2) Configure the following new sockets:
   
    | Name   | Port  | Timeout |End of string | Nagle |
    | ---    | ---   | ---     | ---          | ---   |
    | Motion | 11000 | -1      | 13           | Off   |
    | System | 11001 | -1      | 13           | Off   |
    | State  | 11002 | -1      | 13           | Off   |
    | IO     | 11003 | -1      | 13           | Off   |

## How to use

### Staubli side

Load the driver from the teach pendant home:
1) Application manager --> Val3 applications
2) +Disk --> ros_server
3) VAL# --> Memory --> select `ros_server` --> ▶

### ROS side

Launch the direct driver for a real TX2-60L:

```
ros2 launch staubli_val3_driver robot_interface_streaming.launch.py \
  robot_ip:=<ROBOT_IP>
```

This launch starts state feedback, motion streaming, the
`/manipulator_controller/joint_trajectory_action` action, IO, and system
interfaces. Joint names and velocity limits come from
`staubli_val3_driver/config/tx2_60l_streaming.yaml`; pass
`joint_config:=/path/to/model.yaml` for another explicit configuration.

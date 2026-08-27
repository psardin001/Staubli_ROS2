from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    ThisLaunchFileDir,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def driver_launch(filename):
    return PythonLaunchDescriptionSource(
        PathJoinSubstitution([ThisLaunchFileDir(), filename])
    )


def generate_launch_description():
    robot_ip = LaunchConfiguration('robot_ip')
    joint_config = LaunchConfiguration('joint_config')
    enable_io = LaunchConfiguration('enable_io')
    enable_system = LaunchConfiguration('enable_system')

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'robot_ip',
                description='IP address of the robot',
            ),
            DeclareLaunchArgument(
                'joint_config',
                default_value=PathJoinSubstitution(
                    [
                        FindPackageShare('staubli_val3_driver'),
                        'config',
                        'tx2_60l_streaming.yaml',
                    ]
                ),
                description=(
                    'Joint names and limits for the connected Staubli model'
                ),
            ),
            DeclareLaunchArgument(
                'enable_io',
                default_value='true',
                choices=['true', 'false'],
            ),
            DeclareLaunchArgument(
                'enable_system',
                default_value='true',
                choices=['true', 'false'],
            ),
            IncludeLaunchDescription(
                driver_launch('robot_state.launch.py'),
                launch_arguments={
                    'robot_ip': robot_ip,
                    'joint_config': joint_config,
                }.items(),
            ),
            IncludeLaunchDescription(
                driver_launch('motion_streaming_interface.launch.py'),
                launch_arguments={
                    'robot_ip': robot_ip,
                    'joint_config': joint_config,
                }.items(),
            ),
            IncludeLaunchDescription(
                driver_launch('io_interface.launch.py'),
                launch_arguments={'robot_ip': robot_ip}.items(),
                condition=IfCondition(enable_io),
            ),
            IncludeLaunchDescription(
                driver_launch('system_interface.launch.py'),
                launch_arguments={'robot_ip': robot_ip}.items(),
                condition=IfCondition(enable_system),
            ),
            Node(
                package='industrial_robot_client',
                executable='joint_trajectory_action',
                parameters=[joint_config],
                output='screen',
            ),
        ]
    )

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_ip = LaunchConfiguration('robot_ip')
    joint_config = LaunchConfiguration('joint_config')

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
            Node(
                package='industrial_robot_client',
                executable='motion_streaming_interface',
                parameters=[
                    joint_config,
                    {'robot_ip_address': robot_ip},
                ],
                output='log',
            ),
        ]
    )

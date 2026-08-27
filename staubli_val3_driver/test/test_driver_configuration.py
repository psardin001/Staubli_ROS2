import math
from pathlib import Path

import yaml


PACKAGE = Path(__file__).parents[1]
INDUSTRIAL_CLIENT = PACKAGE.parent / 'industrial_robot_client'
STAUBLI_REPOSITORY = PACKAGE.parent
JOINT_NAMES = [f'joint_{index}' for index in range(1, 7)]


def test_tx2_streaming_parameters_are_complete():
    config = yaml.safe_load(
        (PACKAGE / 'config' / 'tx2_60l_streaming.yaml').read_text()
    )

    state = config['robot_state_interface']['ros__parameters']
    streaming = config['joint_trajectory_interface']['ros__parameters']
    action = config['joint_trajectory_action']['ros__parameters']

    assert state['joint_names'] == JOINT_NAMES
    assert streaming['joint_names'] == JOINT_NAMES
    assert action['joint_names'] == JOINT_NAMES
    assert len(streaming['joint_velocity_limits']) == len(JOINT_NAMES)
    assert all(
        math.isfinite(limit) and limit > 0.0
        for limit in streaming['joint_velocity_limits']
    )


def test_streaming_stack_has_no_move_group_parameter_dependency():
    sources = [
        INDUSTRIAL_CLIENT / 'src' / 'joint_trajectory_action.cpp',
        INDUSTRIAL_CLIENT / 'src' / 'joint_trajectory_interface.cpp',
        INDUSTRIAL_CLIENT / 'src' / 'robot_state_interface.cpp',
    ]

    for source in sources:
        text = source.read_text()
        assert 'move_group' not in text
        assert 'moveit_simple_controller_manager' not in text
        assert 'must contain unique non-empty names' in text


def test_combined_launch_passes_joint_configuration_to_every_motion_node():
    launch = (
        PACKAGE / 'launch' / 'robot_interface_streaming.launch.py'
    ).read_text()

    assert "'joint_config': joint_config" in launch
    assert 'parameters=[joint_config]' in launch
    assert 'staubli_tx2_60l_moveit_config' not in launch


def test_optional_moveit_packages_are_ignored_by_default():
    ignored_directories = (
        STAUBLI_REPOSITORY / 'adaptive_motion_control',
        STAUBLI_REPOSITORY / 'staubli_support',
        STAUBLI_REPOSITORY / 'staubli_tx2_60l_moveit_config',
    )

    for directory in ignored_directories:
        assert (directory / 'COLCON_IGNORE').is_file()

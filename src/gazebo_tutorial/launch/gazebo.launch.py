from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable
from launch.actions import (
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('gazebo_ros'),
                'launch', 'gazebo.launch.py'])])
    )

    robot_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            FindPackageShare('gazebo_tutorial'), 'urdf', 'teslabot.urdf.xacro'
        ])
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen'
    )

    robot_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'robot',
                   '-timeout', '120.0'],
        output='screen'
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    # Load controllers only after the robot has actually spawned, so the
    # controller_manager (provided by gazebo_ros2_control) is available.
    load_broadcaster_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=robot_spawn_node,
            on_exit=[load_joint_state_broadcaster],
        )
    )

    load_trajectory_after_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_joint_state_broadcaster,
            on_exit=[load_joint_trajectory_controller],
        )
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher_node,
        robot_spawn_node,
        load_broadcaster_after_spawn,
        load_trajectory_after_broadcaster,
    ])

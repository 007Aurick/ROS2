import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    pkg_path = get_package_share_directory('my_robot_description')
    default_urdf = os.path.join(pkg_path, 'urdf', 'simple-joint.urdf')

    configs = context.launch_configurations
    urdf_path = default_urdf
    if configs.get('model', default_urdf) != default_urdf:
        urdf_path = configs['model']
    elif configs.get('urdf', default_urdf) != default_urdf:
        urdf_path = configs['urdf']

    urdf_path = os.path.expanduser(urdf_path)

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
        ),
    ]


def generate_launch_description():
    pkg_path = get_package_share_directory('my_robot_description')
    default_urdf = os.path.join(pkg_path, 'urdf', 'simple-joint.urdf')

    return LaunchDescription([
        DeclareLaunchArgument('urdf', default_value=default_urdf),
        DeclareLaunchArgument('model', default_value=default_urdf),
        OpaqueFunction(function=launch_setup),
    ])

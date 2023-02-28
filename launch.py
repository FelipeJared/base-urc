import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from ament_index_python.packages import get_package_share_directory


from launch_ros.actions import Node

def generate_launch_description():
    config_filepath = LaunchConfiguration('config_filepath')
    
    return LaunchDescription([
        DeclareLaunchArgument('config_filepath', default_value=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('teleop_twist_joy'), 'config', '')),
            'xbox', TextSubstitution(text='.config.yaml')]),
            
        # Node(
        #     package='teleop_twist_joy',
        #     executable='launch/teleop-launch.py',
        #     parameters=[{
        #         'joy_config': 'xbox',
        #     }]
        # ),
        Node(
            package='joy', executable='joy_node', name='joy_node',
            parameters=[{
                'dev': '/dev/input/js0',
                'deadzone': 0.3,
                'autorepeat_rate': 20.0,
            }]),
        Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop_twist_joy_node', parameters=[config_filepath]),
        Node(
            package='dynamixel_sdk_examples',
            executable='read_write_node',
        )
    ])
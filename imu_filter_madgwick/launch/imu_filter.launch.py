import os
import yaml
# import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
# import launch.actions
# import launch.substitutions
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

configurable_parameters = [{'name': 'imu/data_raw'      ,'default':'camera/imu',                    'description':''},
                        {'name': 'imu/mag'              ,'default':'sensor_msgs/MagneticField',     'description':''},
                        {'name': 'imu/data'             ,'default':'camera/imu',                    'description':''},
                        {'name': 'gain'                 ,'default':'0.1',                           'description':''},
                        {'name': 'zeta'                 ,'default':'0.0',                           'description':''},
                        {'name': 'mag_bias_x'           ,'default':'0.0',                           'description':''},
                        {'name': 'mag_bias_y'           ,'default':'0.0',                           'description':''},
                        {'name': 'mag_bias_z'           ,'default':'0.0',                           'description':''},
                        {'name': 'orientation_stddev'   ,'default':'0.0',                           'description':''},
                        {'name': 'world_frame'          ,'default':'enu',                           'description':''},
                        {'name': 'use_mag'              ,'default':'true',                          'description':''},
                        {'name': 'fixed_frame'          ,'default':'camera_link',                   'description':''},
                        {'name': 'publish_tf'           ,'default':'true',                          'description':''},
                        {'name': 'reverse_tf'           ,'default':'false',                         'description':''},
                        {'name': 'constant_dt'          ,'default':'0.0',                           'description':''},
                        {'name': 'publish_debug_topics' ,'default':'false',                         'description':''},
                        {'name': 'stateless'            ,'default':'false',                         'description':''},
                        {'name': 'remove_gravity_vector','default':'false',                         'description':''},
                        ]

def declare_configurable_parameters(parameters):
    return [DeclareLaunchArgument(param['name'], default_value=param['default']) for param in parameters]

def set_configurable_parameters(parameters):
    return dict([(param['name'], LaunchConfiguration(param['name'])) for param in parameters])

def yaml_to_dict(path_to_yaml):
    with open(path_to_yaml, "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

# def launch_setup(context, *args, **kwargs):
#     _config_file = LaunchConfiguration("config_file").perform(context)
#     params_from_file = {} if _config_file == "''" else yaml_to_dict(_config_file)
#     log_level = 'info'

#     #imu filter madgwick
#     return [
#             launch_ros.actions.Node(
#                 package='imu_filter_madgwick',
#                 namespace=LaunchConfiguration("imu_filter"),
#                 name=LaunchConfiguration("imu_filter"),
#                 executable='imu_filter_madgwick_node', #changed for ros2-galactic
#                 # name='imu_filter', #changed for ros2-galactic
#                 parameters=[set_configurable_parameters(configurable_parameters), params_from_file],
#                 output='screen',
#                 arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
#                 emulate_tty=True,
#             )
#         ]

def launch_setup(context, *args, **kwargs):
    return[
        Node(
            package='imu_filter_madgwick',
            executable='imu_filter_madgwick_node',
            output='screen',
            parameters=[{
                "gain": LaunchConfiguration('gain'),
                "zeta": LaunchConfiguration('zeta'),
                "mag_bias_x": LaunchConfiguration('mag_bias_x'),
                "mag_bias_y": LaunchConfiguration('mag_bias_y'),
                "mag_bias_z": LaunchConfiguration('mag_bias_z'),
                "orientation_stddev": LaunchConfiguration('orientation_stddev'),
                "world_frame": LaunchConfiguration('world_frame'),
                "use_mag": LaunchConfiguration('use_mag'),
                "fixed_frame": LaunchConfiguration('fixed_frame'),
                "publish_tf": LaunchConfiguration('publish_tf'),
                "reverse_tf": LaunchConfiguration('reverse_tf'),
                "constant_dt": LaunchConfiguration('constant_dt'),
                "publish_debug_topics": LaunchConfiguration('publish_debug_topics'),
                "stateless": LaunchConfiguration('stateless'),
                "remove_gravity_vector": LaunchConfiguration('remove_gravity_vector')
            }],
            # arguments=[]
            remappings=[("camera_imu", LaunchConfiguration('imu/data'))],
        )
    ]

def generate_launch_description():
    return LaunchDescription(declare_configurable_parameters(configurable_parameters) + [
        OpaqueFunction(function=launch_setup)
    ])

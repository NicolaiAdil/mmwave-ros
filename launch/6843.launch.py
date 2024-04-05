from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from math import pi

# Constants
DEVICES = [
    # ID: "Unique ID"   Translation:['x', 'y', 'z'](m)  Rotation:['roll', 'pitch', 'yaw'](rad)
    {"id": "00F48CC4", "translation": ['0', '0', '0'], "rotation": ['0', '0', '0']},
    # {"id": "00ED2284", "translation": ['1', '0', '0'], "rotation": ['0', str(pi/2), '0']},
    # {"id": "00F48C12", "translation": ['0', '1', '0'], "rotation": ['0', '0', str(pi)]},
]

# Filter out detections with SNR below this threshold (reduce false positives)
SNR_THRESHOLD = 20.0

# Configuration file for the radar, see mmwave/cfg/ for more options
CONFIG_FILE = "6843_3d.cfg"

def generate_launch_description():
    nodes = [
        Node(
            package="mmwave",
            executable="mmwave_node",
            namespace=f"mmwave_{i}",
            name="mmwave",
            parameters=[{
                "device_id": device["id"],
                "config_file": PathJoinSubstitution([
                    FindPackageShare("mmwave"),
                    "cfg",
                    CONFIG_FILE
                ]),
                "frame_id": f"mmwave_{i}",
                "snr_threshold": SNR_THRESHOLD,
            }],
            output="screen",
            emulate_tty=True
        ) for i, device in enumerate(DEVICES)
    ]

    transforms = [
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=device["translation"] + device["rotation"] + [f"mmwave_{i}", 'body_flu'],
            name=f'static_tf_mmwave_{i}_to_body_flu'
        ) for i, device in enumerate(DEVICES)
    ]

    return LaunchDescription(nodes + transforms)


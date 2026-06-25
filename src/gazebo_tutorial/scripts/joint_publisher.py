#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class JointPublisher(Node):
    def __init__(self):
        super().__init__('joint_publisher')
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.count_ = 0

    def timer_callback(self):
        message = JointTrajectory()
        message.joint_names = [
            'arm_upper_to_lower_right',
            'arm_upper_to_lower_left',
        ]

        point = JointTrajectoryPoint()
        position1 = 1.5 * (1 - math.cos(self.count_ * 0.1))
        position2 = -position1
        point.positions = [position1, position2]
        point.time_from_start = Duration(seconds=1.0).to_msg()
        message.points = [point]
        self.publisher_.publish(message)

        self.get_logger().info("Publishing: '%f', '%f'" % (position1, position2))
        self.count_ += 1


def main(args=None):
    rclpy.init(args=args)
    node = JointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

from math import pi, sin

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState


class JointPublisher(Node):
    """Publishes oscillating joint positions for the teslabot."""

    def __init__(self):
        super().__init__('joint_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)

        self.joint_names = ['left_wheel_joint', 'right_wheel_joint']
        self.t = 0.0
        self.dt = 1.0 / 30.0

        self.create_timer(self.dt, self.timer_callback)
        self.get_logger().info('joint_publisher started')

    def timer_callback(self):
        self.t += self.dt

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = [sin(self.t) * pi, sin(self.t) * pi]

        self.joint_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = JointPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

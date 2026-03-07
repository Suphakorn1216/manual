import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from turtlebot3_msgs.msg import SensorState


class VWPublisher(Node):
    def __init__(self):
        super().__init__('vw_publisher')

        self.sensor_sub = self.create_subscription(
            SensorState,
            '/sensor_state',
            self.sensor_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            10
        )

        self.vw_pub = self.create_publisher(
            Twist,
            '/vw_est',
            10
        )

        self.timer = self.create_timer(0.02, self.timer_callback)

        self.wheel_radius = 0.033
        self.encoder_resolution = 4096.0

        self.left_encoder = None
        self.right_encoder = None
        self.prev_left_encoder = None
        self.prev_right_encoder = None

        self.omega_imu = 0.0
        self.last_time = self.get_clock().now()

    def sensor_callback(self, msg):
        self.left_encoder = msg.left_encoder
        self.right_encoder = msg.right_encoder

    def imu_callback(self, msg):
        self.omega_imu = msg.angular_velocity.z

    def timer_callback(self):
        if self.left_encoder is None or self.right_encoder is None:
            return

        if self.prev_left_encoder is None:
            self.prev_left_encoder = self.left_encoder
            self.prev_right_encoder = self.right_encoder
            self.last_time = self.get_clock().now()
            return

        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9

        if dt <= 0.0:
            return

        delta_left = self.left_encoder - self.prev_left_encoder
        delta_right = self.right_encoder - self.prev_right_encoder

        ds_left = 2.0 * math.pi * self.wheel_radius * delta_left / self.encoder_resolution
        ds_right = 2.0 * math.pi * self.wheel_radius * delta_right / self.encoder_resolution

        v = (ds_right + ds_left) / (2.0 * dt)
        omega = self.omega_imu

        twist = Twist()
        twist.linear.x = v
        twist.angular.z = omega
        self.vw_pub.publish(twist)

        self.get_logger().info(f'v = {v:.4f} m/s, omega = {omega:.4f} rad/s')

        self.prev_left_encoder = self.left_encoder
        self.prev_right_encoder = self.right_encoder
        self.last_time = current_time


def main(args=None):
    rclpy.init(args=args)
    node = VWPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

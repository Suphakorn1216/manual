import rclpy
from rclpy.node import Node
from turtlebot3_msgs.msg import SensorState
from geometry_msgs.msg import Twist
import math


class OdomCalculator(Node):
    def __init__(self):
        super().__init__('odom_calculator')
        
        self.L = 0.160
        self.R = 0.033
        self.RESOLUTION = 4096
        
        self.prev_left_ticks = 0
        self.prev_right_ticks = 0
        self.prev_time = self.get_clock().now()
        self.first_run = True

        self.subscription = self.create_subscription(
            SensorState,
            '/sensor_state',
            self.sensor_state_callback,
            10
        )

        self.publisher = self.create_publisher(
            Twist,
            '/vw_est',
            10
        )

    def sensor_state_callback(self, msg):
        current_time = self.get_clock().now()
        dt = (current_time - self.prev_time).nanoseconds / 1e9
        
        if dt <= 0:
            return

        if dt < 0.01:
            return

        curr_left_ticks = msg.left_encoder
        curr_right_ticks = msg.right_encoder

        if self.first_run:
            self.prev_left_ticks = curr_left_ticks
            self.prev_right_ticks = curr_right_ticks
            self.prev_time = current_time
            self.first_run = False
            return

        d_ticks_l = curr_left_ticks - self.prev_left_ticks
        d_ticks_r = curr_right_ticks - self.prev_right_ticks

        ds_l = (2 * math.pi * self.R * d_ticks_l) / self.RESOLUTION
        ds_r = (2 * math.pi * self.R * d_ticks_r) / self.RESOLUTION

        v = ((ds_r + ds_l) / 2) / dt
        w = ((ds_r - ds_l) / self.L) / dt

        twist = Twist()
        twist.linear.x = v
        twist.angular.z = w
        self.publisher.publish(twist)

        self.get_logger().info(
            f'Linear Velocity (v): {v:.3f} m/s, Angular Velocity (w): {w:.3f} rad/s'
        )

        self.prev_left_ticks = curr_left_ticks
        self.prev_right_ticks = curr_right_ticks
        self.prev_time = current_time


def main(args=None):
    rclpy.init(args=args)
    node = OdomCalculator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

import math


class DriftEstimator(Node):

    def __init__(self):

        super().__init__('drift_estimator')

        self.predicted = None
        self.actual = None

        self.create_subscription(
            Point,
            '/predicted_foot_position',
            self.predicted_callback,
            10
        )

        self.create_subscription(
            Point,
            '/actual_foot_position',
            self.actual_callback,
            10
        )

    def predicted_callback(self, msg):

        self.predicted = msg

        self.compute_error()

    def actual_callback(self, msg):

        self.actual = msg

        self.compute_error()

    def compute_error(self):

        if self.predicted is None:
            return

        if self.actual is None:
            return

        dx = self.predicted.x - self.actual.x
        dz = self.predicted.z - self.actual.z

        error = math.sqrt(
            dx * dx +
            dz * dz
        )

        print(
            f"DRIFT ERROR = {error:.4f} m",
            end="\r"
        )


def main():

    rclpy.init()

    node = DriftEstimator()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

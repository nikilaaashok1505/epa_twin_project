import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

import math


class TwinModel(Node):

    def __init__(self):

        super().__init__('twin_model')

        self.pub = self.create_publisher(
            Point,
            '/predicted_foot_position',
            10
        )

        self.L1 = 0.197
        self.L2 = 0.145
        self.L3 = 0.270

        self.t = 0

        self.timer = self.create_timer(
            0.02,
            self.publish_prediction
        )


    def publish_prediction(self):

        self.t += 0.03

        hip = 0.5 * math.sin(self.t)

        knee = -0.8 * math.sin(self.t)

        ankle = 0.4 * math.sin(self.t)


        x = (
            self.L1 * math.sin(hip)
            + self.L2 * math.sin(hip+knee)
            + self.L3 * math.sin(hip+knee+ankle)
        )

        z = (
            -self.L1 * math.cos(hip)
            -self.L2 * math.cos(hip+knee)
            -self.L3 * math.cos(hip+knee+ankle)
        )

        p = Point()

        p.x = float(x)

        p.y = 0.075

        p.z = float(z)

        self.pub.publish(p)

        print(
            f"Predicted : {x:.3f} {0.075:.3f} {z:.3f}"
        )


def main():

    rclpy.init()

    node = TwinModel()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':

    main()

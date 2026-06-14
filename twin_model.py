import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
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

        self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )

        self.L1 = 0.197
        self.L2 = 0.145
        self.L3 = 0.270

    def joint_callback(self, msg):

        hip = msg.position[0]
        knee = msg.position[1]
        ankle = msg.position[2]

        x = (
            self.L1 * math.sin(hip)
            + self.L2 * math.sin(hip + knee)
            + self.L3 * math.sin(hip + knee + ankle)
        )

        z = (
            - self.L1 * math.cos(hip)
            - self.L2 * math.cos(hip + knee)
            - self.L3 * math.cos(hip + knee + ankle)
        )

        p = Point()

        p.x = x
        p.y = 0.0
        p.z = z

        self.pub.publish(p)

        print(
            f"Predicted Foot: "
            f"X={x:.3f} "
            f"Z={z:.3f}"
        )


def main():

    rclpy.init()

    node = TwinModel()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

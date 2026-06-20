import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState

import math
import time


class JointPublisher(Node):

    def __init__(self):

        super().__init__('joint_publisher')

        self.pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.t0 = time.time()

        self.timer = self.create_timer(
            0.02,
            self.publish_joint
        )

    def publish_joint(self):

        t = time.time() - self.t0

        msg = JointState()

        msg.name = [
            'Hip',
            'Knee',
            'Ankle'
        ]

        msg.position = [

            0.3*math.sin(t),

            0.5*math.sin(t+1),

            0.2*math.sin(t+2)

        ]

        self.pub.publish(msg)


def main():

    rclpy.init()

    node = JointPublisher()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':

    main()

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

import mujoco
import mujoco.viewer


class FootSensor(Node):

    def __init__(self):

        super().__init__('foot_sensor')

        self.pub = self.create_publisher(
            Point,
            '/actual_foot_position',
            10
        )

        self.model = mujoco.MjModel.from_xml_path(
            "/home/krishna/epa_twin_project/urdf/robot.urdf"
        )

        self.data = mujoco.MjData(self.model)

        self.foot_id = mujoco.mj_name2id(
            self.model,
            mujoco.mjtObj.mjOBJ_BODY,
            "leg_stack_v1_1"
        )

        self.t = 0

        self.timer = self.create_timer(
            0.02,
            self.publish_position
        )

    def publish_position(self):

        import math

        self.t += 0.03

        self.data.qpos[0] = 0.5 * math.sin(self.t)

        self.data.qpos[1] = -0.8 * math.sin(self.t)

        self.data.qpos[2] = 0.4 * math.sin(self.t)

        mujoco.mj_step(
            self.model,
            self.data
        )

        x, y, z = self.data.xpos[
            self.foot_id
        ]

        msg = Point()

        msg.x = float(x)

        msg.y = float(y)

        msg.z = float(z)

        self.pub.publish(msg)

        print(
            f"Actual : {x:.3f} {y:.3f} {z:.3f}"
        )


def main():

    rclpy.init()

    node = FootSensor()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':

    main()

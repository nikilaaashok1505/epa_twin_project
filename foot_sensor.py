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

    def run(self):

        with mujoco.viewer.launch_passive(
            self.model,
            self.data
        ) as viewer:

            while viewer.is_running():

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
                    f"Actual Foot: "
                    f"X={x:.3f} "
                    f"Y={y:.3f} "
                    f"Z={z:.3f}",
                    end="\r"
                )

                rclpy.spin_once(
                    self,
                    timeout_sec=0
                )

                viewer.sync()


def main():

    rclpy.init()

    node = FootSensor()

    node.run()

    rclpy.shutdown()


if __name__ == '__main__':
    main()

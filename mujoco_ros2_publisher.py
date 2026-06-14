import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

import mujoco
import mujoco.viewer
import time
import math


class MujocoPublisher(Node):

    def __init__(self):

        super().__init__('mujoco_publisher')

        self.pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.model = mujoco.MjModel.from_xml_path(
            "/home/krishna/epa_twin_project/urdf/robot.urdf"
        )

        self.data = mujoco.MjData(self.model)

    def run(self):

        with mujoco.viewer.launch_passive(
            self.model,
            self.data
        ) as viewer:

            while viewer.is_running():

                t = time.time()

                self.data.qpos[0] = 0.6 * math.sin(t)
                self.data.qpos[1] = 0.5 * math.sin(t + 1.0)
                self.data.qpos[2] = 0.3 * math.sin(t + 2.0)

                mujoco.mj_forward(
                    self.model,
                    self.data
                )

                msg = JointState()

                msg.header.stamp = (
                    self.get_clock().now().to_msg()
                )

                msg.name = [
                    "Hip",
                    "Knee",
                    "Ankle"
                ]

                msg.position = [
                    float(self.data.qpos[0]),
                    float(self.data.qpos[1]),
                    float(self.data.qpos[2])
                ]

                self.pub.publish(msg)

                viewer.sync()

                rclpy.spin_once(
                    self,
                    timeout_sec=0
                )

                time.sleep(0.01)


def main():

    rclpy.init()

    node = MujocoPublisher()

    node.run()

    rclpy.shutdown()


if __name__ == '__main__':
    main()

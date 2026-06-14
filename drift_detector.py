import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class DriftDetector(Node):

    def __init__(self):

        super().__init__('drift_detector')

        self.reference = None

        self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10
        )

    def callback(self, msg):

        hip = msg.position[0]

        if self.reference is None:
            self.reference = hip
            return

        drift = abs(hip - self.reference)

        if drift > 0.4:
            print(
                f"DRIFT DETECTED: {drift:.3f}"
            )

def main():

    rclpy.init()

    node = DriftDetector()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()

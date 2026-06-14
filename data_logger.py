import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import csv
import time

class Logger(Node):

    def __init__(self):
        super().__init__('logger')

        self.file = open('joint_data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)

        self.writer.writerow([
            'time',
            'hip',
            'knee',
            'ankle'
        ])

        self.sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10
        )

    def callback(self, msg):

        self.writer.writerow([
            time.time(),
            msg.position[0],
            msg.position[1],
            msg.position[2]
        ])

def main():

    rclpy.init()

    node = Logger()

    rclpy.spin(node)

    node.file.close()

    rclpy.shutdown()

if __name__ == '__main__':
    main()

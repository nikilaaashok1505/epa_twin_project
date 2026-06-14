import rclpy
from rclpy.node import Node

from visualization_msgs.msg import Marker

class TestMarker(Node):

    def __init__(self):

        super().__init__('test_marker')

        self.pub = self.create_publisher(
            Marker,
            '/visualization_marker',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_marker
        )

    def publish_marker(self):

        marker = Marker()

        marker.header.frame_id = "map"

        marker.ns = "test"
        marker.id = 0

        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        
        marker.scale.x = 1.0
        marker.scale.y = 1.0
        marker.scale.z = 1.0
        
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        
       
        self.pub.publish(marker)

def main():

    rclpy.init()

    node = TestMarker()

    rclpy.spin(node)

if __name__ == '__main__':
    main()

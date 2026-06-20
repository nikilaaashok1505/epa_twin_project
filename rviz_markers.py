import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker


class MarkerPublisher(Node):

    def __init__(self):

        super().__init__('marker_publisher')

        self.marker_pub = self.create_publisher(
            Marker,
            '/visualization_marker',
            10
        )

        self.create_subscription(
            Point,
            '/actual_foot_position',
            self.actual_callback,
            10
        )

        self.create_subscription(
            Point,
            '/predicted_foot_position',
            self.predicted_callback,
            10
        )

    def actual_callback(self,msg):

        marker=Marker()

        marker.header.frame_id="world"

        marker.ns="actual"

        marker.id=0

        marker.type=Marker.SPHERE

        marker.action=Marker.ADD

        marker.pose.position.x=msg.x
        marker.pose.position.y=msg.y
        marker.pose.position.z=msg.z

        marker.scale.x=0.05
        marker.scale.y=0.05
        marker.scale.z=0.05

        marker.color.r=1.0
        marker.color.g=0.0
        marker.color.b=0.0
        marker.color.a=1.0

        self.marker_pub.publish(marker)


    def predicted_callback(self,msg):

        marker=Marker()

        marker.header.frame_id="world"

        marker.ns="predicted"

        marker.id=1

        marker.type=Marker.SPHERE

        marker.action=Marker.ADD

        marker.pose.position.x=msg.x
        marker.pose.position.y=msg.y
        marker.pose.position.z=msg.z

        marker.scale.x=0.05
        marker.scale.y=0.05
        marker.scale.z=0.05

        marker.color.r=0.0
        marker.color.g=1.0
        marker.color.b=0.0
        marker.color.a=1.0

        self.marker_pub.publish(marker)


def main():

    rclpy.init()

    node=MarkerPublisher()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":

    main()

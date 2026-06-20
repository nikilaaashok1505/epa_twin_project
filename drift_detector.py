import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
import math

actual=None
pred=None

def a(msg):
    global actual
    actual=msg

def p(msg):
    global pred
    pred=msg

    if actual is not None:

        d=math.sqrt(
        (actual.x-pred.x)**2+
        (actual.y-pred.y)**2+
        (actual.z-pred.z)**2
        )

        print("DRIFT =",round(d,4),"m")


rclpy.init()

node=rclpy.create_node("drift")

node.create_subscription(Point,"/actual_foot_position",a,10)

node.create_subscription(Point,"/predicted_foot_position",p,10)

rclpy.spin(node)

#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult
from actionlib_msgs.msg import GoalStatusArray
from nav_msgs.msg import OccupancyGrid
from std_srvs.srv import Empty 
class GoalStatusPublisher:
    def __init__(self):
        rospy.init_node('goal_status_publisher', anonymous=True)

        # Define publishers
        self.goal_status_pub = rospy.Publisher('robot/status', Int32, queue_size=10)

        # Define subscribers
        rospy.Subscriber('move_base/goal', MoveBaseActionGoal, self.goal_received_callback)
        rospy.Subscriber('move_base/result', MoveBaseActionResult, self.goal_result_callback)

        rospy.spin()

    def goal_received_callback(self, msg):
        # Callback when a new move base goal is received
        self.publish_goal_status(1)

    def goal_result_callback(self, msg):
        # Callback when the goal is reached
        if msg.status.status == 3:  # SUCCEEDED status
            self.publish_goal_status(2)
        elif msg.status.status in [2, 4, 5]:  # Cancelled status
            self.publish_goal_status(3)


    def publish_goal_status(self, status):
        # Publish the goal status to the 'robot/goalstatus' topic
        self.goal_status_pub.publish(status)

if __name__ == '__main__':
    try:
        GoalStatusPublisher()
    except rospy.ROSInterruptException:
        pass

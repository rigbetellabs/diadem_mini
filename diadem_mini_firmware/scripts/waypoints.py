#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Point
import pandas as pd
import os, rospkg
import time
rospack = rospkg.RosPack()

# this method will make the robot move to the goal location
def move_to_goal(xGoal, yGoal, zGoal, XGoal, YGoal, ZGoal, WGoal):
    # define a client to send goal requests to the move_base server through a SimpleActionClient # created a server
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    # wait for the action server to come up
    while not ac.wait_for_server(rospy.Duration.from_sec(5.0)):
        rospy.loginfo("Waiting for the move_base action server to come up")

    goal = MoveBaseGoal()  # object

    # set up the frame parameters
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    # moving towards the goal*/
    goal.target_pose.pose.position = Point(xGoal, yGoal, zGoal)  # this or down
    goal.target_pose.pose.orientation.x = XGoal
    goal.target_pose.pose.orientation.y = YGoal
    goal.target_pose.pose.orientation.z = ZGoal
    goal.target_pose.pose.orientation.w = WGoal

    rospy.loginfo("Sending goal location ...")
    ac.send_goal(goal)

    ac.wait_for_result(rospy.Duration(200))

    if ac.get_state() == GoalStatus.SUCCEEDED:
        rospy.loginfo("You have reached the destination")
        time.sleep(5)
        return True
    else:
        rospy.loginfo("The robot failed to reach the destination")
        return False

def read_csv_publish_goal():
    while not rospy.is_shutdown():
        data = pd.read_csv(os.path.join(rospack.get_path("diadem_mini_firmware"), "scripts", "robot_position.csv"))

        store_len = int(len(data.index))

        for i in range(store_len):
            xGoal = data.x[i]
            yGoal = data.y[i]
            zGoal = data.z[i]
            XGoal = data.qx[i]
            YGoal = data.qy[i]
            ZGoal = data.qz[i]
            WGoal = data.qw[i]

            move_to_goal(xGoal, yGoal, zGoal, XGoal, YGoal, ZGoal, WGoal)
            if i == (store_len - 1):
                i = 0

if __name__ == '__main__':
    rospy.init_node('csv_to_goal_publisher', anonymous=True)
    read_csv_publish_goal()
    rospy.spin()
    exit()

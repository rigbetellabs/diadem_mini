#!/usr/bin/env python3

import rospy
import csv
from sensor_msgs.msg import Joy
from nav_msgs.msg import Odometry
import os, rospkg
rospack = rospkg.RosPack()

class JoyOdomToCsvNode:

    def __init__(self):
        self.file_path = os.path.join(rospack.get_path("diadem_mini_firmware"), "scripts", "robot_position.csv")
        self.current_position = None
        self.current_orientation = None
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)

    def joy_callback(self, joy_msg):
        if joy_msg.buttons[1] == 1:
            self.save_to_csv()
            rospy.loginfo('Current position and orientation saved to CSV file')
        elif joy_msg.buttons[3] == 1:
            self.clear_csv_file()
            rospy.loginfo('CSV file cleared')

    def odom_callback(self, odom_msg):
        self.current_position = odom_msg.pose.pose.position
        self.current_orientation = odom_msg.pose.pose.orientation

    def save_to_csv(self):
        with open(self.file_path, mode='a') as csv_file:
            fieldnames = ['x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:
                writer.writeheader()
            writer.writerow({'x': self.current_position.x,
                             'y': self.current_position.y,
                             'z': self.current_position.z,
                             'qx': self.current_orientation.x,
                             'qy': self.current_orientation.y,
                             'qz': self.current_orientation.z,
                             'qw': self.current_orientation.w})

    def clear_csv_file(self):
        with open(self.file_path, mode='w') as csv_file:
            csv_file.truncate()

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('joy_and_odom_to_csv_node')
    node = JoyOdomToCsvNode()
    node.run()
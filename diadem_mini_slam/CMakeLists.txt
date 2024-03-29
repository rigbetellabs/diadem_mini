cmake_minimum_required(VERSION 3.0.2)
project(diadem_mini_slam)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

#   std_msgs

catkin_package(
#  CATKIN_DEPENDS roscpp rospy std_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

install(FILES config/gmapping.yaml
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
)
install(FILES launch/carto_slam.launch launch/gmapping_slam.launch launch/map_saver.launch launch/view_sensors.launch
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
install(FILES rviz/diadem_gmapping.rviz rviz/mapping.rviz rviz/sensors.rviz
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)

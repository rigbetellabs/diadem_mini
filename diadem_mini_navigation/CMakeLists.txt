cmake_minimum_required(VERSION 3.0.2)
project(diadem_mini_navigation)

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

install(FILES launch/diadem_mini_carto_navigation.launch launch/diadem_mini_gmap_amcl.launch launch/amcl.launch launch/move_base.launch
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)
install(FILES param/costmap_common_params.yaml param/dwa_local_planner_params.yaml param/global_costmap_params.yaml param/local_costmap_params.yaml param/move_base_params.yaml param/sim_dwa_local_planner_params.yaml
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/param
)
install(FILES rviz/diadem_navigation.rviz
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)

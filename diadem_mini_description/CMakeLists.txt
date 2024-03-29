cmake_minimum_required(VERSION 2.8.3)
project(diadem_mini_description)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(
#  LIBRARIES fusion2urdf
#  CATKIN_DEPENDS rospy
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

#   src/${PROJECT_NAME}/fusion2urdf.cpp

# add_executable(${PROJECT_NAME}_node src/fusion2urdf_node.cpp)

# catkin_add_gtest(${PROJECT_NAME}-test test/test_fusion2urdf.cpp)

install(FILES LICENSE
        LICENSE
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
install(FILES launch/controller.launch launch/controller.yaml launch/display.launch launch/gazebo.launch launch/urdf.rviz
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

install(FILES urdf/diadem_mini.xacro 
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/urdf
)

cmake_minimum_required(VERSION 3.8)
project(gazebo_tutorial)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ADDED---------------------------------------------------
# 1. Find Packages 
find_package(ament_cmake REQUIRED)

# 2. Install Python Joint Publisher script
install(PROGRAMS
  scripts/joint_publisher.py
  DESTINATION lib/${PROJECT_NAME})

# 3. Copy Files 
install(DIRECTORY 
    launch 
    urdf 
    config
    meshes
    rviz
  DESTINATION share/${PROJECT_NAME}
)
# END ADDED---------------------------------------------------


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
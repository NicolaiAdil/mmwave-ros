cmake_minimum_required(VERSION 3.5)
project(mmwave)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(mmwave_node
  src/mmwave_node.cpp
  src/mmwave/serial.c
  src/mmwave/mmwave.c
  src/mmwave/mmwave_cfg.c)
target_include_directories(mmwave_node
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

ament_target_dependencies(mmwave_node
  rclcpp
  sensor_msgs)

add_executable(mmwave_config
  src/mmwave_config.cpp
  src/mmwave/serial.c
  src/mmwave/mmwave.c
  src/mmwave/mmwave_cfg.c)
target_include_directories(mmwave_config
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

install(
  TARGETS
    mmwave_node
    mmwave_config
  DESTINATION lib/${PROJECT_NAME})

install(
  DIRECTORY
    cfg
    launch
  DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

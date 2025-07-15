// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'coverage_rect'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/Waypoint in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__msg__Waypoint
{
  /// arm pose x,y,z,roll,pitch,yaw
  geometry_msgs__msg__Pose pose;
  /// waypoint index
  int32_t waypoint_index;
  /// camera FOV coverage rectangle
  geometry_msgs__msg__Point__Sequence coverage_rect;
} vision_ai_interfaces__msg__Waypoint;

// Struct for a sequence of vision_ai_interfaces__msg__Waypoint.
typedef struct vision_ai_interfaces__msg__Waypoint__Sequence
{
  vision_ai_interfaces__msg__Waypoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__msg__Waypoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_

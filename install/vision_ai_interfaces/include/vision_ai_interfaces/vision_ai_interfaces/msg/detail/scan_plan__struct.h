// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'strategy'
// Member 'mode'
#include "rosidl_runtime_c/string.h"
// Member 'waypoints'
#include "vision_ai_interfaces/msg/detail/waypoint__struct.h"
// Member 'scan_region'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/ScanPlan in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__msg__ScanPlan
{
  /// single_point or multi_point
  rosidl_runtime_c__String strategy;
  /// scan height in mm
  double scan_height;
  /// calculated required height in mm
  double required_height;
  /// waypoint list
  vision_ai_interfaces__msg__Waypoint__Sequence waypoints;
  /// scan region points
  geometry_msgs__msg__Point__Sequence scan_region;
  /// object height in mm
  double object_height;
  /// mode from request
  rosidl_runtime_c__String mode;
} vision_ai_interfaces__msg__ScanPlan;

// Struct for a sequence of vision_ai_interfaces__msg__ScanPlan.
typedef struct vision_ai_interfaces__msg__ScanPlan__Sequence
{
  vision_ai_interfaces__msg__ScanPlan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__msg__ScanPlan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_H_

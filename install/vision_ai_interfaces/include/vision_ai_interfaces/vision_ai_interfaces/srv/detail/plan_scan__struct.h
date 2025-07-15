// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:srv/PlanScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__STRUCT_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'mode'
#include "rosidl_runtime_c/string.h"
// Member 'points'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in srv/PlanScan in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__PlanScan_Request
{
  /// preset or manual
  rosidl_runtime_c__String mode;
  /// object height in mm
  double object_height;
  /// scan region 4 points
  geometry_msgs__msg__Point__Sequence points;
} vision_ai_interfaces__srv__PlanScan_Request;

// Struct for a sequence of vision_ai_interfaces__srv__PlanScan_Request.
typedef struct vision_ai_interfaces__srv__PlanScan_Request__Sequence
{
  vision_ai_interfaces__srv__PlanScan_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__PlanScan_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.h"

/// Struct defined in srv/PlanScan in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__PlanScan_Response
{
  /// Response: scan plan
  /// planning success
  bool success;
  /// error message or status
  rosidl_runtime_c__String message;
  /// scan plan details
  vision_ai_interfaces__msg__ScanPlan scan_plan;
} vision_ai_interfaces__srv__PlanScan_Response;

// Struct for a sequence of vision_ai_interfaces__srv__PlanScan_Response.
typedef struct vision_ai_interfaces__srv__PlanScan_Response__Sequence
{
  vision_ai_interfaces__srv__PlanScan_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__PlanScan_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__STRUCT_H_

// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:srv/ExecuteScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.h"

/// Struct defined in srv/ExecuteScan in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ExecuteScan_Request
{
  vision_ai_interfaces__msg__ScanPlan scan_plan;
} vision_ai_interfaces__srv__ExecuteScan_Request;

// Struct for a sequence of vision_ai_interfaces__srv__ExecuteScan_Request.
typedef struct vision_ai_interfaces__srv__ExecuteScan_Request__Sequence
{
  vision_ai_interfaces__srv__ExecuteScan_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ExecuteScan_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'output_directory'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ExecuteScan in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ExecuteScan_Response
{
  /// 响应：执行状态
  bool success;
  rosidl_runtime_c__String message;
  rosidl_runtime_c__String output_directory;
} vision_ai_interfaces__srv__ExecuteScan_Response;

// Struct for a sequence of vision_ai_interfaces__srv__ExecuteScan_Response.
typedef struct vision_ai_interfaces__srv__ExecuteScan_Response__Sequence
{
  vision_ai_interfaces__srv__ExecuteScan_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ExecuteScan_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_H_

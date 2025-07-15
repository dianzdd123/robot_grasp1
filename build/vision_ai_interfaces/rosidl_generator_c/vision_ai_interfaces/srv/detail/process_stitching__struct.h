// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:srv/ProcessStitching.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'image_data'
#include "vision_ai_interfaces/msg/detail/image_data__struct.h"
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.h"
// Member 'output_directory'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ProcessStitching in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ProcessStitching_Request
{
  vision_ai_interfaces__msg__ImageData__Sequence image_data;
  vision_ai_interfaces__msg__ScanPlan scan_plan;
  rosidl_runtime_c__String output_directory;
} vision_ai_interfaces__srv__ProcessStitching_Request;

// Struct for a sequence of vision_ai_interfaces__srv__ProcessStitching_Request.
typedef struct vision_ai_interfaces__srv__ProcessStitching_Request__Sequence
{
  vision_ai_interfaces__srv__ProcessStitching_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ProcessStitching_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'result'
#include "vision_ai_interfaces/msg/detail/stitch_result__struct.h"

/// Struct defined in srv/ProcessStitching in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ProcessStitching_Response
{
  /// 响应：拼接结果
  bool success;
  rosidl_runtime_c__String message;
  vision_ai_interfaces__msg__StitchResult result;
} vision_ai_interfaces__srv__ProcessStitching_Response;

// Struct for a sequence of vision_ai_interfaces__srv__ProcessStitching_Response.
typedef struct vision_ai_interfaces__srv__ProcessStitching_Response__Sequence
{
  vision_ai_interfaces__srv__ProcessStitching_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ProcessStitching_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_H_

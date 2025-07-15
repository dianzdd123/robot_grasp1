// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:srv/ProcessDetection.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__STRUCT_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/ProcessDetection in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ProcessDetection_Request
{
  uint8_t structure_needs_at_least_one_member;
} vision_ai_interfaces__srv__ProcessDetection_Request;

// Struct for a sequence of vision_ai_interfaces__srv__ProcessDetection_Request.
typedef struct vision_ai_interfaces__srv__ProcessDetection_Request__Sequence
{
  vision_ai_interfaces__srv__ProcessDetection_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ProcessDetection_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"
// Member 'result'
#include "vision_ai_interfaces/msg/detail/detection_result__struct.h"

/// Struct defined in srv/ProcessDetection in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__ProcessDetection_Response
{
  bool success;
  rosidl_runtime_c__String message;
  vision_ai_interfaces__msg__DetectionResult result;
} vision_ai_interfaces__srv__ProcessDetection_Response;

// Struct for a sequence of vision_ai_interfaces__srv__ProcessDetection_Response.
typedef struct vision_ai_interfaces__srv__ProcessDetection_Response__Sequence
{
  vision_ai_interfaces__srv__ProcessDetection_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__ProcessDetection_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__STRUCT_H_

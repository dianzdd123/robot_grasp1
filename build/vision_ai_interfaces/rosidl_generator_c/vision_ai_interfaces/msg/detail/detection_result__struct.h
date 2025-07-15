// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'output_directory'
#include "rosidl_runtime_c/string.h"
// Member 'objects'
#include "vision_ai_interfaces/msg/detail/detected_object__struct.h"

/// Struct defined in msg/DetectionResult in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__msg__DetectionResult
{
  std_msgs__msg__Header header;
  int32_t detection_count;
  float processing_time;
  rosidl_runtime_c__String output_directory;
  vision_ai_interfaces__msg__DetectedObject__Sequence objects;
} vision_ai_interfaces__msg__DetectionResult;

// Struct for a sequence of vision_ai_interfaces__msg__DetectionResult.
typedef struct vision_ai_interfaces__msg__DetectionResult__Sequence
{
  vision_ai_interfaces__msg__DetectionResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__msg__DetectionResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_H_

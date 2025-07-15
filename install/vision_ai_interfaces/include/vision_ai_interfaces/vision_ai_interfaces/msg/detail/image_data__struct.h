// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:msg/ImageData.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'filename'
#include "rosidl_runtime_c/string.h"
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'waypoint'
#include "vision_ai_interfaces/msg/detail/waypoint__struct.h"
// Member 'image'
#include "sensor_msgs/msg/detail/image__struct.h"

/// Struct defined in msg/ImageData in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__msg__ImageData
{
  rosidl_runtime_c__String filename;
  builtin_interfaces__msg__Time timestamp;
  vision_ai_interfaces__msg__Waypoint waypoint;
  sensor_msgs__msg__Image image;
} vision_ai_interfaces__msg__ImageData;

// Struct for a sequence of vision_ai_interfaces__msg__ImageData.
typedef struct vision_ai_interfaces__msg__ImageData__Sequence
{
  vision_ai_interfaces__msg__ImageData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__msg__ImageData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_H_

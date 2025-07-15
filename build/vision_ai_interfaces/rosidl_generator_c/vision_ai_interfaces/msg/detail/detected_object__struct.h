// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'object_id'
// Member 'class_name'
// Member 'description'
#include "rosidl_runtime_c/string.h"
// Member 'bounding_box'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/DetectedObject in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__msg__DetectedObject
{
  rosidl_runtime_c__String object_id;
  int32_t class_id;
  rosidl_runtime_c__String class_name;
  float confidence;
  rosidl_runtime_c__String description;
  /// [x1, y1, x2, y2]
  rosidl_runtime_c__float__Sequence bounding_box;
  float center_x;
  float center_y;
  float world_x;
  float world_y;
  float world_z;
} vision_ai_interfaces__msg__DetectedObject;

// Struct for a sequence of vision_ai_interfaces__msg__DetectedObject.
typedef struct vision_ai_interfaces__msg__DetectedObject__Sequence
{
  vision_ai_interfaces__msg__DetectedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__msg__DetectedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_

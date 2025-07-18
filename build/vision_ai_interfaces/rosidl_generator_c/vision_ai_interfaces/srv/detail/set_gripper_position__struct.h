// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_ai_interfaces:srv/SetGripperPosition.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_POSITION__STRUCT_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_POSITION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetGripperPosition in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__SetGripperPosition_Request
{
  /// 夹爪位置 (0-850)
  int32_t position;
} vision_ai_interfaces__srv__SetGripperPosition_Request;

// Struct for a sequence of vision_ai_interfaces__srv__SetGripperPosition_Request.
typedef struct vision_ai_interfaces__srv__SetGripperPosition_Request__Sequence
{
  vision_ai_interfaces__srv__SetGripperPosition_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__SetGripperPosition_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetGripperPosition in the package vision_ai_interfaces.
typedef struct vision_ai_interfaces__srv__SetGripperPosition_Response
{
  /// 操作是否成功
  bool success;
  /// 状态消息
  rosidl_runtime_c__String message;
} vision_ai_interfaces__srv__SetGripperPosition_Response;

// Struct for a sequence of vision_ai_interfaces__srv__SetGripperPosition_Response.
typedef struct vision_ai_interfaces__srv__SetGripperPosition_Response__Sequence
{
  vision_ai_interfaces__srv__SetGripperPosition_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_ai_interfaces__srv__SetGripperPosition_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_POSITION__STRUCT_H_

// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vision_ai_interfaces/msg/detail/detection_result__rosidl_typesupport_introspection_c.h"
#include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vision_ai_interfaces/msg/detail/detection_result__functions.h"
#include "vision_ai_interfaces/msg/detail/detection_result__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `output_directory`
#include "rosidl_runtime_c/string_functions.h"
// Member `objects`
#include "vision_ai_interfaces/msg/detected_object.h"
// Member `objects`
#include "vision_ai_interfaces/msg/detail/detected_object__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vision_ai_interfaces__msg__DetectionResult__init(message_memory);
}

void vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_fini_function(void * message_memory)
{
  vision_ai_interfaces__msg__DetectionResult__fini(message_memory);
}

size_t vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__size_function__DetectionResult__objects(
  const void * untyped_member)
{
  const vision_ai_interfaces__msg__DetectedObject__Sequence * member =
    (const vision_ai_interfaces__msg__DetectedObject__Sequence *)(untyped_member);
  return member->size;
}

const void * vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_const_function__DetectionResult__objects(
  const void * untyped_member, size_t index)
{
  const vision_ai_interfaces__msg__DetectedObject__Sequence * member =
    (const vision_ai_interfaces__msg__DetectedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_function__DetectionResult__objects(
  void * untyped_member, size_t index)
{
  vision_ai_interfaces__msg__DetectedObject__Sequence * member =
    (vision_ai_interfaces__msg__DetectedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__fetch_function__DetectionResult__objects(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const vision_ai_interfaces__msg__DetectedObject * item =
    ((const vision_ai_interfaces__msg__DetectedObject *)
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_const_function__DetectionResult__objects(untyped_member, index));
  vision_ai_interfaces__msg__DetectedObject * value =
    (vision_ai_interfaces__msg__DetectedObject *)(untyped_value);
  *value = *item;
}

void vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__assign_function__DetectionResult__objects(
  void * untyped_member, size_t index, const void * untyped_value)
{
  vision_ai_interfaces__msg__DetectedObject * item =
    ((vision_ai_interfaces__msg__DetectedObject *)
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_function__DetectionResult__objects(untyped_member, index));
  const vision_ai_interfaces__msg__DetectedObject * value =
    (const vision_ai_interfaces__msg__DetectedObject *)(untyped_value);
  *item = *value;
}

bool vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__resize_function__DetectionResult__objects(
  void * untyped_member, size_t size)
{
  vision_ai_interfaces__msg__DetectedObject__Sequence * member =
    (vision_ai_interfaces__msg__DetectedObject__Sequence *)(untyped_member);
  vision_ai_interfaces__msg__DetectedObject__Sequence__fini(member);
  return vision_ai_interfaces__msg__DetectedObject__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_member_array[5] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectionResult, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "detection_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectionResult, detection_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "processing_time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectionResult, processing_time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "output_directory",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectionResult, output_directory),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objects",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectionResult, objects),  // bytes offset in struct
    NULL,  // default value
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__size_function__DetectionResult__objects,  // size() function pointer
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_const_function__DetectionResult__objects,  // get_const(index) function pointer
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__get_function__DetectionResult__objects,  // get(index) function pointer
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__fetch_function__DetectionResult__objects,  // fetch(index, &value) function pointer
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__assign_function__DetectionResult__objects,  // assign(index, value) function pointer
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__resize_function__DetectionResult__objects  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_members = {
  "vision_ai_interfaces__msg",  // message namespace
  "DetectionResult",  // message name
  5,  // number of fields
  sizeof(vision_ai_interfaces__msg__DetectionResult),
  vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_member_array,  // message members
  vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_init_function,  // function to initialize message memory (memory has to be allocated)
  vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_type_support_handle = {
  0,
  &vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, DetectionResult)() {
  vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, DetectedObject)();
  if (!vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vision_ai_interfaces__msg__DetectionResult__rosidl_typesupport_introspection_c__DetectionResult_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

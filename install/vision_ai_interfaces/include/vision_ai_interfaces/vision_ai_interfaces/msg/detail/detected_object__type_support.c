// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vision_ai_interfaces/msg/detail/detected_object__rosidl_typesupport_introspection_c.h"
#include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vision_ai_interfaces/msg/detail/detected_object__functions.h"
#include "vision_ai_interfaces/msg/detail/detected_object__struct.h"


// Include directives for member types
// Member `object_id`
// Member `class_name`
// Member `description`
#include "rosidl_runtime_c/string_functions.h"
// Member `bounding_box`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vision_ai_interfaces__msg__DetectedObject__init(message_memory);
}

void vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_fini_function(void * message_memory)
{
  vision_ai_interfaces__msg__DetectedObject__fini(message_memory);
}

size_t vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__size_function__DetectedObject__bounding_box(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_const_function__DetectedObject__bounding_box(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_function__DetectedObject__bounding_box(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__fetch_function__DetectedObject__bounding_box(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_const_function__DetectedObject__bounding_box(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__assign_function__DetectedObject__bounding_box(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_function__DetectedObject__bounding_box(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__resize_function__DetectedObject__bounding_box(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_member_array[11] = {
  {
    "object_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, object_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "class_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, class_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "class_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, class_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "description",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, description),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bounding_box",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, bounding_box),  // bytes offset in struct
    NULL,  // default value
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__size_function__DetectedObject__bounding_box,  // size() function pointer
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_const_function__DetectedObject__bounding_box,  // get_const(index) function pointer
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__get_function__DetectedObject__bounding_box,  // get(index) function pointer
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__fetch_function__DetectedObject__bounding_box,  // fetch(index, &value) function pointer
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__assign_function__DetectedObject__bounding_box,  // assign(index, value) function pointer
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__resize_function__DetectedObject__bounding_box  // resize(index) function pointer
  },
  {
    "center_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, center_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, center_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "world_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, world_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "world_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, world_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "world_z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__DetectedObject, world_z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_members = {
  "vision_ai_interfaces__msg",  // message namespace
  "DetectedObject",  // message name
  11,  // number of fields
  sizeof(vision_ai_interfaces__msg__DetectedObject),
  vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_member_array,  // message members
  vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_init_function,  // function to initialize message memory (memory has to be allocated)
  vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_type_support_handle = {
  0,
  &vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, DetectedObject)() {
  if (!vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vision_ai_interfaces__msg__DetectedObject__rosidl_typesupport_introspection_c__DetectedObject_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

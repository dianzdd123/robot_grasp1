// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vision_ai_interfaces/msg/detail/scan_plan__rosidl_typesupport_introspection_c.h"
#include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vision_ai_interfaces/msg/detail/scan_plan__functions.h"
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.h"


// Include directives for member types
// Member `strategy`
// Member `mode`
#include "rosidl_runtime_c/string_functions.h"
// Member `waypoints`
#include "vision_ai_interfaces/msg/waypoint.h"
// Member `waypoints`
#include "vision_ai_interfaces/msg/detail/waypoint__rosidl_typesupport_introspection_c.h"
// Member `scan_region`
#include "geometry_msgs/msg/point.h"
// Member `scan_region`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vision_ai_interfaces__msg__ScanPlan__init(message_memory);
}

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_fini_function(void * message_memory)
{
  vision_ai_interfaces__msg__ScanPlan__fini(message_memory);
}

size_t vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__size_function__ScanPlan__waypoints(
  const void * untyped_member)
{
  const vision_ai_interfaces__msg__Waypoint__Sequence * member =
    (const vision_ai_interfaces__msg__Waypoint__Sequence *)(untyped_member);
  return member->size;
}

const void * vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__waypoints(
  const void * untyped_member, size_t index)
{
  const vision_ai_interfaces__msg__Waypoint__Sequence * member =
    (const vision_ai_interfaces__msg__Waypoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__waypoints(
  void * untyped_member, size_t index)
{
  vision_ai_interfaces__msg__Waypoint__Sequence * member =
    (vision_ai_interfaces__msg__Waypoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__fetch_function__ScanPlan__waypoints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const vision_ai_interfaces__msg__Waypoint * item =
    ((const vision_ai_interfaces__msg__Waypoint *)
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__waypoints(untyped_member, index));
  vision_ai_interfaces__msg__Waypoint * value =
    (vision_ai_interfaces__msg__Waypoint *)(untyped_value);
  *value = *item;
}

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__assign_function__ScanPlan__waypoints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  vision_ai_interfaces__msg__Waypoint * item =
    ((vision_ai_interfaces__msg__Waypoint *)
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__waypoints(untyped_member, index));
  const vision_ai_interfaces__msg__Waypoint * value =
    (const vision_ai_interfaces__msg__Waypoint *)(untyped_value);
  *item = *value;
}

bool vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__resize_function__ScanPlan__waypoints(
  void * untyped_member, size_t size)
{
  vision_ai_interfaces__msg__Waypoint__Sequence * member =
    (vision_ai_interfaces__msg__Waypoint__Sequence *)(untyped_member);
  vision_ai_interfaces__msg__Waypoint__Sequence__fini(member);
  return vision_ai_interfaces__msg__Waypoint__Sequence__init(member, size);
}

size_t vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__size_function__ScanPlan__scan_region(
  const void * untyped_member)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return member->size;
}

const void * vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__scan_region(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Point__Sequence * member =
    (const geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__scan_region(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  return &member->data[index];
}

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__fetch_function__ScanPlan__scan_region(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Point * item =
    ((const geometry_msgs__msg__Point *)
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__scan_region(untyped_member, index));
  geometry_msgs__msg__Point * value =
    (geometry_msgs__msg__Point *)(untyped_value);
  *value = *item;
}

void vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__assign_function__ScanPlan__scan_region(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Point * item =
    ((geometry_msgs__msg__Point *)
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__scan_region(untyped_member, index));
  const geometry_msgs__msg__Point * value =
    (const geometry_msgs__msg__Point *)(untyped_value);
  *item = *value;
}

bool vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__resize_function__ScanPlan__scan_region(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Point__Sequence * member =
    (geometry_msgs__msg__Point__Sequence *)(untyped_member);
  geometry_msgs__msg__Point__Sequence__fini(member);
  return geometry_msgs__msg__Point__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_member_array[7] = {
  {
    "strategy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, strategy),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scan_height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, scan_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "required_height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, required_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "waypoints",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, waypoints),  // bytes offset in struct
    NULL,  // default value
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__size_function__ScanPlan__waypoints,  // size() function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__waypoints,  // get_const(index) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__waypoints,  // get(index) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__fetch_function__ScanPlan__waypoints,  // fetch(index, &value) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__assign_function__ScanPlan__waypoints,  // assign(index, value) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__resize_function__ScanPlan__waypoints  // resize(index) function pointer
  },
  {
    "scan_region",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, scan_region),  // bytes offset in struct
    NULL,  // default value
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__size_function__ScanPlan__scan_region,  // size() function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_const_function__ScanPlan__scan_region,  // get_const(index) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__get_function__ScanPlan__scan_region,  // get(index) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__fetch_function__ScanPlan__scan_region,  // fetch(index, &value) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__assign_function__ScanPlan__scan_region,  // assign(index, value) function pointer
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__resize_function__ScanPlan__scan_region  // resize(index) function pointer
  },
  {
    "object_height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, object_height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__msg__ScanPlan, mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_members = {
  "vision_ai_interfaces__msg",  // message namespace
  "ScanPlan",  // message name
  7,  // number of fields
  sizeof(vision_ai_interfaces__msg__ScanPlan),
  vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_member_array,  // message members
  vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_init_function,  // function to initialize message memory (memory has to be allocated)
  vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_type_support_handle = {
  0,
  &vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, ScanPlan)() {
  vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, Waypoint)();
  vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vision_ai_interfaces__msg__ScanPlan__rosidl_typesupport_introspection_c__ScanPlan_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

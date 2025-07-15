// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace vision_ai_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ScanPlan_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) vision_ai_interfaces::msg::ScanPlan(_init);
}

void ScanPlan_fini_function(void * message_memory)
{
  auto typed_message = static_cast<vision_ai_interfaces::msg::ScanPlan *>(message_memory);
  typed_message->~ScanPlan();
}

size_t size_function__ScanPlan__waypoints(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<vision_ai_interfaces::msg::Waypoint> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ScanPlan__waypoints(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<vision_ai_interfaces::msg::Waypoint> *>(untyped_member);
  return &member[index];
}

void * get_function__ScanPlan__waypoints(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<vision_ai_interfaces::msg::Waypoint> *>(untyped_member);
  return &member[index];
}

void fetch_function__ScanPlan__waypoints(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const vision_ai_interfaces::msg::Waypoint *>(
    get_const_function__ScanPlan__waypoints(untyped_member, index));
  auto & value = *reinterpret_cast<vision_ai_interfaces::msg::Waypoint *>(untyped_value);
  value = item;
}

void assign_function__ScanPlan__waypoints(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<vision_ai_interfaces::msg::Waypoint *>(
    get_function__ScanPlan__waypoints(untyped_member, index));
  const auto & value = *reinterpret_cast<const vision_ai_interfaces::msg::Waypoint *>(untyped_value);
  item = value;
}

void resize_function__ScanPlan__waypoints(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<vision_ai_interfaces::msg::Waypoint> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ScanPlan__scan_region(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ScanPlan__scan_region(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void * get_function__ScanPlan__scan_region(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  return &member[index];
}

void fetch_function__ScanPlan__scan_region(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const geometry_msgs::msg::Point *>(
    get_const_function__ScanPlan__scan_region(untyped_member, index));
  auto & value = *reinterpret_cast<geometry_msgs::msg::Point *>(untyped_value);
  value = item;
}

void assign_function__ScanPlan__scan_region(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<geometry_msgs::msg::Point *>(
    get_function__ScanPlan__scan_region(untyped_member, index));
  const auto & value = *reinterpret_cast<const geometry_msgs::msg::Point *>(untyped_value);
  item = value;
}

void resize_function__ScanPlan__scan_region(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<geometry_msgs::msg::Point> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ScanPlan_message_member_array[7] = {
  {
    "strategy",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, strategy),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "scan_height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, scan_height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "required_height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, required_height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "waypoints",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<vision_ai_interfaces::msg::Waypoint>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, waypoints),  // bytes offset in struct
    nullptr,  // default value
    size_function__ScanPlan__waypoints,  // size() function pointer
    get_const_function__ScanPlan__waypoints,  // get_const(index) function pointer
    get_function__ScanPlan__waypoints,  // get(index) function pointer
    fetch_function__ScanPlan__waypoints,  // fetch(index, &value) function pointer
    assign_function__ScanPlan__waypoints,  // assign(index, value) function pointer
    resize_function__ScanPlan__waypoints  // resize(index) function pointer
  },
  {
    "scan_region",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Point>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, scan_region),  // bytes offset in struct
    nullptr,  // default value
    size_function__ScanPlan__scan_region,  // size() function pointer
    get_const_function__ScanPlan__scan_region,  // get_const(index) function pointer
    get_function__ScanPlan__scan_region,  // get(index) function pointer
    fetch_function__ScanPlan__scan_region,  // fetch(index, &value) function pointer
    assign_function__ScanPlan__scan_region,  // assign(index, value) function pointer
    resize_function__ScanPlan__scan_region  // resize(index) function pointer
  },
  {
    "object_height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, object_height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "mode",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::ScanPlan, mode),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ScanPlan_message_members = {
  "vision_ai_interfaces::msg",  // message namespace
  "ScanPlan",  // message name
  7,  // number of fields
  sizeof(vision_ai_interfaces::msg::ScanPlan),
  ScanPlan_message_member_array,  // message members
  ScanPlan_init_function,  // function to initialize message memory (memory has to be allocated)
  ScanPlan_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ScanPlan_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ScanPlan_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace vision_ai_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<vision_ai_interfaces::msg::ScanPlan>()
{
  return &::vision_ai_interfaces::msg::rosidl_typesupport_introspection_cpp::ScanPlan_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vision_ai_interfaces, msg, ScanPlan)() {
  return &::vision_ai_interfaces::msg::rosidl_typesupport_introspection_cpp::ScanPlan_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

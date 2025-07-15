// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "vision_ai_interfaces/msg/detail/detection_result__struct.hpp"
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

void DetectionResult_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) vision_ai_interfaces::msg::DetectionResult(_init);
}

void DetectionResult_fini_function(void * message_memory)
{
  auto typed_message = static_cast<vision_ai_interfaces::msg::DetectionResult *>(message_memory);
  typed_message->~DetectionResult();
}

size_t size_function__DetectionResult__objects(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<vision_ai_interfaces::msg::DetectedObject> *>(untyped_member);
  return member->size();
}

const void * get_const_function__DetectionResult__objects(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<vision_ai_interfaces::msg::DetectedObject> *>(untyped_member);
  return &member[index];
}

void * get_function__DetectionResult__objects(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<vision_ai_interfaces::msg::DetectedObject> *>(untyped_member);
  return &member[index];
}

void fetch_function__DetectionResult__objects(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const vision_ai_interfaces::msg::DetectedObject *>(
    get_const_function__DetectionResult__objects(untyped_member, index));
  auto & value = *reinterpret_cast<vision_ai_interfaces::msg::DetectedObject *>(untyped_value);
  value = item;
}

void assign_function__DetectionResult__objects(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<vision_ai_interfaces::msg::DetectedObject *>(
    get_function__DetectionResult__objects(untyped_member, index));
  const auto & value = *reinterpret_cast<const vision_ai_interfaces::msg::DetectedObject *>(untyped_value);
  item = value;
}

void resize_function__DetectionResult__objects(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<vision_ai_interfaces::msg::DetectedObject> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember DetectionResult_message_member_array[5] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::DetectionResult, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "detection_count",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::DetectionResult, detection_count),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "processing_time",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::DetectionResult, processing_time),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "output_directory",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::DetectionResult, output_directory),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "objects",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<vision_ai_interfaces::msg::DetectedObject>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces::msg::DetectionResult, objects),  // bytes offset in struct
    nullptr,  // default value
    size_function__DetectionResult__objects,  // size() function pointer
    get_const_function__DetectionResult__objects,  // get_const(index) function pointer
    get_function__DetectionResult__objects,  // get(index) function pointer
    fetch_function__DetectionResult__objects,  // fetch(index, &value) function pointer
    assign_function__DetectionResult__objects,  // assign(index, value) function pointer
    resize_function__DetectionResult__objects  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers DetectionResult_message_members = {
  "vision_ai_interfaces::msg",  // message namespace
  "DetectionResult",  // message name
  5,  // number of fields
  sizeof(vision_ai_interfaces::msg::DetectionResult),
  DetectionResult_message_member_array,  // message members
  DetectionResult_init_function,  // function to initialize message memory (memory has to be allocated)
  DetectionResult_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t DetectionResult_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &DetectionResult_message_members,
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
get_message_type_support_handle<vision_ai_interfaces::msg::DetectionResult>()
{
  return &::vision_ai_interfaces::msg::rosidl_typesupport_introspection_cpp::DetectionResult_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vision_ai_interfaces, msg, DetectionResult)() {
  return &::vision_ai_interfaces::msg::rosidl_typesupport_introspection_cpp::DetectionResult_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

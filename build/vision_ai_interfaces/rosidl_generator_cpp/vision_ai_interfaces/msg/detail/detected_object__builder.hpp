// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/detected_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_DetectedObject_world_z
{
public:
  explicit Init_DetectedObject_world_z(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::DetectedObject world_z(::vision_ai_interfaces::msg::DetectedObject::_world_z_type arg)
  {
    msg_.world_z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_world_y
{
public:
  explicit Init_DetectedObject_world_y(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_world_z world_y(::vision_ai_interfaces::msg::DetectedObject::_world_y_type arg)
  {
    msg_.world_y = std::move(arg);
    return Init_DetectedObject_world_z(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_world_x
{
public:
  explicit Init_DetectedObject_world_x(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_world_y world_x(::vision_ai_interfaces::msg::DetectedObject::_world_x_type arg)
  {
    msg_.world_x = std::move(arg);
    return Init_DetectedObject_world_y(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_center_y
{
public:
  explicit Init_DetectedObject_center_y(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_world_x center_y(::vision_ai_interfaces::msg::DetectedObject::_center_y_type arg)
  {
    msg_.center_y = std::move(arg);
    return Init_DetectedObject_world_x(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_center_x
{
public:
  explicit Init_DetectedObject_center_x(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_center_y center_x(::vision_ai_interfaces::msg::DetectedObject::_center_x_type arg)
  {
    msg_.center_x = std::move(arg);
    return Init_DetectedObject_center_y(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_bounding_box
{
public:
  explicit Init_DetectedObject_bounding_box(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_center_x bounding_box(::vision_ai_interfaces::msg::DetectedObject::_bounding_box_type arg)
  {
    msg_.bounding_box = std::move(arg);
    return Init_DetectedObject_center_x(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_description
{
public:
  explicit Init_DetectedObject_description(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_bounding_box description(::vision_ai_interfaces::msg::DetectedObject::_description_type arg)
  {
    msg_.description = std::move(arg);
    return Init_DetectedObject_bounding_box(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_confidence
{
public:
  explicit Init_DetectedObject_confidence(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_description confidence(::vision_ai_interfaces::msg::DetectedObject::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_DetectedObject_description(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_class_name
{
public:
  explicit Init_DetectedObject_class_name(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_confidence class_name(::vision_ai_interfaces::msg::DetectedObject::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_DetectedObject_confidence(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_class_id
{
public:
  explicit Init_DetectedObject_class_id(::vision_ai_interfaces::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_class_name class_id(::vision_ai_interfaces::msg::DetectedObject::_class_id_type arg)
  {
    msg_.class_id = std::move(arg);
    return Init_DetectedObject_class_name(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

class Init_DetectedObject_object_id
{
public:
  Init_DetectedObject_object_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectedObject_class_id object_id(::vision_ai_interfaces::msg::DetectedObject::_object_id_type arg)
  {
    msg_.object_id = std::move(arg);
    return Init_DetectedObject_class_id(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::DetectedObject>()
{
  return vision_ai_interfaces::msg::builder::Init_DetectedObject_object_id();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_

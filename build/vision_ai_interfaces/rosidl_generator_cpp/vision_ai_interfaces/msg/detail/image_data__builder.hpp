// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/ImageData.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/image_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_ImageData_image
{
public:
  explicit Init_ImageData_image(::vision_ai_interfaces::msg::ImageData & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::ImageData image(::vision_ai_interfaces::msg::ImageData::_image_type arg)
  {
    msg_.image = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ImageData msg_;
};

class Init_ImageData_waypoint
{
public:
  explicit Init_ImageData_waypoint(::vision_ai_interfaces::msg::ImageData & msg)
  : msg_(msg)
  {}
  Init_ImageData_image waypoint(::vision_ai_interfaces::msg::ImageData::_waypoint_type arg)
  {
    msg_.waypoint = std::move(arg);
    return Init_ImageData_image(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ImageData msg_;
};

class Init_ImageData_timestamp
{
public:
  explicit Init_ImageData_timestamp(::vision_ai_interfaces::msg::ImageData & msg)
  : msg_(msg)
  {}
  Init_ImageData_waypoint timestamp(::vision_ai_interfaces::msg::ImageData::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_ImageData_waypoint(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ImageData msg_;
};

class Init_ImageData_filename
{
public:
  Init_ImageData_filename()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ImageData_timestamp filename(::vision_ai_interfaces::msg::ImageData::_filename_type arg)
  {
    msg_.filename = std::move(arg);
    return Init_ImageData_timestamp(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ImageData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::ImageData>()
{
  return vision_ai_interfaces::msg::builder::Init_ImageData_filename();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__BUILDER_HPP_

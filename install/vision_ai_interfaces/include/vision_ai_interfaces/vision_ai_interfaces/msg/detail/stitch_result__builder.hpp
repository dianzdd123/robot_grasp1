// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/stitch_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_StitchResult_processing_time
{
public:
  explicit Init_StitchResult_processing_time(::vision_ai_interfaces::msg::StitchResult & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::StitchResult processing_time(::vision_ai_interfaces::msg::StitchResult::_processing_time_type arg)
  {
    msg_.processing_time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::StitchResult msg_;
};

class Init_StitchResult_input_images
{
public:
  explicit Init_StitchResult_input_images(::vision_ai_interfaces::msg::StitchResult & msg)
  : msg_(msg)
  {}
  Init_StitchResult_processing_time input_images(::vision_ai_interfaces::msg::StitchResult::_input_images_type arg)
  {
    msg_.input_images = std::move(arg);
    return Init_StitchResult_processing_time(msg_);
  }

private:
  ::vision_ai_interfaces::msg::StitchResult msg_;
};

class Init_StitchResult_output_path
{
public:
  explicit Init_StitchResult_output_path(::vision_ai_interfaces::msg::StitchResult & msg)
  : msg_(msg)
  {}
  Init_StitchResult_input_images output_path(::vision_ai_interfaces::msg::StitchResult::_output_path_type arg)
  {
    msg_.output_path = std::move(arg);
    return Init_StitchResult_input_images(msg_);
  }

private:
  ::vision_ai_interfaces::msg::StitchResult msg_;
};

class Init_StitchResult_method
{
public:
  Init_StitchResult_method()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StitchResult_output_path method(::vision_ai_interfaces::msg::StitchResult::_method_type arg)
  {
    msg_.method = std::move(arg);
    return Init_StitchResult_output_path(msg_);
  }

private:
  ::vision_ai_interfaces::msg::StitchResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::StitchResult>()
{
  return vision_ai_interfaces::msg::builder::Init_StitchResult_method();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__BUILDER_HPP_

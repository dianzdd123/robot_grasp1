// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/detection_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_DetectionResult_objects
{
public:
  explicit Init_DetectionResult_objects(::vision_ai_interfaces::msg::DetectionResult & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::DetectionResult objects(::vision_ai_interfaces::msg::DetectionResult::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectionResult msg_;
};

class Init_DetectionResult_output_directory
{
public:
  explicit Init_DetectionResult_output_directory(::vision_ai_interfaces::msg::DetectionResult & msg)
  : msg_(msg)
  {}
  Init_DetectionResult_objects output_directory(::vision_ai_interfaces::msg::DetectionResult::_output_directory_type arg)
  {
    msg_.output_directory = std::move(arg);
    return Init_DetectionResult_objects(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectionResult msg_;
};

class Init_DetectionResult_processing_time
{
public:
  explicit Init_DetectionResult_processing_time(::vision_ai_interfaces::msg::DetectionResult & msg)
  : msg_(msg)
  {}
  Init_DetectionResult_output_directory processing_time(::vision_ai_interfaces::msg::DetectionResult::_processing_time_type arg)
  {
    msg_.processing_time = std::move(arg);
    return Init_DetectionResult_output_directory(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectionResult msg_;
};

class Init_DetectionResult_detection_count
{
public:
  explicit Init_DetectionResult_detection_count(::vision_ai_interfaces::msg::DetectionResult & msg)
  : msg_(msg)
  {}
  Init_DetectionResult_processing_time detection_count(::vision_ai_interfaces::msg::DetectionResult::_detection_count_type arg)
  {
    msg_.detection_count = std::move(arg);
    return Init_DetectionResult_processing_time(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectionResult msg_;
};

class Init_DetectionResult_header
{
public:
  Init_DetectionResult_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectionResult_detection_count header(::vision_ai_interfaces::msg::DetectionResult::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_DetectionResult_detection_count(msg_);
  }

private:
  ::vision_ai_interfaces::msg::DetectionResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::DetectionResult>()
{
  return vision_ai_interfaces::msg::builder::Init_DetectionResult_header();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__BUILDER_HPP_

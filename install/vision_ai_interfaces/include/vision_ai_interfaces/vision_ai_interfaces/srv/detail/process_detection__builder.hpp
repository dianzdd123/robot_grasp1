// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:srv/ProcessDetection.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__BUILDER_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/srv/detail/process_detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ProcessDetection_Request>()
{
  return ::vision_ai_interfaces::srv::ProcessDetection_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace vision_ai_interfaces


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_ProcessDetection_Response_result
{
public:
  explicit Init_ProcessDetection_Response_result(::vision_ai_interfaces::srv::ProcessDetection_Response & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::ProcessDetection_Response result(::vision_ai_interfaces::srv::ProcessDetection_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessDetection_Response msg_;
};

class Init_ProcessDetection_Response_message
{
public:
  explicit Init_ProcessDetection_Response_message(::vision_ai_interfaces::srv::ProcessDetection_Response & msg)
  : msg_(msg)
  {}
  Init_ProcessDetection_Response_result message(::vision_ai_interfaces::srv::ProcessDetection_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ProcessDetection_Response_result(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessDetection_Response msg_;
};

class Init_ProcessDetection_Response_success
{
public:
  Init_ProcessDetection_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProcessDetection_Response_message success(::vision_ai_interfaces::srv::ProcessDetection_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ProcessDetection_Response_message(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessDetection_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ProcessDetection_Response>()
{
  return vision_ai_interfaces::srv::builder::Init_ProcessDetection_Response_success();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__BUILDER_HPP_

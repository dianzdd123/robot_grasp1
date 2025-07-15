// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:srv/ProcessStitching.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__BUILDER_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/srv/detail/process_stitching__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_ProcessStitching_Request_output_directory
{
public:
  explicit Init_ProcessStitching_Request_output_directory(::vision_ai_interfaces::srv::ProcessStitching_Request & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::ProcessStitching_Request output_directory(::vision_ai_interfaces::srv::ProcessStitching_Request::_output_directory_type arg)
  {
    msg_.output_directory = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Request msg_;
};

class Init_ProcessStitching_Request_scan_plan
{
public:
  explicit Init_ProcessStitching_Request_scan_plan(::vision_ai_interfaces::srv::ProcessStitching_Request & msg)
  : msg_(msg)
  {}
  Init_ProcessStitching_Request_output_directory scan_plan(::vision_ai_interfaces::srv::ProcessStitching_Request::_scan_plan_type arg)
  {
    msg_.scan_plan = std::move(arg);
    return Init_ProcessStitching_Request_output_directory(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Request msg_;
};

class Init_ProcessStitching_Request_image_data
{
public:
  Init_ProcessStitching_Request_image_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProcessStitching_Request_scan_plan image_data(::vision_ai_interfaces::srv::ProcessStitching_Request::_image_data_type arg)
  {
    msg_.image_data = std::move(arg);
    return Init_ProcessStitching_Request_scan_plan(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ProcessStitching_Request>()
{
  return vision_ai_interfaces::srv::builder::Init_ProcessStitching_Request_image_data();
}

}  // namespace vision_ai_interfaces


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_ProcessStitching_Response_result
{
public:
  explicit Init_ProcessStitching_Response_result(::vision_ai_interfaces::srv::ProcessStitching_Response & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::ProcessStitching_Response result(::vision_ai_interfaces::srv::ProcessStitching_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Response msg_;
};

class Init_ProcessStitching_Response_message
{
public:
  explicit Init_ProcessStitching_Response_message(::vision_ai_interfaces::srv::ProcessStitching_Response & msg)
  : msg_(msg)
  {}
  Init_ProcessStitching_Response_result message(::vision_ai_interfaces::srv::ProcessStitching_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ProcessStitching_Response_result(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Response msg_;
};

class Init_ProcessStitching_Response_success
{
public:
  Init_ProcessStitching_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProcessStitching_Response_message success(::vision_ai_interfaces::srv::ProcessStitching_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ProcessStitching_Response_message(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ProcessStitching_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ProcessStitching_Response>()
{
  return vision_ai_interfaces::srv::builder::Init_ProcessStitching_Response_success();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__BUILDER_HPP_

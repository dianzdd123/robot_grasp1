// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:srv/ExecuteScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__BUILDER_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/srv/detail/execute_scan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteScan_Request_scan_plan
{
public:
  Init_ExecuteScan_Request_scan_plan()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vision_ai_interfaces::srv::ExecuteScan_Request scan_plan(::vision_ai_interfaces::srv::ExecuteScan_Request::_scan_plan_type arg)
  {
    msg_.scan_plan = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ExecuteScan_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ExecuteScan_Request>()
{
  return vision_ai_interfaces::srv::builder::Init_ExecuteScan_Request_scan_plan();
}

}  // namespace vision_ai_interfaces


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_ExecuteScan_Response_output_directory
{
public:
  explicit Init_ExecuteScan_Response_output_directory(::vision_ai_interfaces::srv::ExecuteScan_Response & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::ExecuteScan_Response output_directory(::vision_ai_interfaces::srv::ExecuteScan_Response::_output_directory_type arg)
  {
    msg_.output_directory = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ExecuteScan_Response msg_;
};

class Init_ExecuteScan_Response_message
{
public:
  explicit Init_ExecuteScan_Response_message(::vision_ai_interfaces::srv::ExecuteScan_Response & msg)
  : msg_(msg)
  {}
  Init_ExecuteScan_Response_output_directory message(::vision_ai_interfaces::srv::ExecuteScan_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ExecuteScan_Response_output_directory(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ExecuteScan_Response msg_;
};

class Init_ExecuteScan_Response_success
{
public:
  Init_ExecuteScan_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteScan_Response_message success(::vision_ai_interfaces::srv::ExecuteScan_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteScan_Response_message(msg_);
  }

private:
  ::vision_ai_interfaces::srv::ExecuteScan_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::ExecuteScan_Response>()
{
  return vision_ai_interfaces::srv::builder::Init_ExecuteScan_Response_success();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__BUILDER_HPP_

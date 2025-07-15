// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:srv/PlanScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__BUILDER_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/srv/detail/plan_scan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_PlanScan_Request_points
{
public:
  explicit Init_PlanScan_Request_points(::vision_ai_interfaces::srv::PlanScan_Request & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::PlanScan_Request points(::vision_ai_interfaces::srv::PlanScan_Request::_points_type arg)
  {
    msg_.points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Request msg_;
};

class Init_PlanScan_Request_object_height
{
public:
  explicit Init_PlanScan_Request_object_height(::vision_ai_interfaces::srv::PlanScan_Request & msg)
  : msg_(msg)
  {}
  Init_PlanScan_Request_points object_height(::vision_ai_interfaces::srv::PlanScan_Request::_object_height_type arg)
  {
    msg_.object_height = std::move(arg);
    return Init_PlanScan_Request_points(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Request msg_;
};

class Init_PlanScan_Request_mode
{
public:
  Init_PlanScan_Request_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanScan_Request_object_height mode(::vision_ai_interfaces::srv::PlanScan_Request::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return Init_PlanScan_Request_object_height(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::PlanScan_Request>()
{
  return vision_ai_interfaces::srv::builder::Init_PlanScan_Request_mode();
}

}  // namespace vision_ai_interfaces


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_PlanScan_Response_scan_plan
{
public:
  explicit Init_PlanScan_Response_scan_plan(::vision_ai_interfaces::srv::PlanScan_Response & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::PlanScan_Response scan_plan(::vision_ai_interfaces::srv::PlanScan_Response::_scan_plan_type arg)
  {
    msg_.scan_plan = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Response msg_;
};

class Init_PlanScan_Response_message
{
public:
  explicit Init_PlanScan_Response_message(::vision_ai_interfaces::srv::PlanScan_Response & msg)
  : msg_(msg)
  {}
  Init_PlanScan_Response_scan_plan message(::vision_ai_interfaces::srv::PlanScan_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_PlanScan_Response_scan_plan(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Response msg_;
};

class Init_PlanScan_Response_success
{
public:
  Init_PlanScan_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanScan_Response_message success(::vision_ai_interfaces::srv::PlanScan_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PlanScan_Response_message(msg_);
  }

private:
  ::vision_ai_interfaces::srv::PlanScan_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::PlanScan_Response>()
{
  return vision_ai_interfaces::srv::builder::Init_PlanScan_Response_success();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PLAN_SCAN__BUILDER_HPP_

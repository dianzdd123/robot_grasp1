// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/scan_plan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_ScanPlan_mode
{
public:
  explicit Init_ScanPlan_mode(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::ScanPlan mode(::vision_ai_interfaces::msg::ScanPlan::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_object_height
{
public:
  explicit Init_ScanPlan_object_height(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  Init_ScanPlan_mode object_height(::vision_ai_interfaces::msg::ScanPlan::_object_height_type arg)
  {
    msg_.object_height = std::move(arg);
    return Init_ScanPlan_mode(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_scan_region
{
public:
  explicit Init_ScanPlan_scan_region(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  Init_ScanPlan_object_height scan_region(::vision_ai_interfaces::msg::ScanPlan::_scan_region_type arg)
  {
    msg_.scan_region = std::move(arg);
    return Init_ScanPlan_object_height(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_waypoints
{
public:
  explicit Init_ScanPlan_waypoints(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  Init_ScanPlan_scan_region waypoints(::vision_ai_interfaces::msg::ScanPlan::_waypoints_type arg)
  {
    msg_.waypoints = std::move(arg);
    return Init_ScanPlan_scan_region(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_required_height
{
public:
  explicit Init_ScanPlan_required_height(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  Init_ScanPlan_waypoints required_height(::vision_ai_interfaces::msg::ScanPlan::_required_height_type arg)
  {
    msg_.required_height = std::move(arg);
    return Init_ScanPlan_waypoints(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_scan_height
{
public:
  explicit Init_ScanPlan_scan_height(::vision_ai_interfaces::msg::ScanPlan & msg)
  : msg_(msg)
  {}
  Init_ScanPlan_required_height scan_height(::vision_ai_interfaces::msg::ScanPlan::_scan_height_type arg)
  {
    msg_.scan_height = std::move(arg);
    return Init_ScanPlan_required_height(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

class Init_ScanPlan_strategy
{
public:
  Init_ScanPlan_strategy()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ScanPlan_scan_height strategy(::vision_ai_interfaces::msg::ScanPlan::_strategy_type arg)
  {
    msg_.strategy = std::move(arg);
    return Init_ScanPlan_scan_height(msg_);
  }

private:
  ::vision_ai_interfaces::msg::ScanPlan msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::ScanPlan>()
{
  return vision_ai_interfaces::msg::builder::Init_ScanPlan_strategy();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__BUILDER_HPP_

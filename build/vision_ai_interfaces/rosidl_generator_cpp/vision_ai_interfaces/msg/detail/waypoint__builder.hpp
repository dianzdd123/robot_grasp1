// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/msg/detail/waypoint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace msg
{

namespace builder
{

class Init_Waypoint_coverage_rect
{
public:
  explicit Init_Waypoint_coverage_rect(::vision_ai_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::msg::Waypoint coverage_rect(::vision_ai_interfaces::msg::Waypoint::_coverage_rect_type arg)
  {
    msg_.coverage_rect = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_waypoint_index
{
public:
  explicit Init_Waypoint_waypoint_index(::vision_ai_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  Init_Waypoint_coverage_rect waypoint_index(::vision_ai_interfaces::msg::Waypoint::_waypoint_index_type arg)
  {
    msg_.waypoint_index = std::move(arg);
    return Init_Waypoint_coverage_rect(msg_);
  }

private:
  ::vision_ai_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_pose
{
public:
  Init_Waypoint_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Waypoint_waypoint_index pose(::vision_ai_interfaces::msg::Waypoint::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_Waypoint_waypoint_index(msg_);
  }

private:
  ::vision_ai_interfaces::msg::Waypoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::msg::Waypoint>()
{
  return vision_ai_interfaces::msg::builder::Init_Waypoint_pose();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_

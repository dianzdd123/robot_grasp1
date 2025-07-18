// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_ai_interfaces:srv/SetGripperClose.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__BUILDER_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_ai_interfaces/srv/detail/set_gripper_close__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetGripperClose_Request_position
{
public:
  Init_SetGripperClose_Request_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::vision_ai_interfaces::srv::SetGripperClose_Request position(::vision_ai_interfaces::srv::SetGripperClose_Request::_position_type arg)
  {
    msg_.position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::SetGripperClose_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::SetGripperClose_Request>()
{
  return vision_ai_interfaces::srv::builder::Init_SetGripperClose_Request_position();
}

}  // namespace vision_ai_interfaces


namespace vision_ai_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetGripperClose_Response_actual_position
{
public:
  explicit Init_SetGripperClose_Response_actual_position(::vision_ai_interfaces::srv::SetGripperClose_Response & msg)
  : msg_(msg)
  {}
  ::vision_ai_interfaces::srv::SetGripperClose_Response actual_position(::vision_ai_interfaces::srv::SetGripperClose_Response::_actual_position_type arg)
  {
    msg_.actual_position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_ai_interfaces::srv::SetGripperClose_Response msg_;
};

class Init_SetGripperClose_Response_message
{
public:
  explicit Init_SetGripperClose_Response_message(::vision_ai_interfaces::srv::SetGripperClose_Response & msg)
  : msg_(msg)
  {}
  Init_SetGripperClose_Response_actual_position message(::vision_ai_interfaces::srv::SetGripperClose_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_SetGripperClose_Response_actual_position(msg_);
  }

private:
  ::vision_ai_interfaces::srv::SetGripperClose_Response msg_;
};

class Init_SetGripperClose_Response_success
{
public:
  Init_SetGripperClose_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetGripperClose_Response_message success(::vision_ai_interfaces::srv::SetGripperClose_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetGripperClose_Response_message(msg_);
  }

private:
  ::vision_ai_interfaces::srv::SetGripperClose_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_ai_interfaces::srv::SetGripperClose_Response>()
{
  return vision_ai_interfaces::srv::builder::Init_SetGripperClose_Response_success();
}

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__BUILDER_HPP_

// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:srv/SetGripperClose.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__TRAITS_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/srv/detail/set_gripper_close__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetGripperClose_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetGripperClose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetGripperClose_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use vision_ai_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vision_ai_interfaces::srv::SetGripperClose_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::SetGripperClose_Request & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::SetGripperClose_Request>()
{
  return "vision_ai_interfaces::srv::SetGripperClose_Request";
}

template<>
inline const char * name<vision_ai_interfaces::srv::SetGripperClose_Request>()
{
  return "vision_ai_interfaces/srv/SetGripperClose_Request";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::SetGripperClose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::SetGripperClose_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vision_ai_interfaces::srv::SetGripperClose_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetGripperClose_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: actual_position
  {
    out << "actual_position: ";
    rosidl_generator_traits::value_to_yaml(msg.actual_position, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetGripperClose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: actual_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "actual_position: ";
    rosidl_generator_traits::value_to_yaml(msg.actual_position, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetGripperClose_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use vision_ai_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vision_ai_interfaces::srv::SetGripperClose_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::SetGripperClose_Response & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::SetGripperClose_Response>()
{
  return "vision_ai_interfaces::srv::SetGripperClose_Response";
}

template<>
inline const char * name<vision_ai_interfaces::srv::SetGripperClose_Response>()
{
  return "vision_ai_interfaces/srv/SetGripperClose_Response";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::SetGripperClose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::SetGripperClose_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::srv::SetGripperClose_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vision_ai_interfaces::srv::SetGripperClose>()
{
  return "vision_ai_interfaces::srv::SetGripperClose";
}

template<>
inline const char * name<vision_ai_interfaces::srv::SetGripperClose>()
{
  return "vision_ai_interfaces/srv/SetGripperClose";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::SetGripperClose>
  : std::integral_constant<
    bool,
    has_fixed_size<vision_ai_interfaces::srv::SetGripperClose_Request>::value &&
    has_fixed_size<vision_ai_interfaces::srv::SetGripperClose_Response>::value
  >
{
};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::SetGripperClose>
  : std::integral_constant<
    bool,
    has_bounded_size<vision_ai_interfaces::srv::SetGripperClose_Request>::value &&
    has_bounded_size<vision_ai_interfaces::srv::SetGripperClose_Response>::value
  >
{
};

template<>
struct is_service<vision_ai_interfaces::srv::SetGripperClose>
  : std::true_type
{
};

template<>
struct is_service_request<vision_ai_interfaces::srv::SetGripperClose_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vision_ai_interfaces::srv::SetGripperClose_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__SET_GRIPPER_CLOSE__TRAITS_HPP_

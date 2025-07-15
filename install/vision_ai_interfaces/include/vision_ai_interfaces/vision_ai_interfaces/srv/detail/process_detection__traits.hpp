// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:srv/ProcessDetection.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__TRAITS_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/srv/detail/process_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ProcessDetection_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProcessDetection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProcessDetection_Request & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::srv::ProcessDetection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::ProcessDetection_Request & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::ProcessDetection_Request>()
{
  return "vision_ai_interfaces::srv::ProcessDetection_Request";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ProcessDetection_Request>()
{
  return "vision_ai_interfaces/srv/ProcessDetection_Request";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ProcessDetection_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ProcessDetection_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vision_ai_interfaces::srv::ProcessDetection_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
#include "vision_ai_interfaces/msg/detail/detection_result__traits.hpp"

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ProcessDetection_Response & msg,
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

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProcessDetection_Response & msg,
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

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProcessDetection_Response & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::srv::ProcessDetection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::ProcessDetection_Response & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::ProcessDetection_Response>()
{
  return "vision_ai_interfaces::srv::ProcessDetection_Response";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ProcessDetection_Response>()
{
  return "vision_ai_interfaces/srv/ProcessDetection_Response";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ProcessDetection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ProcessDetection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::srv::ProcessDetection_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vision_ai_interfaces::srv::ProcessDetection>()
{
  return "vision_ai_interfaces::srv::ProcessDetection";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ProcessDetection>()
{
  return "vision_ai_interfaces/srv/ProcessDetection";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ProcessDetection>
  : std::integral_constant<
    bool,
    has_fixed_size<vision_ai_interfaces::srv::ProcessDetection_Request>::value &&
    has_fixed_size<vision_ai_interfaces::srv::ProcessDetection_Response>::value
  >
{
};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ProcessDetection>
  : std::integral_constant<
    bool,
    has_bounded_size<vision_ai_interfaces::srv::ProcessDetection_Request>::value &&
    has_bounded_size<vision_ai_interfaces::srv::ProcessDetection_Response>::value
  >
{
};

template<>
struct is_service<vision_ai_interfaces::srv::ProcessDetection>
  : std::true_type
{
};

template<>
struct is_service_request<vision_ai_interfaces::srv::ProcessDetection_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vision_ai_interfaces::srv::ProcessDetection_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_DETECTION__TRAITS_HPP_

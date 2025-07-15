// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:srv/ExecuteScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__TRAITS_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/srv/detail/execute_scan__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__traits.hpp"

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExecuteScan_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: scan_plan
  {
    out << "scan_plan: ";
    to_flow_style_yaml(msg.scan_plan, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteScan_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: scan_plan
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scan_plan:\n";
    to_block_style_yaml(msg.scan_plan, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteScan_Request & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::srv::ExecuteScan_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::ExecuteScan_Request & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::ExecuteScan_Request>()
{
  return "vision_ai_interfaces::srv::ExecuteScan_Request";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ExecuteScan_Request>()
{
  return "vision_ai_interfaces/srv/ExecuteScan_Request";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ExecuteScan_Request>
  : std::integral_constant<bool, has_fixed_size<vision_ai_interfaces::msg::ScanPlan>::value> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ExecuteScan_Request>
  : std::integral_constant<bool, has_bounded_size<vision_ai_interfaces::msg::ScanPlan>::value> {};

template<>
struct is_message<vision_ai_interfaces::srv::ExecuteScan_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace vision_ai_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ExecuteScan_Response & msg,
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

  // member: output_directory
  {
    out << "output_directory: ";
    rosidl_generator_traits::value_to_yaml(msg.output_directory, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteScan_Response & msg,
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

  // member: output_directory
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "output_directory: ";
    rosidl_generator_traits::value_to_yaml(msg.output_directory, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteScan_Response & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::srv::ExecuteScan_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::srv::ExecuteScan_Response & msg)
{
  return vision_ai_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::srv::ExecuteScan_Response>()
{
  return "vision_ai_interfaces::srv::ExecuteScan_Response";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ExecuteScan_Response>()
{
  return "vision_ai_interfaces/srv/ExecuteScan_Response";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ExecuteScan_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ExecuteScan_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::srv::ExecuteScan_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<vision_ai_interfaces::srv::ExecuteScan>()
{
  return "vision_ai_interfaces::srv::ExecuteScan";
}

template<>
inline const char * name<vision_ai_interfaces::srv::ExecuteScan>()
{
  return "vision_ai_interfaces/srv/ExecuteScan";
}

template<>
struct has_fixed_size<vision_ai_interfaces::srv::ExecuteScan>
  : std::integral_constant<
    bool,
    has_fixed_size<vision_ai_interfaces::srv::ExecuteScan_Request>::value &&
    has_fixed_size<vision_ai_interfaces::srv::ExecuteScan_Response>::value
  >
{
};

template<>
struct has_bounded_size<vision_ai_interfaces::srv::ExecuteScan>
  : std::integral_constant<
    bool,
    has_bounded_size<vision_ai_interfaces::srv::ExecuteScan_Request>::value &&
    has_bounded_size<vision_ai_interfaces::srv::ExecuteScan_Response>::value
  >
{
};

template<>
struct is_service<vision_ai_interfaces::srv::ExecuteScan>
  : std::true_type
{
};

template<>
struct is_service_request<vision_ai_interfaces::srv::ExecuteScan_Request>
  : std::true_type
{
};

template<>
struct is_service_response<vision_ai_interfaces::srv::ExecuteScan_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__TRAITS_HPP_

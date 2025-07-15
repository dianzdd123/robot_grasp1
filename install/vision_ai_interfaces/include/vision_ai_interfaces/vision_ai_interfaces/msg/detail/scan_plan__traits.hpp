// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__TRAITS_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/msg/detail/scan_plan__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'waypoints'
#include "vision_ai_interfaces/msg/detail/waypoint__traits.hpp"
// Member 'scan_region'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace vision_ai_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ScanPlan & msg,
  std::ostream & out)
{
  out << "{";
  // member: strategy
  {
    out << "strategy: ";
    rosidl_generator_traits::value_to_yaml(msg.strategy, out);
    out << ", ";
  }

  // member: scan_height
  {
    out << "scan_height: ";
    rosidl_generator_traits::value_to_yaml(msg.scan_height, out);
    out << ", ";
  }

  // member: required_height
  {
    out << "required_height: ";
    rosidl_generator_traits::value_to_yaml(msg.required_height, out);
    out << ", ";
  }

  // member: waypoints
  {
    if (msg.waypoints.size() == 0) {
      out << "waypoints: []";
    } else {
      out << "waypoints: [";
      size_t pending_items = msg.waypoints.size();
      for (auto item : msg.waypoints) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: scan_region
  {
    if (msg.scan_region.size() == 0) {
      out << "scan_region: []";
    } else {
      out << "scan_region: [";
      size_t pending_items = msg.scan_region.size();
      for (auto item : msg.scan_region) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: object_height
  {
    out << "object_height: ";
    rosidl_generator_traits::value_to_yaml(msg.object_height, out);
    out << ", ";
  }

  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ScanPlan & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: strategy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "strategy: ";
    rosidl_generator_traits::value_to_yaml(msg.strategy, out);
    out << "\n";
  }

  // member: scan_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scan_height: ";
    rosidl_generator_traits::value_to_yaml(msg.scan_height, out);
    out << "\n";
  }

  // member: required_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "required_height: ";
    rosidl_generator_traits::value_to_yaml(msg.required_height, out);
    out << "\n";
  }

  // member: waypoints
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.waypoints.size() == 0) {
      out << "waypoints: []\n";
    } else {
      out << "waypoints:\n";
      for (auto item : msg.waypoints) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: scan_region
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.scan_region.size() == 0) {
      out << "scan_region: []\n";
    } else {
      out << "scan_region:\n";
      for (auto item : msg.scan_region) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: object_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_height: ";
    rosidl_generator_traits::value_to_yaml(msg.object_height, out);
    out << "\n";
  }

  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ScanPlan & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace vision_ai_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use vision_ai_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vision_ai_interfaces::msg::ScanPlan & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::msg::ScanPlan & msg)
{
  return vision_ai_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::msg::ScanPlan>()
{
  return "vision_ai_interfaces::msg::ScanPlan";
}

template<>
inline const char * name<vision_ai_interfaces::msg::ScanPlan>()
{
  return "vision_ai_interfaces/msg/ScanPlan";
}

template<>
struct has_fixed_size<vision_ai_interfaces::msg::ScanPlan>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::msg::ScanPlan>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::msg::ScanPlan>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__TRAITS_HPP_

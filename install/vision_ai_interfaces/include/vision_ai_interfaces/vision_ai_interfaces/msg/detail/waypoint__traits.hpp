// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__TRAITS_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/msg/detail/waypoint__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'coverage_rect'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace vision_ai_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Waypoint & msg,
  std::ostream & out)
{
  out << "{";
  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: waypoint_index
  {
    out << "waypoint_index: ";
    rosidl_generator_traits::value_to_yaml(msg.waypoint_index, out);
    out << ", ";
  }

  // member: coverage_rect
  {
    if (msg.coverage_rect.size() == 0) {
      out << "coverage_rect: []";
    } else {
      out << "coverage_rect: [";
      size_t pending_items = msg.coverage_rect.size();
      for (auto item : msg.coverage_rect) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Waypoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: waypoint_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "waypoint_index: ";
    rosidl_generator_traits::value_to_yaml(msg.waypoint_index, out);
    out << "\n";
  }

  // member: coverage_rect
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.coverage_rect.size() == 0) {
      out << "coverage_rect: []\n";
    } else {
      out << "coverage_rect:\n";
      for (auto item : msg.coverage_rect) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Waypoint & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::msg::Waypoint & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::msg::Waypoint & msg)
{
  return vision_ai_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::msg::Waypoint>()
{
  return "vision_ai_interfaces::msg::Waypoint";
}

template<>
inline const char * name<vision_ai_interfaces::msg::Waypoint>()
{
  return "vision_ai_interfaces/msg/Waypoint";
}

template<>
struct has_fixed_size<vision_ai_interfaces::msg::Waypoint>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::msg::Waypoint>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::msg::Waypoint>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__WAYPOINT__TRAITS_HPP_

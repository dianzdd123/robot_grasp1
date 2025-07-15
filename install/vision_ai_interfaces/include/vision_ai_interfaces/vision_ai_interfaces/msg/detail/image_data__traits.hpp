// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:msg/ImageData.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__TRAITS_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/msg/detail/image_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"
// Member 'waypoint'
#include "vision_ai_interfaces/msg/detail/waypoint__traits.hpp"
// Member 'image'
#include "sensor_msgs/msg/detail/image__traits.hpp"

namespace vision_ai_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ImageData & msg,
  std::ostream & out)
{
  out << "{";
  // member: filename
  {
    out << "filename: ";
    rosidl_generator_traits::value_to_yaml(msg.filename, out);
    out << ", ";
  }

  // member: timestamp
  {
    out << "timestamp: ";
    to_flow_style_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: waypoint
  {
    out << "waypoint: ";
    to_flow_style_yaml(msg.waypoint, out);
    out << ", ";
  }

  // member: image
  {
    out << "image: ";
    to_flow_style_yaml(msg.image, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ImageData & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: filename
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "filename: ";
    rosidl_generator_traits::value_to_yaml(msg.filename, out);
    out << "\n";
  }

  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp:\n";
    to_block_style_yaml(msg.timestamp, out, indentation + 2);
  }

  // member: waypoint
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "waypoint:\n";
    to_block_style_yaml(msg.waypoint, out, indentation + 2);
  }

  // member: image
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image:\n";
    to_block_style_yaml(msg.image, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ImageData & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::msg::ImageData & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::msg::ImageData & msg)
{
  return vision_ai_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::msg::ImageData>()
{
  return "vision_ai_interfaces::msg::ImageData";
}

template<>
inline const char * name<vision_ai_interfaces::msg::ImageData>()
{
  return "vision_ai_interfaces/msg/ImageData";
}

template<>
struct has_fixed_size<vision_ai_interfaces::msg::ImageData>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::msg::ImageData>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::msg::ImageData>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__TRAITS_HPP_

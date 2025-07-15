// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__TRAITS_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/msg/detail/stitch_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vision_ai_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const StitchResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: method
  {
    out << "method: ";
    rosidl_generator_traits::value_to_yaml(msg.method, out);
    out << ", ";
  }

  // member: output_path
  {
    out << "output_path: ";
    rosidl_generator_traits::value_to_yaml(msg.output_path, out);
    out << ", ";
  }

  // member: input_images
  {
    out << "input_images: ";
    rosidl_generator_traits::value_to_yaml(msg.input_images, out);
    out << ", ";
  }

  // member: processing_time
  {
    out << "processing_time: ";
    rosidl_generator_traits::value_to_yaml(msg.processing_time, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StitchResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: method
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "method: ";
    rosidl_generator_traits::value_to_yaml(msg.method, out);
    out << "\n";
  }

  // member: output_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "output_path: ";
    rosidl_generator_traits::value_to_yaml(msg.output_path, out);
    out << "\n";
  }

  // member: input_images
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input_images: ";
    rosidl_generator_traits::value_to_yaml(msg.input_images, out);
    out << "\n";
  }

  // member: processing_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "processing_time: ";
    rosidl_generator_traits::value_to_yaml(msg.processing_time, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StitchResult & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::msg::StitchResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::msg::StitchResult & msg)
{
  return vision_ai_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::msg::StitchResult>()
{
  return "vision_ai_interfaces::msg::StitchResult";
}

template<>
inline const char * name<vision_ai_interfaces::msg::StitchResult>()
{
  return "vision_ai_interfaces/msg/StitchResult";
}

template<>
struct has_fixed_size<vision_ai_interfaces::msg::StitchResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::msg::StitchResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::msg::StitchResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__TRAITS_HPP_

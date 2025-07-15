// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vision_ai_interfaces/msg/detail/detected_object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vision_ai_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const DetectedObject & msg,
  std::ostream & out)
{
  out << "{";
  // member: object_id
  {
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << ", ";
  }

  // member: class_id
  {
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << ", ";
  }

  // member: class_name
  {
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: description
  {
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << ", ";
  }

  // member: bounding_box
  {
    if (msg.bounding_box.size() == 0) {
      out << "bounding_box: []";
    } else {
      out << "bounding_box: [";
      size_t pending_items = msg.bounding_box.size();
      for (auto item : msg.bounding_box) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: center_x
  {
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << ", ";
  }

  // member: center_y
  {
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << ", ";
  }

  // member: world_x
  {
    out << "world_x: ";
    rosidl_generator_traits::value_to_yaml(msg.world_x, out);
    out << ", ";
  }

  // member: world_y
  {
    out << "world_y: ";
    rosidl_generator_traits::value_to_yaml(msg.world_y, out);
    out << ", ";
  }

  // member: world_z
  {
    out << "world_z: ";
    rosidl_generator_traits::value_to_yaml(msg.world_z, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DetectedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: object_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_id: ";
    rosidl_generator_traits::value_to_yaml(msg.object_id, out);
    out << "\n";
  }

  // member: class_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_id: ";
    rosidl_generator_traits::value_to_yaml(msg.class_id, out);
    out << "\n";
  }

  // member: class_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: description
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << "\n";
  }

  // member: bounding_box
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.bounding_box.size() == 0) {
      out << "bounding_box: []\n";
    } else {
      out << "bounding_box:\n";
      for (auto item : msg.bounding_box) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: center_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << "\n";
  }

  // member: center_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << "\n";
  }

  // member: world_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "world_x: ";
    rosidl_generator_traits::value_to_yaml(msg.world_x, out);
    out << "\n";
  }

  // member: world_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "world_y: ";
    rosidl_generator_traits::value_to_yaml(msg.world_y, out);
    out << "\n";
  }

  // member: world_z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "world_z: ";
    rosidl_generator_traits::value_to_yaml(msg.world_z, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DetectedObject & msg, bool use_flow_style = false)
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
  const vision_ai_interfaces::msg::DetectedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  vision_ai_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vision_ai_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const vision_ai_interfaces::msg::DetectedObject & msg)
{
  return vision_ai_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vision_ai_interfaces::msg::DetectedObject>()
{
  return "vision_ai_interfaces::msg::DetectedObject";
}

template<>
inline const char * name<vision_ai_interfaces::msg::DetectedObject>()
{
  return "vision_ai_interfaces/msg/DetectedObject";
}

template<>
struct has_fixed_size<vision_ai_interfaces::msg::DetectedObject>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<vision_ai_interfaces::msg::DetectedObject>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<vision_ai_interfaces::msg::DetectedObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_

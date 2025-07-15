// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:msg/ImageData.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'timestamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"
// Member 'waypoint'
#include "vision_ai_interfaces/msg/detail/waypoint__struct.hpp"
// Member 'image'
#include "sensor_msgs/msg/detail/image__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__msg__ImageData __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__msg__ImageData __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ImageData_
{
  using Type = ImageData_<ContainerAllocator>;

  explicit ImageData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : timestamp(_init),
    waypoint(_init),
    image(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->filename = "";
    }
  }

  explicit ImageData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : filename(_alloc),
    timestamp(_alloc, _init),
    waypoint(_alloc, _init),
    image(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->filename = "";
    }
  }

  // field types and members
  using _filename_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _filename_type filename;
  using _timestamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _timestamp_type timestamp;
  using _waypoint_type =
    vision_ai_interfaces::msg::Waypoint_<ContainerAllocator>;
  _waypoint_type waypoint;
  using _image_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _image_type image;

  // setters for named parameter idiom
  Type & set__filename(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->filename = _arg;
    return *this;
  }
  Type & set__timestamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__waypoint(
    const vision_ai_interfaces::msg::Waypoint_<ContainerAllocator> & _arg)
  {
    this->waypoint = _arg;
    return *this;
  }
  Type & set__image(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->image = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::msg::ImageData_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::msg::ImageData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__msg__ImageData
    std::shared_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__msg__ImageData
    std::shared_ptr<vision_ai_interfaces::msg::ImageData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ImageData_ & other) const
  {
    if (this->filename != other.filename) {
      return false;
    }
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->waypoint != other.waypoint) {
      return false;
    }
    if (this->image != other.image) {
      return false;
    }
    return true;
  }
  bool operator!=(const ImageData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ImageData_

// alias to use template instance with default allocator
using ImageData =
  vision_ai_interfaces::msg::ImageData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__IMAGE_DATA__STRUCT_HPP_

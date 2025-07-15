// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'objects'
#include "vision_ai_interfaces/msg/detail/detected_object__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__msg__DetectionResult __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__msg__DetectionResult __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DetectionResult_
{
  using Type = DetectionResult_<ContainerAllocator>;

  explicit DetectionResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->detection_count = 0l;
      this->processing_time = 0.0f;
      this->output_directory = "";
    }
  }

  explicit DetectionResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    output_directory(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->detection_count = 0l;
      this->processing_time = 0.0f;
      this->output_directory = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _detection_count_type =
    int32_t;
  _detection_count_type detection_count;
  using _processing_time_type =
    float;
  _processing_time_type processing_time;
  using _output_directory_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _output_directory_type output_directory;
  using _objects_type =
    std::vector<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>>;
  _objects_type objects;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__detection_count(
    const int32_t & _arg)
  {
    this->detection_count = _arg;
    return *this;
  }
  Type & set__processing_time(
    const float & _arg)
  {
    this->processing_time = _arg;
    return *this;
  }
  Type & set__output_directory(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->output_directory = _arg;
    return *this;
  }
  Type & set__objects(
    const std::vector<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>> & _arg)
  {
    this->objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__msg__DetectionResult
    std::shared_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__msg__DetectionResult
    std::shared_ptr<vision_ai_interfaces::msg::DetectionResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectionResult_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->detection_count != other.detection_count) {
      return false;
    }
    if (this->processing_time != other.processing_time) {
      return false;
    }
    if (this->output_directory != other.output_directory) {
      return false;
    }
    if (this->objects != other.objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectionResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectionResult_

// alias to use template instance with default allocator
using DetectionResult =
  vision_ai_interfaces::msg::DetectionResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTION_RESULT__STRUCT_HPP_

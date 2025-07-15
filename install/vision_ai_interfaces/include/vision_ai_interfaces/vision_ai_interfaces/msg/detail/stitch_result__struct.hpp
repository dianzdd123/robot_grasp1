// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__STRUCT_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__msg__StitchResult __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__msg__StitchResult __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct StitchResult_
{
  using Type = StitchResult_<ContainerAllocator>;

  explicit StitchResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->method = "";
      this->output_path = "";
      this->input_images = 0l;
      this->processing_time = 0.0;
    }
  }

  explicit StitchResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : method(_alloc),
    output_path(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->method = "";
      this->output_path = "";
      this->input_images = 0l;
      this->processing_time = 0.0;
    }
  }

  // field types and members
  using _method_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _method_type method;
  using _output_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _output_path_type output_path;
  using _input_images_type =
    int32_t;
  _input_images_type input_images;
  using _processing_time_type =
    double;
  _processing_time_type processing_time;

  // setters for named parameter idiom
  Type & set__method(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->method = _arg;
    return *this;
  }
  Type & set__output_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->output_path = _arg;
    return *this;
  }
  Type & set__input_images(
    const int32_t & _arg)
  {
    this->input_images = _arg;
    return *this;
  }
  Type & set__processing_time(
    const double & _arg)
  {
    this->processing_time = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__msg__StitchResult
    std::shared_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__msg__StitchResult
    std::shared_ptr<vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const StitchResult_ & other) const
  {
    if (this->method != other.method) {
      return false;
    }
    if (this->output_path != other.output_path) {
      return false;
    }
    if (this->input_images != other.input_images) {
      return false;
    }
    if (this->processing_time != other.processing_time) {
      return false;
    }
    return true;
  }
  bool operator!=(const StitchResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct StitchResult_

// alias to use template instance with default allocator
using StitchResult =
  vision_ai_interfaces::msg::StitchResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__STRUCT_HPP_

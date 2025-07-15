// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__msg__DetectedObject __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__msg__DetectedObject __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DetectedObject_
{
  using Type = DetectedObject_<ContainerAllocator>;

  explicit DetectedObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = "";
      this->class_id = 0l;
      this->class_name = "";
      this->confidence = 0.0f;
      this->description = "";
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->world_x = 0.0f;
      this->world_y = 0.0f;
      this->world_z = 0.0f;
    }
  }

  explicit DetectedObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : object_id(_alloc),
    class_name(_alloc),
    description(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->object_id = "";
      this->class_id = 0l;
      this->class_name = "";
      this->confidence = 0.0f;
      this->description = "";
      this->center_x = 0.0f;
      this->center_y = 0.0f;
      this->world_x = 0.0f;
      this->world_y = 0.0f;
      this->world_z = 0.0f;
    }
  }

  // field types and members
  using _object_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _object_id_type object_id;
  using _class_id_type =
    int32_t;
  _class_id_type class_id;
  using _class_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _class_name_type class_name;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _description_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _description_type description;
  using _bounding_box_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _bounding_box_type bounding_box;
  using _center_x_type =
    float;
  _center_x_type center_x;
  using _center_y_type =
    float;
  _center_y_type center_y;
  using _world_x_type =
    float;
  _world_x_type world_x;
  using _world_y_type =
    float;
  _world_y_type world_y;
  using _world_z_type =
    float;
  _world_z_type world_z;

  // setters for named parameter idiom
  Type & set__object_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->object_id = _arg;
    return *this;
  }
  Type & set__class_id(
    const int32_t & _arg)
  {
    this->class_id = _arg;
    return *this;
  }
  Type & set__class_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->class_name = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__description(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->description = _arg;
    return *this;
  }
  Type & set__bounding_box(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->bounding_box = _arg;
    return *this;
  }
  Type & set__center_x(
    const float & _arg)
  {
    this->center_x = _arg;
    return *this;
  }
  Type & set__center_y(
    const float & _arg)
  {
    this->center_y = _arg;
    return *this;
  }
  Type & set__world_x(
    const float & _arg)
  {
    this->world_x = _arg;
    return *this;
  }
  Type & set__world_y(
    const float & _arg)
  {
    this->world_y = _arg;
    return *this;
  }
  Type & set__world_z(
    const float & _arg)
  {
    this->world_z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__msg__DetectedObject
    std::shared_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__msg__DetectedObject
    std::shared_ptr<vision_ai_interfaces::msg::DetectedObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectedObject_ & other) const
  {
    if (this->object_id != other.object_id) {
      return false;
    }
    if (this->class_id != other.class_id) {
      return false;
    }
    if (this->class_name != other.class_name) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->description != other.description) {
      return false;
    }
    if (this->bounding_box != other.bounding_box) {
      return false;
    }
    if (this->center_x != other.center_x) {
      return false;
    }
    if (this->center_y != other.center_y) {
      return false;
    }
    if (this->world_x != other.world_x) {
      return false;
    }
    if (this->world_y != other.world_y) {
      return false;
    }
    if (this->world_z != other.world_z) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectedObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectedObject_

// alias to use template instance with default allocator
using DetectedObject =
  vision_ai_interfaces::msg::DetectedObject_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_

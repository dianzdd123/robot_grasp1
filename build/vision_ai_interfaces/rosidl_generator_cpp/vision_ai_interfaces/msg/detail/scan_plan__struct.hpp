// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_HPP_
#define VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'waypoints'
#include "vision_ai_interfaces/msg/detail/waypoint__struct.hpp"
// Member 'scan_region'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__msg__ScanPlan __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__msg__ScanPlan __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ScanPlan_
{
  using Type = ScanPlan_<ContainerAllocator>;

  explicit ScanPlan_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->strategy = "";
      this->scan_height = 0.0;
      this->required_height = 0.0;
      this->object_height = 0.0;
      this->mode = "";
    }
  }

  explicit ScanPlan_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : strategy(_alloc),
    mode(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->strategy = "";
      this->scan_height = 0.0;
      this->required_height = 0.0;
      this->object_height = 0.0;
      this->mode = "";
    }
  }

  // field types and members
  using _strategy_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _strategy_type strategy;
  using _scan_height_type =
    double;
  _scan_height_type scan_height;
  using _required_height_type =
    double;
  _required_height_type required_height;
  using _waypoints_type =
    std::vector<vision_ai_interfaces::msg::Waypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::Waypoint_<ContainerAllocator>>>;
  _waypoints_type waypoints;
  using _scan_region_type =
    std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>>;
  _scan_region_type scan_region;
  using _object_height_type =
    double;
  _object_height_type object_height;
  using _mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mode_type mode;

  // setters for named parameter idiom
  Type & set__strategy(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->strategy = _arg;
    return *this;
  }
  Type & set__scan_height(
    const double & _arg)
  {
    this->scan_height = _arg;
    return *this;
  }
  Type & set__required_height(
    const double & _arg)
  {
    this->required_height = _arg;
    return *this;
  }
  Type & set__waypoints(
    const std::vector<vision_ai_interfaces::msg::Waypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::Waypoint_<ContainerAllocator>>> & _arg)
  {
    this->waypoints = _arg;
    return *this;
  }
  Type & set__scan_region(
    const std::vector<geometry_msgs::msg::Point_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Point_<ContainerAllocator>>> & _arg)
  {
    this->scan_region = _arg;
    return *this;
  }
  Type & set__object_height(
    const double & _arg)
  {
    this->object_height = _arg;
    return *this;
  }
  Type & set__mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__msg__ScanPlan
    std::shared_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__msg__ScanPlan
    std::shared_ptr<vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ScanPlan_ & other) const
  {
    if (this->strategy != other.strategy) {
      return false;
    }
    if (this->scan_height != other.scan_height) {
      return false;
    }
    if (this->required_height != other.required_height) {
      return false;
    }
    if (this->waypoints != other.waypoints) {
      return false;
    }
    if (this->scan_region != other.scan_region) {
      return false;
    }
    if (this->object_height != other.object_height) {
      return false;
    }
    if (this->mode != other.mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const ScanPlan_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ScanPlan_

// alias to use template instance with default allocator
using ScanPlan =
  vision_ai_interfaces::msg::ScanPlan_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__STRUCT_HPP_

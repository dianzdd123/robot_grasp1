// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:srv/ExecuteScan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Request __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Request __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteScan_Request_
{
  using Type = ExecuteScan_Request_<ContainerAllocator>;

  explicit ExecuteScan_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : scan_plan(_init)
  {
    (void)_init;
  }

  explicit ExecuteScan_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : scan_plan(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _scan_plan_type =
    vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>;
  _scan_plan_type scan_plan;

  // setters for named parameter idiom
  Type & set__scan_plan(
    const vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> & _arg)
  {
    this->scan_plan = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Request
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Request
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteScan_Request_ & other) const
  {
    if (this->scan_plan != other.scan_plan) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteScan_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteScan_Request_

// alias to use template instance with default allocator
using ExecuteScan_Request =
  vision_ai_interfaces::srv::ExecuteScan_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vision_ai_interfaces


#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Response __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Response __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ExecuteScan_Response_
{
  using Type = ExecuteScan_Response_<ContainerAllocator>;

  explicit ExecuteScan_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->output_directory = "";
    }
  }

  explicit ExecuteScan_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    output_directory(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->output_directory = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _output_directory_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _output_directory_type output_directory;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__output_directory(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->output_directory = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Response
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__srv__ExecuteScan_Response
    std::shared_ptr<vision_ai_interfaces::srv::ExecuteScan_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteScan_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->output_directory != other.output_directory) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteScan_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteScan_Response_

// alias to use template instance with default allocator
using ExecuteScan_Response =
  vision_ai_interfaces::srv::ExecuteScan_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace vision_ai_interfaces
{

namespace srv
{

struct ExecuteScan
{
  using Request = vision_ai_interfaces::srv::ExecuteScan_Request;
  using Response = vision_ai_interfaces::srv::ExecuteScan_Response;
};

}  // namespace srv

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__EXECUTE_SCAN__STRUCT_HPP_

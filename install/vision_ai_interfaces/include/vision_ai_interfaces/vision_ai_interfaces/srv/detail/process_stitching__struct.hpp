// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vision_ai_interfaces:srv/ProcessStitching.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_HPP_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'image_data'
#include "vision_ai_interfaces/msg/detail/image_data__struct.hpp"
// Member 'scan_plan'
#include "vision_ai_interfaces/msg/detail/scan_plan__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Request __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Request __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ProcessStitching_Request_
{
  using Type = ProcessStitching_Request_<ContainerAllocator>;

  explicit ProcessStitching_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : scan_plan(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->output_directory = "";
    }
  }

  explicit ProcessStitching_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : scan_plan(_alloc, _init),
    output_directory(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->output_directory = "";
    }
  }

  // field types and members
  using _image_data_type =
    std::vector<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>>;
  _image_data_type image_data;
  using _scan_plan_type =
    vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator>;
  _scan_plan_type scan_plan;
  using _output_directory_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _output_directory_type output_directory;

  // setters for named parameter idiom
  Type & set__image_data(
    const std::vector<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<vision_ai_interfaces::msg::ImageData_<ContainerAllocator>>> & _arg)
  {
    this->image_data = _arg;
    return *this;
  }
  Type & set__scan_plan(
    const vision_ai_interfaces::msg::ScanPlan_<ContainerAllocator> & _arg)
  {
    this->scan_plan = _arg;
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
    vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Request
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Request
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ProcessStitching_Request_ & other) const
  {
    if (this->image_data != other.image_data) {
      return false;
    }
    if (this->scan_plan != other.scan_plan) {
      return false;
    }
    if (this->output_directory != other.output_directory) {
      return false;
    }
    return true;
  }
  bool operator!=(const ProcessStitching_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ProcessStitching_Request_

// alias to use template instance with default allocator
using ProcessStitching_Request =
  vision_ai_interfaces::srv::ProcessStitching_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vision_ai_interfaces


// Include directives for member types
// Member 'result'
#include "vision_ai_interfaces/msg/detail/stitch_result__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Response __attribute__((deprecated))
#else
# define DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Response __declspec(deprecated)
#endif

namespace vision_ai_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ProcessStitching_Response_
{
  using Type = ProcessStitching_Response_<ContainerAllocator>;

  explicit ProcessStitching_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit ProcessStitching_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _result_type =
    vision_ai_interfaces::msg::StitchResult_<ContainerAllocator>;
  _result_type result;

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
  Type & set__result(
    const vision_ai_interfaces::msg::StitchResult_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Response
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vision_ai_interfaces__srv__ProcessStitching_Response
    std::shared_ptr<vision_ai_interfaces::srv::ProcessStitching_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ProcessStitching_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ProcessStitching_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ProcessStitching_Response_

// alias to use template instance with default allocator
using ProcessStitching_Response =
  vision_ai_interfaces::srv::ProcessStitching_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace vision_ai_interfaces
{

namespace srv
{

struct ProcessStitching
{
  using Request = vision_ai_interfaces::srv::ProcessStitching_Request;
  using Response = vision_ai_interfaces::srv::ProcessStitching_Response;
};

}  // namespace srv

}  // namespace vision_ai_interfaces

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__STRUCT_HPP_

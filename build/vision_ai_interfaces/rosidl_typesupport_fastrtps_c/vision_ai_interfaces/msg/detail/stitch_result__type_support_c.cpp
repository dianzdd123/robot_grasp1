// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/stitch_result__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "vision_ai_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "vision_ai_interfaces/msg/detail/stitch_result__struct.h"
#include "vision_ai_interfaces/msg/detail/stitch_result__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // method, output_path
#include "rosidl_runtime_c/string_functions.h"  // method, output_path

// forward declare type support functions


using _StitchResult__ros_msg_type = vision_ai_interfaces__msg__StitchResult;

static bool _StitchResult__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _StitchResult__ros_msg_type * ros_message = static_cast<const _StitchResult__ros_msg_type *>(untyped_ros_message);
  // Field name: method
  {
    const rosidl_runtime_c__String * str = &ros_message->method;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: output_path
  {
    const rosidl_runtime_c__String * str = &ros_message->output_path;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: input_images
  {
    cdr << ros_message->input_images;
  }

  // Field name: processing_time
  {
    cdr << ros_message->processing_time;
  }

  return true;
}

static bool _StitchResult__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _StitchResult__ros_msg_type * ros_message = static_cast<_StitchResult__ros_msg_type *>(untyped_ros_message);
  // Field name: method
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->method.data) {
      rosidl_runtime_c__String__init(&ros_message->method);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->method,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'method'\n");
      return false;
    }
  }

  // Field name: output_path
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->output_path.data) {
      rosidl_runtime_c__String__init(&ros_message->output_path);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->output_path,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'output_path'\n");
      return false;
    }
  }

  // Field name: input_images
  {
    cdr >> ros_message->input_images;
  }

  // Field name: processing_time
  {
    cdr >> ros_message->processing_time;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_vision_ai_interfaces
size_t get_serialized_size_vision_ai_interfaces__msg__StitchResult(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _StitchResult__ros_msg_type * ros_message = static_cast<const _StitchResult__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name method
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->method.size + 1);
  // field.name output_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->output_path.size + 1);
  // field.name input_images
  {
    size_t item_size = sizeof(ros_message->input_images);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name processing_time
  {
    size_t item_size = sizeof(ros_message->processing_time);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _StitchResult__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_vision_ai_interfaces__msg__StitchResult(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_vision_ai_interfaces
size_t max_serialized_size_vision_ai_interfaces__msg__StitchResult(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: method
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: output_path
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: input_images
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: processing_time
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = vision_ai_interfaces__msg__StitchResult;
    is_plain =
      (
      offsetof(DataType, processing_time) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _StitchResult__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_vision_ai_interfaces__msg__StitchResult(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_StitchResult = {
  "vision_ai_interfaces::msg",
  "StitchResult",
  _StitchResult__cdr_serialize,
  _StitchResult__cdr_deserialize,
  _StitchResult__get_serialized_size,
  _StitchResult__max_serialized_size
};

static rosidl_message_type_support_t _StitchResult__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_StitchResult,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, vision_ai_interfaces, msg, StitchResult)() {
  return &_StitchResult__type_support;
}

#if defined(__cplusplus)
}
#endif

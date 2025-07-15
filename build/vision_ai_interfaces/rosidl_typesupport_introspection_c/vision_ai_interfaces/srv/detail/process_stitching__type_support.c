// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from vision_ai_interfaces:srv/ProcessStitching.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "vision_ai_interfaces/srv/detail/process_stitching__rosidl_typesupport_introspection_c.h"
#include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "vision_ai_interfaces/srv/detail/process_stitching__functions.h"
#include "vision_ai_interfaces/srv/detail/process_stitching__struct.h"


// Include directives for member types
// Member `image_data`
#include "vision_ai_interfaces/msg/image_data.h"
// Member `image_data`
#include "vision_ai_interfaces/msg/detail/image_data__rosidl_typesupport_introspection_c.h"
// Member `scan_plan`
#include "vision_ai_interfaces/msg/scan_plan.h"
// Member `scan_plan`
#include "vision_ai_interfaces/msg/detail/scan_plan__rosidl_typesupport_introspection_c.h"
// Member `output_directory`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vision_ai_interfaces__srv__ProcessStitching_Request__init(message_memory);
}

void vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_fini_function(void * message_memory)
{
  vision_ai_interfaces__srv__ProcessStitching_Request__fini(message_memory);
}

size_t vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__size_function__ProcessStitching_Request__image_data(
  const void * untyped_member)
{
  const vision_ai_interfaces__msg__ImageData__Sequence * member =
    (const vision_ai_interfaces__msg__ImageData__Sequence *)(untyped_member);
  return member->size;
}

const void * vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_const_function__ProcessStitching_Request__image_data(
  const void * untyped_member, size_t index)
{
  const vision_ai_interfaces__msg__ImageData__Sequence * member =
    (const vision_ai_interfaces__msg__ImageData__Sequence *)(untyped_member);
  return &member->data[index];
}

void * vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_function__ProcessStitching_Request__image_data(
  void * untyped_member, size_t index)
{
  vision_ai_interfaces__msg__ImageData__Sequence * member =
    (vision_ai_interfaces__msg__ImageData__Sequence *)(untyped_member);
  return &member->data[index];
}

void vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__fetch_function__ProcessStitching_Request__image_data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const vision_ai_interfaces__msg__ImageData * item =
    ((const vision_ai_interfaces__msg__ImageData *)
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_const_function__ProcessStitching_Request__image_data(untyped_member, index));
  vision_ai_interfaces__msg__ImageData * value =
    (vision_ai_interfaces__msg__ImageData *)(untyped_value);
  *value = *item;
}

void vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__assign_function__ProcessStitching_Request__image_data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  vision_ai_interfaces__msg__ImageData * item =
    ((vision_ai_interfaces__msg__ImageData *)
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_function__ProcessStitching_Request__image_data(untyped_member, index));
  const vision_ai_interfaces__msg__ImageData * value =
    (const vision_ai_interfaces__msg__ImageData *)(untyped_value);
  *item = *value;
}

bool vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__resize_function__ProcessStitching_Request__image_data(
  void * untyped_member, size_t size)
{
  vision_ai_interfaces__msg__ImageData__Sequence * member =
    (vision_ai_interfaces__msg__ImageData__Sequence *)(untyped_member);
  vision_ai_interfaces__msg__ImageData__Sequence__fini(member);
  return vision_ai_interfaces__msg__ImageData__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_member_array[3] = {
  {
    "image_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Request, image_data),  // bytes offset in struct
    NULL,  // default value
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__size_function__ProcessStitching_Request__image_data,  // size() function pointer
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_const_function__ProcessStitching_Request__image_data,  // get_const(index) function pointer
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__get_function__ProcessStitching_Request__image_data,  // get(index) function pointer
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__fetch_function__ProcessStitching_Request__image_data,  // fetch(index, &value) function pointer
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__assign_function__ProcessStitching_Request__image_data,  // assign(index, value) function pointer
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__resize_function__ProcessStitching_Request__image_data  // resize(index) function pointer
  },
  {
    "scan_plan",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Request, scan_plan),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "output_directory",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Request, output_directory),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_members = {
  "vision_ai_interfaces__srv",  // message namespace
  "ProcessStitching_Request",  // message name
  3,  // number of fields
  sizeof(vision_ai_interfaces__srv__ProcessStitching_Request),
  vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_member_array,  // message members
  vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_type_support_handle = {
  0,
  &vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Request)() {
  vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, ImageData)();
  vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, ScanPlan)();
  if (!vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vision_ai_interfaces__srv__ProcessStitching_Request__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "vision_ai_interfaces/srv/detail/process_stitching__rosidl_typesupport_introspection_c.h"
// already included above
// #include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "vision_ai_interfaces/srv/detail/process_stitching__functions.h"
// already included above
// #include "vision_ai_interfaces/srv/detail/process_stitching__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `result`
#include "vision_ai_interfaces/msg/stitch_result.h"
// Member `result`
#include "vision_ai_interfaces/msg/detail/stitch_result__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  vision_ai_interfaces__srv__ProcessStitching_Response__init(message_memory);
}

void vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_fini_function(void * message_memory)
{
  vision_ai_interfaces__srv__ProcessStitching_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_member_array[3] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(vision_ai_interfaces__srv__ProcessStitching_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_members = {
  "vision_ai_interfaces__srv",  // message namespace
  "ProcessStitching_Response",  // message name
  3,  // number of fields
  sizeof(vision_ai_interfaces__srv__ProcessStitching_Response),
  vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_member_array,  // message members
  vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_type_support_handle = {
  0,
  &vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Response)() {
  vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, msg, StitchResult)();
  if (!vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &vision_ai_interfaces__srv__ProcessStitching_Response__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "vision_ai_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "vision_ai_interfaces/srv/detail/process_stitching__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_members = {
  "vision_ai_interfaces__srv",  // service namespace
  "ProcessStitching",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_Request_message_type_support_handle,
  NULL  // response message
  // vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_Response_message_type_support_handle
};

static rosidl_service_type_support_t vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_type_support_handle = {
  0,
  &vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_vision_ai_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching)() {
  if (!vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_type_support_handle.typesupport_identifier) {
    vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, vision_ai_interfaces, srv, ProcessStitching_Response)()->data;
  }

  return &vision_ai_interfaces__srv__detail__process_stitching__rosidl_typesupport_introspection_c__ProcessStitching_service_type_support_handle;
}

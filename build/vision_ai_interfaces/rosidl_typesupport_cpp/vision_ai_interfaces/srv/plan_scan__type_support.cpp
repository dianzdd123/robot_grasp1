// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from vision_ai_interfaces:srv/PlanScan.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "vision_ai_interfaces/srv/detail/plan_scan__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace vision_ai_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _PlanScan_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _PlanScan_Request_type_support_ids_t;

static const _PlanScan_Request_type_support_ids_t _PlanScan_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _PlanScan_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _PlanScan_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _PlanScan_Request_type_support_symbol_names_t _PlanScan_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, vision_ai_interfaces, srv, PlanScan_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vision_ai_interfaces, srv, PlanScan_Request)),
  }
};

typedef struct _PlanScan_Request_type_support_data_t
{
  void * data[2];
} _PlanScan_Request_type_support_data_t;

static _PlanScan_Request_type_support_data_t _PlanScan_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _PlanScan_Request_message_typesupport_map = {
  2,
  "vision_ai_interfaces",
  &_PlanScan_Request_message_typesupport_ids.typesupport_identifier[0],
  &_PlanScan_Request_message_typesupport_symbol_names.symbol_name[0],
  &_PlanScan_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t PlanScan_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_PlanScan_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<vision_ai_interfaces::srv::PlanScan_Request>()
{
  return &::vision_ai_interfaces::srv::rosidl_typesupport_cpp::PlanScan_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, vision_ai_interfaces, srv, PlanScan_Request)() {
  return get_message_type_support_handle<vision_ai_interfaces::srv::PlanScan_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "vision_ai_interfaces/srv/detail/plan_scan__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace vision_ai_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _PlanScan_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _PlanScan_Response_type_support_ids_t;

static const _PlanScan_Response_type_support_ids_t _PlanScan_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _PlanScan_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _PlanScan_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _PlanScan_Response_type_support_symbol_names_t _PlanScan_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, vision_ai_interfaces, srv, PlanScan_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vision_ai_interfaces, srv, PlanScan_Response)),
  }
};

typedef struct _PlanScan_Response_type_support_data_t
{
  void * data[2];
} _PlanScan_Response_type_support_data_t;

static _PlanScan_Response_type_support_data_t _PlanScan_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _PlanScan_Response_message_typesupport_map = {
  2,
  "vision_ai_interfaces",
  &_PlanScan_Response_message_typesupport_ids.typesupport_identifier[0],
  &_PlanScan_Response_message_typesupport_symbol_names.symbol_name[0],
  &_PlanScan_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t PlanScan_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_PlanScan_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<vision_ai_interfaces::srv::PlanScan_Response>()
{
  return &::vision_ai_interfaces::srv::rosidl_typesupport_cpp::PlanScan_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, vision_ai_interfaces, srv, PlanScan_Response)() {
  return get_message_type_support_handle<vision_ai_interfaces::srv::PlanScan_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "vision_ai_interfaces/srv/detail/plan_scan__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace vision_ai_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _PlanScan_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _PlanScan_type_support_ids_t;

static const _PlanScan_type_support_ids_t _PlanScan_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _PlanScan_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _PlanScan_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _PlanScan_type_support_symbol_names_t _PlanScan_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, vision_ai_interfaces, srv, PlanScan)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, vision_ai_interfaces, srv, PlanScan)),
  }
};

typedef struct _PlanScan_type_support_data_t
{
  void * data[2];
} _PlanScan_type_support_data_t;

static _PlanScan_type_support_data_t _PlanScan_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _PlanScan_service_typesupport_map = {
  2,
  "vision_ai_interfaces",
  &_PlanScan_service_typesupport_ids.typesupport_identifier[0],
  &_PlanScan_service_typesupport_symbol_names.symbol_name[0],
  &_PlanScan_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t PlanScan_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_PlanScan_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace vision_ai_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<vision_ai_interfaces::srv::PlanScan>()
{
  return &::vision_ai_interfaces::srv::rosidl_typesupport_cpp::PlanScan_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, vision_ai_interfaces, srv, PlanScan)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<vision_ai_interfaces::srv::PlanScan>();
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:srv/PlanScan.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/srv/detail/plan_scan__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `mode`
#include "rosidl_runtime_c/string_functions.h"
// Member `points`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
vision_ai_interfaces__srv__PlanScan_Request__init(vision_ai_interfaces__srv__PlanScan_Request * msg)
{
  if (!msg) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__init(&msg->mode)) {
    vision_ai_interfaces__srv__PlanScan_Request__fini(msg);
    return false;
  }
  // object_height
  // points
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->points, 0)) {
    vision_ai_interfaces__srv__PlanScan_Request__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__srv__PlanScan_Request__fini(vision_ai_interfaces__srv__PlanScan_Request * msg)
{
  if (!msg) {
    return;
  }
  // mode
  rosidl_runtime_c__String__fini(&msg->mode);
  // object_height
  // points
  geometry_msgs__msg__Point__Sequence__fini(&msg->points);
}

bool
vision_ai_interfaces__srv__PlanScan_Request__are_equal(const vision_ai_interfaces__srv__PlanScan_Request * lhs, const vision_ai_interfaces__srv__PlanScan_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  // object_height
  if (lhs->object_height != rhs->object_height) {
    return false;
  }
  // points
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->points), &(rhs->points)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__srv__PlanScan_Request__copy(
  const vision_ai_interfaces__srv__PlanScan_Request * input,
  vision_ai_interfaces__srv__PlanScan_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  // object_height
  output->object_height = input->object_height;
  // points
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->points), &(output->points)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__srv__PlanScan_Request *
vision_ai_interfaces__srv__PlanScan_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Request * msg = (vision_ai_interfaces__srv__PlanScan_Request *)allocator.allocate(sizeof(vision_ai_interfaces__srv__PlanScan_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__srv__PlanScan_Request));
  bool success = vision_ai_interfaces__srv__PlanScan_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__srv__PlanScan_Request__destroy(vision_ai_interfaces__srv__PlanScan_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__srv__PlanScan_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__srv__PlanScan_Request__Sequence__init(vision_ai_interfaces__srv__PlanScan_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Request * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__srv__PlanScan_Request *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__srv__PlanScan_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__srv__PlanScan_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__srv__PlanScan_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vision_ai_interfaces__srv__PlanScan_Request__Sequence__fini(vision_ai_interfaces__srv__PlanScan_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vision_ai_interfaces__srv__PlanScan_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vision_ai_interfaces__srv__PlanScan_Request__Sequence *
vision_ai_interfaces__srv__PlanScan_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Request__Sequence * array = (vision_ai_interfaces__srv__PlanScan_Request__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__srv__PlanScan_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__srv__PlanScan_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__srv__PlanScan_Request__Sequence__destroy(vision_ai_interfaces__srv__PlanScan_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__srv__PlanScan_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__srv__PlanScan_Request__Sequence__are_equal(const vision_ai_interfaces__srv__PlanScan_Request__Sequence * lhs, const vision_ai_interfaces__srv__PlanScan_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__srv__PlanScan_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__srv__PlanScan_Request__Sequence__copy(
  const vision_ai_interfaces__srv__PlanScan_Request__Sequence * input,
  vision_ai_interfaces__srv__PlanScan_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__srv__PlanScan_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__srv__PlanScan_Request * data =
      (vision_ai_interfaces__srv__PlanScan_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__srv__PlanScan_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__srv__PlanScan_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__srv__PlanScan_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `scan_plan`
#include "vision_ai_interfaces/msg/detail/scan_plan__functions.h"

bool
vision_ai_interfaces__srv__PlanScan_Response__init(vision_ai_interfaces__srv__PlanScan_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    vision_ai_interfaces__srv__PlanScan_Response__fini(msg);
    return false;
  }
  // scan_plan
  if (!vision_ai_interfaces__msg__ScanPlan__init(&msg->scan_plan)) {
    vision_ai_interfaces__srv__PlanScan_Response__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__srv__PlanScan_Response__fini(vision_ai_interfaces__srv__PlanScan_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // scan_plan
  vision_ai_interfaces__msg__ScanPlan__fini(&msg->scan_plan);
}

bool
vision_ai_interfaces__srv__PlanScan_Response__are_equal(const vision_ai_interfaces__srv__PlanScan_Response * lhs, const vision_ai_interfaces__srv__PlanScan_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  // scan_plan
  if (!vision_ai_interfaces__msg__ScanPlan__are_equal(
      &(lhs->scan_plan), &(rhs->scan_plan)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__srv__PlanScan_Response__copy(
  const vision_ai_interfaces__srv__PlanScan_Response * input,
  vision_ai_interfaces__srv__PlanScan_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  // scan_plan
  if (!vision_ai_interfaces__msg__ScanPlan__copy(
      &(input->scan_plan), &(output->scan_plan)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__srv__PlanScan_Response *
vision_ai_interfaces__srv__PlanScan_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Response * msg = (vision_ai_interfaces__srv__PlanScan_Response *)allocator.allocate(sizeof(vision_ai_interfaces__srv__PlanScan_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__srv__PlanScan_Response));
  bool success = vision_ai_interfaces__srv__PlanScan_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__srv__PlanScan_Response__destroy(vision_ai_interfaces__srv__PlanScan_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__srv__PlanScan_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__srv__PlanScan_Response__Sequence__init(vision_ai_interfaces__srv__PlanScan_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Response * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__srv__PlanScan_Response *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__srv__PlanScan_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__srv__PlanScan_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__srv__PlanScan_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vision_ai_interfaces__srv__PlanScan_Response__Sequence__fini(vision_ai_interfaces__srv__PlanScan_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vision_ai_interfaces__srv__PlanScan_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vision_ai_interfaces__srv__PlanScan_Response__Sequence *
vision_ai_interfaces__srv__PlanScan_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__PlanScan_Response__Sequence * array = (vision_ai_interfaces__srv__PlanScan_Response__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__srv__PlanScan_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__srv__PlanScan_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__srv__PlanScan_Response__Sequence__destroy(vision_ai_interfaces__srv__PlanScan_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__srv__PlanScan_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__srv__PlanScan_Response__Sequence__are_equal(const vision_ai_interfaces__srv__PlanScan_Response__Sequence * lhs, const vision_ai_interfaces__srv__PlanScan_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__srv__PlanScan_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__srv__PlanScan_Response__Sequence__copy(
  const vision_ai_interfaces__srv__PlanScan_Response__Sequence * input,
  vision_ai_interfaces__srv__PlanScan_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__srv__PlanScan_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__srv__PlanScan_Response * data =
      (vision_ai_interfaces__srv__PlanScan_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__srv__PlanScan_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__srv__PlanScan_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__srv__PlanScan_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

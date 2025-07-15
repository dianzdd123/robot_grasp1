// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/scan_plan__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `strategy`
// Member `mode`
#include "rosidl_runtime_c/string_functions.h"
// Member `waypoints`
#include "vision_ai_interfaces/msg/detail/waypoint__functions.h"
// Member `scan_region`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
vision_ai_interfaces__msg__ScanPlan__init(vision_ai_interfaces__msg__ScanPlan * msg)
{
  if (!msg) {
    return false;
  }
  // strategy
  if (!rosidl_runtime_c__String__init(&msg->strategy)) {
    vision_ai_interfaces__msg__ScanPlan__fini(msg);
    return false;
  }
  // scan_height
  // required_height
  // waypoints
  if (!vision_ai_interfaces__msg__Waypoint__Sequence__init(&msg->waypoints, 0)) {
    vision_ai_interfaces__msg__ScanPlan__fini(msg);
    return false;
  }
  // scan_region
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->scan_region, 0)) {
    vision_ai_interfaces__msg__ScanPlan__fini(msg);
    return false;
  }
  // object_height
  // mode
  if (!rosidl_runtime_c__String__init(&msg->mode)) {
    vision_ai_interfaces__msg__ScanPlan__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__msg__ScanPlan__fini(vision_ai_interfaces__msg__ScanPlan * msg)
{
  if (!msg) {
    return;
  }
  // strategy
  rosidl_runtime_c__String__fini(&msg->strategy);
  // scan_height
  // required_height
  // waypoints
  vision_ai_interfaces__msg__Waypoint__Sequence__fini(&msg->waypoints);
  // scan_region
  geometry_msgs__msg__Point__Sequence__fini(&msg->scan_region);
  // object_height
  // mode
  rosidl_runtime_c__String__fini(&msg->mode);
}

bool
vision_ai_interfaces__msg__ScanPlan__are_equal(const vision_ai_interfaces__msg__ScanPlan * lhs, const vision_ai_interfaces__msg__ScanPlan * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // strategy
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->strategy), &(rhs->strategy)))
  {
    return false;
  }
  // scan_height
  if (lhs->scan_height != rhs->scan_height) {
    return false;
  }
  // required_height
  if (lhs->required_height != rhs->required_height) {
    return false;
  }
  // waypoints
  if (!vision_ai_interfaces__msg__Waypoint__Sequence__are_equal(
      &(lhs->waypoints), &(rhs->waypoints)))
  {
    return false;
  }
  // scan_region
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->scan_region), &(rhs->scan_region)))
  {
    return false;
  }
  // object_height
  if (lhs->object_height != rhs->object_height) {
    return false;
  }
  // mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__ScanPlan__copy(
  const vision_ai_interfaces__msg__ScanPlan * input,
  vision_ai_interfaces__msg__ScanPlan * output)
{
  if (!input || !output) {
    return false;
  }
  // strategy
  if (!rosidl_runtime_c__String__copy(
      &(input->strategy), &(output->strategy)))
  {
    return false;
  }
  // scan_height
  output->scan_height = input->scan_height;
  // required_height
  output->required_height = input->required_height;
  // waypoints
  if (!vision_ai_interfaces__msg__Waypoint__Sequence__copy(
      &(input->waypoints), &(output->waypoints)))
  {
    return false;
  }
  // scan_region
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->scan_region), &(output->scan_region)))
  {
    return false;
  }
  // object_height
  output->object_height = input->object_height;
  // mode
  if (!rosidl_runtime_c__String__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__msg__ScanPlan *
vision_ai_interfaces__msg__ScanPlan__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ScanPlan * msg = (vision_ai_interfaces__msg__ScanPlan *)allocator.allocate(sizeof(vision_ai_interfaces__msg__ScanPlan), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__ScanPlan));
  bool success = vision_ai_interfaces__msg__ScanPlan__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__ScanPlan__destroy(vision_ai_interfaces__msg__ScanPlan * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__ScanPlan__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__ScanPlan__Sequence__init(vision_ai_interfaces__msg__ScanPlan__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ScanPlan * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__ScanPlan *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__ScanPlan), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__ScanPlan__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__ScanPlan__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__ScanPlan__Sequence__fini(vision_ai_interfaces__msg__ScanPlan__Sequence * array)
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
      vision_ai_interfaces__msg__ScanPlan__fini(&array->data[i]);
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

vision_ai_interfaces__msg__ScanPlan__Sequence *
vision_ai_interfaces__msg__ScanPlan__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ScanPlan__Sequence * array = (vision_ai_interfaces__msg__ScanPlan__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__ScanPlan__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__ScanPlan__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__ScanPlan__Sequence__destroy(vision_ai_interfaces__msg__ScanPlan__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__ScanPlan__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__ScanPlan__Sequence__are_equal(const vision_ai_interfaces__msg__ScanPlan__Sequence * lhs, const vision_ai_interfaces__msg__ScanPlan__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__ScanPlan__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__ScanPlan__Sequence__copy(
  const vision_ai_interfaces__msg__ScanPlan__Sequence * input,
  vision_ai_interfaces__msg__ScanPlan__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__ScanPlan);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__ScanPlan * data =
      (vision_ai_interfaces__msg__ScanPlan *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__ScanPlan__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__ScanPlan__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__ScanPlan__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

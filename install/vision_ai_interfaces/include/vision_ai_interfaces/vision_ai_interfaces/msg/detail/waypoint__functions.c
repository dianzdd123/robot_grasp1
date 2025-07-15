// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/waypoint__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `coverage_rect`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
vision_ai_interfaces__msg__Waypoint__init(vision_ai_interfaces__msg__Waypoint * msg)
{
  if (!msg) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    vision_ai_interfaces__msg__Waypoint__fini(msg);
    return false;
  }
  // waypoint_index
  // coverage_rect
  if (!geometry_msgs__msg__Point__Sequence__init(&msg->coverage_rect, 0)) {
    vision_ai_interfaces__msg__Waypoint__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__msg__Waypoint__fini(vision_ai_interfaces__msg__Waypoint * msg)
{
  if (!msg) {
    return;
  }
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // waypoint_index
  // coverage_rect
  geometry_msgs__msg__Point__Sequence__fini(&msg->coverage_rect);
}

bool
vision_ai_interfaces__msg__Waypoint__are_equal(const vision_ai_interfaces__msg__Waypoint * lhs, const vision_ai_interfaces__msg__Waypoint * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // waypoint_index
  if (lhs->waypoint_index != rhs->waypoint_index) {
    return false;
  }
  // coverage_rect
  if (!geometry_msgs__msg__Point__Sequence__are_equal(
      &(lhs->coverage_rect), &(rhs->coverage_rect)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__Waypoint__copy(
  const vision_ai_interfaces__msg__Waypoint * input,
  vision_ai_interfaces__msg__Waypoint * output)
{
  if (!input || !output) {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // waypoint_index
  output->waypoint_index = input->waypoint_index;
  // coverage_rect
  if (!geometry_msgs__msg__Point__Sequence__copy(
      &(input->coverage_rect), &(output->coverage_rect)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__msg__Waypoint *
vision_ai_interfaces__msg__Waypoint__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__Waypoint * msg = (vision_ai_interfaces__msg__Waypoint *)allocator.allocate(sizeof(vision_ai_interfaces__msg__Waypoint), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__Waypoint));
  bool success = vision_ai_interfaces__msg__Waypoint__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__Waypoint__destroy(vision_ai_interfaces__msg__Waypoint * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__Waypoint__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__Waypoint__Sequence__init(vision_ai_interfaces__msg__Waypoint__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__Waypoint * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__Waypoint *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__Waypoint), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__Waypoint__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__Waypoint__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__Waypoint__Sequence__fini(vision_ai_interfaces__msg__Waypoint__Sequence * array)
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
      vision_ai_interfaces__msg__Waypoint__fini(&array->data[i]);
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

vision_ai_interfaces__msg__Waypoint__Sequence *
vision_ai_interfaces__msg__Waypoint__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__Waypoint__Sequence * array = (vision_ai_interfaces__msg__Waypoint__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__Waypoint__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__Waypoint__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__Waypoint__Sequence__destroy(vision_ai_interfaces__msg__Waypoint__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__Waypoint__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__Waypoint__Sequence__are_equal(const vision_ai_interfaces__msg__Waypoint__Sequence * lhs, const vision_ai_interfaces__msg__Waypoint__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__Waypoint__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__Waypoint__Sequence__copy(
  const vision_ai_interfaces__msg__Waypoint__Sequence * input,
  vision_ai_interfaces__msg__Waypoint__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__Waypoint);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__Waypoint * data =
      (vision_ai_interfaces__msg__Waypoint *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__Waypoint__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__Waypoint__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__Waypoint__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

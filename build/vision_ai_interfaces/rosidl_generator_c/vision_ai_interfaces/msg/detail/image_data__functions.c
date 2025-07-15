// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/ImageData.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/image_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `filename`
#include "rosidl_runtime_c/string_functions.h"
// Member `timestamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `waypoint`
#include "vision_ai_interfaces/msg/detail/waypoint__functions.h"
// Member `image`
#include "sensor_msgs/msg/detail/image__functions.h"

bool
vision_ai_interfaces__msg__ImageData__init(vision_ai_interfaces__msg__ImageData * msg)
{
  if (!msg) {
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__init(&msg->filename)) {
    vision_ai_interfaces__msg__ImageData__fini(msg);
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__init(&msg->timestamp)) {
    vision_ai_interfaces__msg__ImageData__fini(msg);
    return false;
  }
  // waypoint
  if (!vision_ai_interfaces__msg__Waypoint__init(&msg->waypoint)) {
    vision_ai_interfaces__msg__ImageData__fini(msg);
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__init(&msg->image)) {
    vision_ai_interfaces__msg__ImageData__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__msg__ImageData__fini(vision_ai_interfaces__msg__ImageData * msg)
{
  if (!msg) {
    return;
  }
  // filename
  rosidl_runtime_c__String__fini(&msg->filename);
  // timestamp
  builtin_interfaces__msg__Time__fini(&msg->timestamp);
  // waypoint
  vision_ai_interfaces__msg__Waypoint__fini(&msg->waypoint);
  // image
  sensor_msgs__msg__Image__fini(&msg->image);
}

bool
vision_ai_interfaces__msg__ImageData__are_equal(const vision_ai_interfaces__msg__ImageData * lhs, const vision_ai_interfaces__msg__ImageData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->filename), &(rhs->filename)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->timestamp), &(rhs->timestamp)))
  {
    return false;
  }
  // waypoint
  if (!vision_ai_interfaces__msg__Waypoint__are_equal(
      &(lhs->waypoint), &(rhs->waypoint)))
  {
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->image), &(rhs->image)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__ImageData__copy(
  const vision_ai_interfaces__msg__ImageData * input,
  vision_ai_interfaces__msg__ImageData * output)
{
  if (!input || !output) {
    return false;
  }
  // filename
  if (!rosidl_runtime_c__String__copy(
      &(input->filename), &(output->filename)))
  {
    return false;
  }
  // timestamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->timestamp), &(output->timestamp)))
  {
    return false;
  }
  // waypoint
  if (!vision_ai_interfaces__msg__Waypoint__copy(
      &(input->waypoint), &(output->waypoint)))
  {
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__copy(
      &(input->image), &(output->image)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__msg__ImageData *
vision_ai_interfaces__msg__ImageData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ImageData * msg = (vision_ai_interfaces__msg__ImageData *)allocator.allocate(sizeof(vision_ai_interfaces__msg__ImageData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__ImageData));
  bool success = vision_ai_interfaces__msg__ImageData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__ImageData__destroy(vision_ai_interfaces__msg__ImageData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__ImageData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__ImageData__Sequence__init(vision_ai_interfaces__msg__ImageData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ImageData * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__ImageData *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__ImageData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__ImageData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__ImageData__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__ImageData__Sequence__fini(vision_ai_interfaces__msg__ImageData__Sequence * array)
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
      vision_ai_interfaces__msg__ImageData__fini(&array->data[i]);
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

vision_ai_interfaces__msg__ImageData__Sequence *
vision_ai_interfaces__msg__ImageData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__ImageData__Sequence * array = (vision_ai_interfaces__msg__ImageData__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__ImageData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__ImageData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__ImageData__Sequence__destroy(vision_ai_interfaces__msg__ImageData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__ImageData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__ImageData__Sequence__are_equal(const vision_ai_interfaces__msg__ImageData__Sequence * lhs, const vision_ai_interfaces__msg__ImageData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__ImageData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__ImageData__Sequence__copy(
  const vision_ai_interfaces__msg__ImageData__Sequence * input,
  vision_ai_interfaces__msg__ImageData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__ImageData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__ImageData * data =
      (vision_ai_interfaces__msg__ImageData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__ImageData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__ImageData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__ImageData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

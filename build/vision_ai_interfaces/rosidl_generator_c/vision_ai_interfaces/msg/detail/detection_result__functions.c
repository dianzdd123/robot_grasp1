// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/DetectionResult.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/detection_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `output_directory`
#include "rosidl_runtime_c/string_functions.h"
// Member `objects`
#include "vision_ai_interfaces/msg/detail/detected_object__functions.h"

bool
vision_ai_interfaces__msg__DetectionResult__init(vision_ai_interfaces__msg__DetectionResult * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    vision_ai_interfaces__msg__DetectionResult__fini(msg);
    return false;
  }
  // detection_count
  // processing_time
  // output_directory
  if (!rosidl_runtime_c__String__init(&msg->output_directory)) {
    vision_ai_interfaces__msg__DetectionResult__fini(msg);
    return false;
  }
  // objects
  if (!vision_ai_interfaces__msg__DetectedObject__Sequence__init(&msg->objects, 0)) {
    vision_ai_interfaces__msg__DetectionResult__fini(msg);
    return false;
  }
  return true;
}

void
vision_ai_interfaces__msg__DetectionResult__fini(vision_ai_interfaces__msg__DetectionResult * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // detection_count
  // processing_time
  // output_directory
  rosidl_runtime_c__String__fini(&msg->output_directory);
  // objects
  vision_ai_interfaces__msg__DetectedObject__Sequence__fini(&msg->objects);
}

bool
vision_ai_interfaces__msg__DetectionResult__are_equal(const vision_ai_interfaces__msg__DetectionResult * lhs, const vision_ai_interfaces__msg__DetectionResult * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // detection_count
  if (lhs->detection_count != rhs->detection_count) {
    return false;
  }
  // processing_time
  if (lhs->processing_time != rhs->processing_time) {
    return false;
  }
  // output_directory
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->output_directory), &(rhs->output_directory)))
  {
    return false;
  }
  // objects
  if (!vision_ai_interfaces__msg__DetectedObject__Sequence__are_equal(
      &(lhs->objects), &(rhs->objects)))
  {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__DetectionResult__copy(
  const vision_ai_interfaces__msg__DetectionResult * input,
  vision_ai_interfaces__msg__DetectionResult * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // detection_count
  output->detection_count = input->detection_count;
  // processing_time
  output->processing_time = input->processing_time;
  // output_directory
  if (!rosidl_runtime_c__String__copy(
      &(input->output_directory), &(output->output_directory)))
  {
    return false;
  }
  // objects
  if (!vision_ai_interfaces__msg__DetectedObject__Sequence__copy(
      &(input->objects), &(output->objects)))
  {
    return false;
  }
  return true;
}

vision_ai_interfaces__msg__DetectionResult *
vision_ai_interfaces__msg__DetectionResult__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectionResult * msg = (vision_ai_interfaces__msg__DetectionResult *)allocator.allocate(sizeof(vision_ai_interfaces__msg__DetectionResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__DetectionResult));
  bool success = vision_ai_interfaces__msg__DetectionResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__DetectionResult__destroy(vision_ai_interfaces__msg__DetectionResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__DetectionResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__DetectionResult__Sequence__init(vision_ai_interfaces__msg__DetectionResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectionResult * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__DetectionResult *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__DetectionResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__DetectionResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__DetectionResult__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__DetectionResult__Sequence__fini(vision_ai_interfaces__msg__DetectionResult__Sequence * array)
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
      vision_ai_interfaces__msg__DetectionResult__fini(&array->data[i]);
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

vision_ai_interfaces__msg__DetectionResult__Sequence *
vision_ai_interfaces__msg__DetectionResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectionResult__Sequence * array = (vision_ai_interfaces__msg__DetectionResult__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__DetectionResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__DetectionResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__DetectionResult__Sequence__destroy(vision_ai_interfaces__msg__DetectionResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__DetectionResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__DetectionResult__Sequence__are_equal(const vision_ai_interfaces__msg__DetectionResult__Sequence * lhs, const vision_ai_interfaces__msg__DetectionResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__DetectionResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__DetectionResult__Sequence__copy(
  const vision_ai_interfaces__msg__DetectionResult__Sequence * input,
  vision_ai_interfaces__msg__DetectionResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__DetectionResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__DetectionResult * data =
      (vision_ai_interfaces__msg__DetectionResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__DetectionResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__DetectionResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__DetectionResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

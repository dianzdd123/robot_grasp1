// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/stitch_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `method`
// Member `output_path`
#include "rosidl_runtime_c/string_functions.h"

bool
vision_ai_interfaces__msg__StitchResult__init(vision_ai_interfaces__msg__StitchResult * msg)
{
  if (!msg) {
    return false;
  }
  // method
  if (!rosidl_runtime_c__String__init(&msg->method)) {
    vision_ai_interfaces__msg__StitchResult__fini(msg);
    return false;
  }
  // output_path
  if (!rosidl_runtime_c__String__init(&msg->output_path)) {
    vision_ai_interfaces__msg__StitchResult__fini(msg);
    return false;
  }
  // input_images
  // processing_time
  return true;
}

void
vision_ai_interfaces__msg__StitchResult__fini(vision_ai_interfaces__msg__StitchResult * msg)
{
  if (!msg) {
    return;
  }
  // method
  rosidl_runtime_c__String__fini(&msg->method);
  // output_path
  rosidl_runtime_c__String__fini(&msg->output_path);
  // input_images
  // processing_time
}

bool
vision_ai_interfaces__msg__StitchResult__are_equal(const vision_ai_interfaces__msg__StitchResult * lhs, const vision_ai_interfaces__msg__StitchResult * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // method
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->method), &(rhs->method)))
  {
    return false;
  }
  // output_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->output_path), &(rhs->output_path)))
  {
    return false;
  }
  // input_images
  if (lhs->input_images != rhs->input_images) {
    return false;
  }
  // processing_time
  if (lhs->processing_time != rhs->processing_time) {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__StitchResult__copy(
  const vision_ai_interfaces__msg__StitchResult * input,
  vision_ai_interfaces__msg__StitchResult * output)
{
  if (!input || !output) {
    return false;
  }
  // method
  if (!rosidl_runtime_c__String__copy(
      &(input->method), &(output->method)))
  {
    return false;
  }
  // output_path
  if (!rosidl_runtime_c__String__copy(
      &(input->output_path), &(output->output_path)))
  {
    return false;
  }
  // input_images
  output->input_images = input->input_images;
  // processing_time
  output->processing_time = input->processing_time;
  return true;
}

vision_ai_interfaces__msg__StitchResult *
vision_ai_interfaces__msg__StitchResult__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__StitchResult * msg = (vision_ai_interfaces__msg__StitchResult *)allocator.allocate(sizeof(vision_ai_interfaces__msg__StitchResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__StitchResult));
  bool success = vision_ai_interfaces__msg__StitchResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__StitchResult__destroy(vision_ai_interfaces__msg__StitchResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__StitchResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__StitchResult__Sequence__init(vision_ai_interfaces__msg__StitchResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__StitchResult * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__StitchResult *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__StitchResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__StitchResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__StitchResult__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__StitchResult__Sequence__fini(vision_ai_interfaces__msg__StitchResult__Sequence * array)
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
      vision_ai_interfaces__msg__StitchResult__fini(&array->data[i]);
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

vision_ai_interfaces__msg__StitchResult__Sequence *
vision_ai_interfaces__msg__StitchResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__StitchResult__Sequence * array = (vision_ai_interfaces__msg__StitchResult__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__StitchResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__StitchResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__StitchResult__Sequence__destroy(vision_ai_interfaces__msg__StitchResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__StitchResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__StitchResult__Sequence__are_equal(const vision_ai_interfaces__msg__StitchResult__Sequence * lhs, const vision_ai_interfaces__msg__StitchResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__StitchResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__StitchResult__Sequence__copy(
  const vision_ai_interfaces__msg__StitchResult__Sequence * input,
  vision_ai_interfaces__msg__StitchResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__StitchResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__StitchResult * data =
      (vision_ai_interfaces__msg__StitchResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__StitchResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__StitchResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__StitchResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

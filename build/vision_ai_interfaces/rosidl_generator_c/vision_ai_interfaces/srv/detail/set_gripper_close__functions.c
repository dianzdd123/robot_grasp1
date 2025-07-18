// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:srv/SetGripperClose.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/srv/detail/set_gripper_close__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
vision_ai_interfaces__srv__SetGripperClose_Request__init(vision_ai_interfaces__srv__SetGripperClose_Request * msg)
{
  if (!msg) {
    return false;
  }
  // position
  return true;
}

void
vision_ai_interfaces__srv__SetGripperClose_Request__fini(vision_ai_interfaces__srv__SetGripperClose_Request * msg)
{
  if (!msg) {
    return;
  }
  // position
}

bool
vision_ai_interfaces__srv__SetGripperClose_Request__are_equal(const vision_ai_interfaces__srv__SetGripperClose_Request * lhs, const vision_ai_interfaces__srv__SetGripperClose_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // position
  if (lhs->position != rhs->position) {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__srv__SetGripperClose_Request__copy(
  const vision_ai_interfaces__srv__SetGripperClose_Request * input,
  vision_ai_interfaces__srv__SetGripperClose_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // position
  output->position = input->position;
  return true;
}

vision_ai_interfaces__srv__SetGripperClose_Request *
vision_ai_interfaces__srv__SetGripperClose_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Request * msg = (vision_ai_interfaces__srv__SetGripperClose_Request *)allocator.allocate(sizeof(vision_ai_interfaces__srv__SetGripperClose_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__srv__SetGripperClose_Request));
  bool success = vision_ai_interfaces__srv__SetGripperClose_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__srv__SetGripperClose_Request__destroy(vision_ai_interfaces__srv__SetGripperClose_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__srv__SetGripperClose_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__init(vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Request * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__srv__SetGripperClose_Request *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__srv__SetGripperClose_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__srv__SetGripperClose_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__srv__SetGripperClose_Request__fini(&data[i - 1]);
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
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__fini(vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * array)
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
      vision_ai_interfaces__srv__SetGripperClose_Request__fini(&array->data[i]);
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

vision_ai_interfaces__srv__SetGripperClose_Request__Sequence *
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * array = (vision_ai_interfaces__srv__SetGripperClose_Request__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__srv__SetGripperClose_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__destroy(vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__are_equal(const vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * lhs, const vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__srv__SetGripperClose_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__srv__SetGripperClose_Request__Sequence__copy(
  const vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * input,
  vision_ai_interfaces__srv__SetGripperClose_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__srv__SetGripperClose_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__srv__SetGripperClose_Request * data =
      (vision_ai_interfaces__srv__SetGripperClose_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__srv__SetGripperClose_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__srv__SetGripperClose_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__srv__SetGripperClose_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
vision_ai_interfaces__srv__SetGripperClose_Response__init(vision_ai_interfaces__srv__SetGripperClose_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    vision_ai_interfaces__srv__SetGripperClose_Response__fini(msg);
    return false;
  }
  // actual_position
  return true;
}

void
vision_ai_interfaces__srv__SetGripperClose_Response__fini(vision_ai_interfaces__srv__SetGripperClose_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // actual_position
}

bool
vision_ai_interfaces__srv__SetGripperClose_Response__are_equal(const vision_ai_interfaces__srv__SetGripperClose_Response * lhs, const vision_ai_interfaces__srv__SetGripperClose_Response * rhs)
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
  // actual_position
  if (lhs->actual_position != rhs->actual_position) {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__srv__SetGripperClose_Response__copy(
  const vision_ai_interfaces__srv__SetGripperClose_Response * input,
  vision_ai_interfaces__srv__SetGripperClose_Response * output)
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
  // actual_position
  output->actual_position = input->actual_position;
  return true;
}

vision_ai_interfaces__srv__SetGripperClose_Response *
vision_ai_interfaces__srv__SetGripperClose_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Response * msg = (vision_ai_interfaces__srv__SetGripperClose_Response *)allocator.allocate(sizeof(vision_ai_interfaces__srv__SetGripperClose_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__srv__SetGripperClose_Response));
  bool success = vision_ai_interfaces__srv__SetGripperClose_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__srv__SetGripperClose_Response__destroy(vision_ai_interfaces__srv__SetGripperClose_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__srv__SetGripperClose_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__init(vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Response * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__srv__SetGripperClose_Response *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__srv__SetGripperClose_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__srv__SetGripperClose_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__srv__SetGripperClose_Response__fini(&data[i - 1]);
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
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__fini(vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * array)
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
      vision_ai_interfaces__srv__SetGripperClose_Response__fini(&array->data[i]);
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

vision_ai_interfaces__srv__SetGripperClose_Response__Sequence *
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * array = (vision_ai_interfaces__srv__SetGripperClose_Response__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__srv__SetGripperClose_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__destroy(vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__are_equal(const vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * lhs, const vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__srv__SetGripperClose_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__srv__SetGripperClose_Response__Sequence__copy(
  const vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * input,
  vision_ai_interfaces__srv__SetGripperClose_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__srv__SetGripperClose_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__srv__SetGripperClose_Response * data =
      (vision_ai_interfaces__srv__SetGripperClose_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__srv__SetGripperClose_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__srv__SetGripperClose_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__srv__SetGripperClose_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

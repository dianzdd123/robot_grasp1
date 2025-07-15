// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vision_ai_interfaces:msg/DetectedObject.idl
// generated code does not contain a copyright notice
#include "vision_ai_interfaces/msg/detail/detected_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `object_id`
// Member `class_name`
// Member `description`
#include "rosidl_runtime_c/string_functions.h"
// Member `bounding_box`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
vision_ai_interfaces__msg__DetectedObject__init(vision_ai_interfaces__msg__DetectedObject * msg)
{
  if (!msg) {
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__init(&msg->object_id)) {
    vision_ai_interfaces__msg__DetectedObject__fini(msg);
    return false;
  }
  // class_id
  // class_name
  if (!rosidl_runtime_c__String__init(&msg->class_name)) {
    vision_ai_interfaces__msg__DetectedObject__fini(msg);
    return false;
  }
  // confidence
  // description
  if (!rosidl_runtime_c__String__init(&msg->description)) {
    vision_ai_interfaces__msg__DetectedObject__fini(msg);
    return false;
  }
  // bounding_box
  if (!rosidl_runtime_c__float__Sequence__init(&msg->bounding_box, 0)) {
    vision_ai_interfaces__msg__DetectedObject__fini(msg);
    return false;
  }
  // center_x
  // center_y
  // world_x
  // world_y
  // world_z
  return true;
}

void
vision_ai_interfaces__msg__DetectedObject__fini(vision_ai_interfaces__msg__DetectedObject * msg)
{
  if (!msg) {
    return;
  }
  // object_id
  rosidl_runtime_c__String__fini(&msg->object_id);
  // class_id
  // class_name
  rosidl_runtime_c__String__fini(&msg->class_name);
  // confidence
  // description
  rosidl_runtime_c__String__fini(&msg->description);
  // bounding_box
  rosidl_runtime_c__float__Sequence__fini(&msg->bounding_box);
  // center_x
  // center_y
  // world_x
  // world_y
  // world_z
}

bool
vision_ai_interfaces__msg__DetectedObject__are_equal(const vision_ai_interfaces__msg__DetectedObject * lhs, const vision_ai_interfaces__msg__DetectedObject * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->object_id), &(rhs->object_id)))
  {
    return false;
  }
  // class_id
  if (lhs->class_id != rhs->class_id) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->class_name), &(rhs->class_name)))
  {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // description
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->description), &(rhs->description)))
  {
    return false;
  }
  // bounding_box
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->bounding_box), &(rhs->bounding_box)))
  {
    return false;
  }
  // center_x
  if (lhs->center_x != rhs->center_x) {
    return false;
  }
  // center_y
  if (lhs->center_y != rhs->center_y) {
    return false;
  }
  // world_x
  if (lhs->world_x != rhs->world_x) {
    return false;
  }
  // world_y
  if (lhs->world_y != rhs->world_y) {
    return false;
  }
  // world_z
  if (lhs->world_z != rhs->world_z) {
    return false;
  }
  return true;
}

bool
vision_ai_interfaces__msg__DetectedObject__copy(
  const vision_ai_interfaces__msg__DetectedObject * input,
  vision_ai_interfaces__msg__DetectedObject * output)
{
  if (!input || !output) {
    return false;
  }
  // object_id
  if (!rosidl_runtime_c__String__copy(
      &(input->object_id), &(output->object_id)))
  {
    return false;
  }
  // class_id
  output->class_id = input->class_id;
  // class_name
  if (!rosidl_runtime_c__String__copy(
      &(input->class_name), &(output->class_name)))
  {
    return false;
  }
  // confidence
  output->confidence = input->confidence;
  // description
  if (!rosidl_runtime_c__String__copy(
      &(input->description), &(output->description)))
  {
    return false;
  }
  // bounding_box
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->bounding_box), &(output->bounding_box)))
  {
    return false;
  }
  // center_x
  output->center_x = input->center_x;
  // center_y
  output->center_y = input->center_y;
  // world_x
  output->world_x = input->world_x;
  // world_y
  output->world_y = input->world_y;
  // world_z
  output->world_z = input->world_z;
  return true;
}

vision_ai_interfaces__msg__DetectedObject *
vision_ai_interfaces__msg__DetectedObject__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectedObject * msg = (vision_ai_interfaces__msg__DetectedObject *)allocator.allocate(sizeof(vision_ai_interfaces__msg__DetectedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vision_ai_interfaces__msg__DetectedObject));
  bool success = vision_ai_interfaces__msg__DetectedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vision_ai_interfaces__msg__DetectedObject__destroy(vision_ai_interfaces__msg__DetectedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vision_ai_interfaces__msg__DetectedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vision_ai_interfaces__msg__DetectedObject__Sequence__init(vision_ai_interfaces__msg__DetectedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectedObject * data = NULL;

  if (size) {
    data = (vision_ai_interfaces__msg__DetectedObject *)allocator.zero_allocate(size, sizeof(vision_ai_interfaces__msg__DetectedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vision_ai_interfaces__msg__DetectedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vision_ai_interfaces__msg__DetectedObject__fini(&data[i - 1]);
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
vision_ai_interfaces__msg__DetectedObject__Sequence__fini(vision_ai_interfaces__msg__DetectedObject__Sequence * array)
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
      vision_ai_interfaces__msg__DetectedObject__fini(&array->data[i]);
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

vision_ai_interfaces__msg__DetectedObject__Sequence *
vision_ai_interfaces__msg__DetectedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vision_ai_interfaces__msg__DetectedObject__Sequence * array = (vision_ai_interfaces__msg__DetectedObject__Sequence *)allocator.allocate(sizeof(vision_ai_interfaces__msg__DetectedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vision_ai_interfaces__msg__DetectedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vision_ai_interfaces__msg__DetectedObject__Sequence__destroy(vision_ai_interfaces__msg__DetectedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vision_ai_interfaces__msg__DetectedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vision_ai_interfaces__msg__DetectedObject__Sequence__are_equal(const vision_ai_interfaces__msg__DetectedObject__Sequence * lhs, const vision_ai_interfaces__msg__DetectedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vision_ai_interfaces__msg__DetectedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vision_ai_interfaces__msg__DetectedObject__Sequence__copy(
  const vision_ai_interfaces__msg__DetectedObject__Sequence * input,
  vision_ai_interfaces__msg__DetectedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vision_ai_interfaces__msg__DetectedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vision_ai_interfaces__msg__DetectedObject * data =
      (vision_ai_interfaces__msg__DetectedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vision_ai_interfaces__msg__DetectedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vision_ai_interfaces__msg__DetectedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vision_ai_interfaces__msg__DetectedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

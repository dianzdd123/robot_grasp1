// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vision_ai_interfaces:msg/ScanPlan.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__FUNCTIONS_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vision_ai_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "vision_ai_interfaces/msg/detail/scan_plan__struct.h"

/// Initialize msg/ScanPlan message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vision_ai_interfaces__msg__ScanPlan
 * )) before or use
 * vision_ai_interfaces__msg__ScanPlan__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__init(vision_ai_interfaces__msg__ScanPlan * msg);

/// Finalize msg/ScanPlan message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__ScanPlan__fini(vision_ai_interfaces__msg__ScanPlan * msg);

/// Create msg/ScanPlan message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vision_ai_interfaces__msg__ScanPlan__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__msg__ScanPlan *
vision_ai_interfaces__msg__ScanPlan__create();

/// Destroy msg/ScanPlan message.
/**
 * It calls
 * vision_ai_interfaces__msg__ScanPlan__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__ScanPlan__destroy(vision_ai_interfaces__msg__ScanPlan * msg);

/// Check for msg/ScanPlan message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__are_equal(const vision_ai_interfaces__msg__ScanPlan * lhs, const vision_ai_interfaces__msg__ScanPlan * rhs);

/// Copy a msg/ScanPlan message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__copy(
  const vision_ai_interfaces__msg__ScanPlan * input,
  vision_ai_interfaces__msg__ScanPlan * output);

/// Initialize array of msg/ScanPlan messages.
/**
 * It allocates the memory for the number of elements and calls
 * vision_ai_interfaces__msg__ScanPlan__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__Sequence__init(vision_ai_interfaces__msg__ScanPlan__Sequence * array, size_t size);

/// Finalize array of msg/ScanPlan messages.
/**
 * It calls
 * vision_ai_interfaces__msg__ScanPlan__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__ScanPlan__Sequence__fini(vision_ai_interfaces__msg__ScanPlan__Sequence * array);

/// Create array of msg/ScanPlan messages.
/**
 * It allocates the memory for the array and calls
 * vision_ai_interfaces__msg__ScanPlan__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__msg__ScanPlan__Sequence *
vision_ai_interfaces__msg__ScanPlan__Sequence__create(size_t size);

/// Destroy array of msg/ScanPlan messages.
/**
 * It calls
 * vision_ai_interfaces__msg__ScanPlan__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__ScanPlan__Sequence__destroy(vision_ai_interfaces__msg__ScanPlan__Sequence * array);

/// Check for msg/ScanPlan message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__Sequence__are_equal(const vision_ai_interfaces__msg__ScanPlan__Sequence * lhs, const vision_ai_interfaces__msg__ScanPlan__Sequence * rhs);

/// Copy an array of msg/ScanPlan messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__ScanPlan__Sequence__copy(
  const vision_ai_interfaces__msg__ScanPlan__Sequence * input,
  vision_ai_interfaces__msg__ScanPlan__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__SCAN_PLAN__FUNCTIONS_H_

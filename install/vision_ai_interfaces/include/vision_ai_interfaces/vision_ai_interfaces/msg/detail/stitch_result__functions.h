// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vision_ai_interfaces:msg/StitchResult.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__FUNCTIONS_H_
#define VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vision_ai_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "vision_ai_interfaces/msg/detail/stitch_result__struct.h"

/// Initialize msg/StitchResult message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vision_ai_interfaces__msg__StitchResult
 * )) before or use
 * vision_ai_interfaces__msg__StitchResult__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__StitchResult__init(vision_ai_interfaces__msg__StitchResult * msg);

/// Finalize msg/StitchResult message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__StitchResult__fini(vision_ai_interfaces__msg__StitchResult * msg);

/// Create msg/StitchResult message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vision_ai_interfaces__msg__StitchResult__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__msg__StitchResult *
vision_ai_interfaces__msg__StitchResult__create();

/// Destroy msg/StitchResult message.
/**
 * It calls
 * vision_ai_interfaces__msg__StitchResult__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__StitchResult__destroy(vision_ai_interfaces__msg__StitchResult * msg);

/// Check for msg/StitchResult message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__StitchResult__are_equal(const vision_ai_interfaces__msg__StitchResult * lhs, const vision_ai_interfaces__msg__StitchResult * rhs);

/// Copy a msg/StitchResult message.
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
vision_ai_interfaces__msg__StitchResult__copy(
  const vision_ai_interfaces__msg__StitchResult * input,
  vision_ai_interfaces__msg__StitchResult * output);

/// Initialize array of msg/StitchResult messages.
/**
 * It allocates the memory for the number of elements and calls
 * vision_ai_interfaces__msg__StitchResult__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__StitchResult__Sequence__init(vision_ai_interfaces__msg__StitchResult__Sequence * array, size_t size);

/// Finalize array of msg/StitchResult messages.
/**
 * It calls
 * vision_ai_interfaces__msg__StitchResult__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__StitchResult__Sequence__fini(vision_ai_interfaces__msg__StitchResult__Sequence * array);

/// Create array of msg/StitchResult messages.
/**
 * It allocates the memory for the array and calls
 * vision_ai_interfaces__msg__StitchResult__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__msg__StitchResult__Sequence *
vision_ai_interfaces__msg__StitchResult__Sequence__create(size_t size);

/// Destroy array of msg/StitchResult messages.
/**
 * It calls
 * vision_ai_interfaces__msg__StitchResult__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__msg__StitchResult__Sequence__destroy(vision_ai_interfaces__msg__StitchResult__Sequence * array);

/// Check for msg/StitchResult message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__msg__StitchResult__Sequence__are_equal(const vision_ai_interfaces__msg__StitchResult__Sequence * lhs, const vision_ai_interfaces__msg__StitchResult__Sequence * rhs);

/// Copy an array of msg/StitchResult messages.
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
vision_ai_interfaces__msg__StitchResult__Sequence__copy(
  const vision_ai_interfaces__msg__StitchResult__Sequence * input,
  vision_ai_interfaces__msg__StitchResult__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__MSG__DETAIL__STITCH_RESULT__FUNCTIONS_H_

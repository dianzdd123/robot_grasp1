// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from vision_ai_interfaces:srv/ProcessStitching.idl
// generated code does not contain a copyright notice

#ifndef VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__FUNCTIONS_H_
#define VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "vision_ai_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "vision_ai_interfaces/srv/detail/process_stitching__struct.h"

/// Initialize srv/ProcessStitching message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vision_ai_interfaces__srv__ProcessStitching_Request
 * )) before or use
 * vision_ai_interfaces__srv__ProcessStitching_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Request__init(vision_ai_interfaces__srv__ProcessStitching_Request * msg);

/// Finalize srv/ProcessStitching message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Request__fini(vision_ai_interfaces__srv__ProcessStitching_Request * msg);

/// Create srv/ProcessStitching message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__srv__ProcessStitching_Request *
vision_ai_interfaces__srv__ProcessStitching_Request__create();

/// Destroy srv/ProcessStitching message.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Request__destroy(vision_ai_interfaces__srv__ProcessStitching_Request * msg);

/// Check for srv/ProcessStitching message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Request__are_equal(const vision_ai_interfaces__srv__ProcessStitching_Request * lhs, const vision_ai_interfaces__srv__ProcessStitching_Request * rhs);

/// Copy a srv/ProcessStitching message.
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
vision_ai_interfaces__srv__ProcessStitching_Request__copy(
  const vision_ai_interfaces__srv__ProcessStitching_Request * input,
  vision_ai_interfaces__srv__ProcessStitching_Request * output);

/// Initialize array of srv/ProcessStitching messages.
/**
 * It allocates the memory for the number of elements and calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__init(vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * array, size_t size);

/// Finalize array of srv/ProcessStitching messages.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__fini(vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * array);

/// Create array of srv/ProcessStitching messages.
/**
 * It allocates the memory for the array and calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence *
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__create(size_t size);

/// Destroy array of srv/ProcessStitching messages.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__destroy(vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * array);

/// Check for srv/ProcessStitching message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__are_equal(const vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * lhs, const vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * rhs);

/// Copy an array of srv/ProcessStitching messages.
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
vision_ai_interfaces__srv__ProcessStitching_Request__Sequence__copy(
  const vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * input,
  vision_ai_interfaces__srv__ProcessStitching_Request__Sequence * output);

/// Initialize srv/ProcessStitching message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * vision_ai_interfaces__srv__ProcessStitching_Response
 * )) before or use
 * vision_ai_interfaces__srv__ProcessStitching_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Response__init(vision_ai_interfaces__srv__ProcessStitching_Response * msg);

/// Finalize srv/ProcessStitching message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Response__fini(vision_ai_interfaces__srv__ProcessStitching_Response * msg);

/// Create srv/ProcessStitching message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__srv__ProcessStitching_Response *
vision_ai_interfaces__srv__ProcessStitching_Response__create();

/// Destroy srv/ProcessStitching message.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Response__destroy(vision_ai_interfaces__srv__ProcessStitching_Response * msg);

/// Check for srv/ProcessStitching message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Response__are_equal(const vision_ai_interfaces__srv__ProcessStitching_Response * lhs, const vision_ai_interfaces__srv__ProcessStitching_Response * rhs);

/// Copy a srv/ProcessStitching message.
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
vision_ai_interfaces__srv__ProcessStitching_Response__copy(
  const vision_ai_interfaces__srv__ProcessStitching_Response * input,
  vision_ai_interfaces__srv__ProcessStitching_Response * output);

/// Initialize array of srv/ProcessStitching messages.
/**
 * It allocates the memory for the number of elements and calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__init(vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * array, size_t size);

/// Finalize array of srv/ProcessStitching messages.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__fini(vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * array);

/// Create array of srv/ProcessStitching messages.
/**
 * It allocates the memory for the array and calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence *
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__create(size_t size);

/// Destroy array of srv/ProcessStitching messages.
/**
 * It calls
 * vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
void
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__destroy(vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * array);

/// Check for srv/ProcessStitching message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_vision_ai_interfaces
bool
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__are_equal(const vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * lhs, const vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * rhs);

/// Copy an array of srv/ProcessStitching messages.
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
vision_ai_interfaces__srv__ProcessStitching_Response__Sequence__copy(
  const vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * input,
  vision_ai_interfaces__srv__ProcessStitching_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // VISION_AI_INTERFACES__SRV__DETAIL__PROCESS_STITCHING__FUNCTIONS_H_

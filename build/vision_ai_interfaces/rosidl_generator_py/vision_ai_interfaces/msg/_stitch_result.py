# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vision_ai_interfaces:msg/StitchResult.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_StitchResult(type):
    """Metaclass of message 'StitchResult'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('vision_ai_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'vision_ai_interfaces.msg.StitchResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__stitch_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__stitch_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__stitch_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__stitch_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__stitch_result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class StitchResult(metaclass=Metaclass_StitchResult):
    """Message class 'StitchResult'."""

    __slots__ = [
        '_method',
        '_output_path',
        '_input_images',
        '_processing_time',
    ]

    _fields_and_field_types = {
        'method': 'string',
        'output_path': 'string',
        'input_images': 'int32',
        'processing_time': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.method = kwargs.get('method', str())
        self.output_path = kwargs.get('output_path', str())
        self.input_images = kwargs.get('input_images', int())
        self.processing_time = kwargs.get('processing_time', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.method != other.method:
            return False
        if self.output_path != other.output_path:
            return False
        if self.input_images != other.input_images:
            return False
        if self.processing_time != other.processing_time:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def method(self):
        """Message field 'method'."""
        return self._method

    @method.setter
    def method(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'method' field must be of type 'str'"
        self._method = value

    @builtins.property
    def output_path(self):
        """Message field 'output_path'."""
        return self._output_path

    @output_path.setter
    def output_path(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'output_path' field must be of type 'str'"
        self._output_path = value

    @builtins.property
    def input_images(self):
        """Message field 'input_images'."""
        return self._input_images

    @input_images.setter
    def input_images(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'input_images' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'input_images' field must be an integer in [-2147483648, 2147483647]"
        self._input_images = value

    @builtins.property
    def processing_time(self):
        """Message field 'processing_time'."""
        return self._processing_time

    @processing_time.setter
    def processing_time(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'processing_time' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'processing_time' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._processing_time = value

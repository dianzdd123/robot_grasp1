# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vision_ai_interfaces:srv/ProcessStitching.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ProcessStitching_Request(type):
    """Metaclass of message 'ProcessStitching_Request'."""

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
                'vision_ai_interfaces.srv.ProcessStitching_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__process_stitching__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__process_stitching__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__process_stitching__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__process_stitching__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__process_stitching__request

            from vision_ai_interfaces.msg import ImageData
            if ImageData.__class__._TYPE_SUPPORT is None:
                ImageData.__class__.__import_type_support__()

            from vision_ai_interfaces.msg import ScanPlan
            if ScanPlan.__class__._TYPE_SUPPORT is None:
                ScanPlan.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ProcessStitching_Request(metaclass=Metaclass_ProcessStitching_Request):
    """Message class 'ProcessStitching_Request'."""

    __slots__ = [
        '_image_data',
        '_scan_plan',
        '_output_directory',
    ]

    _fields_and_field_types = {
        'image_data': 'sequence<vision_ai_interfaces/ImageData>',
        'scan_plan': 'vision_ai_interfaces/ScanPlan',
        'output_directory': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['vision_ai_interfaces', 'msg'], 'ImageData')),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['vision_ai_interfaces', 'msg'], 'ScanPlan'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.image_data = kwargs.get('image_data', [])
        from vision_ai_interfaces.msg import ScanPlan
        self.scan_plan = kwargs.get('scan_plan', ScanPlan())
        self.output_directory = kwargs.get('output_directory', str())

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
        if self.image_data != other.image_data:
            return False
        if self.scan_plan != other.scan_plan:
            return False
        if self.output_directory != other.output_directory:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def image_data(self):
        """Message field 'image_data'."""
        return self._image_data

    @image_data.setter
    def image_data(self, value):
        if __debug__:
            from vision_ai_interfaces.msg import ImageData
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, ImageData) for v in value) and
                 True), \
                "The 'image_data' field must be a set or sequence and each value of type 'ImageData'"
        self._image_data = value

    @builtins.property
    def scan_plan(self):
        """Message field 'scan_plan'."""
        return self._scan_plan

    @scan_plan.setter
    def scan_plan(self, value):
        if __debug__:
            from vision_ai_interfaces.msg import ScanPlan
            assert \
                isinstance(value, ScanPlan), \
                "The 'scan_plan' field must be a sub message of type 'ScanPlan'"
        self._scan_plan = value

    @builtins.property
    def output_directory(self):
        """Message field 'output_directory'."""
        return self._output_directory

    @output_directory.setter
    def output_directory(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'output_directory' field must be of type 'str'"
        self._output_directory = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ProcessStitching_Response(type):
    """Metaclass of message 'ProcessStitching_Response'."""

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
                'vision_ai_interfaces.srv.ProcessStitching_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__process_stitching__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__process_stitching__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__process_stitching__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__process_stitching__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__process_stitching__response

            from vision_ai_interfaces.msg import StitchResult
            if StitchResult.__class__._TYPE_SUPPORT is None:
                StitchResult.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ProcessStitching_Response(metaclass=Metaclass_ProcessStitching_Response):
    """Message class 'ProcessStitching_Response'."""

    __slots__ = [
        '_success',
        '_message',
        '_result',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
        'result': 'vision_ai_interfaces/StitchResult',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['vision_ai_interfaces', 'msg'], 'StitchResult'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())
        from vision_ai_interfaces.msg import StitchResult
        self.result = kwargs.get('result', StitchResult())

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
        if self.success != other.success:
            return False
        if self.message != other.message:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from vision_ai_interfaces.msg import StitchResult
            assert \
                isinstance(value, StitchResult), \
                "The 'result' field must be a sub message of type 'StitchResult'"
        self._result = value


class Metaclass_ProcessStitching(type):
    """Metaclass of service 'ProcessStitching'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('vision_ai_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'vision_ai_interfaces.srv.ProcessStitching')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__process_stitching

            from vision_ai_interfaces.srv import _process_stitching
            if _process_stitching.Metaclass_ProcessStitching_Request._TYPE_SUPPORT is None:
                _process_stitching.Metaclass_ProcessStitching_Request.__import_type_support__()
            if _process_stitching.Metaclass_ProcessStitching_Response._TYPE_SUPPORT is None:
                _process_stitching.Metaclass_ProcessStitching_Response.__import_type_support__()


class ProcessStitching(metaclass=Metaclass_ProcessStitching):
    from vision_ai_interfaces.srv._process_stitching import ProcessStitching_Request as Request
    from vision_ai_interfaces.srv._process_stitching import ProcessStitching_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')

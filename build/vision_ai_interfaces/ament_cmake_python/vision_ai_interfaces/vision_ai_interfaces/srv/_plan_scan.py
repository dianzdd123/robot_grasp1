# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vision_ai_interfaces:srv/PlanScan.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_PlanScan_Request(type):
    """Metaclass of message 'PlanScan_Request'."""

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
                'vision_ai_interfaces.srv.PlanScan_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__plan_scan__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__plan_scan__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__plan_scan__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__plan_scan__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__plan_scan__request

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanScan_Request(metaclass=Metaclass_PlanScan_Request):
    """Message class 'PlanScan_Request'."""

    __slots__ = [
        '_mode',
        '_object_height',
        '_points',
    ]

    _fields_and_field_types = {
        'mode': 'string',
        'object_height': 'double',
        'points': 'sequence<geometry_msgs/Point>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.mode = kwargs.get('mode', str())
        self.object_height = kwargs.get('object_height', float())
        self.points = kwargs.get('points', [])

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
        if self.mode != other.mode:
            return False
        if self.object_height != other.object_height:
            return False
        if self.points != other.points:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def mode(self):
        """Message field 'mode'."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'mode' field must be of type 'str'"
        self._mode = value

    @builtins.property
    def object_height(self):
        """Message field 'object_height'."""
        return self._object_height

    @object_height.setter
    def object_height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'object_height' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'object_height' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._object_height = value

    @builtins.property
    def points(self):
        """Message field 'points'."""
        return self._points

    @points.setter
    def points(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
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
                 all(isinstance(v, Point) for v in value) and
                 True), \
                "The 'points' field must be a set or sequence and each value of type 'Point'"
        self._points = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanScan_Response(type):
    """Metaclass of message 'PlanScan_Response'."""

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
                'vision_ai_interfaces.srv.PlanScan_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__plan_scan__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__plan_scan__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__plan_scan__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__plan_scan__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__plan_scan__response

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


class PlanScan_Response(metaclass=Metaclass_PlanScan_Response):
    """Message class 'PlanScan_Response'."""

    __slots__ = [
        '_success',
        '_message',
        '_scan_plan',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
        'scan_plan': 'vision_ai_interfaces/ScanPlan',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['vision_ai_interfaces', 'msg'], 'ScanPlan'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())
        from vision_ai_interfaces.msg import ScanPlan
        self.scan_plan = kwargs.get('scan_plan', ScanPlan())

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
        if self.scan_plan != other.scan_plan:
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


class Metaclass_PlanScan(type):
    """Metaclass of service 'PlanScan'."""

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
                'vision_ai_interfaces.srv.PlanScan')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__plan_scan

            from vision_ai_interfaces.srv import _plan_scan
            if _plan_scan.Metaclass_PlanScan_Request._TYPE_SUPPORT is None:
                _plan_scan.Metaclass_PlanScan_Request.__import_type_support__()
            if _plan_scan.Metaclass_PlanScan_Response._TYPE_SUPPORT is None:
                _plan_scan.Metaclass_PlanScan_Response.__import_type_support__()


class PlanScan(metaclass=Metaclass_PlanScan):
    from vision_ai_interfaces.srv._plan_scan import PlanScan_Request as Request
    from vision_ai_interfaces.srv._plan_scan import PlanScan_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')

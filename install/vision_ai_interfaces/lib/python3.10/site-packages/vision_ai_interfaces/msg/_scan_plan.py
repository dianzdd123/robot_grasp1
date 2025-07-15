# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vision_ai_interfaces:msg/ScanPlan.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ScanPlan(type):
    """Metaclass of message 'ScanPlan'."""

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
                'vision_ai_interfaces.msg.ScanPlan')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__scan_plan
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__scan_plan
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__scan_plan
            cls._TYPE_SUPPORT = module.type_support_msg__msg__scan_plan
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__scan_plan

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

            from vision_ai_interfaces.msg import Waypoint
            if Waypoint.__class__._TYPE_SUPPORT is None:
                Waypoint.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ScanPlan(metaclass=Metaclass_ScanPlan):
    """Message class 'ScanPlan'."""

    __slots__ = [
        '_strategy',
        '_scan_height',
        '_required_height',
        '_waypoints',
        '_scan_region',
        '_object_height',
        '_mode',
    ]

    _fields_and_field_types = {
        'strategy': 'string',
        'scan_height': 'double',
        'required_height': 'double',
        'waypoints': 'sequence<vision_ai_interfaces/Waypoint>',
        'scan_region': 'sequence<geometry_msgs/Point>',
        'object_height': 'double',
        'mode': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['vision_ai_interfaces', 'msg'], 'Waypoint')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point')),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.strategy = kwargs.get('strategy', str())
        self.scan_height = kwargs.get('scan_height', float())
        self.required_height = kwargs.get('required_height', float())
        self.waypoints = kwargs.get('waypoints', [])
        self.scan_region = kwargs.get('scan_region', [])
        self.object_height = kwargs.get('object_height', float())
        self.mode = kwargs.get('mode', str())

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
        if self.strategy != other.strategy:
            return False
        if self.scan_height != other.scan_height:
            return False
        if self.required_height != other.required_height:
            return False
        if self.waypoints != other.waypoints:
            return False
        if self.scan_region != other.scan_region:
            return False
        if self.object_height != other.object_height:
            return False
        if self.mode != other.mode:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def strategy(self):
        """Message field 'strategy'."""
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'strategy' field must be of type 'str'"
        self._strategy = value

    @builtins.property
    def scan_height(self):
        """Message field 'scan_height'."""
        return self._scan_height

    @scan_height.setter
    def scan_height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'scan_height' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'scan_height' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._scan_height = value

    @builtins.property
    def required_height(self):
        """Message field 'required_height'."""
        return self._required_height

    @required_height.setter
    def required_height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'required_height' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'required_height' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._required_height = value

    @builtins.property
    def waypoints(self):
        """Message field 'waypoints'."""
        return self._waypoints

    @waypoints.setter
    def waypoints(self, value):
        if __debug__:
            from vision_ai_interfaces.msg import Waypoint
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
                 all(isinstance(v, Waypoint) for v in value) and
                 True), \
                "The 'waypoints' field must be a set or sequence and each value of type 'Waypoint'"
        self._waypoints = value

    @builtins.property
    def scan_region(self):
        """Message field 'scan_region'."""
        return self._scan_region

    @scan_region.setter
    def scan_region(self, value):
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
                "The 'scan_region' field must be a set or sequence and each value of type 'Point'"
        self._scan_region = value

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

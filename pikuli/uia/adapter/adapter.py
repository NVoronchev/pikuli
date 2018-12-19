# -*- coding: utf-8 -*-

from pikuli import logger
from pikuli.uia import DriverException
from pikuli.utils import class_property

from .identifer_names import element_property_names, control_type_names
from .patterns_plain_description import patterns_plain_description
from .helper_types import IdNameMap
from .platform_init import OsAdapterMixin


class AdapterMixin(object):

    @class_property
    def Enums(cls):
        """
        Check enum values with the current API version.
        """
        return cls._enums

    @classmethod
    def get_property_id(cls, name):
        id_ = cls.try_get_property_id(name)
        if id_ is None:
            raise DriverException("Property {!r} is no available".format(name))
        return id_

    @classmethod
    def try_get_property_id(cls, name):
        return (cls._element_properties_map.try_name2id(name) or
                cls._properties_of_pattern_availability_map.try_name2id(name))

    @classmethod
    def get_control_type_id(cls, name):
        id_ = cls.try_get_control_type_id(name)
        if id_ is None:
            raise DriverException("Control Type {!r} is no available".format(name))
        return id_

    @classmethod
    def try_get_control_type_id(cls, name):
        return cls._control_type_map.try_name2id(name)

    @classmethod
    def get_control_type_name(cls, id_):
        name = cls._control_type_map.try_id2name(id_)
        if name is None:
            raise DriverException("Control Type id {!r} is no available".format(id_))
        return name

    @classmethod
    def get_pattern_id(cls, name):
        id_ = cls.try_get_pattern_id(name)
        if id_ is None:
            raise DriverException("Pattern {!r} is no available".format(name))
        return id_

    @classmethod
    def try_get_pattern_id(cls, name):
        return cls._patterns_map.try_name2id(name)

    """
    @classmethod
    def get_pattern_name(cls, id_):
        name = cls._patterns_map.try_id2name(id_)
        if name is None:
            raise DriverException("Pattern id {!r} is no available".format(id_))
        return name
    """

    @classmethod
    def get_api_property_names():
        """
        Returns all Propoperty names are known in current API.
        """
        return sorted(cls._element_properties_map.names())

    @classmethod
    def _build_map(cls, get_attr_from, name_format, err_msg_preamble, names):
        """
        Is used in derived classes :class:`mono.Adapter` and :class:`windows.Adapter`.
        """
        name2id = {}
        for name in names:
            api_name = name_format.format(name=name)
            id_ = getattr(get_attr_from, api_name, None)
            if id_ is None:
                logger.warning("{preamble} {name} ({api_name}) not exist in current UIA namespace".format(
                    preamble=err_msg_preamble, name=name, api_name=api_name))
                continue
            name2id[name] = id_
        return name2id


class AdapterMeta(type):

    def __new__(mcls, name, bases, dct):
        cls = super(AdapterMeta, mcls).__new__(mcls, name, bases, dct)

        """
        This code targets to :class:`mono.MonoAdapter` and :class:`windows.WinAdapter`.
        Build-function are defined in those classses.
        """
        cls._enums = cls._make_enums()

        cls._element_properties_map = IdNameMap(
            cls._build_properties_map, element_property_names)

        cls._properties_of_pattern_availability_map = IdNameMap(
            cls._build_properties_map,
            ["Is{pattern_name}Available".format(pattern_name=n) for n in patterns_plain_description])

        cls._control_type_map = IdNameMap(
            cls._build_control_types_map, control_type_names)

        cls._patterns_map = IdNameMap(
            cls._build_patterns_map, patterns_plain_description.keys())

        return cls


class Adapter(AdapterMixin, OsAdapterMixin):

    __metaclass__ = AdapterMeta

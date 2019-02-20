# -*- coding: utf-8 -*-

''' Пока что этот модуль -- прослойка для Sikuli.
    В перспективе мы сможем отказаться от Sikuli, дописывая только этот модуль

Doc pywin32:
    http://timgolden.me.uk/pywin32-docs/modules.html

Особенности использования памяти:
    -- При создании объекта Pattern, от сделает
       self._cv2_pattern = cv2.imread(self.getFilename())

'''

#SUPPORT_UIA = True

import os
import logging
import sys


logger = logging.getLogger('axxon.pikuli')
from .utils import basic_logger_config
basic_logger_config()

from ._SettingsClass import SettingsClass
Settings = SettingsClass()

from ._exceptions import FailExit, FindFailed
from ._functions import *  # TODO: remove it

from .geom.vector import Vector, RelativeVec
from .geom.region import Region
from .geom.location import Location, LocationF

from .Screen import Screen
from .Match import Match
from .Pattern import Pattern

if os.name == 'nt':
    from .hwnd.hwnd_element import HWNDElement

#if SUPPORT_UIA:
#    from .uia import UIAElement  # , AutomationElement
#    from .uia.control_wrappers import RegistredControlClasses
#    RegistredControlClasses._register_all()

try:
    Settings.addImagePath(
        os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)))
except Exception as e:
    logging.getLogger('axxon.pikuli').error(
        'Problem with addImagePath: {}'.format(e))

__all__ = [
    'Settings',
    'Region',
    'Screen',
    'Match',
    'Location',
    'LocationF',
    'Pattern',
    'FailExit',
    'FindFailed',
]  # TODO: shorter this list

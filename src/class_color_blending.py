'''
This file contains all for Class Color Blending
''' 

from enum import Enum


from funcs_errors import ErrorValueUnknown

from consts_sivf_keywords import *





class ColorBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2
    minimum = 3
    maximum = 4

    def from_str (s: str) -> 'ColorBlendingType':
        if s == KW_BLENDINGTYPE_DEFAULT:
            return ColorBlendingType.default

        elif s == KW_BLENDINGTYPE_OVERLAP:
            return ColorBlendingType.overlap

        elif s == KW_BLENDINGTYPE_ADD:
            return ColorBlendingType.add

        elif s == KW_BLENDINGTYPE_AVG:
            return ColorBlendingType.avg

        elif s == KW_BLENDINGTYPE_MIN:
            return ColorBlendingType.minimum

        elif s == KW_BLENDINGTYPE_MAX:
            return ColorBlendingType.maximum

        else:
            raise ErrorValueUnknown(s)




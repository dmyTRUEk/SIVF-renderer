'''
This file contains all for Class Alpha Blending
''' 

from enum import Enum


from funcs_errors import ErrorValueUnknown

from consts_sivf_keywords import *





class AlphaBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2

    def from_str (s: str) -> 'AlphaBlendingType':
        if s == KW_BLENDINGTYPE_DEFAULT:
            return AlphaBlendingType.default

        elif s == KW_BLENDINGTYPE_OVERLAP:
            return AlphaBlendingType.overlap

        elif s == KW_BLENDINGTYPE_ADD:
            return AlphaBlendingType.add

        elif s == KW_BLENDINGTYPE_AVG:
            return AlphaBlendingType.avg

        else:
            raise ErrorValueUnknown(s)




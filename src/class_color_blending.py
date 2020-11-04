'''
This file contains all for Class Color Blending
''' 



from enum import Enum





class ColorBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2

    def from_str (s: str) -> 'ColorBlendingType':
        if s == 'default':
            return ColorBlendingType.default

        elif s == 'overlap':
            return ColorBlendingType.overlap

        elif s == 'add':
            return ColorBlendingType.add

        elif s == 'avg':
            return ColorBlendingType.avg

        else:
            raise Exception(f'Error: Unsupported ColorBlendingType: {s}')




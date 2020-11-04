'''
This file contains all for Class Alpha Blending
''' 



from enum import Enum





class AlphaBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2

    def from_str (s: str) -> 'AlphaBlendingType':
        if s == 'default':
            return AlphaBlendingType.default

        elif s == 'overlap':
            return AlphaBlendingType.overlap

        elif s == 'add':
            return AlphaBlendingType.add

        elif s == 'avg':
            return AlphaBlendingType.avg

        else:
            raise Exception(f'Error: Unsupported AlphaBlendingType: {s}')




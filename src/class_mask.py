'''
This file contains all for Class Mask
''' 

import numpy as np


from funcs_errors import *
from funcs_warnings import *

from funcs_convert import c_rgbau_rgba





class Mask:
    '''
    For accessing pixels[y,x] use:
    - get: get_pixels
    - set: __init__ or Mask._pixels[y, x]

    _pixels = [[bool]]
    '''
    def __init__ (self, _canvas_w: int, _canvas_h: int, _pixels: 'nparray2d'=None):
        if (t:=type(_pixels)) != np.ndarray and _pixels != None:
            raise ErrorTypeWrong(_pixels, '_pixels', np.ndarray)

        elif type(_pixels) != np.ndarray and _pixels == None:
            _pixels = np.zeros((_canvas_h, _canvas_w), dtype=np.uint8)
        
        elif (t:=_pixels.ndim) != 2:
            raise ErrorNotEqual(t, 2, '_pixels.ndim', '2')

        elif (t:=_pixels.shape[0:2][::-1]) != (_canvas_w, _canvas_h):
            raise ErrorValuesNotEqual(t, _canvas_w, _canvas_h, '_pixels.shape[0:2][::-1]', '(_canvas_w, canvas_h)')

        # PUBLIC:
        self.w, self.h = _canvas_w, _canvas_h

        # PRIVATE:
        self._pixels = _pixels

    def get_pixels (self) -> 'nparray2d':
        return self._pixels




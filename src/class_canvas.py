'''
This file contains all for Class Canvas
''' 

import numpy as np


from funcs_errors import *
from funcs_warnings import *

from funcs_convert import c_rgbau_rgba





class Canvas:
    '''
    For accessing pixels use:
    - get: get_pixels
    - set: __init__ or blend_canvases

    _pixels = [[r, g, b, a, used]]
    '''
    def __init__ (self, _canvas_w: int, _canvas_h: int, _pixels: 'nparray2d'=None):
        if (t:=type(_pixels)) != np.ndarray and _pixels != None:
            raise ErrorTypeWrong(_pixels, '_pixels', np.ndarray)

        elif type(_pixels) != np.ndarray and _pixels == None:
            # 5 because: red, green, blue, alpha, used
            _pixels = np.zeros((_canvas_h, _canvas_w, 5), dtype=np.uint8)
        
        elif (t:=_pixels.ndim) != 3:
            raise ErrorNotEqual(t, 3, '_pixels.ndim', '3')

        elif (t:=_pixels.shape[0:2][::-1]) != (_canvas_w, _canvas_h):
            raise ErrorValuesNotEqual(t, _canvas_w, _canvas_h, '_pixels.shape[0:2][::-1]', '(_canvas_w, canvas_h)')

        # PUBLIC:
        self.w, self.h = _canvas_w, _canvas_h

        # PRIVATE:
        self._pixels = _pixels

    def get_pixels_rgbau (self) -> 'nparray2d: rgbau':
        return self._pixels

    def get_pixels_rgba (self) -> 'nparray2d: rgba':
        return c_rgbau_rgba(self.get_pixels_rgbau())




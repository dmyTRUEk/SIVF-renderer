'''
This file contains all for Class Canvas
''' 

import numpy as np


from funcs_errors import *
from funcs_warnings import *

from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import c_rgbau_rgba





class Canvas:
    '''
    For accessing pixels use:
    - get: get_pixels
    - set: __init__ or blend_canvases

    _pixels = [[r, g, b, a, used]]
    '''
    def __init__ (self, _canvas_wh: '(canvas_w, canvas_h)', _pixels: 'nparray2d'=None):
        if (t:=type(_pixels)) != np.ndarray and _pixels != None:
            raise ErrorWrongType(_pixels, '_pixels', np.ndarray)

        elif type(_pixels) != np.ndarray and _pixels == None:
            # 5 because: red, green, blue, alpha, used
            _pixels = np.zeros((_canvas_wh[1], _canvas_wh[0], 5), dtype=np.uint8)
        
        elif (t:=_pixels.ndim) != 3:
            raise ErrorNotEqual(t, 3, '_pixels.ndim', '3')

        elif (t:=_pixels.shape[0:2][::-1]) != _canvas_wh:
            # raise ValueError(f'_pixels sizes must be {_canvas_wh}, but it is {t}')

            raise ErrorValuesNotEqual(t, _canvas_wh, '_pixels.shape[0:2][::-1]', '_canvas_wh')

        # PUBLIC:
        self.wh = _canvas_wh
        self.w, self.h = _canvas_wh

        # PRIVATE:
        self._pixels = _pixels

    def get_pixels_rgbau (self) -> 'nparray2d: rgbau':
        return self._pixels

    def get_pixels_rgba (self) -> 'nparray2d: rgba':
        return c_rgbau_rgba(self.get_pixels_rgbau())




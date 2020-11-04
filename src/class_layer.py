'''
This file contains all for Class Layer
''' 



import numpy as np



from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import c_rgbau_rgba





class Layer:
    '''
    For accessing pixels use:
    - get: get_pixels
    - set: __init__ or blend_layers

    _pixels = [[[r, g, b, a, used]]]
    '''
    def __init__ (self, _layer_wh: '(layer_w, layer_h)', _pixels: 'nparray2d'=None):
        if (t:=type(_pixels)) != np.ndarray and _pixels != None:
            raise TypeError(f'_pixels must be numpy.ndarray, but it is {t}')

        elif type(_pixels) != np.ndarray and _pixels == None:
            # 5 because: r, g, b, a, used
            _pixels = np.zeros((_layer_wh[1], _layer_wh[0], 5), dtype=np.uint8)
        
        elif (t:=_pixels.ndim) != 3:
            raise ValueError('_pixels must be 3d (x, y, rgba) numpy array, but it is {t}d')

        elif (t:=_pixels.shape[0:2]) != _layer_wh:
            raise ValueError(f'_pixels sizes must be {_layer_wh}, but it is {t}')

        # PUBLIC:
        self.wh = _layer_wh
        self.w, self.h = _layer_wh
        # print(self.w, self.h)

        # PRIVATE:
        self._pixels = _pixels

    def get_pixels_rgbau (self) -> 'nparray2d: rgbau':
        return self._pixels

    def get_pixels_rgba (self) -> 'nparray2d: rgba':
        return c_rgbau_rgba(self.get_pixels_rgbau())




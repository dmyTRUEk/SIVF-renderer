'''
This file contains all heavy functions, that should be accelerated with Cython
''' 

import numpy as np
cimport numpy as np
import random
# from enum import Enum


from funcs_errors import *
from funcs_warnings import *
from funcs_log import *

from config import *
from consts_sivf_keywords import *

from class_mask import Mask
from class_canvas import Canvas
# from class_alpha_blending import AlphaBlendingType
# from class_color_blending import ColorBlendingType

from funcs_convert import *
from funcs_utils import *





cdef str CHECK_BOUNDS_OPTIMIZATION = 'Check bounds optimization'
cdef int C_OUTPUT_RENDER_PROGRESS_PERIOD = OUTPUT_RENDER_PROGRESS_PERIOD



# cdef class Canvas:
#     def __init__ (self, int _canvas_w, int _canvas_h,
#             np.ndarray[unsigned char, ndim=3, mode='c'] _pixels: 'nparray2d'=None):
#         if type(_pixels) != np.ndarray and _pixels != None:
#             raise ErrorWrongType(_pixels, '_pixels', np.ndarray)

#         elif type(_pixels) != np.ndarray and _pixels == None:
#             # 5 because: red, green, blue, alpha, used
#             _pixels = np.zeros((_canvas_wh[1], _canvas_wh[0], 5), dtype=np.uint8)
        
#         elif _pixels.ndim != 3:
#             raise ErrorNotEqual(_pixels.ndim, 3, '_pixels.ndim', '3')

#         WarningTodo()
#         # elif _pixels.shape[0:2][::-1] != _canvas_wh:
#         #     # raise ValueError(f'_pixels sizes must be {_canvas_wh}, but it is {t}')

#         #     raise ErrorValuesNotEqual(_pixels.shape[0:2][::-1],
#         #         _canvas_wh, '_pixels.shape[0:2][::-1]', '_canvas_wh')

#         # PUBLIC:
#         self.wh = _canvas_wh
#         self.w, self.h = _canvas_wh

#         # PRIVATE:
#         self._pixels = _pixels

#     cdef np.ndarray[unsigned char, ndim=3, mode='c'] get_pixels_rgbau (self):
#         return self._pixels

#     cdef np.ndarray[unsigned char, ndim=3, mode='c'] get_pixels_rgba (self):
#         return c_rgbau_rgba(self.get_pixels_rgbau())



cdef enum BlendingType:
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2
    minimum = 3
    maximum = 4

cdef BlendingType BlendingType_from_str (str s):
    if s == KW_BLENDINGTYPE_DEFAULT:
        return BlendingType.default

    elif s == KW_BLENDINGTYPE_OVERLAP:
        return BlendingType.overlap

    elif s == KW_BLENDINGTYPE_ADD:
        return BlendingType.add

    elif s == KW_BLENDINGTYPE_AVG:
        return BlendingType.avg

    elif s == KW_BLENDINGTYPE_MIN:
        return BlendingType.minimum

    elif s == KW_BLENDINGTYPE_MAX:
        return BlendingType.maximum

    else:
        raise ErrorValueUnknown(s)



# cpdef enum ColorBlendingType:
#     default = 0   # default is overlap
#     overlap = 0
#     add = 1
#     avg = 2
#     minimum = 3
#     maximum = 4

# cdef ColorBlendingType ColorBlendingType_from_str (str s):
#     if s == KW_BLENDINGTYPE_DEFAULT:
#         return ColorBlendingType.default

#     elif s == KW_BLENDINGTYPE_OVERLAP:
#         return ColorBlendingType.overlap

#     elif s == KW_BLENDINGTYPE_ADD:
#         return ColorBlendingType.add

#     elif s == KW_BLENDINGTYPE_AVG:
#         return ColorBlendingType.avg

#     elif s == KW_BLENDINGTYPE_MIN:
#         return ColorBlendingType.minimum

#     elif s == KW_BLENDINGTYPE_MAX:
#         return ColorBlendingType.maximum

#     else:
#         raise ErrorValueUnknown(s)



def debug_show_image (canvas: Canvas):
    '''This function is for testing and mustnt be used on release'''
    Warning('This function is for testing and mustnt be used on release')
    from PIL import Image
    Image.fromarray(canvas.get_pixels_rgba(), PIL_IMAGE_OUTPUT_MODE).show()



cpdef parse_and_render_entity (entity: dict, entity_name: str,
        int shape_number, int canvas_w, int canvas_h,
        defined_vars: dict, delta_x: int, delta_y: int, tabs: int):

    canvas_result = Canvas(canvas_w, canvas_h)

    alpha_blending_type = BlendingType.default
    color_blending_type = BlendingType.default

    # tabs += 1

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    #for      key      in  dict :
    for subentity_name in entity:
        # Log(f'{tabs = }')
        Log((tabs)*TAB+f'parsing {subentity_name}:')
        subentity = entity[subentity_name]

        tabs += 1

        if subentity_name.startswith(KW_BLENDING):   # blending
            alpha_blending_type = BlendingType_from_str(entity[KW_BLENDING][0])
            color_blending_type = BlendingType_from_str(entity[KW_BLENDING][1])
            # Log(f'{alpha_blending_type = }')
            # Log(f'{color_blending_type = }')

        elif subentity_name.startswith(KW_LAYER):   # layer
            # tabs += 1
            canvas_layer = parse_and_render_entity(
                subentity, subentity_name, shape_number,
                canvas_w, canvas_h, defined_vars, 0, 0, tabs
            )
            # tabs -= 1
            canvas_result = blend_canvases(
                canvas_result, canvas_layer, shape_number,
                alpha_blending_type, color_blending_type,
                delta_x, delta_y, tabs,
            )

        elif subentity_name.startswith(KW_LAYER_DELTA_XY):
            delta_x = +int( cetu(subentity[0], canvas_wh, defined_vars) )
            delta_y = -int( cetu(subentity[1], canvas_wh, defined_vars) )
            # delta_x, delta_y = delta_x, delta_y

        # elif subentity_name.startswith(KW_COMBINE):
        #     raise ErrorNotImpemented(f'{KW_COMBINE}')

        elif subentity_name.startswith(KW_MESH):   # mesh
            raise ErrorNotImpemented(f'{KW_MESH}')

            entity_layer_repeated = subentity[KW_LAYER]
            n_xleft_ydown_xright_yup = subentity[KW_MESH_N_XLEFT_YDOWN_XRIGHT_YUP]
            nxyxy = n_xleft_ydown_xright_yup   # for shorteness
            nxyxy = (
                int(cetu(nxyxy[0], canvas_wh, defined_vars)),
                int(cetu(nxyxy[1], canvas_wh, defined_vars)),
                int(cetu(nxyxy[2], canvas_wh, defined_vars)),
                int(cetu(nxyxy[3], canvas_wh, defined_vars))
            )
            _delta_xy_str = subentity[KW_LAYER_DELTA_XY]

            _delta_x = cetu(_delta_xy_str[0], canvas_wh, defined_vars)
            _delta_y = cetu(_delta_xy_str[1], canvas_wh, defined_vars)

            tabs += 1
            for h in range(-nxyxy[1], nxyxy[3]+1):
                for w in range(-nxyxy[0], nxyxy[2]+1):
                    Log((tabs)*TAB+f'parsing mesh[{w}][{h}]:')
                    tabs += 1
                    parse_and_render_entity(
                        entity_layer_repeated,
                        KW_LAYER,
                        shape_number,
                        canvas_wh,
                        (w*_delta_x, h*_delta_y)
                    )
                    tabs -= 1
            tabs -= 1

        #elif ...:   # other special entities

        else:   # shape
            canvas_shape = parse_and_render_shape(
                subentity, subentity_name, shape_number,
                canvas_w, canvas_h, defined_vars,
                alpha_blending_type, color_blending_type,
                tabs
            )
            canvas_result = blend_canvases(
                canvas_result, canvas_shape, shape_number,
                alpha_blending_type, color_blending_type,
                delta_x, delta_y, tabs
            )

        tabs -= 1

    return canvas_result

    # end of parse_and_render_entity()



def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        canvas_w, canvas_h, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        tabs: int=0) -> Canvas:

    # tabs += 1
    Log((tabs)*TAB+f'rendering {shape_name}:')

    tabs += 1
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    Log((tabs)*TAB+f'{KW_INVERSE} = {inverse}')

    if KW_COLOR in shape:
        a, r, g, b = cctargb(shape[KW_COLOR][1:])
        # Log((tabs)*TAB+f'{a=}, {r=}, {g=}, {b=}')
        # print((tabs)*TAB + f'{a=} ' + f'{r=} ' + f'{g=} ' + f'{b=} ')
        print('[LOG]: ' + (tabs)*TAB + 'a='+str(a) + ', r='+str(r) + ', g='+str(g) + ', b='+str(b))

    canvas_w, canvas_h = canvas_w, canvas_h
    canvas_result = Canvas(canvas_w, canvas_h)

    tabs += 1

    if shape_name.startswith(KW_CIRCLE):        # circle
        canvas_result = parse_and_render_circle(shape, canvas_w, canvas_h, defined_vars, tabs)
    
    elif shape_name.startswith(KW_SQUARE):      # square
        canvas_result = parse_and_render_square(shape, canvas_w, canvas_h, defined_vars, tabs)

    elif shape_name.startswith(KW_TRIANGLE):    # triangle
        canvas_result = parse_and_render_triangle(shape, canvas_w, canvas_h, defined_vars, tabs)

    elif shape_name.startswith(KW_GRADIENT):    # gradient
        canvas_result = parse_and_render_gradient(shape, canvas_w, canvas_h, defined_vars, tabs)

    elif shape_name.startswith(KW_COMBINE):     # combine
        canvas_result = parse_and_render_combine(shape, canvas_w, canvas_h, defined_vars, tabs)

    else:
        raise ErrorValueUnknown(f"'{shape_name}'", 'Unknown shape')

    return canvas_result

    # end of parse_and_render_shape()



cpdef render_mask_circle (int canvas_w, int canvas_h, float radius, float tx, float ty, bint inverse, int tabs):

    # TODO: make this BOOL array: bint, np.bool
    cdef np.ndarray[unsigned char, ndim=2, mode='c'] pixels = np.zeros((canvas_h, canvas_w), dtype=np.uint8)

    cdef float radius2 = radius**2
    cdef int x, y

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse:
                pixels[y, x] = True
            else:
                pixels[y, x] = False

    mask_result = Mask(canvas_w, canvas_h, pixels)
    return mask_result

cpdef render_canvas_circle (int canvas_w, int canvas_h, mask, unsigned char a, unsigned char r, unsigned char g, unsigned char b, int tabs):

    cdef np.ndarray[unsigned char, ndim=2, mode='c'] pixels_mask = mask._pixels
    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels = np.zeros((canvas_h, canvas_w, 5), dtype=np.ubyte)

    cdef int x, y

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if pixels_mask[y, x]:
                pixels[y, x, 0] = r
                pixels[y, x, 1] = g
                pixels[y, x, 2] = b
                pixels[y, x, 3] = a
                pixels[y, x, 4] = True

    canvas_result = Canvas(canvas_w, canvas_h, pixels)
    return canvas_result

cpdef parse_and_render_circle (dict shape, int canvas_w, int canvas_h,
        dict defined_vars, int tabs):

    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    cdef int x0 =  cetu(shape[KW_XY][0], canvas_w, canvas_h, defined_vars)
    cdef int y0 = -cetu(shape[KW_XY][1], canvas_w, canvas_h, defined_vars)
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    radius = cetu(shape[KW_CIRCLE_R], canvas_w, canvas_h, defined_vars)
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')
        # ErrorValueWrong(shape[KW_USED], 'must not be in this shape')
        # used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT

    # +1/2 for pixel perfect
    tx = -canvas_w/2 - x0 + 1/2
    ty = -canvas_h/2 - y0 + 1/2

    mask = render_mask_circle(canvas_w, canvas_h, radius, tx, ty, inverse, tabs)
    canvas_result = render_canvas_circle(canvas_w, canvas_h, mask, a, r, g, b, tabs)

    return canvas_result
    # end of parse_and_render_circle()



def render_mask_square (canvas_w, canvas_h,
        side: float, x0: float, y0: float,
        inverse: bool, tabs: int) -> Mask:
    canvas_w, canvas_h = canvas_w, canvas_h

    tx = -canvas_w/2
    ty = -canvas_h/2
    x_min = x0 - side/2
    y_min = y0 - side/2
    x_max = x0 + side/2
    y_max = y0 + side/2

    mask_result = Mask(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse:
                mask_result._pixels[y, x] = True
            else:
                mask_result._pixels[y, x] = False

    return mask_result

def render_canvas_square (canvas_w, canvas_h,
        mask: Mask, color: '(a, r, g, b)', tabs: int) -> Canvas:
    canvas_w, canvas_h = canvas_w, canvas_h
    a, r, g, b = color

    canvas_result = Canvas(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if mask._pixels[y, x]:
                canvas_result._pixels[y, x] = [
                    r,
                    g,
                    b,
                    a,
                    True
                ]
    return canvas_result

def parse_and_render_square (shape: dict, canvas_w, canvas_h,
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_w, canvas_h
    color = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    x0 =  cetu(shape[KW_XY][0], canvas_w, canvas_h, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_w, canvas_h, defined_vars)
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    side = cetu(shape[KW_SQUARE_SIDE], canvas_w, canvas_h, defined_vars)
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')
        # ErrorValueWrong(shape[KW_USED], 'must not be in this shape')
        # used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT

    mask = render_mask_square(canvas_w, canvas_h, side, x0, y0, inverse, tabs)
    canvas_result = render_canvas_square(canvas_w, canvas_h, mask, color, tabs)

    return canvas_result
    # end of parse_and_render_circle()



def render_mask_triangle (canvas_w, canvas_h,
        x1: float, y1: float, x2: float, y2: float, x3: float, y3: float,
        inverse: bool, tabs: int) -> Mask:
    canvas_w, canvas_h = canvas_w, canvas_h

    # +1/2 for pixel perfect
    tx = -canvas_w/2
    ty = -canvas_h/2

    mask_result = Mask(canvas_w, canvas_h)

    def _triangle_sign (x1: float, y1: float,
            x2: float, y2: float, x3: float, y3: float) -> float:
        return (x1-x3)*(y2-y3) - (x2-x3)*(y1-y3)

    def _is_inside_triangle (x: float, y: float, x1: float, y1: float,
            x2: float, y2: float, x3: float, y3: float) -> bool:
        d1 = _triangle_sign(x, y, x1, y1, x2, y2)
        d2 = _triangle_sign(x, y, x2, y2, x3, y3)
        d3 = _triangle_sign(x, y, x3, y3, x1, y1)
        #has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        #has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        #return not (has_neg and has_pos)
        return not ( ((d1 < 0) or (d2 < 0) or (d3 < 0)) and ((d1 > 0) or (d2 > 0) or (d3 > 0)) )

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if _is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse:
                mask_result._pixels[y, x] = True
            else:
                mask_result._pixels[y, x] = False

    return mask_result

def render_canvas_triangle (canvas_w, canvas_h,
        mask: Mask, color: '(a, r, g, b)', tabs: int) -> Canvas:
    canvas_w, canvas_h = canvas_w, canvas_h
    a, r, g, b = color

    canvas_result = Canvas(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            if mask._pixels[y, x]:
                canvas_result._pixels[y, x] = [
                    r,
                    g,
                    b,
                    a,
                    True
                ]
    return canvas_result

def parse_and_render_triangle (shape: dict, canvas_w, canvas_h,
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_w, canvas_h
    color = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    x1 =  cetu(shape[KW_XY][0], canvas_w, canvas_h, defined_vars)
    y1 = -cetu(shape[KW_XY][1], canvas_w, canvas_h, defined_vars)
    x2 =  cetu(shape[KW_XY][2], canvas_w, canvas_h, defined_vars)
    y2 = -cetu(shape[KW_XY][3], canvas_w, canvas_h, defined_vars)
    x3 =  cetu(shape[KW_XY][4], canvas_w, canvas_h, defined_vars)
    y3 = -cetu(shape[KW_XY][5], canvas_w, canvas_h, defined_vars)
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')
        # ErrorValueWrong(shape[KW_USED], 'must not be in this shape')
        # used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT

    mask = render_mask_triangle(canvas_w, canvas_h, x1, y1, x2, y2, x3, y3, inverse, tabs)
    canvas_result = render_canvas_triangle(canvas_w, canvas_h, mask, color, tabs)

    return canvas_result
    # end of parse_and_render_circle()



def parse_and_render_gradient (shape: dict, canvas_w, canvas_h,
        defined_vars: dict, tabs: int=0) -> Canvas:
    canvas_w, canvas_h = canvas_w, canvas_h

    if KW_INVERSE in shape:
        raise ErrorValueWrong(shape[KW_INVERSE], f'{KW_INVERSE} mustnt be in {KW_GRADIENT}')

    A, R, G, B = cctargb(shape[KW_COLOR][1:])
    # Log(f'{A=}, {R=}, {G=}, {B=}')

    x0 =  cetu(shape[KW_XY][0], canvas_w, canvas_h, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_w, canvas_h, defined_vars)
    is_fading = (shape[KW_GRADIENT_FADING] == KW_TRUE) if KW_GRADIENT_FADING in shape else KW_GRADIENT_FADING_DEFAULT
    points_json = shape[KW_GRADIENT_POINTS]
    used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT
    # Log(points_json)

    class Point:
        def __init__ (self, x: float, y: float, sigma: float, color: '(a, r, g, b)'):
            self.x = x
            self.y = y
            self.sigma = sigma
            self.color = color

        def __repr__ (self):
            return f'Point(x={self.x}, y={self.y}, color={self.color})'

    points = []
    for key_point_json in points_json:
        point_json = points_json[key_point_json]
        # Log(point_json)
        points.append(
            Point(
                +cetu(point_json[KW_XY][0], canvas_w, canvas_h, defined_vars),
                -cetu(point_json[KW_XY][1], canvas_w, canvas_h, defined_vars),
                cetu(point_json[KW_GRADIENT_SIGMA], canvas_w, canvas_h, defined_vars),
                cctargb(point_json[KW_COLOR][1:])
            )
        )
    # Log(points)

    def _render_gradient () -> Canvas:
        def _dist (dx: float, dy: float):
            return sqrt(dx**2 + dy**2)

        def _gauss (dist: float, sigma: float):
            return exp(-(dist)**2 / (2 * sigma**2))

        # precalculations
        tx = -canvas_w/2 - x0 + 1/2
        ty = -canvas_h/2 - y0 + 1/2
        
        _canvas = Canvas(canvas_w, canvas_h)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        gausses = []

        if is_fading:   # is_fading == True
            for y in range(canvas_h):
                if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                    Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
                for x in range(canvas_w):
                    gausses = []
                    for point in points:
                        gausses.append(_gauss( _dist(point.x-(x+tx), -point.y+(y+ty)), point.sigma ))
                    gausses_sum = sum(gausses)

                    a, r, g, b = 0, 0, 0, 0
                    for i in range(len(gausses)):
                        k = gausses[i]
                        a += k * points[i].color[0]
                        r += k * points[i].color[1]
                        g += k * points[i].color[2]
                        b += k * points[i].color[3]

                    # include fading:
                    k = 1 - gausses_sum
                    a += k * A
                    r += k * R
                    g += k * G
                    b += k * B

                    # if random.randint(0, 10**3) < 1:
                    #     Log(f'{gausses=}')
                    #     Log(f'{a=}, {r=}, {g=}, {b=}')
                    #     Log()

                    _canvas._pixels[y, x] = [ r, g, b, a, True ]

        else:   # is_fading == False
            for y in range(canvas_h):
                if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                    Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
                for x in range(canvas_w):
                    gausses = []
                    for point in points:
                        gausses.append(_gauss( _dist(point.x-(x+tx), -point.y+(y+ty)), point.sigma ))
                    gausses_sum = sum(gausses)

                    a, r, g, b = 0, 0, 0, 0
                    for i in range(len(gausses)):
                        k = gausses[i] / gausses_sum
                        a += k * points[i].color[0]
                        r += k * points[i].color[1]
                        g += k * points[i].color[2]
                        b += k * points[i].color[3]

                    # if random.randint(0, 10**3) < 1:
                    #     Log(f'{gausses=}')
                    #     Log(f'{a=}, {r=}, {g=}, {b=}')
                    #     Log()

                    _canvas._pixels[y, x] = [ r, g, b, a, True ]

        return _canvas
        # end of _render_gradient()

    canvas_result = _render_gradient()
    return canvas_result
    # end of parse_and_render_gradient()



ctypedef int (*func_2int2bint_int) (int, int, bint, bint)
ctypedef bint (*func_2bint_bint) (bint, bint)

cdef int _combine_value_1plus2 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return v1
    elif used1 and not used2:
        return v1
    elif not used1 and used2:
        return v2
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_1plus2 (bint used1, bint used2):
    return used1 or used2

cdef int _combine_value_2plus1 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return v2
    elif used1 and not used2:
        return v1
    elif not used1 and used2:
        return v2
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_2plus1 (bint used1, bint used2):
    return used1 or used2


cdef int _combine_value_1minus2 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return 0
    elif used1 and not used2:
        return v1
    elif not used1 and used2:
        return 0
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_1minus2 (bint used1, bint used2):
    return (used1) and (not used2)

cdef int _combine_value_2minus1 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return 0
    elif used1 and not used2:
        return 0
    elif not used1 and used2:
        return v2
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_2minus1 (bint used1, bint used2):
    return (not used1) and (used2)


cdef int _combine_value_1product2 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return v1
    elif used1 and not used2:
        return 0
    elif not used1 and used2:
        return 0
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_1product2 (bint used1, bint used2):
    return (used1) and (used2)

cdef int _combine_value_2product1 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return v2
    elif used1 and not used2:
        return 0
    elif not used1 and used2:
        return 0
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_2product1 (bint used1, bint used2):
    return (used1) and (used2)


cdef int _combine_value_1symdiff2 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return 0
    elif used1 and not used2:
        return v1
    elif not used1 and used2:
        return v2
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_1symdiff2 (bint used1, bint used2):
    return used1 ^ used2

cdef int _combine_value_2symdiff1 (int v1, int v2, bint used1, bint used2):
    if used1 and used2:
        return 0
    elif used1 and not used2:
        return v1
    elif not used1 and used2:
        return v2
    else:   # not used1 and not used2
        return 0
cdef bint _combine_used_2symdiff1 (bint used1, bint used2):
    return used1 ^ used2



cpdef parse_and_render_combine (dict shape, int canvas_w, int canvas_h,
        dict defined_vars, int tabs=0):
    # canvas_w, canvas_h = canvas_w, canvas_h

    # if KW_INVERSE in shape:
    #     raise ErrorValueWrong(shape[KW_INVERSE], f'{KW_INVERSE} mustnt be in {KW_COMBINE}')

    # if KW_COMBINE_TYPE not in shape:
    #     raise ErrorValueWrong(f'{KW_COMBINE_TYPE} must be provided')
    combine_type_str = shape[KW_COMBINE_TYPE]

    cdef int combine_type = 0
    if combine_type_str == KW_COMBINE_TYPE_1PLUS2:
        combine_type = 0
    elif combine_type_str == KW_COMBINE_TYPE_2PLUS1:
        combine_type = 1
    elif combine_type_str == KW_COMBINE_TYPE_1MINUS2:
        combine_type = 2
    elif combine_type_str == KW_COMBINE_TYPE_2MINUS1:
        combine_type = 3
    elif combine_type_str == KW_COMBINE_TYPE_1PRODUCT2:
        combine_type = 4
    elif combine_type_str == KW_COMBINE_TYPE_2PRODUCT1:
        combine_type = 5
    elif combine_type_str == KW_COMBINE_TYPE_1SYMDIFF2:
        combine_type = 6
    elif combine_type_str == KW_COMBINE_TYPE_2SYMDIFF1:
        combine_type = 7
    # Log(f'{combine_type = }')

    # if KW_COMBINE_FIGURES not in shape:
    #     raise ErrorValueWrong(f'{KW_COMBINE_FIGURES} must be provided')
    combine_figures = shape[KW_COMBINE_FIGURES]

    canvases = []
    for subentity_name in combine_figures:
        if not subentity_name.startswith(KW_LAYER):
            raise ErrorValueWrong(f'must be {KW_LAYER}')
        # Log(combine_figures[subentity_name])

        canvases.append(
            parse_and_render_entity(
                combine_figures[subentity_name],
                subentity_name, 0, canvas_w, canvas_h,
                defined_vars, 0, 0, tabs,
            )
        )

    # combine_value_funcs = {
    #     KW_COMBINE_TYPE_1PLUS2: _combine_value_1plus2,
    #     KW_COMBINE_TYPE_2PLUS1: _combine_value_2plus1,
    #     KW_COMBINE_TYPE_1MINUS2: _combine_value_1minus2,
    #     KW_COMBINE_TYPE_2MINUS1: _combine_value_2minus1,
    #     KW_COMBINE_TYPE_1PRODUCT2: _combine_value_1product2,
    #     KW_COMBINE_TYPE_2PRODUCT1: _combine_value_2product1,
    #     KW_COMBINE_TYPE_1SYMDIFF2: _combine_value_1symdiff2,
    #     KW_COMBINE_TYPE_2SYMDIFF1: _combine_value_2symdiff1,
    # }
    cdef func_2int2bint_int[8] combine_value_funcs = (
        _combine_value_1plus2,
        _combine_value_2plus1,
        _combine_value_1minus2,
        _combine_value_2minus1,
        _combine_value_1product2,
        _combine_value_2product1,
        _combine_value_1symdiff2,
        _combine_value_2symdiff1,
    )

    # combine_used_funcs = {
    #     KW_COMBINE_TYPE_1PLUS2: _combine_used_1plus2,
    #     KW_COMBINE_TYPE_2PLUS1: _combine_used_2plus1,
    #     KW_COMBINE_TYPE_1MINUS2: _combine_used_1minus2,
    #     KW_COMBINE_TYPE_2MINUS1: _combine_used_2minus1,
    #     KW_COMBINE_TYPE_1PRODUCT2: _combine_used_1product2,
    #     KW_COMBINE_TYPE_2PRODUCT1: _combine_used_2product1,
    #     KW_COMBINE_TYPE_1SYMDIFF2: _combine_used_1symdiff2,
    #     KW_COMBINE_TYPE_2SYMDIFF1: _combine_used_2symdiff1,
    # }
    cdef func_2bint_bint[8] combine_used_funcs = (
        _combine_used_1plus2,
        _combine_used_2plus1,
        _combine_used_1minus2,
        _combine_used_2minus1,
        _combine_used_1product2,
        _combine_used_2product1,
        _combine_used_1symdiff2,
        _combine_used_2symdiff1,
    )

    # if combine_type not in combine_value_funcs:
    #     raise ErrorValueUnknown(f'{combine_type} is unknown for combine type')

    cdef int a1, r1, g1, b1
    cdef int a2, r2, g2, b2
    cdef bint USED, used
    cdef int i, x, y

    # pixelses = []
    # for i in range(len(canvases)):
    #     pixelses.append(canvases[i].get_pixels_rgbau())

    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels_result = canvases[0]._pixels
    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels_fg

    Log((tabs)*TAB+'combining:')
    tabs += 1
    for i in range(1, len(canvases)):
        pixels_fg = canvases[i].get_pixels_rgbau()
        for y in range(canvas_h):
            if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
            for x in range(canvas_w):
                # color_1 = canvas_result._pixels[y, x]
                # color_2 = canvases[i]._pixels[y, x]
                # r1, g1, b1, a1, used1 = color_1
                # r2, g2, b2, a2, used2 = color_2

                r1    = pixels_result[y, x, 0]
                g1    = pixels_result[y, x, 1]
                b1    = pixels_result[y, x, 2]
                a1    = pixels_result[y, x, 3]
                used1 = pixels_result[y, x, 4]

                r2    = pixels_fg[y, x, 0]
                g2    = pixels_fg[y, x, 1]
                b2    = pixels_fg[y, x, 2]
                a2    = pixels_fg[y, x, 3]
                used2 = pixels_fg[y, x, 4]

                pixels_result[y, x, 0] = combine_value_funcs[combine_type](r1, r2, used1, used2)
                pixels_result[y, x, 1] = combine_value_funcs[combine_type](g1, g2, used1, used2)
                pixels_result[y, x, 2] = combine_value_funcs[combine_type](b1, b2, used1, used2)
                pixels_result[y, x, 3] = combine_value_funcs[combine_type](a1, a2, used1, used2)
                pixels_result[y, x, 4] = combine_used_funcs[combine_type](used1, used2)
                
    canvas_result = Canvas(canvas_w, canvas_h, pixels_result)
    return canvas_result
    # ErrorNotImpemented('parse_and_render_combine')
    # end of parse_and_render_combine()



ctypedef int (*func_3int2bint_int) (int, int, bint, bint, int)

cdef int _blend_overlap (int V, int v, bint USED, bint used, int shape_number):
    if used:
        return v
    else:
        return V

cdef int _blend_add (int V, int v, bint USED, bint used, int shape_number):
    return V + v

cdef int _blend_avg (int V, int v, bint USED, bint used, int shape_number):
    return (shape_number*V + v) // (shape_number+1)

cdef int _blend_min (int V, int v, bint USED, bint used, int shape_number):
    if USED and used:
        return min(V, v)
    elif USED:
        return V
    elif used:
        return v
    else:
        return V

cdef int _blend_max (int V, int v, bint USED, bint used, int shape_number):
    if USED and used:
        return max(V, v)
    elif USED:
        return V
    elif used:
        return v
    else:
        return V



cpdef blend_canvases (canvas_bg, canvas_fg,
        int shape_number,
        BlendingType alpha_blending_type,
        BlendingType color_blending_type,
        delta_x: int, delta_y: int, tabs: int):

    # t = type(canvas_bg)
    # if (t) != Canvas:
    #     raise ErrorTypeWrong(t, 'canvas_bg', Canvas)

    # t = type(canvas_fg)
    # if (t) != Canvas:
    #     raise ErrorTypeWrong(t, 'canvas_fg', Canvas)

    # Log('--------------------- started blending ---------------------')
    Log((tabs)*TAB+'blending canvases:')
    tabs += 1
    # Log()


    # Log('showing canvas_bg:'); tmp_show_image(canvas_bg)
    # Log('showing canvas_fg:'); tmp_show_image(canvas_fg)

    # Log(f'{canvas_bg._pixels = }')
    # Log(f'{canvas_fg._pixels = }')

    # cdef int[5] tmp_5int = [1, 2, 3, 4, 5]

    # cpdef blending_funcs = {
    #     BlendingType.overlap: _blend_overlap,
    #     BlendingType.add: _blend_add,
    #     BlendingType.avg: _blend_avg,
    #     BlendingType.minimum: _blend_min,
    #     BlendingType.maximum: _blend_max,
    # }
    # blending_funcs = (
    cdef func_3int2bint_int[5] blending_funcs = (
        _blend_overlap,
        _blend_add,
        _blend_avg,
        _blend_min,
        _blend_max,
    )

    # delta_x, delta_y = delta_xy

    # old bounds for blending
    # x_from = delta_x - canvas_fg.w//2
    # y_from = delta_y - canvas_fg.h//2
    # x_to = canvas_bg.w // 2
    # y_to = canvas_bg.h // 2

    cdef int canvas_w = canvas_bg.w
    cdef int canvas_h = canvas_bg.h

    cdef int x_from = 0
    cdef int y_from = 0
    cdef int x_to = canvas_w
    cdef int y_to = canvas_h

    canvas_result = Canvas(canvas_w, canvas_h, canvas_bg.get_pixels_rgbau())

    WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

    cdef int A, R, G, B
    cdef int a, r, g, b
    cdef bint USED, used
    cdef int x, y
    # cdef unsigned char[5] color_bg, color_fg

    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels_bg = canvas_bg._pixels
    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels_fg = canvas_fg._pixels
    cdef np.ndarray[unsigned char, ndim=3, mode='c'] pixels_result = pixels_bg

    for y in range(y_from, y_to):
        if y % C_OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(y_to-y_from)}%')
        for x in range(x_from, x_to):
            # if not (0 <= x-delta_x < canvas_fg.w) or not (0 <= y-delta_y < canvas_fg.h):
                # if x or y of foreground not in its bounds, skip this x,y
                # continue

            # color_bg = pixels_bg[y, x]
            # color_fg = pixels_fg[y-delta_y, x-delta_x]

            # R, G, B, A, USED = color_bg     # BACKGROUND
            R    = pixels_bg[y, x, 0]
            G    = pixels_bg[y, x, 1]
            B    = pixels_bg[y, x, 2]
            A    = pixels_bg[y, x, 3]
            USED = pixels_bg[y, x, 4]

            # r, g, b, a, used = color_fg     # foreground
            r    = pixels_fg[y, x, 0]
            g    = pixels_fg[y, x, 1]
            b    = pixels_fg[y, x, 2]
            a    = pixels_fg[y, x, 3]
            used = pixels_fg[y, x, 4]

            # canvas_result._pixels[y, x] = [
            #     blending_funcs[color_blending_type.value](R, r, USED, used, shape_number),
            #     blending_funcs[color_blending_type.value](G, g, USED, used, shape_number),
            #     blending_funcs[color_blending_type.value](B, b, USED, used, shape_number),
            #     blending_funcs[alpha_blending_type.value](A, a, USED, used, shape_number),
            #     USED or used
            # ]
            pixels_result[y, x, 0] = blending_funcs[int(color_blending_type)](R, r, USED, used, shape_number)
            pixels_result[y, x, 1] = blending_funcs[int(color_blending_type)](G, g, USED, used, shape_number)
            pixels_result[y, x, 2] = blending_funcs[int(color_blending_type)](B, b, USED, used, shape_number)
            pixels_result[y, x, 3] = blending_funcs[int(alpha_blending_type)](A, a, USED, used, shape_number)
            pixels_result[y, x, 4] = USED or used

            # if random.randint(0, 10**3) < 1:
            #     Log(f'{canvas_blend._pixels[y, x]}')

    canvas_result = Canvas(canvas_w, canvas_h, pixels_result)
    return canvas_result

    # end of blend_canvases




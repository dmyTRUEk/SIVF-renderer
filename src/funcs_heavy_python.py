'''
This file contains all heavy functions, that should be accelerated with Cython
''' 

import numpy as np
import random
from math import exp, sqrt
from functools import cache


from funcs_errors import *
from funcs_warnings import *
from funcs_log import *

from config import *
from consts_sivf_keywords import *

from class_mask import Mask
from class_canvas import Canvas
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

import funcs_utils





CHECK_BOUNDS_OPTIMIZATION = 'Check bounds optimization'



def debug_show_image (canvas: Canvas):
    '''This function is for testing and mustnt be used on release'''
    Warning('This function is for testing and mustnt be used on release')
    from PIL import Image
    Image.fromarray(canvas.get_pixels_rgba(), PIL_IMAGE_OUTPUT_MODE).show()



def parse_and_render_entity (entity: dict,
        canvas_w: int, canvas_h: int, delta_x: int, delta_y: int,
        defined_vars: dict, shape_number: int, tabs: int) -> Canvas:

    canvas_result = Canvas(canvas_w, canvas_h)

    alpha_blending_type = AlphaBlendingType.default
    color_blending_type = ColorBlendingType.default

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    #for      key      in  dict :
    for subentity_name in entity:
        # Log(f'{tabs = }')
        Log((tabs)*TAB+f'parsing {subentity_name}:')
        subentity = entity[subentity_name]

        tabs += 1

        time_begin = funcs_utils.get_current_time()

        if subentity_name == KW_BLENDING:   # blending
            alpha_blending_type, color_blending_type = entity[KW_BLENDING]
            # Log(f'{alpha_blending_type = }')
            # Log(f'{color_blending_type = }')

        elif subentity_name.startswith(KW_LAYER):   # layer
            canvas_layer = parse_and_render_entity( subentity, canvas_w, canvas_h, 0, 0, defined_vars, shape_number, tabs)
            canvas_result = blend_canvases(
                canvas_result, canvas_layer, shape_number,
                alpha_blending_type, color_blending_type,
                delta_x, delta_y, tabs,
            )

        elif subentity_name == KW_LAYER_DELTA_XY:
            delta_x, delta_y = entity[KW_LAYER_DELTA_XY]
            Log((tabs)*TAB+f'{delta_x=}, {delta_y=}')

        # elif subentity_name.startswith(KW_COMBINE):
        #     raise ErrorNotImpemented(f'{KW_COMBINE}')

        elif subentity_name.startswith(KW_MESH):   # mesh
            raise ErrorNotImpemented(f'{KW_MESH}')

            # entity_layer_repeated = subentity[KW_LAYER]
            # n_xleft_ydown_xright_yup = subentity[KW_MESH_N_XLEFT_YDOWN_XRIGHT_YUP]
            # nxyxy = n_xleft_ydown_xright_yup   # for shorteness
            # nxyxy = (
            #     int(cetu(nxyxy[0], canvas_w, canvas_h, defined_vars)),
            #     int(cetu(nxyxy[1], canvas_w, canvas_h, defined_vars)),
            #     int(cetu(nxyxy[2], canvas_w, canvas_h, defined_vars)),
            #     int(cetu(nxyxy[3], canvas_w, canvas_h, defined_vars))
            # )
            # _delta_xy_str = subentity[KW_LAYER_DELTA_XY]

            # _delta_x = cetu(_delta_xy_str[0], canvas_w, canvas_h, defined_vars)
            # _delta_y = cetu(_delta_xy_str[1], canvas_w, canvas_h, defined_vars)

            # tabs += 1
            # for h in range(-nxyxy[1], nxyxy[3]+1):
            #     for w in range(-nxyxy[0], nxyxy[2]+1):
            #         Log((tabs)*TAB+f'parsing mesh[{w}][{h}]:')
            #         tabs += 1
            #         parse_and_render_entity(
            #             entity_layer_repeated,
            #             KW_LAYER,
            #             shape_number,
            #             canvas_w, canvas_h,
            #             (w*_delta_x, h*_delta_y)
            #         )
            #         tabs -= 1
            # tabs -= 1

        #elif ...:   # other special entities

        else:   # shape
            time_begin_shape = funcs_utils.get_current_time()
            canvas_shape = parse_and_render_shape(
                subentity, subentity_name, shape_number,
                canvas_w, canvas_h, defined_vars,
                alpha_blending_type, color_blending_type,
                tabs
            )
            time_end_shape = funcs_utils.get_current_time()
            Log((tabs+2)*TAB+f'time elapsed for shape: {funcs_utils.delta_time(time_begin_shape, time_end_shape)} s')

            time_begin_blend = funcs_utils.get_current_time()
            canvas_result = blend_canvases(
                canvas_result, canvas_shape, shape_number,
                alpha_blending_type, color_blending_type,
                delta_x, delta_y, tabs
            )
            time_end_blend = funcs_utils.get_current_time()
            Log((tabs+1)*TAB+f'time elapsed for blending: {funcs_utils.delta_time(time_begin_blend, time_end_blend)} s')

        timer_end = funcs_utils.get_current_time()

        Log((tabs+1)*TAB+f'time elapsed totally for {subentity_name}: {funcs_utils.delta_time(time_begin, timer_end)} s')

        tabs -= 1

    # debug_show_image(canvas_result)

    return canvas_result

    # end of parse_and_render_entity()



def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        canvas_w: int, canvas_h: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        tabs: int) -> Canvas:

    Log((tabs)*TAB+f'rendering {shape_name}:')

    tabs += 1

    if KW_INVERSE in shape:
        inverse = shape[KW_INVERSE]
    else:
        inverse = KW_INVERSE_DEFAULT
    Log((tabs)*TAB+f'{KW_INVERSE} = {inverse}')

    # if KW_COLOR in shape:
    #     a, r, g, b = shape[KW_COLOR]
    #     Log((tabs)*TAB+f'{a, r, g, b = }')

    canvas_result = Canvas(canvas_w, canvas_h)

    tabs += 1

    if shape_name.startswith(KW_CIRCLE):        # circle
        canvas_result = parse_and_render_circle(shape, canvas_w, canvas_h, inverse, defined_vars, tabs)
    
    elif shape_name.startswith(KW_SQUARE):      # square
        canvas_result = parse_and_render_square(shape, canvas_w, canvas_h, inverse, defined_vars, tabs)

    elif shape_name.startswith(KW_TRIANGLE):    # triangle
        canvas_result = parse_and_render_triangle(shape, canvas_w, canvas_h, inverse, defined_vars, tabs)

    elif shape_name.startswith(KW_GRADIENT):    # gradient
        canvas_result = parse_and_render_gradient(shape, canvas_w, canvas_h, defined_vars, tabs)

    elif shape_name.startswith(KW_COMBINE):     # combine
        canvas_result = parse_and_render_combine(shape, canvas_w, canvas_h, defined_vars, tabs)

    else:
        raise ErrorValueUnknown(f"'{shape_name}'", 'Unknown shape')

    return canvas_result

    # end of parse_and_render_shape()



@cache
def render_mask_circle (canvas_w: int, canvas_h: int, radius: float,
        tx: float, ty: float, inverse: bool, tabs: int) -> Mask:

    radius2 = radius**2
    mask_result = Mask(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            mask_result._pixels[y, x] = ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse

    return mask_result

@cache
def render_canvas_circle (canvas_w: int, canvas_h: int, mask: Mask,
        color: '(a, r, g, b)', tabs: int) -> Canvas:

    a, r, g, b = color
    canvas_result = Canvas(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
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

def parse_and_render_circle (shape: dict, canvas_w: int, canvas_h: int,
        inverse: bool, defined_vars: dict, tabs: int) -> Canvas:

    color = shape[KW_COLOR]
    a, r, g, b = color
    Log((tabs)*TAB+f'{a, r, g, b = }')

    x0, y0 = shape[KW_XY]
    radius = shape[KW_CIRCLE_R]
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')

    # +1/2 for pixel perfect
    tx = -canvas_w/2 - x0 + 1/2
    ty = -canvas_h/2 - y0 + 1/2

    mask = render_mask_circle(canvas_w, canvas_h, radius, tx, ty, inverse, tabs)
    canvas_result = render_canvas_circle(canvas_w, canvas_h, mask, color, tabs)

    return canvas_result
    # end of parse_and_render_circle()



@cache
def render_mask_square (canvas_w: int, canvas_h: int, side: float,
        x0: float, y0: float, inverse: bool, tabs: int) -> Mask:

    tx = -canvas_w/2
    ty = -canvas_h/2
    x_min = x0 - side/2
    y_min = y0 - side/2
    x_max = x0 + side/2
    y_max = y0 + side/2

    mask_result = Mask(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            mask_result._pixels[y, x] = ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse

    return mask_result

@cache
def render_canvas_square (canvas_w: int, canvas_h: int, mask: Mask,
        color: '(a, r, g, b)', tabs: int) -> Canvas:

    a, r, g, b = color
    canvas_result = Canvas(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
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

def parse_and_render_square (shape: dict, canvas_w: int, canvas_h: int,
        inverse: bool, defined_vars: dict, tabs: int) -> Canvas:

    color = shape[KW_COLOR]
    a, r, g, b = color
    Log((tabs)*TAB+f'{a, r, g, b = }')

    x0, y0 = shape[KW_XY]
    side = shape[KW_SQUARE_SIDE]
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')

    mask = render_mask_square(canvas_w, canvas_h, side, x0, y0, inverse, tabs)
    canvas_result = render_canvas_square(canvas_w, canvas_h, mask, color, tabs)

    return canvas_result
    # end of parse_and_render_square()



@cache
def render_mask_triangle (canvas_w: int, canvas_h: int,
        x1: float, y1: float, x2: float, y2: float, x3: float, y3: float,
        inverse: bool, tabs: int) -> Mask:

    # +1/2 for pixel perfect ?
    tx = -canvas_w/2
    ty = -canvas_h/2

    mask_result = Mask(canvas_w, canvas_h)

    def _triangle_sign (x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> float:
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
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
        for x in range(canvas_w):
            mask_result._pixels[y, x] = _is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse

    return mask_result

@cache
def render_canvas_triangle (canvas_w: int, canvas_h: int, mask: Mask,
        color: '(a, r, g, b)', tabs: int) -> Canvas:

    a, r, g, b = color
    canvas_result = Canvas(canvas_w, canvas_h)

    for y in range(canvas_h):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
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

def parse_and_render_triangle (shape: dict, canvas_w: int, canvas_h: int,
        inverse: bool, defined_vars: dict, tabs: int) -> Canvas:

    color = shape[KW_COLOR]
    a, r, g, b = color
    Log((tabs)*TAB+f'{a, r, g, b = }')

    x1, y1, x2, y2, x3, y3 = shape[KW_XY]
    if KW_USED in shape:
        ErrorDeprecated(f'{KW_USED}')

    mask = render_mask_triangle(canvas_w, canvas_h, x1, y1, x2, y2, x3, y3, inverse, tabs)
    canvas_result = render_canvas_triangle(canvas_w, canvas_h, mask, color, tabs)

    return canvas_result
    # end of parse_and_render_circle()



def parse_and_render_gradient (shape: dict, canvas_w: int, canvas_h: int,
        defined_vars: dict, tabs: int) -> Canvas:

    if KW_INVERSE in shape:
        raise ErrorValueWrong(shape[KW_INVERSE], f'{KW_INVERSE} mustnt be in {KW_GRADIENT}')

    COLOR = shape[KW_COLOR]
    A, R, G, B = COLOR
    # Log(f'{A, R, G, B =}')
    Log((tabs)*TAB+f'{A, R, G, B = }')

    x0, y0 = shape[KW_XY]

    if KW_GRADIENT_IS_FADING in shape:
        is_fading = shape[KW_GRADIENT_IS_FADING]
    else:
        is_fading = KW_GRADIENT_IS_FADING_DEFAULT

    Log((tabs)*TAB+f'{is_fading = }')
    points_json = shape[KW_GRADIENT_POINTS]
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
                point_json[KW_XY][0], point_json[KW_XY][1],
                point_json[KW_GRADIENT_SIGMA], point_json[KW_COLOR]
            )
        )
    # Log(points)

    def _render_gradient () -> Canvas:
        def _dist (dx: float, dy: float) -> float:
            return sqrt(dx**2 + dy**2)
        
        @cache
        def _dist2 (dx: float, dy: float) -> float:
            return dx**2 + dy**2

        @cache
        def _gauss (dist2: float, sigma: float) -> float:
            # return exp(-(dist)**2 / (2 * sigma**2))
            return exp(-dist2 / (2 * sigma**2))

        # precalculations
        tx = -canvas_w/2 - x0 + 1/2
        ty = -canvas_h/2 - y0 + 1/2
        
        _canvas = Canvas(canvas_w, canvas_h)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        if is_fading:   # is_fading == True
            for y in range(canvas_h):
                if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                    Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
                for x in range(canvas_w):
                    gausses = []
                    for point in points:
                        gausses.append(_gauss( _dist2(point.x-(x+tx), point.y+(y+ty)), point.sigma ))
                    gausses_sum = sum(gausses)

                    a, r, g, b = 0, 0, 0, 0
                    for i in range(len(gausses)):
                        k = gausses[i]
                        a = min(255, a + k * points[i].color[0])
                        r = min(255, r + k * points[i].color[1])
                        g = min(255, g + k * points[i].color[2])
                        b = min(255, b + k * points[i].color[3])

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
                if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                    Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
                for x in range(canvas_w):
                    gausses = []
                    for point in points:
                        gausses.append(_gauss( _dist2(point.x-(x+tx), -point.y+(y+ty)), point.sigma ))
                    gausses_sum = sum(gausses)

                    a, r, g, b = 0, 0, 0, 0
                    for i in range(len(gausses)):
                        k = gausses[i] / gausses_sum
                        # TODO: add min(255, ...)
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



def parse_and_render_combine (shape: dict, canvas_w, canvas_h: '(canvas_w, canvas_h)',
        defined_vars: dict, tabs: int) -> Canvas:

    if KW_INVERSE in shape:
        raise ErrorValueWrong(shape[KW_INVERSE], f'{KW_INVERSE} mustnt be in {KW_COMBINE}')

    if KW_COMBINE_TYPE not in shape:
        raise ErrorValueWrong(f'{KW_COMBINE_TYPE} must be provided')
    combine_type = shape[KW_COMBINE_TYPE]
    # Log(f'{combine_type = }')

    if KW_COMBINE_FIGURES not in shape:
        raise ErrorValueWrong(f'{KW_COMBINE_FIGURES} must be provided')
    combine_figures = shape[KW_COMBINE_FIGURES]

    canvases = []
    for subentity_name in combine_figures:
        if not subentity_name.startswith(KW_LAYER):
            raise ErrorValueWrong(f'must be {KW_LAYER}')
        # Log(combine_figures[subentity_name])

        canvases.append(
            parse_and_render_entity(
                combine_figures[subentity_name], canvas_w, canvas_h, 0, 0, defined_vars, 0, tabs
            )
        )

    # @cache
    def _combine_value_1plus2 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return v1
        elif used1 and not used2:
            return v1
        elif not used1 and used2:
            return v2
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_1plus2 (used1: bool, used2: bool) -> bool:
        return used1 or used2

    # @cache
    def _combine_value_2plus1 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return v2
        elif used1 and not used2:
            return v1
        elif not used1 and used2:
            return v2
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_2plus1 (used1: bool, used2: bool) -> bool:
        return used1 or used2


    # @cache
    def _combine_value_1minus2 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return 0
        elif used1 and not used2:
            return v1
        elif not used1 and used2:
            return 0
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_1minus2 (used1: bool, used2: bool) -> bool:
        return (used1) and (not used2)

    # @cache
    def _combine_value_2minus1 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return 0
        elif used1 and not used2:
            return 0
        elif not used1 and used2:
            return v2
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_2minus1 (used1: bool, used2: bool) -> bool:
        return (not used1) and (used2)


    # @cache
    def _combine_value_1product2 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return v1
        elif used1 and not used2:
            return 0
        elif not used1 and used2:
            return 0
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_1product2 (used1: bool, used2: bool) -> bool:
        return (used1) and (used2)

    # @cache
    def _combine_value_2product1 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return v2
        elif used1 and not used2:
            return 0
        elif not used1 and used2:
            return 0
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_2product1 (used1: bool, used2: bool) -> bool:
        return (used1) and (used2)


    # @cache
    def _combine_value_1symdiff2 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return 0
        elif used1 and not used2:
            return v1
        elif not used1 and used2:
            return v2
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_1symdiff2 (used1: bool, used2: bool) -> bool:
        return used1 ^ used2

    # @cache
    def _combine_value_2symdiff1 (v1: int, v2: int, used1: bool, used2: bool) -> int:
        if used1 and used2:
            return 0
        elif used1 and not used2:
            return v1
        elif not used1 and used2:
            return v2
        else:   # not used1 and not used2
            return 0
    # @cache
    def _combine_used_2symdiff1 (used1: bool, used2: bool) -> bool:
        return used1 ^ used2

    combine_value_funcs = {
        KW_COMBINE_TYPE_1PLUS2: _combine_value_1plus2,
        KW_COMBINE_TYPE_2PLUS1: _combine_value_2plus1,
        KW_COMBINE_TYPE_1MINUS2: _combine_value_1minus2,
        KW_COMBINE_TYPE_2MINUS1: _combine_value_2minus1,
        KW_COMBINE_TYPE_1PRODUCT2: _combine_value_1product2,
        KW_COMBINE_TYPE_2PRODUCT1: _combine_value_2product1,
        KW_COMBINE_TYPE_1SYMDIFF2: _combine_value_1symdiff2,
        KW_COMBINE_TYPE_2SYMDIFF1: _combine_value_2symdiff1,
    }
    combine_used_funcs = {
        KW_COMBINE_TYPE_1PLUS2: _combine_used_1plus2,
        KW_COMBINE_TYPE_2PLUS1: _combine_used_2plus1,
        KW_COMBINE_TYPE_1MINUS2: _combine_used_1minus2,
        KW_COMBINE_TYPE_2MINUS1: _combine_used_2minus1,
        KW_COMBINE_TYPE_1PRODUCT2: _combine_used_1product2,
        KW_COMBINE_TYPE_2PRODUCT1: _combine_used_2product1,
        KW_COMBINE_TYPE_1SYMDIFF2: _combine_used_1symdiff2,
        KW_COMBINE_TYPE_2SYMDIFF1: _combine_used_2symdiff1,
    }

    if combine_type not in combine_value_funcs:
        raise ErrorValueUnknown(f'{combine_type} is unknown for combine type')

    canvas_result = canvases[0]

    Log((tabs)*TAB+'combining:')
    tabs += 1
    for i in range(1, len(canvases)):
        for y in range(canvas_h):
            if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
            for x in range(canvas_w):
                color1 = canvas_result._pixels[y, x]
                color2 = canvases[i]._pixels[y, x]

                r1, g1, b1, a1, used1 = color1
                r2, g2, b2, a2, used2 = color2

                canvas_result._pixels[y, x] = [
                    combine_value_funcs[combine_type](r1, r2, used1, used2),
                    combine_value_funcs[combine_type](g1, g2, used1, used2),
                    combine_value_funcs[combine_type](b1, b2, used1, used2),
                    combine_value_funcs[combine_type](a1, a2, used1, used2),
                    combine_used_funcs[combine_type](used1, used2)
                ]

    return canvas_result
    # end of parse_and_render_combine()



# @cache
def blend_canvases (canvas_bg: Canvas, canvas_fg: Canvas, shape_number: int,
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_x: int, delta_y: int, tabs: int) -> Canvas:

    if (t:=type(canvas_bg)) != Canvas:
        raise ErrorTypeWrong(t, 'canvas_bg', Canvas)
    if (t:=type(canvas_fg)) != Canvas:
        raise ErrorTypeWrong(t, 'canvas_fg', Canvas)

    # Log('--------------------- started blending ---------------------')
    Log((tabs)*TAB+'blending canvases:')
    tabs += 1

    # Log('showing canvas_bg:'); tmp_show_image(canvas_bg)
    # Log('showing canvas_fg:'); tmp_show_image(canvas_fg)

    # Log(f'{canvas_bg._pixels = }')
    # Log(f'{canvas_fg._pixels = }')

    # @cache
    def _blend_overlap (V, v, USED, used, shape_number):
        if used:
            return v
        else:
            return V

    # @cache
    def _blend_add (V, v, USED, used, shape_number):
        return V + v

    # @cache
    def _blend_avg (V, v, USED, used, shape_number):
        return (shape_number*V + v) // (shape_number+1)

    # @cache
    def _blend_min (V, v, USED, used, shape_number):
        if USED and used:
            return min(V, v)
        elif USED:
            return V
        elif used:
            return v
        else:
            return V

    # @cache
    def _blend_max (V, v, USED, used, shape_number):
        if USED and used:
            return max(V, v)
        elif USED:
            return V
        elif used:
            return v
        else:
            return V

    blending_funcs = (
        # overlap:
        # lambda V, v, USED, used, shape_number: v if used else V,
        _blend_overlap,

        # add:
        # lambda V, v, USED, used, shape_number: V + v,
        _blend_add,

        # avg:
        # lambda V, v, USED, used, shape_number: (shape_number*V + v) // (shape_number+1),
        _blend_avg,

        # min:
        _blend_min,

        # max:
        _blend_max,
    )

    x_from = 0
    y_from = 0
    x_to = canvas_bg.w
    y_to = canvas_bg.h

    canvas_result = Canvas(canvas_bg.w, canvas_bg.h, canvas_bg.get_pixels_rgbau())

    WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

    for y in range(y_from, y_to):
        if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
            Log((tabs)*TAB+f'{100*y//(y_to-y_from)}%')
        for x in range(x_from, x_to):
            if not (0 <= x-delta_x < canvas_fg.w) or not (0 <= y-delta_y < canvas_fg.h):
                # if x or y of foreground not in its bounds, skip this x,y
                continue

            color_bg = canvas_bg._pixels[y, x]
            color_fg = canvas_fg._pixels[y-delta_y, x-delta_x]

            R, G, B, A, USED = color_bg     # BACKGROUND
            r, g, b, a, used = color_fg     # foreground

            canvas_result._pixels[y, x] = [
                blending_funcs[color_blending_type.value](R, r, USED, used, shape_number),
                blending_funcs[color_blending_type.value](G, g, USED, used, shape_number),
                blending_funcs[color_blending_type.value](B, b, USED, used, shape_number),
                blending_funcs[alpha_blending_type.value](A, a, USED, used, shape_number),
                used or USED
            ]

            # if random.randint(0, 10**3) < 1:
            #     Log(f'{canvas_blend._pixels[y, x]}')

    return canvas_result

    # end of blend_canvases()




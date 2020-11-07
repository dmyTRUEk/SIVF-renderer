'''
This file contains all heavy functions, that should be accelerated with Cython
''' 

import numpy as np
import random


from funcs_errors import *
from funcs_warnings import *

from consts_sivf_keywords import *

from class_canvas import Canvas
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *
from funcs_utils import *





CHECK_BOUNDS_OPTIMIZATION = 'Check bounds optimization'



def debug_show_image (canvas: Canvas):
    '''This function is for testing and mustnt be used on release'''
    from PIL import Image
    Image.fromarray(canvas.get_pixels_rgba(), 'RGBA').show()





def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType) -> Canvas:

    print((1+tabs)*tab+f'rendering {shape_name}:')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    print((2+tabs)*tab+f'{KW_INVERSE} = {inverse}')

    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    print((2+tabs)*tab+f'{a=}, {r=}, {g=}, {b=}')

    canvas_w, canvas_h = canvas_wh
    canvas = Canvas(canvas_wh)

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    if shape_name.startswith(KW_CIRCLE):   # circle
        canvas_tmp = parse_and_render_circle(shape, canvas_wh, tab, tabs, defined_vars)
        canvas = blend_canvases(canvas, canvas_tmp, shape_number, alpha_blending_type, color_blending_type)
    
    elif shape_name.startswith(KW_SQUARE):   # square
        canvas_tmp = parse_and_render_square(shape, canvas_wh, tab, tabs, defined_vars)
        canvas = blend_canvases(canvas, canvas_tmp, shape_number, alpha_blending_type, color_blending_type)

    elif shape_name.startswith(KW_TRIANGLE):   # triangle
        canvas_tmp = parse_and_render_triangle(shape, canvas_wh, tab, tabs, defined_vars)
        canvas = blend_canvases(canvas, canvas_tmp, shape_number, alpha_blending_type, color_blending_type)

    elif shape_name.startswith(KW_GRADIENT):
        canvas_tmp = parse_and_render_gradient(shape, canvas_wh, tab, tabs, defined_vars)
        canvas = blend_canvases(canvas, canvas_tmp, shape_number, alpha_blending_type, color_blending_type)

    else:
        raise ErrorValueUnknown(f"'{shape_name}'", 'Unknown shape')

    return canvas

    # end of parse_and_render_shape()



def parse_and_render_circle (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        tab: str, tabs: int, defined_vars: dict) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # print(f'{r=}, {g=}, {b=}, {a=}')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
    radius = cetu(shape[KW_CIRCLE_R], canvas_wh, defined_vars)

    def _render_circle () -> Canvas:
        # precalculations
        radius2 = radius**2
        tx = -canvas_w/2 - x0 + 1/2
        ty = -canvas_h/2 - y0 + 1/2
        
        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        for y in range(canvas_h):
            for x in range(canvas_w):
                if ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        True
                    ]
        return _canvas
        # end of _render_circle()

    canvas = _render_circle()
    return canvas
    # end of parse_and_render_circle()



def parse_and_render_square (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        tab: str, tabs: int, defined_vars: dict) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # print(f'{r=}, {g=}, {b=}, {a=}')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars) - 1/2
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars) - 1/2
    side = cetu(shape[KW_SQUARE_SIDE], canvas_wh, defined_vars)

    def _render_square () -> Canvas:
        # precalculations:
        x_min = x0 - side/2
        y_min = y0 - side/2
        x_max = x0 + side/2
        y_max = y0 + side/2
        tx = -canvas_w/2
        ty = -canvas_h/2

        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        for y in range(canvas_h):
            for x in range(canvas_w):
                if ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        True
                    ]
        return _canvas
        # end of _render_square()

    canvas = _render_square()
    return canvas
    # end of parse_and_render_square()



def parse_and_render_triangle (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        tab: str, tabs: int, defined_vars: dict) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # print(f'{r=}, {g=}, {b=}, {a=}')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    x1 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y1 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
    x2 =  cetu(shape[KW_XY][2], canvas_wh, defined_vars)
    y2 = -cetu(shape[KW_XY][3], canvas_wh, defined_vars)
    x3 =  cetu(shape[KW_XY][4], canvas_wh, defined_vars)
    y3 = -cetu(shape[KW_XY][5], canvas_wh, defined_vars)
    
    def _render_triangle () -> Canvas:
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

        # precalculations:
        tx = -canvas_w/2
        ty = -canvas_h/2

        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        for y in range(canvas_h):
            for x in range(canvas_w):
                if _is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        True
                    ]
        return _canvas
        # end of _render_triangle()

    canvas = _render_triangle()
    return canvas
    # end of parse_and_render_triangle()



def parse_and_render_gradient (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        tab: str, tabs: int, defined_vars: dict) -> Canvas:

    canvas_w, canvas_h = canvas_wh

    if KW_INVERSE in shape:
        raise ErrorValueWrong(shape[KW_INVERSE], '{KW_INVERSE} mustnt be in gradient')
        # inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False

    A, R, G, B = cctargb(shape[KW_COLOR][1:])
    # print(f'{A=}, {R=}, {G=}, {B=}')

    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
    is_fading = (shape[KW_GRADIENT_FADING] == KW_TRUE) if KW_GRADIENT_FADING in shape else False
    points_json = shape[KW_GRADIENT_POINTS]
    # print(points_json)

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
        # print(point_json)
        points.append(
            Point(
                +cetu(point_json[KW_XY][0], canvas_wh, defined_vars),
                -cetu(point_json[KW_XY][1], canvas_wh, defined_vars),
                cetu(point_json[KW_GRADIENT_SIGMA], canvas_wh, defined_vars),
                cctargb(point_json[KW_COLOR][1:])
            )
        )
    # print(points)

    def _render_gradient () -> Canvas:
        def _dist (dx: float, dy: float):
            return sqrt(dx**2 + dy**2)

        def _gauss (dist: float, sigma: float):
            return exp(-(dist)**2 / (2 * sigma**2))

        # precalculations
        tx = -canvas_w/2 - x0 + 1/2
        ty = -canvas_h/2 - y0 + 1/2
        
        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        gausses = []

        if is_fading:   # is_fading == True
            for y in range(canvas_h):
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
                    #     print(f'{gausses=}')
                    #     print(f'{a=}, {r=}, {g=}, {b=}')
                    #     print()

                    _canvas._pixels[y, x] = [ r, g, b, a, True ]

        else:   # is_fading == False
            for y in range(canvas_h):
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
                    #     print(f'{gausses=}')
                    #     print(f'{a=}, {r=}, {g=}, {b=}')
                    #     print()

                    _canvas._pixels[y, x] = [ r, g, b, a, True ]

        return _canvas
        # end of _render_gradient()

    canvas = _render_gradient()
    return canvas
    # end of parse_and_render_gradient()



def blend_canvases (canvas_bg: Canvas, canvas_fg: Canvas, shape_number: int,
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)'=(0, 0)) -> Canvas:

    if (t:=type(canvas_bg)) != Canvas:
        raise TypeError(f'canvas_bg must be instance of Canvas, but it is {t}')
    if (t:=type(canvas_fg)) != Canvas:
        raise TypeError(f'canvas_fg must be instance of Canvas, bit it is {t}')

    # print('showing canvas_bg:'); tmp_show_image(canvas_bg)
    # print('showing canvas_fg:'); tmp_show_image(canvas_fg)

    # print(f'{canvas_bg._pixels = }')
    # print(f'{canvas_fg._pixels = }')

    blending_funcs = (
        # overlap:
        lambda V, v, USED, used, shape_number: v if used else V,
        # add:
        lambda V, v, USED, used, shape_number: V + v,
        # avg:
        lambda V, v, USED, used, shape_number: (V*shape_number+v)//(shape_number+1)
    )

    delta_x, delta_y = delta_xy

    # old bounds for blending
    # x_from = delta_x - canvas_fg.w//2
    # y_from = delta_y - canvas_fg.h//2
    # x_to = canvas_bg.w // 2
    # y_to = canvas_bg.h // 2

    x_from = 0
    y_from = 0
    x_to = canvas_bg.w
    y_to = canvas_bg.h

    canvas_blend = Canvas(canvas_bg.wh, canvas_bg.get_pixels_rgbau())

    WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

    for y in range(y_from, y_to):
        for x in range(x_from, x_to):
            if not (0 <= x-delta_x < canvas_fg.w) or not (0 <= y-delta_y < canvas_fg.h):
                # if x or y of foreground not in its bounds, skip this x,y
                continue

            color_bg = canvas_bg._pixels[y, x]
            color_fg = canvas_fg._pixels[y-delta_y, x-delta_x]

            R, G, B, A, USED = color_bg     # BACKGROUND
            r, g, b, a, used = color_fg     # foreground

            canvas_blend._pixels[y, x] = [
                blending_funcs[color_blending_type.value](R, r, USED, used, shape_number),
                blending_funcs[color_blending_type.value](G, g, USED, used, shape_number),
                blending_funcs[color_blending_type.value](B, b, USED, used, shape_number),
                blending_funcs[alpha_blending_type.value](A, a, USED, used, shape_number),
                used or USED
            ]

    return canvas_blend

    # end of blend_canvases



# [TODO]: replace by blend_canvases and parse_and_render_<shape>
def render_shape (color: '(a, r, g, b)', check_func: 'function', shape_n: int,
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default) -> 'ndarray2d':

    raise ErrorDeprecated('func render_shape is deprecated, and shouldnt be used from now')

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = color[0], color[1], color[2], color[3]

    # canvas = Canvas(canvas_wh)

    pixels = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)

    if alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.overlap:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [r, g, b, a]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.add:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        pixels[y, x, 0] + r,
                        pixels[y, x, 1] + g,
                        pixels[y, x, 2] + b,
                        a
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.add and color_blending_type == ColorBlendingType.add:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        pixels[y, x, 0] + r,
                        pixels[y, x, 1] + g,
                        pixels[y, x, 2] + b,
                        pixels[y, x, 3] + a,
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.add and color_blending_type == ColorBlendingType.overlap:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        r,
                        g,
                        b,
                        pixels[y, x, 3] + a,
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    
    elif alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.avg:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        (pixels[y, x, 0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x, 1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x, 2]*shape_n+b)//(shape_n+1),
                        a
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.avg and color_blending_type == ColorBlendingType.avg:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        (pixels[y, x, 0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x, 1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x, 2]*shape_n+b)//(shape_n+1),
                        (pixels[y, x, 3]*shape_n+a)//(shape_n+1)
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    else:
        raise Exception(f'Error: This Blending Type Combination is unsupported for now: {color_blending_type = }, {alpha_blending_type = }')

    # end of render_shape 




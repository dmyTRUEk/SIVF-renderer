'''
This file contains all heavy functions, that should be accelerated with Cython
''' 

import numpy as np
import random


from funcs_errors import *
from funcs_warnings import *
from funcs_log import *

from config import *
from consts_sivf_keywords import *

from class_canvas import Canvas
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *
from funcs_utils import *





CHECK_BOUNDS_OPTIMIZATION = 'Check bounds optimization'



def debug_show_image (canvas: Canvas):
    '''This function is for testing and mustnt be used on release'''
    Warning('This function is for testing and mustnt be used on release')
    from PIL import Image
    Image.fromarray(canvas.get_pixels_rgba(), PIL_IMAGE_OUTPUT_MODE).show()





def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        tabs: int=0) -> Canvas:

    # tabs += 1
    Log((tabs)*TAB+f'rendering {shape_name}:')

    tabs += 1
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    Log((tabs)*TAB+f'{KW_INVERSE} = {inverse}')

    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    Log((tabs)*TAB+f'{a=}, {r=}, {g=}, {b=}')

    canvas_w, canvas_h = canvas_wh
    canvas = Canvas(canvas_wh)

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    tabs += 1

    if shape_name.startswith(KW_CIRCLE):   # circle
        canvas = parse_and_render_circle(shape, canvas_wh, defined_vars, tabs)
    
    elif shape_name.startswith(KW_SQUARE):   # square
        canvas = parse_and_render_square(shape, canvas_wh, defined_vars, tabs)

    elif shape_name.startswith(KW_TRIANGLE):   # triangle
        canvas = parse_and_render_triangle(shape, canvas_wh, defined_vars, tabs)

    elif shape_name.startswith(KW_GRADIENT):
        canvas = parse_and_render_gradient(shape, canvas_wh, defined_vars, tabs)

    else:
        raise ErrorValueUnknown(f"'{shape_name}'", 'Unknown shape')

    return canvas

    # end of parse_and_render_shape()



def parse_and_render_circle (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    radius = cetu(shape[KW_CIRCLE_R], canvas_wh, defined_vars)
    used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT

    def _render_circle () -> Canvas:
        # precalculations
        radius2 = radius**2
        tx = -canvas_w/2 - x0 + 1/2
        ty = -canvas_h/2 - y0 + 1/2
        
        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        for y in range(canvas_h):
            if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
            for x in range(canvas_w):
                if ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        used
                    ]
        return _canvas
        # end of _render_circle()

    canvas = _render_circle()
    return canvas
    # end of parse_and_render_circle()



def parse_and_render_square (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars) - 1/2
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars) - 1/2
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    side = cetu(shape[KW_SQUARE_SIDE], canvas_wh, defined_vars)
    used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT

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
            if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
            for x in range(canvas_w):
                if ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        used
                    ]
        return _canvas
        # end of _render_square()

    canvas = _render_square()
    return canvas
    # end of parse_and_render_square()



def parse_and_render_triangle (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # Log(f'{r=}, {g=}, {b=}, {a=}')

    x1 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y1 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
    x2 =  cetu(shape[KW_XY][2], canvas_wh, defined_vars)
    y2 = -cetu(shape[KW_XY][3], canvas_wh, defined_vars)
    x3 =  cetu(shape[KW_XY][4], canvas_wh, defined_vars)
    y3 = -cetu(shape[KW_XY][5], canvas_wh, defined_vars)
    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else KW_INVERSE_DEFAULT
    used = (shape[KW_USED] == KW_TRUE) if KW_USED in shape else KW_USED_DEFAULT
    
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
            if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
                Log((tabs)*TAB+f'{100*y//(canvas_h)}%')
            for x in range(canvas_w):
                if _is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse:
                    _canvas._pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        used
                    ]
        return _canvas
        # end of _render_triangle()

    canvas = _render_triangle()
    return canvas
    # end of parse_and_render_triangle()



def parse_and_render_gradient (shape: dict, canvas_wh: '(canvas_w, canvas_h)',
        defined_vars: dict, tabs: int=0) -> Canvas:

    canvas_w, canvas_h = canvas_wh

    if KW_INVERSE in shape:
        raise ErrorValueWrong(shape[KW_INVERSE], '{KW_INVERSE} mustnt be in gradient')
        # inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False

    A, R, G, B = cctargb(shape[KW_COLOR][1:])
    # Log(f'{A=}, {R=}, {G=}, {B=}')

    x0 =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    y0 = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)
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
                +cetu(point_json[KW_XY][0], canvas_wh, defined_vars),
                -cetu(point_json[KW_XY][1], canvas_wh, defined_vars),
                cetu(point_json[KW_GRADIENT_SIGMA], canvas_wh, defined_vars),
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
        
        _canvas = Canvas(canvas_wh)

        WarningTodo(CHECK_BOUNDS_OPTIMIZATION)

        gausses = []

        if is_fading:   # is_fading == True
            for y in range(canvas_h):
                if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
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
                if y % OUTPUT_RENDER_PROGRESS_PERIOD == 0:
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

    canvas = _render_gradient()
    return canvas
    # end of parse_and_render_gradient()



def blend_canvases (canvas_bg: Canvas, canvas_fg: Canvas, shape_number: int,
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)'=(0, 0), tabs: int=0) -> Canvas:

    if (t:=type(canvas_bg)) != Canvas:
        raise ErrorWrongType(t, 'canvas_bg', Canvas)
    if (t:=type(canvas_fg)) != Canvas:
        raise ErrorWrongType(t, 'canvas_fg', Canvas)

    # Log('--------------------- started blending ---------------------')
    Log((tabs)*TAB+'blending canvases:')
    tabs += 1
    # Log()


    # Log('showing canvas_bg:'); tmp_show_image(canvas_bg)
    # Log('showing canvas_fg:'); tmp_show_image(canvas_fg)

    # Log(f'{canvas_bg._pixels = }')
    # Log(f'{canvas_fg._pixels = }')

    def _blend_min (V, v, USED, used, shape_number):
        if USED and used:
            return min(V, v)
        elif USED:
            return V
        elif used:
            return v
        else:
            return V

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
        lambda V, v, USED, used, shape_number: v if used else V,

        # add:
        lambda V, v, USED, used, shape_number: V + v,

        # avg:
        lambda V, v, USED, used, shape_number: (shape_number*V + v) // (shape_number+1),

        # min:
        # lambda V, v, USED, used, shape_number: min(V, v) if (USED and used) else V,
        _blend_min,

        # max:
        # lambda V, v, USED, used, shape_number: max(V, v) if (USED and used) else V,
        _blend_max,
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

            canvas_blend._pixels[y, x] = [
                blending_funcs[color_blending_type.value](R, r, USED, used, shape_number),
                blending_funcs[color_blending_type.value](G, g, USED, used, shape_number),
                blending_funcs[color_blending_type.value](B, b, USED, used, shape_number),
                blending_funcs[alpha_blending_type.value](A, a, USED, used, shape_number),
                used or USED
            ]

            # if random.randint(0, 10**3) < 1:
            #     Log(f'{canvas_blend._pixels[y, x]}')

    return canvas_blend

    # end of blend_canvases




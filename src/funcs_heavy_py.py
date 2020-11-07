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





def debug_show_image (canvas: Canvas):
    '''This function is for testing and mustnt be used on release'''
    from PIL import Image
    Image.fromarray(canvas.get_pixels_rgba(), 'RGBA').show()





def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Canvas:

    print((1+tabs)*tab+f'rendering {shape_name}:')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    print((2+tabs)*tab+f'{KW_INVERSE} = {inverse}')

    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    print((2+tabs)*tab+f'{a=}, {r=}, {g=}, {b=}')

    print((2+tabs)*tab+f'{KW_DELTA_XY} = {delta_xy}')

    canvas_w, canvas_h = canvas_wh
    canvas = Canvas(canvas_wh)

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    if shape_name.startswith(KW_CIRCLE):   # circle
        canvas_tmp = parse_and_render_circle(
            shape, shape_number,
            canvas_wh, tab, tabs, defined_vars,
            alpha_blending_type,
            color_blending_type,
        )
        canvas = blend_canvases(canvas, canvas_tmp, shape_number, alpha_blending_type, color_blending_type)
    
    elif shape_name.startswith(KW_SQUARE):   # square
        raise ErrorNotImpemented('square processing')

        square_x = cetu(shape[KW_XY][0], canvas_wh, defined_vars) + delta_xy[0]
        square_y = -cetu(shape[KW_XY][1], canvas_wh, defined_vars) + delta_xy[1]
        side = cetu(shape[KW_SIDE], canvas_wh, defined_vars)

        x_min = square_x - side/2
        y_min = square_y - side/2
        x_max = square_x + side/2
        y_max = square_y + side/2
        tx = -canvas_w/2
        ty = -canvas_h/2
        render_shape(
            (a, r, g, b),
            lambda x, y: ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse,
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type,
        )

    elif shape_name.startswith('triangle'):   # triangle
        raise ErrorNotImpemented('triangle processing')

        def triangle_sign (x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> float:
            return (x1-x3)*(y2-y3) - (x2-x3)*(y1-y3)

        def is_inside_triangle (x: float, y: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> bool:
            d1 = triangle_sign(x, y, x1, y1, x2, y2)
            d2 = triangle_sign(x, y, x2, y2, x3, y3)
            d3 = triangle_sign(x, y, x3, y3, x1, y1)
            #has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            #has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            #return not (has_neg and has_pos)
            return not ( ((d1 < 0) or (d2 < 0) or (d3 < 0)) and ((d1 > 0) or (d2 > 0) or (d3 > 0)) )

        x1 =  cetu(shape['xy'][0], canvas_wh, defined_vars) + delta_xy[0]
        y1 = -cetu(shape['xy'][1], canvas_wh, defined_vars) + delta_xy[1]
        x2 =  cetu(shape['xy'][2], canvas_wh, defined_vars) + delta_xy[0]
        y2 = -cetu(shape['xy'][3], canvas_wh, defined_vars) + delta_xy[1]
        x3 =  cetu(shape['xy'][4], canvas_wh, defined_vars) + delta_xy[0]
        y3 = -cetu(shape['xy'][5], canvas_wh, defined_vars) + delta_xy[1]

        tx = -canvas_w/2
        ty = -canvas_h/2

        render_shape(
            (a, r, g, b),
            lambda x, y: is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse,
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type
        )

    else:
        raise ErrorUnknownValue(f"'{shape_name}'", 'Unknown shape')

    return canvas

    # end of parse_and_render_shape()



def parse_and_render_circle (shape: dict, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType) -> Canvas:

    canvas_w, canvas_h = canvas_wh

    a, r, g, b = cctargb(shape[KW_COLOR][1:])
    # print(f'{r=}, {g=}, {b=}, {a=}')

    inverse = (shape[KW_INVERSE] == KW_TRUE) if KW_INVERSE in shape else False
    radius = cetu(shape[KW_R], canvas_wh, defined_vars)
    circle_x =  cetu(shape[KW_XY][0], canvas_wh, defined_vars)
    circle_y = -cetu(shape[KW_XY][1], canvas_wh, defined_vars)

    def _render_circle () -> Canvas:
        radius2 = radius**2
        tx = -canvas_w/2 - circle_x + 1/2
        ty = -canvas_h/2 - circle_y + 1/2
        
        _canvas = Canvas(canvas_wh)

        WarningTodo('Check if bounds optimized')

        for y in range(canvas_h):
            for x in range(canvas_w):
                if is_true := ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse:
                    # if random.randint(0, 10**2) < 1 and not inverse:
                    #     print(f'\n{x=}, {y=}\n{tx=}, {ty=}\n{radius=}\n{is_true=}\n')
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



def parse_and_render_square (shape: dict, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Canvas:
    
    def _render_square () -> Canvas:
        raise ErrorNotImpemented()

    raise ErrorNotImpemented()



def parse_and_render_triangle (shape: dict, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, defined_vars: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Canvas:
    
    def _render_triangle () -> Canvas:
        raise ErrorNotImpemented()

    raise ErrorNotImpemented()



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

    WarningTodo('Check bound optimization')

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




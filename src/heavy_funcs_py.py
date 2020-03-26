'''
This file contains all heavy functions, that should be accelerated with Cython
''' 



import numpy as np

from alpha_blending import *
from color_blending import *

from convert_funcs import *





def parse_shape (pixels: 'nparray2d', shape: dict, shape_name: str, shape_number: int, 
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int, var: dict, 
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> None:

    print((1+tabs)*tab+f'rendering {shape_name}:')

    inverse = (shape['inverse'] == 'true') if 'inverse' in shape else False
    print((2+tabs)*tab+f'{inverse = }')

    a, r, g, b = cctargb(shape['color'][1:])
    print((2+tabs)*tab+f'{a=}, {r=}, {g=}, {b=}')

    print((2+tabs)*tab+f'{delta_xy = }')

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    canvas_w, canvas_h = canvas_wh

    if shape_name.startswith('circle'):   # circle
        circle_x = cetu(shape['xy'][0], canvas_wh, var) + delta_xy[0]
        circle_y = -cetu(shape['xy'][1], canvas_wh, var) + delta_xy[1]
        radius = cetu(shape['r'], canvas_wh, var)

        tx = -canvas_w/2 - circle_x + 1/2
        ty = -canvas_h/2 - circle_y + 1/2
        radius2 = radius**2
        render_shape(
            pixels, (a, r, g, b),
            lambda x, y: ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse,
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type,
        )
    
    elif shape_name.startswith('square'):   # square
        square_x = cetu(shape['xy'][0], canvas_wh, var) + delta_xy[0]
        square_y = -cetu(shape['xy'][1], canvas_wh, var) + delta_xy[1]
        side = cetu(shape['side'], canvas_wh, var)

        x_min = square_x - side/2
        y_min = square_y - side/2
        x_max = square_x + side/2
        y_max = square_y + side/2
        tx = -canvas_w/2
        ty = -canvas_h/2
        render_shape(
            pixels, (a, r, g, b),
            lambda x, y: ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse,
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type,
        )

    elif shape_name.startswith('triangle'):   # triangle
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

        x1 = cetu(shape['xy'][0], canvas_wh, var) + delta_xy[0]
        y1 = -cetu(shape['xy'][1], canvas_wh, var) + delta_xy[1]
        x2 = cetu(shape['xy'][2], canvas_wh, var) + delta_xy[0]
        y2 = -cetu(shape['xy'][3], canvas_wh, var) + delta_xy[1]
        x3 = cetu(shape['xy'][4], canvas_wh, var) + delta_xy[0]
        y3 = -cetu(shape['xy'][5], canvas_wh, var) + delta_xy[1]

        tx = -canvas_w/2
        ty = -canvas_h/2

        render_shape(
            pixels, (a, r, g, b),
            lambda x, y: is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse,
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type
        )

    else:
        raise Exception(f'Unknown shape: {shape_name = }, {shape= }')

    # end of parse_shape()





def render_shape (pixels: 'nparray2d', color: '(a, r, g, b)', check_func: 'function', shape_n: int,
        canvas_wh: '(canvas_w, canvas_h)', tab: str, tabs: int,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default) -> None:

    canvas_w, canvas_h = canvas_wh
    a, r, g, b = color[0], color[1], color[2], color[3]

    if alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.overlap :
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

    # end of render_object 




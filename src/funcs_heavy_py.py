'''
This file contains all heavy functions, that should be accelerated with Cython
''' 



import numpy as np
import random

from class_layer import Layer

from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *





def tmp_show_image (layer: Layer):
    from PIL import Image
    Image.fromarray(layer.get_pixels_rgba(), 'RGBA').show()





def parse_and_render_shape (shape: dict, shape_name: str, shape_number: int, 
        layer_wh: '(layer_w, layer_h)', tab: str, tabs: int, var: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Layer:

    print((1+tabs)*tab+f'rendering {shape_name}:')

    inverse = (shape['inverse'] == 'true') if 'inverse' in shape else False
    print((2+tabs)*tab+f'{inverse = }')

    a, r, g, b = cctargb(shape['color'][1:])
    print((2+tabs)*tab+f'{a=}, {r=}, {g=}, {b=}')

    print((2+tabs)*tab+f'{delta_xy = }')

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    layer_w, layer_h = layer_wh
    layer = Layer(layer_wh)

    if shape_name.startswith('circle'):   # circle
        layer_tmp = parse_and_render_circle(
            shape, shape_number,
            layer_wh, tab, tabs, var,
            alpha_blending_type,
            color_blending_type,
            delta_xy
        )
        # print(f'{layer_tmp.get_pixels() = }')
        layer = blend_layers(layer, layer_tmp, shape_number, alpha_blending_type, color_blending_type)
    
    elif shape_name.startswith('square'):   # square
        raise NotImplementedError('square processing is not implemented yet')
        square_x = cetu(shape['xy'][0], layer_wh, var) + delta_xy[0]
        square_y = -cetu(shape['xy'][1], layer_wh, var) + delta_xy[1]
        side = cetu(shape['side'], layer_wh, var)

        x_min = square_x - side/2
        y_min = square_y - side/2
        x_max = square_x + side/2
        y_max = square_y + side/2
        tx = -layer_w/2
        ty = -layer_h/2
        render_shape(
            (a, r, g, b),
            lambda x, y: ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse,
            shape_number, layer_wh, tab, tabs,
            alpha_blending_type, color_blending_type,
        )

    elif shape_name.startswith('triangle'):   # triangle
        raise NotImplementedError('triangle processing is not implemented yet')
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

        x1 =  cetu(shape['xy'][0], layer_wh, var) + delta_xy[0]
        y1 = -cetu(shape['xy'][1], layer_wh, var) + delta_xy[1]
        x2 =  cetu(shape['xy'][2], layer_wh, var) + delta_xy[0]
        y2 = -cetu(shape['xy'][3], layer_wh, var) + delta_xy[1]
        x3 =  cetu(shape['xy'][4], layer_wh, var) + delta_xy[0]
        y3 = -cetu(shape['xy'][5], layer_wh, var) + delta_xy[1]

        tx = -layer_w/2
        ty = -layer_h/2

        render_shape(
            (a, r, g, b),
            lambda x, y: is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse,
            shape_number, layer_wh, tab, tabs,
            alpha_blending_type, color_blending_type
        )

    else:
        raise Exception(f'Unknown shape: {shape_name = }, {shape = }')

    # print(f'in parse_and_render_shape: {layer.get_pixels() = }')
    return layer

    # end of parse_shape()



def parse_and_render_circle (shape: dict, shape_number: int, 
        layer_wh: '(layer_w, layer_h)', tab: str, tabs: int, var: dict, 
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Layer:

    layer_w, layer_h = layer_wh

    a, r, g, b = cctargb(shape['color'][1:])
    # print(f'---------------- {r=}, {g=}, {b=}, {a=}')

    inverse = (shape['inverse'] == 'true') if 'inverse' in shape else False
    radius = cetu(shape['r'], layer_wh, var)
    circle_x = cetu(shape['xy'][0], layer_wh, var) + delta_xy[0]
    circle_y = -cetu(shape['xy'][1], layer_wh, var) + delta_xy[1]

    radius2 = radius**2
    tx = -layer_w/2 - circle_x + 1/2
    ty = -layer_h/2 - circle_y + 1/2
    
    def render_circle () -> 'ndarray2d':
        # layer = Layer(layer_wh)
        _pixels = np.zeros((layer_h, layer_w, 5), dtype=np.uint8)

        for y in range(layer_h):
            for x in range(layer_w):
                if ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse:
                    _pixels[y, x] = [
                        r,
                        g,
                        b,
                        a,
                        True
                    ]
        return _pixels
        # end of render_cirlce()

    pixels = render_circle(
        # (a, r, g, b),
        # lambda x, y: ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse,
        # shape_number, layer_wh, tab, tabs,
        # alpha_blending_type, color_blending_type,
    )

    layer = Layer(layer_wh, pixels)
    return layer
    # end of parse_and_render_circle()



def parse_and_render_square ():
    
    def render_square ():
        raise NotImplementedError('not implemented yet')

    raise NotImplementedError('not implemented yet')



def parse_and_render_triangle ():
    
    def render_triangle ():
        raise NotImplementedError('not implemented yet')

    raise NotImplementedError('not implemented yet')



def blend_layers (layer_bg: Layer, layer_fg: Layer, shape_number: int,
        alpha_blending_type: AlphaBlendingType,
        color_blending_type: ColorBlendingType,
        delta_xy: '(delta_x, delta_y)'=(0, 0)) -> Layer:

    if (t:=type(layer_bg)) != Layer:
        raise TypeError(f'layer_bg must be instance of Layer, but it is {t}')
    if (t:=type(layer_fg)) != Layer:
        raise TypeError(f'layer_fg must be instance of Layer, bit it is {t}')

    # print('showing layer_bg:'); tmp_show_image(layer_bg)
    # print('showing layer_fg:'); tmp_show_image(layer_fg)

    blending_funcs = (
        # overlap:
        lambda V, v, USED, used, shape_number: v if used else V,
        # add:
        lambda V, v, USED, used, shape_number: V + v,
        # avg:
        lambda V, v, USED, used, shape_number: (V*shape_number+v)//(shape_number+1)
    )

    delta_x, delta_y = delta_xy

    x_from = delta_x - layer_fg.w//2
    y_from = delta_y - layer_fg.h//2

    x_to = layer_bg.w // 2
    y_to = layer_bg.h // 2

    layer_blend = Layer(layer_bg.wh, layer_bg.get_pixels_rgbau())

    for y in range(y_from, y_to):
        for x in range(x_from, x_to):
            color_bg = layer_bg._pixels[y, x]
            color_fg = layer_fg._pixels[y-delta_y, x-delta_x]

            R, G, B, A, USED = color_bg     # BACKGROUND
            r, g, b, a, used = color_fg     # foreground

            # if random.randint(0, 10**3) < 1: 
            #     print(f'{r=}, {g=}, {b=}, {a=}')

            layer_blend._pixels[y, x] = [
                blending_funcs[color_blending_type.value](R, r, USED, used, shape_number),
                blending_funcs[color_blending_type.value](G, g, USED, used, shape_number),
                blending_funcs[color_blending_type.value](B, b, USED, used, shape_number),
                blending_funcs[alpha_blending_type.value](A, a, USED, used, shape_number),
                used or USED
            ]

    return layer_blend

    # end of blend_layers



# [TODO]: replace by blend_layers and parse_and_render_<shape>
def render_shape (color: '(a, r, g, b)', check_func: 'function', shape_n: int,
        layer_wh: '(layer_w, layer_h)', tab: str, tabs: int,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default) -> Layer:

    raise DeprecatedException('func render_shape is deprecated, and shouldnt be used from now')

    layer_w, layer_h = layer_wh
    a, r, g, b = color[0], color[1], color[2], color[3]

    # layer = Layer(layer_wh)

    pixels = np.zeros((layer_h, layer_w, 4), dtype=np.uint8)

    if alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.overlap:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [r, g, b, a]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.add:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        pixels[y, x, 0] + r,
                        pixels[y, x, 1] + g,
                        pixels[y, x, 2] + b,
                        a
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.add and color_blending_type == ColorBlendingType.add:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        pixels[y, x, 0] + r,
                        pixels[y, x, 1] + g,
                        pixels[y, x, 2] + b,
                        pixels[y, x, 3] + a,
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.add and color_blending_type == ColorBlendingType.overlap:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        r,
                        g,
                        b,
                        pixels[y, x, 3] + a,
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    
    elif alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.avg:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        (pixels[y, x, 0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x, 1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x, 2]*shape_n+b)//(shape_n+1),
                        a
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.avg and color_blending_type == ColorBlendingType.avg:
        for y in range(layer_h):
            for x in range(layer_w):
                if check_func(x, y):
                    pixels[y, x] = [
                        (pixels[y, x, 0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x, 1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x, 2]*shape_n+b)//(shape_n+1),
                        (pixels[y, x, 3]*shape_n+a)//(shape_n+1)
                    ]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//layer_h}%')
            #print('\n\n\n')

    else:
        raise Exception(f'Error: This Blending Type Combination is unsupported for now: {color_blending_type = }, {alpha_blending_type = }')

    # end of render_shape 




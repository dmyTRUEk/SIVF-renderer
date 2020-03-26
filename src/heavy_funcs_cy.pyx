'''
This file contains all heavy functions, that accelerated with Cython

for compiling look in 'setup.py'

for manual generating html file on linux:   $ cython -a heavy_funcs_cy.pyx
''' 



from math import *

import numpy as np
cimport numpy as np



from alpha_blending import *
from color_blending import *





cpdef tuple cctargb (str color):
    return convert_color_to_argb(color)

cpdef tuple convert_color_to_argb (str color):
    cdef int a = 0, r = 0, g = 0, b = 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)
    else:
        raise Exception(f'Error -> convert_color_to_argb -> this color type is unsupported: {color}')
    return a, r, g, b



cpdef double cetu (str expression, tuple canvas_wh, dict var = {}):
    return convert_expression_to_units(expression, canvas_wh, var)

cpdef double convert_expression_to_units (str expression, tuple canvas_wh, dict var = {}):
    '''value could be:
    - units == pixels (145px)
    - precents (34%)
    - m, dm, cm, mm, nm ;)
    '''
    #print(f'{var = }')
    #print(f'{expression = }')
    for var_name in var:
         expression = expression.replace(var_name, var[var_name])
    #print(f'{expression = }\n')

    if expression[-1].isdigit():
        value = eval(expression)
        return float(value)
    
    elif expression.endswith('%'):
        canvas_w = canvas_wh[0]
        canvas_h = canvas_wh[1]
        value = eval(expression[:-1])
        return canvas_h * float(value) / 100

    elif expression.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise Exception('m, cm, mm, etc is not supported for now')

    else:
        raise Exception(f'Unknown dimension in {expression}')





ctypedef bint (*type_check_func) (double, double, tuple)



cdef bint is_in_circle (double x, double y, tuple args):
    return ( (x+args[0])**2 + (y+args[1])**2 < args[2] ) ^ args[3]



#                 0      1   2      3      4   5      6
#         args = (x_min, tx, x_max, y_min, ty, y_max, inverse)
cdef bint is_in_square (double x, double y, tuple args):
    return ( args[0] <= x+args[1] <= args[2] and args[3] <= y+args[4] <= args[5] ) ^ args[6]



cdef double triangle_sign (double x1, double y1, double x2, double y2, double x3, double y3):
    return (x1-x3)*(y2-y3) - (x2-x3)*(y1-y3)

#                                 x         y  0   1          2          3          4          5          6          7        8
#cdef bint is_in_triangle (double x, double y, tx, ty, double x1, double y1, double x2, double y2, double x3, double y3, bint inverse):
cdef bint is_in_triangle (double x, double y, tuple args): 
    cdef double d1 = triangle_sign(x+args[0], y+args[1], args[2], args[3], args[4], args[5])
    cdef double d2 = triangle_sign(x+args[0], y+args[1], args[4], args[5], args[6], args[7])
    cdef double d3 = triangle_sign(x+args[0], y+args[1], args[6], args[7], args[2], args[3])
    #has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    #has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    #return not (has_neg and has_pos)
    return not ( ((d1 < 0) or (d2 < 0) or (d3 < 0)) and ((d1 > 0) or (d2 > 0) or (d3 > 0)) ) ^ args[8]



#, dtype=np.uint8
cpdef void parse_shape (np.ndarray[unsigned char, ndim=3] pixels, dict shape, str shape_name, int shape_number,
        tuple canvas_wh, str tab, int tabs, dict var, 
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default,
        tuple delta_xy = (0, 0)):

    print((1+tabs)*tab+f'rendering {shape_name}:')

    cdef bint inverse = (shape['inverse'] == 'true') if 'inverse' in shape else False
    print((2+tabs)*tab+f'inverse = {inverse}')

    argb = cctargb(shape['color'][1:])
    cdef int a = argb[0]
    cdef int r = argb[1]
    cdef int g = argb[2]
    cdef int b = argb[3]
    print((2+tabs)*tab+f'a={a}, r={r}, g={g}, b={b}')

    print((2+tabs)*tab+f'delta_xy = {delta_xy}')

    cdef int canvas_w = canvas_wh[0]
    cdef int canvas_h = canvas_wh[1]

    cdef double tx, ty
    cdef double circle_x, circle_y, radius, radius2
    cdef double square_x, square_y, side, x_min, y_min, x_max, y_max

    #print(np_pixels.shape)
    #cdef unsigned char pixels[np_pixels.shape[0]][np_pixels.shape[1]][np_pixels.shape[2]]
    #= np_pixels

    # on every Y MINUS because pixel grid is growing down, but math coords grows to up

    if shape_name.startswith('circle'):   # circle
        circle_x = cetu(shape['xy'][0], canvas_wh, var) + delta_xy[0]
        circle_y = -cetu(shape['xy'][1], canvas_wh, var) + delta_xy[1]
        radius = cetu(shape['r'], canvas_wh, var)

        tx = -canvas_w/2 - circle_x + 1/2
        ty = -canvas_h/2 - circle_y + 1/2
        radius2 = radius**2

        render_shape(
            pixels, (a, r, g, b),
            #lambda double x, double y: ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse,
            is_in_circle, (tx, ty, radius2, inverse),
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
            #lambda double x, double y: ( x_min <= x+tx <= x_max and y_min <= y+ty <= y_max ) ^ inverse,
            is_in_square, (x_min, tx, x_max, y_min, ty, y_max, inverse),
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type,
        )

    elif shape_name.startswith('triangle'):   # triangle
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
            #lambda x, y: is_inside_triangle(x+tx, y+ty, x1, y1, x2, y2, x3, y3) ^ inverse,
            is_in_triangle, (tx, ty, x1, y1, x2, y2, x3, y3, inverse),
            shape_number, canvas_wh, tab, tabs,
            alpha_blending_type, color_blending_type
        )

    else:
        raise Exception(f'Unknown shape: shape_name = {shape_name}, shape = {shape}')

    # end of parse_shape()





cdef void render_shape (np.ndarray[unsigned char, ndim=3] pixels, tuple color,
        type_check_func check_func, tuple args,
        int shape_n, tuple canvas_wh, str tab, int tabs,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default,
        color_blending_type: ColorBlendingType = ColorBlendingType.default):

    cdef int canvas_w = canvas_wh[0], canvas_h = canvas_wh[1]

    #a, r, g, b = color[0], color[1], color[2], color[3]
    cdef int a = color[0]
    cdef int r = color[1]
    cdef int g = color[2]
    cdef int b = color[3]

    cdef int x, y

    if alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.overlap:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y, args):
                    pixels[y, x] = [r, g, b, a]
                #print(pixels[y, x], end=' ')
            if y % (100) == 0:
                print((tabs+3)*tab+f'{100*y//canvas_h}%')
            #print('\n\n\n')

    elif alpha_blending_type == AlphaBlendingType.overlap and color_blending_type == ColorBlendingType.add:
        for y in range(canvas_h):
            for x in range(canvas_w):
                if check_func(x, y, args):
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
                if check_func(x, y, args):
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
                if check_func(x, y, args):
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
                if check_func(x, y, args):
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
                if check_func(x, y, args):
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
        raise Exception(f'Unsupported Feature: Blending Type Combination: alpha_blending_type={alpha_blending_type}, color_blending_type={color_blending_type}')

    # end of render_object 




'''
This file contains all functions, responsible for value convertations
'''

from math import *
# from math import sqrt, abs, sin, cos


from funcs_errors import *





def c_rgbau_rgba (pixels_rgbau: 'array of r, g, b, a, used') -> 'array of r, g, b, a':
    ''' For documentation look into full named function. '''
    return convert_array_rgbau_to_array_rgba(pixels_rgbau)

def convert_array_rgbau_to_array_rgba (pixels_rgbau: 'array of (r,g,b,a,u') -> 'array of (r,g,b,a)':
    '''
    Converts array by Y by X of (r,g,b,a,u) -> array by Y by X of (r,g,b,a)
    '''
    return pixels_rgbau[:, :, :4]



def cctargb (color: '#aarrggbb') -> '(a, r, g, b)':
    ''' For documentation look into full named function. '''
    return convert_color_to_argb(color)

def convert_color_to_argb (color: '#aarrggbb') -> '(a, r, g, b)':
    '''
    Converts '#ffaabbcc' -> (255, 170, 187, 204)
    '''
    a, r, g, b = 0, 0, 0, 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)
    else:
        raise ErrorValueUnknown(color, 'maybe, len != 8 ?')
    return a, r, g, b



def cetu (expression: str, canvas_wh: '(canvas_w, canvas_h)', var: dict = {}):
    ''' For documentation look into full named function. '''
    return convert_expression_to_units(expression, canvas_wh, var)

def convert_expression_to_units (expression: str, canvas_wh: '(canvas_w, canvas_h)', var: dict = {}):
    '''
    Converts '42<dimention>' -> <dimetion rule>(42)

    Value could be:
    - units == pixels (145px)
    - precents (34%)
    - m, dm, cm, mm, nm, km ;)
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
        raise ErrorNotImpemented('m, cm, mm, etc is not supported for now')

    else:
        # raise ErrorUnknownValue(f'Unknown dimension in {expression = }')
        raise ErrorValueUnknown(expression, 'Unknown dimension')




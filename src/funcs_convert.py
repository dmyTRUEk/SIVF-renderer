'''
This file contains all functions, responsible for value convertations
'''

# from math import *
from math import sqrt, sin, cos   # abs
from random import randint, uniform, choice


from funcs_errors import *





def c_rgbau_rgba (pixels_rgbau: 'array of r, g, b, a, used') -> 'array of r, g, b, a':
    ''' For documentation look into full named function. '''
    return convert_array_rgbau_to_array_rgba(pixels_rgbau)

def convert_array_rgbau_to_array_rgba (pixels_rgbau: 'array of (r,g,b,a,u') -> 'array of (r,g,b,a)':
    '''
    Converts array by Y by X of (r,g,b,a,u) -> array by Y by X of (r,g,b,a)
    '''
    return pixels_rgbau[:, :, :4]



def cctargb (color: 'aarrggbb') -> '(a, r, g, b)':
    ''' For documentation look into full named function. '''
    return convert_color_to_argb(color)

def convert_color_to_argb (color: 'aarrggbb') -> '(a, r, g, b)':
    '''
    Converts 'ffaabbcc' -> (255, 170, 187, 204)
    '''
    def random_color_rgb (alpha: str) -> 'AARRGGBB':
        symbols = '0123456789abcdef'
        if len(alpha) != 2:
            raise ErrorValueWrong(alpha, 'len(alpha) must be 2')
        res = alpha
        for _ in range(6):
            res += choice(symbols)
        return res

    def random_color_argb () -> 'AARRGGBB':
        symbols = '0123456789abcdef'
        for _ in range(8):
            res += choice(symbols)
        return res

    color = str(color)
    a, r, g, b = 0, 0, 0, 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)
    elif len(color) < 8:
        # this needed for YAML :(
        while len(color) < 8:
            color = '0' + color
        a, r, g, b = bytes.fromhex(color)
    elif len(color) > 8:
        color = eval(color)
        a, r, g, b = bytes.fromhex(color)
    else:
        raise ErrorValueUnknown(color, 'maybe, len != 8 ?')

    return a, r, g, b



def cetu (expression: str, canvas_w: int, canvas_h: int, var: dict = {}):
    ''' For documentation look into full named function. '''
    return convert_expression_to_units(expression, canvas_w, canvas_h, var)

def convert_expression_to_units (expression: str, canvas_w: int, canvas_h: int, var: dict = {}):
    '''
    Converts '42<dimention>' -> <dimetion rule>(42)

    Value could be:
    - units == pixels (145px)
    - precents (34%)
    - m, dm, cm, mm, nm, km ;)
    '''
    expression = str(expression)
    #print(f'{var = }')
    #print(f'{expression = }')
    for var_name in var:
        expression = expression.replace(var_name, str(var[var_name]))
    #print(f'{expression = }\n')

    # def random_float (x_min: float, x_max: float) -> float:
    #     return uniform(x_min, x_max)
    random_int = randint
    random_float = uniform

    if expression[-1].isdigit():
        value = eval(expression)
        return float(value)
    
    elif expression.endswith('%'):
        # canvas_w = canvas_w, canvas_h[0]
        # canvas_h = canvas_w, canvas_h[1]
        value = eval(expression[:-1])
        return canvas_h * float(value) / 100

    elif expression.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise ErrorNotImpemented('m, cm, mm, etc is not supported for now')

    else:
        # raise ErrorUnknownValue(f'Unknown dimension in {expression = }')
        raise ErrorValueUnknown(expression, 'Unknown dimension')




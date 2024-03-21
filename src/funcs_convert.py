'''
This file contains all functions, responsible for value convertations
'''

# from math import *
from math import sqrt, sin, cos   # abs
from random import randint, uniform, choice


from funcs_errors import *


from consts_sivf_keywords import *
from funcs_utils import remove_prefix, add_prefix
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType





def convert_dict_sivf_to_dict_data (dict_sivf: str, canvas_w: int, canvas_h: int, defined_vars: dict) -> dict:
    '''
    using convert functions everywhere where needed
    '''
    # print(f'\n"{dict_sivf = }"\n')

    # def cbstbd (bool_sivf):
    #     return convert_bool_sivf_to_bool_data(bool_sivf)
    def convert_bool_sivf_to_bool_data (bool_sivf: 'bool or str') -> bool:
        if (t := type(bool_sivf)) == bool:
            inverse = bool_sivf
        elif t == str:
            inverse = (bool_sivf == KW_TRUE)
        else:
            ErrorTypeWrong(bool_sivf, 'bool_sivf', 'bool or str')
        return inverse

    dict_data = {}

    for key in dict_sivf:
        if key == KW_CANVAS_WH:
            dict_data[KW_CANVAS_WH] = [
                int(dict_sivf[KW_CANVAS_WH][0]),
                int(dict_sivf[KW_CANVAS_WH][1])
            ]

        elif key == KW_COLOR_SCHEME:
            dict_data[KW_COLOR_SCHEME] = dict_sivf[KW_COLOR_SCHEME]

        elif key == KW_IMAGE:
            dict_data[KW_IMAGE] = convert_dict_sivf_to_dict_data(dict_sivf[KW_IMAGE], canvas_w, canvas_h, defined_vars)

        elif key == KW_VARS:
            # TODO: add support for eval() in vars
            dict_data[KW_VARS] = dict_sivf[KW_VARS]

        elif key == KW_BLENDING:
            # dict_data[KW_BLENDING] = dict_sivf[KW_BLENDING]
            alpha_blending_type = AlphaBlendingType.from_str(dict_sivf[KW_BLENDING][0])
            color_blending_type = ColorBlendingType.from_str(dict_sivf[KW_BLENDING][1])
            dict_data[KW_BLENDING] = [alpha_blending_type, color_blending_type]

        elif key == KW_COLOR:
            dict_data[KW_COLOR] = cctargb(str(dict_sivf[KW_COLOR]))

        elif key == KW_INVERSE:
            dict_data[KW_INVERSE] = convert_bool_sivf_to_bool_data(dict_sivf[KW_INVERSE])

        elif key == KW_USED:
            dict_data[KW_USED] = convert_bool_sivf_to_bool_data(dict_sivf[KW_USED])

        elif key == KW_XY:
            i = 0
            tmp = []
            for value in dict_sivf[KW_XY]:
                tmp.append(
                    (1.0 if (i % 2 == 0) else -1.0) * convert_expression_to_units(
                        value, canvas_w, canvas_h, defined_vars
                    )
                )
                i += 1

            dict_data[KW_XY] = tmp

        elif key.startswith(KW_CIRCLE):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        elif key == KW_CIRCLE_R:
            dict_data[KW_CIRCLE_R] = convert_expression_to_units(dict_sivf[KW_CIRCLE_R], canvas_w, canvas_h, defined_vars)

        elif key.startswith(KW_COMBINE):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        elif key == KW_COMBINE_FIGURES:
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[KW_COMBINE_FIGURES], canvas_w, canvas_h, defined_vars)


        elif key == KW_COMBINE_TYPE:
            dict_data[KW_COMBINE_TYPE] = dict_sivf[KW_COMBINE_TYPE]

        elif key.startswith(KW_GRADIENT):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        elif key == KW_GRADIENT_IS_FADING:
            dict_data[KW_GRADIENT_IS_FADING] = dict_sivf[KW_GRADIENT_IS_FADING]

        elif key == KW_GRADIENT_POINTS:
            dict_data[KW_GRADIENT_POINTS] = {}
            for key_point in dict_sivf[KW_GRADIENT_POINTS]:
                dict_data[KW_GRADIENT_POINTS][key_point] = convert_dict_sivf_to_dict_data(dict_sivf[KW_GRADIENT_POINTS][key_point], canvas_w, canvas_h, defined_vars)

        elif key == KW_GRADIENT_SIGMA:
            dict_data[KW_GRADIENT_SIGMA] = convert_expression_to_units(dict_sivf[KW_GRADIENT_SIGMA], canvas_w, canvas_h, defined_vars)

        elif key.startswith(KW_LAYER):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        elif key == KW_LAYER_DELTA_XY:
            dict_data[KW_LAYER_DELTA_XY] = [
                int(convert_expression_to_units(dict_sivf[KW_LAYER_DELTA_XY][0], canvas_w, canvas_h, defined_vars)),
                -int(convert_expression_to_units(dict_sivf[KW_LAYER_DELTA_XY][1], canvas_w, canvas_h, defined_vars))
            ]

        elif key.startswith(KW_MESH) or key == KW_MESH_N_XLEFT_YDOWN_XRIGHT_YUP:
            raise ErrorNotImpemented('mesh isnt ready yet... :(')

        elif key.startswith(KW_SQUARE):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        elif key == KW_SQUARE_SIDE:
            dict_data[KW_SQUARE_SIDE] = convert_expression_to_units(dict_sivf[KW_SQUARE_SIDE], canvas_w, canvas_h, defined_vars)

        elif key.startswith(KW_TRIANGLE):
            dict_data[key] = convert_dict_sivf_to_dict_data(dict_sivf[key], canvas_w, canvas_h, defined_vars)

        else:
            raise ErrorValueUnknown(key, f'{key = } in {dict_sivf = }')

    # print(f'\n"{dict_data = }"\n')
    return dict_data

    # end of convert_dict_sivf_to_dict_data()



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
    Converts 'ffaabbcc' or '#ffaabbcc' -> (255, 170, 187, 204)
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

    elif len(color) == 9:
        color = remove_prefix(color, '#')
        a, r, g, b = bytes.fromhex(color)

    elif len(color) < 8:
        # this needed for YAML :(
        color = add_prefix(color, '0', 8)
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
    expression = expression.strip()
    #print(f'{var = }')
    #print(f'{expression = }')
    # TODO: sort by length, so firstly it replaces longest vars, and only then shorter
    for var_name in var:
        expression = expression.replace(var_name, str(var[var_name]))
    #print(f'{expression = }\n')

    random_int = randint
    random_float = uniform

    if expression[-1].isdigit():
        value = eval(expression)
        return float(value)
    
    elif expression.endswith('%'):
        value = eval(expression[:-1])
        return canvas_h * float(value) / 100

    elif expression.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise ErrorNotImpemented('m, cm, mm, etc is not supported for now')

    else:
        # raise ErrorUnknownValue(f'Unknown dimension in {expression = }')
        raise ErrorValueUnknown(expression, 'Unknown dimension')




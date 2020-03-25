'''
This file contains all functions, responsible for value convertations
'''



from math import *





def cctargb (color: str) -> '(a, r, g, b)':
    return convert_color_to_argb(color)

def convert_color_to_argb (color: str) -> '(a, r, g, b)':
    a, r, g, b = 255, 0, 255, 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)
    else:
        raise Exception(f'Error -> convert_color_to_argb -> this color type is unsupported: {color = }')
    return a, r, g, b



def cetu (expression: str, canvas_wh: '(canvas_w, canvas_h)', var: dict = {}):
    return convert_expression_to_units(expression, canvas_wh, var)

def convert_expression_to_units (expression: str, canvas_wh: '(canvas_w, canvas_h)', var: dict = {}):
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
        return float(expression)
    
    elif expression.endswith('%'):
        canvas_w = canvas_wh[0]
        canvas_h = canvas_wh[1]
        value = eval(expression[:-1])
        return canvas_h * float(value) / 100

    elif expression.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise Exception('m, cm, mm, etc is not supported for now')

    else:
        raise Exception(f'Unknown dimension in {expression = }')














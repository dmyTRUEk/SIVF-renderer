'''
This file contains all functions, responsible for value convertations
'''



def cctargb (color: str) -> '(a, r, g, b)':
    return convert_color_to_argb(color)

def convert_color_to_argb (color: str) -> '(a, r, g, b)':
    a, r, g, b = 255, 0, 255, 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)
    else:
        raise Exception(f'Error -> convert_color_to_argb -> this color type is unsupported: {color = }')
    return a, r, g, b



def cetu (value: str, canvas_wh: '(canvas_w, canvas_h)'):
    return convert_expression_to_units(value, canvas_wh)

def convert_expression_to_units (value: str, canvas_wh: '(canvas_w, canvas_h)'):
    '''value could be:
    - units == pixels (145px)
    - precents (34%)
    - m, dm, cm, mm, nm ;)
    '''
    if value[-1].isdigit():
        return float(value)
    
    elif value.endswith('%'):
        canvas_w = canvas_wh[0]
        canvas_h = canvas_wh[1]
        return canvas_h * float(value[:-1]) / 100

    elif value.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise Exception('m, cm, mm, etc is not supported for now')

    else:
        raise Exception(f'Unknown dimension in \'{value = }\'')














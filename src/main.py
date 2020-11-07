'''
SIVF-renderer   v0.4.0a2

This is main file of SIVF-renderer
''' 

import sys
# import random

import re
# import json
from os import listdir
from os.path import isfile, join

import numpy as np
from PIL import Image


from funcs_errors import *
from funcs_warnings import *

from consts_sivf_keywords import *
from config import *

from class_canvas import Canvas
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *
import funcs_utils


if CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_JSON:
    import json

elif CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_YAML:
    raise ErrorNotImpemented('YAML sivf backend')

elif CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_ANY:
    raise ErrorNotImpemented('Any sivf backend')


if CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_PYTHON:
    from funcs_heavy_py import *

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_CYTHON:
    raise ErrorNotImpemented('Cython render backend')
    # from funcs_heavy_cy import *

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_RUST:
    raise ErrorNotImpemented('Rust render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_NUMPY:
    raise ErrorNotImpemented('Numpy render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_GPU:
    raise ErrorNotImpemented('GPU render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_ANY:
    raise ErrorNotImpemented('Any render backend')





TAB = '    '   # for fancy logs
tabs = 0





def main () -> None:
    argv = sys.argv
    argv.pop(0)

    file_to_open = ''

    if argv:
        file_to_open = argv[0]
        #print(f'I will open \'{file_to_open}\'')
        render_from_file(file_to_open)

    else:   # ask what file you want to open
        path_to_here = '.'
        all_files = [f for f in listdir(path_to_here) if isfile(join(path_to_here, f))]
        all_sivf_files = [f_sivf for f_sivf in all_files if f_sivf.endswith('.sivf')]
        all_sivf_files.sort()
        #print(all_sivf_files)

        max_number = len(all_sivf_files)
        print(f'Choose file: (input 1..{max_number})')
        for i in range(len(all_sivf_files)):
            print(f'{i+1}) {all_sivf_files[i]}')
        print()

        while inputed_text := input():   # input until int and in range 1..max_number
            if inputed_text.isdigit() and 1 <= (inputed_number:=int(inputed_text)) <= max_number:
                #print(f'So, your input is {inputed_number}')
                file_to_open = all_sivf_files[inputed_number-1]   # because of arrays counts from 0
                #print(f'I will open \'{file_to_open}\'')
                render_from_file(file_to_open)
                break
            else:
                print(f'Please input number in 1..{max_number} to choose file')
        print()
    
    # end of main



def render_from_file (file_name: str) -> None:
    print(f'Starting Render of \'{file_name}\'\n')

    file = open(file_name, 'r')
    content = ''
    #print('content = ', end='')
    for line in file:
        print(line, end='')
        content += line
    print()

    render_from_content(content)



def render_from_content (content: dict) -> None:
    # delete all comments   /* blahblahblah */
    content = re.sub(re.compile('/\*.*?\*/', re.DOTALL), '', content)

    # delete all comment   // blahblahblah
    content = re.sub(re.compile('//.*?\n'), '', content)

    #print(content)
    content_dict = json.loads(content)
    #print_all_about(content_dict)

    global defined_vars

    canvas_wh = ( int(content_dict[KW_CANVAS_WH][0]), int(content_dict[KW_CANVAS_WH][1]) )

    color_scheme = content_dict[KW_COLOR_SCHEME]
    image_dict = content_dict[KW_IMAGE]
    #print(f'{image_dict = }\n')

    # [TODO]: wtf is this?
    # delete all what is not layer
    keys_to_delete = []
    for key in image_dict:
        if not key.startswith(KW_LAYER):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del image_dict[key]

    # print(f'{image_dict = }\n')

    defined_vars = content_dict[KW_VARS] if KW_VARS in content_dict else {}

    shape_number = 0

    funcs_utils.timer_begin()
    canvas_rendered = parse_and_render_entity(image_dict, '', shape_number, canvas_wh)
    funcs_utils.timer_end()
    funcs_utils.timer_show()

    if canvas_rendered.wh != canvas_wh:
        raise ErrorNotEqual(canvas_rendered.wh, canvas_wh, 'canvas_rendered.wh', KW_CANVAS_WH)

    save_canvas_to_image(canvas_rendered, 'image.png')
    show_canvas_to_image(canvas_rendered)

    # end of render_from_content



def save_canvas_to_image (canvas: Canvas, output_file_name: str):
    result_image = Image.fromarray(canvas.get_pixels_rgba(), 'RGBA')
    result_image.save(output_file_name)



def show_canvas_to_image (canvas: Canvas):
    Image.fromarray(canvas.get_pixels_rgba(), 'RGBA').show()



def parse_and_render_entity (entity: dict, entity_name: str, shape_number: int,
        canvas_wh: '(canvas_w, canvas_h)', delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Canvas:
    global TAB, tabs, defined_vars

    canvas_rendering = Canvas(canvas_wh)

    alpha_blending_type = AlphaBlendingType.default
    color_blending_type = ColorBlendingType.default

    #for      key      in  dict :
    for subentity_name in entity:
        print((tabs)*TAB+f'parsing {subentity_name}:')
        subentity = entity[subentity_name]

        if subentity_name.startswith(KW_BLENDING):   # blending
            alpha_blending_type = AlphaBlendingType.from_str(entity[KW_BLENDING][0])
            color_blending_type = ColorBlendingType.from_str(entity[KW_BLENDING][1])
            # print(f'{alpha_blending_type = }')
            # print(f'{color_blending_type = }')

        elif subentity_name.startswith(KW_LAYER):   # layer
            tabs += 1
            canvas_layer = parse_and_render_entity(subentity, subentity_name, shape_number, canvas_wh, delta_xy)
            tabs -= 1
            canvas_rendering = blend_canvases(
                canvas_rendering, canvas_layer, shape_number,
                alpha_blending_type, color_blending_type
            )

        elif subentity_name.startswith(KW_DELTA_XY):
            # print(f'{subentity = }')
            delta_x = int( cetu(subentity[0], canvas_wh, defined_vars) )
            delta_y = int( cetu(subentity[1], canvas_wh, defined_vars) )
            delta_xy = delta_x, delta_y

        elif subentity_name.startswith(KW_MESH):   # mesh
            raise ErrorNotImpemented()
            entity_layer_repeated = subentity[KW_LAYER]
            n_xleft_ydown_xright_yup = subentity[KW_N_XLEFT_YDOWN_XRIGHT_YUP]
            nxyxy = n_xleft_ydown_xright_yup   # for shorteness
            nxyxy = (
                int(cetu(nxyxy[0], canvas_wh, defined_vars)),
                int(cetu(nxyxy[1], canvas_wh, defined_vars)),
                int(cetu(nxyxy[2], canvas_wh, defined_vars)),
                int(cetu(nxyxy[3], canvas_wh, defined_vars))
            )
            _delta_xy_str = subentity[KW_DELTA_XY]

            _delta_x = cetu(_delta_xy_str[0], canvas_wh, defined_vars)
            _delta_y = cetu(_delta_xy_str[1], canvas_wh, defined_vars)

            tabs += 1
            for h in range(-nxyxy[1], nxyxy[3]+1):
                for w in range(-nxyxy[0], nxyxy[2]+1):
                    print((tabs)*TAB+f'parsing mesh[{w}][{h}]:')
                    tabs += 1
                    parse_and_render_entity(
                        entity_layer_repeated,
                        KW_LAYER,
                        shape_number,
                        canvas_wh,
                        (w*_delta_x, h*_delta_y)
                    )
                    tabs -= 1
            tabs -= 1

        #elif ...:   # other special entities

        else:   # shape
            canvas_shape = parse_and_render_shape(
                subentity, subentity_name, shape_number,
                canvas_wh, TAB, tabs, defined_vars,
                alpha_blending_type, color_blending_type,
            )
            canvas_rendering = blend_canvases(
                canvas_rendering, canvas_shape, shape_number,
                alpha_blending_type, color_blending_type, delta_xy
            )

        print()

    return canvas_rendering

    # end of parse_and_render_entity()





if __name__ == '__main__':
    main()
    print('\n'*5)




'''
SIVF-renderer   v0.5.0a1

This is main file of SIVF-renderer
''' 

import sys
# import random

import re
# import json
from os import listdir
from os.path import isfile, join
import datetime

import numpy as np
from PIL import Image


from funcs_errors import *
from funcs_warnings import *

from config import *
from consts_sivf_keywords import *

from class_canvas import Canvas
from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *
import funcs_utils


if CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_JSON:
    import json

elif CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_YAML:
    import yaml
    # raise ErrorNotImpemented('YAML sivf backend')

elif CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_ANY:
    raise ErrorNotImpemented('Any sivf backend')

else:
    raise ErrorValueUnknown(CONFIG_SIVF_BACKEND)


if CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_PYTHON:
    from funcs_heavy_python import *

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_CYTHON:
    # raise ErrorNotImpemented('Cython render backend')
    from funcs_heavy_cython import *

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_NUMBA:
    raise ErrorNotImpemented('Numba render backend')
    # from funcs_heavy_numba import *

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_RUST:
    raise ErrorNotImpemented('Rust render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_NUMPY:
    raise ErrorNotImpemented('Numpy render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_GPU:
    raise ErrorNotImpemented('GPU render backend')

elif CONFIG_RENDER_BACKEND == CONFIG_RENDER_BACKEND_ANY:
    raise ErrorNotImpemented('Any render backend')

else:
    raise ErrorValueUnknown(CONFIG_RENDER_BACKEND)





def main () -> None:
    argv = sys.argv
    argv.pop(0)

    file_to_open = ''

    if argv:
        file_to_open = argv[0]
        #print(f'I will open \'{file_to_open}\'')
        # render_from_file(file_to_open)

    else:   # ask what file you want to open
        file_to_open = unpure_ask_user_for_file()

    content_str, file_output_name_without_ext = unpure_load_sivf_file(file_to_open)

    content_str = remove_comments(content_str)
    # Log(content_str)

    # convert str to dict
    content_dict_sivf = load_dict_from_str(content_str)
    Log(content_dict_sivf)

    # load canvas sizes and defined_vars
    canvas_w = int(content_dict_sivf[KW_CANVAS_WH][0])
    canvas_h = int(content_dict_sivf[KW_CANVAS_WH][1])
    defined_vars = load_vars_from_dict(content_dict_sivf)

    print(f'\nbefore = "{content_dict_sivf}"\n')
    content_dict_data = convert_dict_sivf_to_dict_data(content_dict_sivf, canvas_w, canvas_h, defined_vars)
    print(f'\nafter  = "{content_dict_data}"\n')

    # render:
    canvas_rendered = render_from_content(content_dict_data)

    # add_prefix = funcs_utils.add_prefix
    def add_prefix(text: str, length: int):
        text = str(text)
        return funcs_utils.add_prefix(text, '0', length)

    dt_now = datetime.datetime.now()
    dt_now_str = f'{add_prefix(dt_now.year, 4)}_{add_prefix(dt_now.month, 2)}_{add_prefix(dt_now.day, 2)}__{add_prefix(dt_now.hour, 2)}_{add_prefix(dt_now.minute, 2)}_{add_prefix(dt_now.second, 2)}__{add_prefix(dt_now.microsecond, 6)}'
    # print(dt_now_str)
    file_output_name = f'{file_output_name_without_ext}_{dt_now_str}_{canvas_w}x{canvas_h}' + '.png'

    # save all:
    unpure_save_canvas_to_image(canvas_rendered, file_output_name)
    unpure_show_canvas_to_image(canvas_rendered)
    
    # end of main



def unpure_ask_user_for_file () -> str:
    path_to_here = '.'
    all_files = [f for f in listdir(path_to_here) if isfile(join(path_to_here, f))]
    all_sivf_files = [f_sivf for f_sivf in all_files if f_sivf.endswith('.sivf')]
    all_sivf_files.sort()

    max_number = len(all_sivf_files)
    print(f'Choose file: (input 1..{max_number})')
    for i in range(len(all_sivf_files)):
        print(f'{i+1}) {all_sivf_files[i]}')
    print()

    while inputed_text := input():   # input until int and in range 1..max_number
        if inputed_text.isdigit() and 1 <= (inputed_number:=int(inputed_text)) <= max_number:
            file_to_open = all_sivf_files[inputed_number-1]   # because of arrays counts from 0
            return file_to_open
        else:
            print(f'Please input number in range 1..{max_number} to choose file')
    print()



def unpure_load_sivf_file (file_to_open: str) -> None:
    Log(f'Starting Render of \'{file_to_open}\'\n')

    # TODO: rewrite using with ... open...
    file_input = open(file_to_open, 'r')
    file_content = ''
    #print('file_content = ', end='')
    for line in file_input:
        # Log(line, end='')
        file_content += line
    Log('\n'+file_content)

    # file_output_name_without_ext -> file output name without extension
    file_output_name_without_ext = funcs_utils.remove_suffix(file_to_open, '.sivf')
    return file_content, file_output_name_without_ext



def load_dict_from_str (content_str: str) -> dict:
    '''convert JSON or YAML or any other to PYTHON DICT '''

    if CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_JSON:
        content_dict = json.loads(content_str)

    elif CONFIG_SIVF_BACKEND == CONFIG_SIVF_BACKEND_YAML:
        content_dict = yaml.load(content_str, Loader=yaml.FullLoader)

    else:
        raise ErrorValueWrong(CONFIG_SIVF_BACKEND)

    return content_dict



def remove_comments (content_str: str) -> str:
    return remove_comments_oneline(remove_comments_multiline(content_str))

def remove_comments_oneline (content_str: str) -> str:
    '''delete all comments   // blahblahblah '''
    # return re.sub(re.compile('//.*?\n'), '', content_str)
    # return re.sub(re.compile('//.*?$'), '', content_str)
    return re.sub(re.compile('//.*?\n'), '\n', content_str)

def remove_comments_multiline (content_str: str) -> str:
    '''delete all comments   /* blahblahblah */ '''
    return re.sub(re.compile('/\*.*?\*/', re.DOTALL), '', content_str)



def load_vars_from_dict (content_dict: dict) -> dict:
    return content_dict[KW_VARS] if KW_VARS in content_dict else {}


def render_from_content (content_dict_data: dict) -> Canvas:
    canvas_w, canvas_h = content_dict_data[KW_CANVAS_WH]

    # color_scheme = content_dict[KW_COLOR_SCHEME]
    image_dict = content_dict_data[KW_IMAGE]

    # deletes all what is not layer in "image" (for example blending):
    # keys_to_delete = []
    # for key in image_dict:
    #     if not key.startswith(KW_LAYER):
    #         keys_to_delete.append(key)
    # for key in keys_to_delete:
    #     del image_dict[key]
    # Log(f'{image_dict = }\n')

    if KW_VARS in content_dict_data:
        defined_vars = content_dict_data[KW_VARS]
    else:
        defined_vars = {}

    # funcs_utils.timer_begin()
    time_begin = funcs_utils.get_current_time()
    canvas_rendered = parse_and_render_entity(image_dict, canvas_w, canvas_h, 0, 0, defined_vars, 0, 0)
    timer_end = funcs_utils.get_current_time()
    # funcs_utils.timer_end()
    # funcs_utils.timer_show()
    print()
    Log(f'Time elapsed TOTALLY: {funcs_utils.delta_time(time_begin, timer_end)} seconds')

    if canvas_rendered.w != canvas_w or canvas_rendered.h != canvas_h:
        raise ErrorNotEqual((canvas_rendered.w, canvas_rendered.h), (canvas_w, canvas_h), 'canvas_rendered.wh', KW_CANVAS_WH)

    return canvas_rendered

    # end of render_from_content



def unpure_save_canvas_to_image (canvas: Canvas, output_file_name: str) -> None:
    result_image = Image.fromarray(canvas.get_pixels_rgba(), PIL_IMAGE_OUTPUT_MODE)
    result_image.save(output_file_name)



def unpure_show_canvas_to_image (canvas: Canvas) -> None:
    Image.fromarray(canvas.get_pixels_rgba(), PIL_IMAGE_OUTPUT_MODE).show()





if __name__ == '__main__':
    main()
    print('\n'*5)




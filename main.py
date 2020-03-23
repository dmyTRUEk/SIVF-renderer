'''
SIVF-renderer   v0.2

This is main file of SIVF-renderer
''' 



import sys
import random

from os import listdir
from os.path import isfile, join
import re
import json

import numpy as np
from PIL import Image

from enum import Enum



import utils





class ColorsBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2

class AlphaBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2





def render_object (pixels: 'nparray2d', color: '(a, r, g, b)', check_func: 'function', obj_n: int,
        colors_blending_type: 'ColorsBlendingType' = ColorsBlendingType.default,
        alpha_blending_type: 'AlphaBlendingType' = AlphaBlendingType.default) -> None:
    global canvas_w, canvas_h

    a, r, g, b = color[0], color[1], color[2], color[3]

    if colors_blending_type == ColorsBlendingType.overlap and alpha_blending_type == AlphaBlendingType.overlap:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (r, g, b, a)
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    elif colors_blending_type == ColorsBlendingType.add and alpha_blending_type == AlphaBlendingType.overlap:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        pixels[y, x][0] + r,
                        pixels[y, x][1] + g,
                        pixels[y, x][2] + b,
                        a
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    elif colors_blending_type == ColorsBlendingType.add and alpha_blending_type == AlphaBlendingType.add:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        pixels[y, x][0] + r,
                        pixels[y, x][1] + g,
                        pixels[y, x][2] + b,
                        pixels[y, x][3] + a,
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')
    
    elif colors_blending_type == ColorsBlendingType.avg and alpha_blending_type == AlphaBlendingType.overlap:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        (pixels[y, x][0]*obj_n+r)//(obj_n+1),
                        (pixels[y, x][1]*obj_n+g)//(obj_n+1),
                        (pixels[y, x][2]*obj_n+b)//(obj_n+1),
                        a
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    elif colors_blending_type == ColorsBlendingType.avg and alpha_blending_type == AlphaBlendingType.avg:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        (pixels[y, x][0]*obj_n+r)//(obj_n+1),
                        (pixels[y, x][1]*obj_n+g)//(obj_n+1),
                        (pixels[y, x][2]*obj_n+b)//(obj_n+1),
                        (pixels[y, x][3]*obj_n+a)//(obj_n+1)
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    else:
        raise Exception(f'This blending type is unsupported for now: {colors_blending_type = }, {alpha_blending_type = }')

    # end of render_object 



def prepare_render_object (pixels: 'nparray2d', obj_name: str, obj: dict, obj_number: int) -> None:
    print(1*'    '+f'rendering {obj_name}:')

    inverse = (obj['inverse'] == 'true') if 'inverse' in obj else False
    print(2*'    '+f'{inverse = }')

    a, r, g, b = cctargb(obj['color'][1:])
    print(2*'    '+f'{a=}, {r=}, {g=}, {b=}')

    if obj_name.startswith('circle'):
        circle_x = cetu(obj['xy'][0])
        circle_y = -cetu(obj['xy'][1])   # MINUS because pixel grid is growing down, but math coords grows to up
        radius = cetu(obj['r'])

        tx = -canvas_w/2 - circle_x + 1/2
        ty = -canvas_h/2 - circle_y + 1/2
        radius2 = radius**2
        render_object(
            pixels,
            (a, r, g, b),
            lambda x, y: ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse,
            obj_number,
            ColorsBlendingType.overlap,
            AlphaBlendingType.overlap
        )
    
    elif obj_name.startswith('square'):
        square_x = cetu(obj['xy'][0])
        square_y = -cetu(obj['xy'][1])   # MINUS because pixel grid is growing down, but math coords grows to up
        side = cetu(obj['side'])

        tx_min = square_x - side/2;   tx_max = square_x + side/2
        ty_min = square_y - side/2;   ty_max = square_y + side/2
        render_object(
            pixels,
            (a, r, g, b),
            lambda x, y: ( tx_min <= x-canvas_w/2 <= tx_max and ty_min <= y-canvas_h/2 <= ty_max ) ^ inverse,
            obj_number,
            ColorsBlendingType.overlap,
            AlphaBlendingType.overlap
        )

    #print()



def render_from_image_code (image_sizes: '(w, h)', color_scheme: str, image_code: dict) -> None:
    global canvas_w, canvas_h
    canvas_w, canvas_h = image_sizes

    pixels = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)   # create np array

    # unneccesary, because np.zeros already do this :)
    #pixels[:, :] = (0, 0, 0, 0)   # set default value as tranparent

    obj_number = 0

    utils.timer_begin()

    for layer_name in image_code:
        print(f'rendering {layer_name}:')
        layer = image_code[layer_name]

        for obj_name in image_code[layer_name]:
            obj_number += 1

            obj = layer[obj_name]

            prepare_render_object(pixels, obj_name, obj, obj_number)
        print()

    print()

    utils.timer_end()


    #print(pixels)

    result_image = Image.fromarray(pixels, 'RGBA')
    result_image.save('image.png')
    result_image.show()



def cctargb (color: str) -> '(a, r, g, b)':
    return convert_color_to_argb(color)

def convert_color_to_argb (color: str) -> '(a, r, g, b)':
    a, r, g, b = 255, 0, 255, 0
    if len(color) == 8:
        a, r, g, b = bytes.fromhex(color)

    return a, r, g, b



def cetu (value: str):
    return convert_expression_to_units(value)

def convert_expression_to_units (value: str):
    '''value could be:
    - units == pixels (145px)
    - precents (34%)
    - m, dm, cm, mm, nm ;)
    '''
    if value[-1].isdigit():
        return float(value)
    
    elif value.endswith('%'):
        global canvas_w, canvas_h
        return canvas_w * float(value[:-1]) / 100

    elif value.endswith('m'):
        # find if it is m of dm or cm or mm ot nm or other
        raise Exception('m, cm, mm, etc is not supported for now')

    else:
        raise Exception(f'Unknown dimension in \'{value = }\'')



def render_from_content (content: dict):
    # delete all comments   /* blahblahblah */
    content = re.sub(re.compile('/\*.*?\*/', re.DOTALL), '', content)

    # delete all comment   // blahblahblah
    content = re.sub(re.compile('//.*?\n'), '', content)

    #print(content)
    content_dict = json.loads(content)
    #print_all_about(content_dict)

    sizes_wh = content_dict['sizes_wh']
    image_sizes = ( int(sizes_wh[0]), int(sizes_wh[1]) )
    color_scheme = content_dict['color_scheme']
    image_dict = content_dict['image']

    #print('image =', image_dict, '\n')

    # delete all what is not layer
    keys_to_delete = []
    for key in image_dict:
        if not key.startswith('layer'):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del image_dict[key]

    #print(f'{image_dict = }\n')

    render_from_image_code(image_sizes, color_scheme, image_dict)



def render_from_file (file_name: str):
    print(f'Starting Render \'{file_name}\'\n')

    file = open(file_name, 'r')
    content = ''
    #print('content = ', end='')
    for line in file:
        print(line, end='')
        content += line
    print()

    render_from_content(content)



def render_from_random (seed=None):
    if seed:
        random.seed(seed)

    content_dict = {
        'sizes_wh': ['1000', '1000'],
        'color_scheme': 'rgb'
    }

    image_dict = {}
    for i in range(100):
        image_dict['layer1']




def run_custom ():
    print('Choose type:\nr) Random\ns) Random with Seed\nb) Back\n')
    while inputed_text := input():   # input until int and in range 1..max_number
        if inputed_text == 'r':   # random
            render_from_random()
            break
        elif inputed_text == 's':   # random with seed
            seed = int(input('Input seed: '))
            render_from_random(seed)
            break
        elif inputed_text == 'b':   # back
            print()
            return 'back'
        else:
            print('Please choose type:\nr) Random\nrs) Random with Seed\nb) Back\n')
    


def main ():
    argv = sys.argv
    argv.pop(0)

    file_to_open = ''

    if argv:
        file_to_open = argv[0]
        #print(f'I will open \'{file_to_open}\'')
        render_from_file(file_to_open)

    else:
        # ask what file you want to open
        path_to_here = '.'
        all_files = [f for f in listdir(path_to_here) if isfile(join(path_to_here, f))]
        all_sivf_files = [f_sivf for f_sivf in all_files if f_sivf.endswith('.sivf')]
        all_sivf_files.sort()
        #print(all_sivf_files)

        max_number = len(all_sivf_files)
        print(f'Choose file: (press 1..{max_number})')
        for i in range(len(all_sivf_files)):
            print(f'{i+1}) {all_sivf_files[i]}')
        print()

        while inputed_text := input():   # input until int and in range 1..max_number
            if inputed_text.isdigit() and 1 <= int(inputed_text) <= max_number:
                inputed_number = int(inputed_text)
                #print(f'So, your input is {inputed_number}')
                file_to_open = all_sivf_files[inputed_number-1]   # because of arrays counts from 0
                #print(f'I will open \'{file_to_open}\'')
                render_from_file(file_to_open)
                break
            elif inputed_text == 'c':
                print()
                if run_custom() == None:
                    break
            else:
                print(f'Please input number in 1..{max_number} to choose file')
        print()
    
    # end of main



if __name__ == '__main__':
    main()
    print('\n'*5)














''' SOME OLD CODE PIECES:

for x in range(canvas_w):
    for y in range(canvas_h):
        if (x+tx)**2 + (y+ty)**2 < radius2:
            pixels[y, x] = (r, g, b, a)



for x in range(canvas_w):
    for y in range(canvas_h):
        if tx_min <= x-canvas_w/2 <= tx_max and ty_min <= y-canvas_h/2 <= ty_max:
            pixels[y, x] = (r, g, b, a)












'''

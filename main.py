'''
SIVF-renderer   v0.3

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
from value_converting_funcs import *





tab = '    '   # for fancy logs
tabs = 0



class ColorBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2

class AlphaBlendingType (Enum):
    default = 0   # default is overlap
    overlap = 0
    add = 1
    avg = 2





def render_shape (pixels: 'nparray2d', color: '(a, r, g, b)', check_func: 'function', shape_n: int,
        color_blending_type: ColorBlendingType = ColorBlendingType.default,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default) -> None:
    global canvas_w, canvas_h

    a, r, g, b = color[0], color[1], color[2], color[3]

    if color_blending_type == ColorBlendingType.overlap and alpha_blending_type == AlphaBlendingType.overlap:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (r, g, b, a)
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    elif color_blending_type == ColorBlendingType.add and alpha_blending_type == AlphaBlendingType.overlap:
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

    elif color_blending_type == ColorBlendingType.add and alpha_blending_type == AlphaBlendingType.add:
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
    
    elif color_blending_type == ColorBlendingType.avg and alpha_blending_type == AlphaBlendingType.overlap:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        (pixels[y, x][0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x][1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x][2]*shape_n+b)//(shape_n+1),
                        a
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    elif color_blending_type == ColorBlendingType.avg and alpha_blending_type == AlphaBlendingType.avg:
        for x in range(canvas_w):
            for y in range(canvas_h):
                if check_func(x, y):
                    pixels[y, x] = (
                        (pixels[y, x][0]*shape_n+r)//(shape_n+1),
                        (pixels[y, x][1]*shape_n+g)//(shape_n+1),
                        (pixels[y, x][2]*shape_n+b)//(shape_n+1),
                        (pixels[y, x][3]*shape_n+a)//(shape_n+1)
                    )
                #print(pixels[y, x], end=' ')
            #print('\n\n\n')

    else:
        raise Exception(f'This blending type is unsupported for now: {color_blending_type = }, {alpha_blending_type = }')

    # end of render_object 



def parse_shape (pixels: 'nparray2d', shape: dict, shape_name: str,
        color_blending_type: ColorBlendingType = ColorBlendingType.default,
        alpha_blending_type: AlphaBlendingType = AlphaBlendingType.default) -> None:
    print((1+tabs)*tab+f'rendering {shape_name}:')

    inverse = (shape['inverse'] == 'true') if 'inverse' in shape else False
    print((2+tabs)*tab+f'{inverse = }')

    a, r, g, b = cctargb(shape['color'][1:])
    print((2+tabs)*tab+f'{a=}, {r=}, {g=}, {b=}')

    global canvas_wh, shape_number

    if shape_name.startswith('circle'):
        circle_x = cetu(shape['xy'][0], canvas_wh)
        circle_y = -cetu(shape['xy'][1], canvas_wh)   # MINUS because pixel grid is growing down, but math coords grows to up
        radius = cetu(shape['r'], canvas_wh)

        tx = -canvas_w/2 - circle_x + 1/2
        ty = -canvas_h/2 - circle_y + 1/2
        radius2 = radius**2
        render_shape(
            pixels,
            (a, r, g, b),
            lambda x, y: ( (x+tx)**2 + (y+ty)**2 < radius2 ) ^ inverse,
            shape_number,
            color_blending_type,
            alpha_blending_type,
        )
    
    elif shape_name.startswith('square'):
        square_x = cetu(shape['xy'][0], canvas_wh)
        square_y = -cetu(shape['xy'][1], canvas_wh)   # MINUS because pixel grid is growing down, but math coords grows to up
        side = cetu(shape['side'], canvas_wh)

        tx_min = square_x - side/2;   tx_max = square_x + side/2
        ty_min = square_y - side/2;   ty_max = square_y + side/2
        render_shape(
            pixels,
            (a, r, g, b),
            lambda x, y: ( tx_min <= x-canvas_w/2 <= tx_max and ty_min <= y-canvas_h/2 <= ty_max ) ^ inverse,
            shape_number,
            color_blending_type,
            alpha_blending_type,
        )

    # end of parse_shape()



def parse_entity (pixels: 'nparray2d', entity: dict, entity_name: str = '') -> None:
    global tab, tabs
    for subentity_name in entity:
        print((tabs)*tab+f'parsing {subentity_name}')
        subentity = entity[subentity_name]

        color_blending_type = ColorBlendingType.default
        alpha_blending_type = AlphaBlendingType.default

        if (entity_name == '' or entity_name.startswith('l')) and 'blending' in entity:
            color_blending_type = entity['blending'][0]
            alpha_blending_type = entity['blending'][1]

            if color_blending_type == 'default':
                color_blending_type = ColorBlendingType.default
            elif color_blending_type == 'overlap':
                color_blending_type = ColorBlendingType.overlap
            elif color_blending_type == 'add':
                color_blending_type = ColorBlendingType.add
            elif color_blending_type == 'avg':
                color_blending_type = ColorBlendingType.avg
            else:
                raise Exception(f'Unsupported ColorBlendingType: {color_blending_type = }')

            if alpha_blending_type == 'default':
                alpha_blending_type = AlphaBlendingType.default
            elif alpha_blending_type == 'overlap':
                alpha_blending_type = AlphaBlendingType.overlap
            elif alpha_blending_type == 'add':
                alpha_blending_type = AlphaBlendingType.add
            elif alpha_blending_type == 'avg':
                alpha_blending_type = AlphaBlendingType.avg
            else:
                raise Exception(f'Unsupported AlphaBlendingType: {alpha_blending_type = }')

        if subentity_name.startswith('b'):   # blending
            pass

        elif subentity_name.startswith('l'):   # layer
            tabs += 1
            parse_entity(
                pixels,
                subentity,
                subentity_name
            )
            tabs -=1

        #elif ...: object or other special entities

        else:   # shape
            parse_shape(
                pixels,
                subentity,
                subentity_name,
                color_blending_type,
                alpha_blending_type
            )

        print()

    # end of parse_entity()




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

    global canvas_wh, canvas_w, canvas_h, shape_number
    canvas_wh = image_sizes
    canvas_w, canvas_h = canvas_wh

    #render_from_image_code(color_scheme, image_dict)

    pixels = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)   # create np array

    # unneccesary, because np.zeros already do this :)
    #pixels[:, :] = (0, 0, 0, 0)   # set default value as tranparent

    shape_number = 0

    utils.timer_begin()
    parse_entity(pixels, image_dict)
    utils.timer_end()

    #print(pixels)
    result_image = Image.fromarray(pixels, 'RGBA')
    result_image.save('image.png')
    result_image.show()




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



def main ():
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
    


def render_from_image_code (color_scheme: str, image_code: dict) -> None:
    global canvas_w, canvas_h
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

            process_shape(pixels, obj_name, obj, obj_number)
        print()

    print()

    utils.timer_end()

    #print(pixels)

    result_image = Image.fromarray(pixels, 'RGBA')
    result_image.save('image.png')
    result_image.show()




















'''

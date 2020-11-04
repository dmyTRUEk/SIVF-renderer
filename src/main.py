'''
SIVF-renderer   v0.4.0a1

This is main file of SIVF-renderer
''' 



import sys
# import random

from os import listdir
from os.path import isfile, join
import re
import json

import numpy as np
from PIL import Image



import utils

from class_layer import Layer

from class_alpha_blending import AlphaBlendingType
from class_color_blending import ColorBlendingType

from funcs_convert import *

from funcs_heavy_py import *
# from funcs_heavy_cy import *





tab = '    '   # for fancy logs
tabs = 0





def tmp_show_image (layer: Layer):
    Image.fromarray(layer.get_pixels(), 'RGBA').show()



def parse_and_render_entity (entity: dict, entity_name: str,
        canvas_wh: '(canvas_w, canvas_h)', delta_xy: '(delta_x, delta_y)' = (0, 0)) -> Layer:
    global tab, tabs, var, shape_number

    layer_rendering = Layer(canvas_wh)

    #for      key      in  dict :
    for subentity_name in entity:
        print((tabs)*tab+f'parsing {subentity_name}:')
        subentity = entity[subentity_name]

        # [TODO]: move this out of for loop?
        alpha_blending_type = AlphaBlendingType.default
        color_blending_type = ColorBlendingType.default

        if (entity_name == 'image' or entity_name.startswith('layer')) and ('blending' in entity):
            # print('setting blending types')
            # print(f'{entity["blending"] = }')
            alpha_blending_type = AlphaBlendingType.from_str(entity['blending'][0])
            color_blending_type = ColorBlendingType.from_str(entity['blending'][1])

        # print(f'{alpha_blending_type = }')
        # print(f'{color_blending_type = }')
        # print()


        if subentity_name.startswith('blending'):   # blending
            pass

        elif subentity_name.startswith('layer'):   # layer
            # raise NotImplementedError()
            tabs += 1
            layer_tmp = parse_and_render_entity(subentity, subentity_name, canvas_wh, delta_xy)
            tabs -= 1
            layer_rendering = blend_layers(layer_rendering, layer_tmp, shape_number, alpha_blending_type, color_blending_type)

        elif subentity_name.startswith('mesh'):   # mesh
            raise NotImplementedError()
            repeated_layer = subentity['layer']
            n_xleft_ydown_xright_yup = subentity['n_xleft_ydown_xright_yup']
            nxyxy = n_xleft_ydown_xright_yup   # for shorteness
            nxyxy = (
                int(cetu(nxyxy[0], canvas_wh, var)),
                int(cetu(nxyxy[1], canvas_wh, var)),
                int(cetu(nxyxy[2], canvas_wh, var)),
                int(cetu(nxyxy[3], canvas_wh, var))
            )
            delta_xy_str = subentity['delta_xy']

            delta_x = cetu(delta_xy_str[0], canvas_wh, var)
            delta_y = cetu(delta_xy_str[1], canvas_wh, var)

            tabs += 1
            for h in range(-nxyxy[1], nxyxy[3]+1):
                for w in range(-nxyxy[0], nxyxy[2]+1):
                    print((tabs)*tab+f'parsing mesh[{w}][{h}]:')
                    tabs += 1
                    parse_and_render_entity(
                        repeated_layer,
                        'layer',
                        canvas_wh,
                        (w*delta_x, h*delta_y)
                    )
                    tabs -= 1
            tabs -= 1

        #elif ...:   # other special entities

        else:   # shape
            layer_tmp = parse_and_render_shape(
                subentity, subentity_name, shape_number,
                canvas_wh, tab, tabs, var,
                alpha_blending_type, color_blending_type,
                delta_xy
            )
            # print(f'{layer_tmp.get_pixels() = }')
            layer_rendering = blend_layers(layer_rendering, layer_tmp, shape_number, alpha_blending_type, color_blending_type)

        print()

    # print(f'{layer_rendering.get_pixels() = }')
    # tmp_show_image(layer_rendering)

    return layer_rendering

    # end of parse_entity()



def render_from_content (content: dict) -> None:
    # delete all comments   /* blahblahblah */
    content = re.sub(re.compile('/\*.*?\*/', re.DOTALL), '', content)

    # delete all comment   // blahblahblah
    content = re.sub(re.compile('//.*?\n'), '', content)

    #print(content)
    content_dict = json.loads(content)
    #print_all_about(content_dict)

    # global canvas_wh, canvas_w, canvas_h, shape_number, var
    global canvas_wh, shape_number, var

    canvas_wh = ( int(content_dict['sizes_wh'][0]), int(content_dict['sizes_wh'][1]) )
    # canvas_w, canvas_h = canvas_wh
    # canvas_wh = ( int(sizes_wh[0]), int(sizes_wh[1]) )

    color_scheme = content_dict['color_scheme']
    image_dict = content_dict['image']

    #print(f'{image_dict = }\n')

    # [TODO]: wtf is this?
    # delete all what is not layer
    keys_to_delete = []
    for key in image_dict:
        if not key.startswith('layer'):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del image_dict[key]

    #print(f'{image_dict = }\n')

    var = content_dict['vars'] if 'vars' in content_dict else {}

    # pixels = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)   # create np array
    # layer_main = Layer(canvas_wh)

    shape_number = 0

    utils.timer_begin()
    layer_rendered = parse_and_render_entity(image_dict, '', canvas_wh)
    utils.timer_end()
    utils.timer_show()

    if layer_rendered.wh != canvas_wh:
        raise ValueError()

    # layer_main = blend_layers(
    #     layer_main, layer_rendered,
    #     shape_number,
    #     AlphaBlendingType.default,
    #     ColorBlendingType.default
    # )
    # layer_main = layer_rendered

    save_pixels_to_image(layer_rendered.get_pixels_rgba(), 'image.png', show=True)

    # end of render_from_content



def save_pixels_to_image (pixels: 'ndarray2d', output_file_name: str, show: bool=False):
    #print(pixels)
    result_image = Image.fromarray(pixels, 'RGBA')
    result_image.save(output_file_name)
    if show:
        result_image.show()



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
    


render_from_image_code(color_scheme, image_dict)

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

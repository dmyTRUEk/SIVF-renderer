'''
This file needed for cython compiling

compline on linux:   $ python setup.py build_ext --inplace
'''

import os
import sys
from setuptools import setup

from Cython.Build import cythonize
from Cython.Compiler import Options

import numpy





Options.annotate = True



print(f'Compiling Cython with language_level = {sys.version_info[0]}\n')

additional_path_to_pyx = ''
if os.path.basename(os.getcwd()) != 'src':
    additional_path_to_pyx = 'src/'

setup(
    ext_modules = cythonize(
        additional_path_to_pyx+'funcs_heavy_cython.pyx',
        compiler_directives={'language_level' : sys.version_info[0]}
    ),
    include_dirs = [numpy.get_include()]
) 



if os.path.basename(os.getcwd()) != 'src':
    # delete old builded files
    os.system('rm src/heavy_funcs_cy.cpython-39-x86_64-linux-gnu.so')
    os.system('rm -rf src/build')

    # move new bulid files to /src
    os.system('mv funcs_heavy_cython.cpython-39-x86_64-linux-gnu.so src/funcs_heavy_cython.cpython-39-x86_64-linux-gnu.so')
    os.system('mv build/ src/')

print('\n\n')



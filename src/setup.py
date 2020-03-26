'''
This file needed for cython compiling?

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
        additional_path_to_pyx+'heavy_funcs_cy.pyx',
        compiler_directives={'language_level' : sys.version_info[0]}
    ),
    include_dirs = [numpy.get_include()]
) 




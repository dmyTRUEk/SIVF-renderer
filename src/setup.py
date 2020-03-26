'''
This file needed for cython compiling?

compline on linux:   $ python setup.py build_ext --inplace
'''



import sys
from setuptools import setup

from Cython.Build import cythonize
from Cython.Compiler import Options

import numpy




Options.annotate = True



print(f'Compiling Cython with language_level = {sys.version_info[0]}\n')

setup(
    ext_modules = cythonize(
        'heavy_funcs_cy.pyx',
        compiler_directives={'language_level' : sys.version_info[0]}
    ),
    include_dirs = [numpy.get_include()]
) 




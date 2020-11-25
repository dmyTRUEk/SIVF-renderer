'''
This file contains Configurations
''' 



# FOR ERRORS, WARNINGS, LOGS:
TAG = '[{0}]: '

# ERRORS:
TAG_ERROR = 'ERROR'
DIVIDER_ERROR = ' -> '

# WARNINGS:
TAG_WARNING = 'WARNING'
IS_SHOWING_WARNINGS = False
IS_SHOWING_WARNING_TRACEBACK = False
DIVIDER_WARNINGS = ' -> '

# LOGS:
TAG_LOG = 'LOG'
IS_SHOWING_LOG = True



# RENDERING BACKEND:
CONFIG_RENDER_BACKEND_ANY = 'config_render_backend_any'
CONFIG_RENDER_BACKEND_PYTHON = 'config_render_backend_python'
CONFIG_RENDER_BACKEND_CYTHON = 'config_render_backend_cython'
CONFIG_RENDER_BACKEND_NUMBA  = 'config_render_backend_numba'
CONFIG_RENDER_BACKEND_NUMPY  = 'config_render_backend_nympy'
CONFIG_RENDER_BACKEND_RUST   = 'config_render_backend_rust'
CONFIG_RENDER_BACKEND_GPU    = 'config_render_backend_gpu'

CONFIG_RENDER_BACKEND = CONFIG_RENDER_BACKEND_CYTHON



# SIVF BACKEND:
CONFIG_SIVF_BACKEND_ANY = 'config_sivf_backend_any'
CONFIG_SIVF_BACKEND_JSON = 'config_sivf_backend_json'
CONFIG_SIVF_BACKEND_YAML = 'config_sivf_backend_yaml'

CONFIG_SIVF_BACKEND = CONFIG_SIVF_BACKEND_JSON



# RENDER PROGRESS:
TAB = 2 * ' '                            # for fancy logs
OUTPUT_RENDER_PROGRESS = True
OUTPUT_RENDER_PROGRESS_PERIOD = 100



# PIL SETTINGS:
PIL_IMAGE_OUTPUT_MODE = 'RGBA'



# SIVF DEFAULTS:
# KW_INVERSE_DEFAULT = False
# KW_GRADIENT_FADING_DEFAULT = True
# KW_USED_DEFAULT = True




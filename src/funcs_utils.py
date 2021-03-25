'''
My usefull utils
'''

import random
import time
import traceback


from funcs_errors import *
from funcs_warnings import *
from funcs_log import *





def print_traceback ():
    t = traceback.format_stack(limit=None)
    t = ''.join(t[:-2])
    t = '\n  '.join(t.split('\n'))
    print(t)



def print_all_about (var, var_name):
    print(f'Printing all about var:')
    #print(f'Printing all about \'{get_var_name(var)}\'')
    print(f'    type({var_name}) = {type(var)}')
    print(f'    content = {var}')
    print()

def get_var_name (var):
    raise WarningDeprecated('This is DEPRECATED, because it cant work in python')
    return [k for k, v in locals().items() if v == var][0]



def avg (some_list):
    return sum(some_list) / len(some_list)



def rand_m1_p1 ():
    return random.choice((-1, +1))



def min_dist2 (np_point, np_points):
    #np_points = np.asarray(np_points)
    deltas = np_points - np_point
    dist2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist2)



def timer_begin ():
    global timer_begin_0
    timer_begin_0 = time.time()

def timer_end ():
    global timer_end_0
    timer_end_0 = time.time()

def timer_show ():
    global timer_begin_0, timer_end_0
    Log(f'Time elapsed from BEGIN..END = {timer_end_0-timer_begin_0} seconds')



def remove_suffix (text: str, suffix: str) -> str:
    if text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text

def remove_prefix (text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text




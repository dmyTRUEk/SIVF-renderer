'''
Here my usefull utils
'''



import time
import random





def print_all_about (var):
    print(f'Printing all about var:')
    #print(f'Printing all about \'{get_var_name(var)}\'')
    print(f'  {type(var) = }')
    print('  content =', var)
    print()



def get_var_name (var):
    return [k for k, v in locals().iteritems() if v == my_var][0]



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
    print(f'Time elapsed from BEGIN..END = {timer_end_0-timer_begin_0}')
    #sys.exit(0)




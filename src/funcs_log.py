'''
This file contain LOGGING funcs
''' 


from config import TAG, TAG_LOG, IS_SHOWING_LOG





class Log:
    BEGIN_OF_LOG = TAG.format(TAG_LOG)
    def __init__ (self, *args, **kwargs):
        if IS_SHOWING_LOG:
            print(self.BEGIN_OF_LOG, end='')
            print(*args, **kwargs)




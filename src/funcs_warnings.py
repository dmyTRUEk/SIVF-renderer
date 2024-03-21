'''
This file conains all my ERRORS
''' 

import traceback


from config import TAG, TAG_WARNING, IS_SHOWING_WARNINGS, IS_SHOWING_WARNING_TRACEBACK, DIVIDER_WARNINGS





class Warning:
    BEGIN_OF_WARNING = TAG.format(TAG_WARNING)
    def __init__ (self, message=''):
        if IS_SHOWING_WARNINGS:
            if IS_SHOWING_WARNING_TRACEBACK:
                t = traceback.format_stack(limit=None)
                t = ''.join(t[:-2])
                t = '\n  '.join(t.split('\n'))
            print(
                self.BEGIN_OF_WARNING +
                ( (t) if (IS_SHOWING_WARNING_TRACEBACK) else ('') ) +
                ( message ) + 
                ( ('\n') if (IS_SHOWING_WARNING_TRACEBACK) else ('') )
            )



class WarningDeprecated (Warning):
    MESSAGE_DEFAULT = 'This is DEPRECATED'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_WARNINGS+message_additional) if (message_additional!='') else ('') )
        )



class WarningTodo (Warning):
    MESSAGE_DEFAULT = 'TODO'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_WARNINGS+message_additional) if (message_additional!='') else ('') )
        )




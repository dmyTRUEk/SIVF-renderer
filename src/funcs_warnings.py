'''
This file conains all my ERRORS
''' 

import traceback


from config import IS_SHOWING_WARNINGS, IS_SHOWING_WARNING_TRACEBACK, DIVIDER_WARNINGS





class Warning:
    MESSAGE_DEFAULT = 'WARNING'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        if IS_SHOWING_WARNINGS:
            if IS_SHOWING_WARNING_TRACEBACK:
                t = traceback.format_stack(limit=None)
                t = ''.join(t[:-2])
                t = '\n  '.join(t.split('\n'))
            print(
                ( (t) if (IS_SHOWING_TRACEBACK) else ('') ) +
                ( message_main ) + 
                ( (DIVIDER_WARNINGS+message_additional) if (message_additional!='') else ('') ) +
                ( ('\n') if (IS_SHOWING_TRACEBACK) else ('') )
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




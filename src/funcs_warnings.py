'''
This file conains all my ERRORS
''' 



DIVIDER = ' -> '

IS_SHOWING_WARNINGS = True



class Warning:
    MESSAGE_DEFAULT = 'WARNING'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        if IS_SHOWING_WARNINGS:
            print(
                ( message_main ) + 
                ( (DIVIDER+message_additional) if (message_additional!='') else '' )
            )



class WarningDeprecated (Warning):
    MESSAGE_DEFAULT = 'This is DEPRECATED'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER+message_additional) if (message_additional!='') else '' )
        )



class WarningTodo (Warning):
    MESSAGE_DEFAULT = 'This is TODO, so it is unfinished and must be done'
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER+message_additional) if (message_additional!='') else '' )
        )




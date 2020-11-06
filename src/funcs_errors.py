'''
This file conains all my ERRORS
''' 



DIVIDER = ' -> '



class ErrorUnknownValue (Exception):
    MESSAGE_DEFAULT = 'Value is UNKNOWN'
    def __init__ (self, value=None, message_additional='', message_main=MESSAGE_DEFAULT):
        print(f'{value = }')
        super().__init__(
            ( message_main ) +
            ( (DIVIDER+message_additional) if (message_additional!='') else ('') ) +
            ( (DIVIDER+str(value)) if (value!=None) else ('') )
        )



class ErrorDeprecated (Exception):
    MESSAGE_DEFAULT = 'This is DEPREATED' 
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER+message_additional) if (message_additional!='') else ('') )
        )



class ErrorNotImpemented (Exception):
    MESSAGE_DEFAULT ='This is NOT IMPLEMENTED yet' 
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER+message_additional) if (message_additional!='') else ('') )
        )



class ErrorNotEqualTypes (Exception):
    MESSAGE_DEFAULT = 'Vars \'{2}\' and \'{3}\' must have equal types, but:\n  type({2}) = {4}\n  type({3}) = {5}'
    def __init__ (self, var1, var2, var1_name, var2_name, message_main=MESSAGE_DEFAULT):
        super().__init__(message_main.format(var1, var2, var1_name, var2_name, type(var1), type(var2)))



class ErrorNotEqual (Exception):
    MESSAGE_DEFAULT = 'Vars \'{2}\' and \'{3}\' must be equal, but:\n  {2} = {0}\n  {3} = {1}'
    def __init__ (self, var1, var2, var1_name, var2_name, message_main=MESSAGE_DEFAULT):
        super().__init__(message_main.format(var1, var2, var1_name, var2_name))




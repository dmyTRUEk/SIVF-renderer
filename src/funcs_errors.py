'''
This file conains all my ERRORS
''' 

from config import DIVIDER_ERROR





class ErrorValueUnknown (Exception):
    MESSAGE_DEFAULT = 'Value is UNKNOWN'
    def __init__ (self, value=None, message_additional='', message_main=MESSAGE_DEFAULT):
        print(f'{value = }')
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_ERROR+message_additional) if (message_additional!='') else ('') ) +
            ( (DIVIDER_ERROR+str(value)) if (value!=None) else ('') )
        )



class ErrorValueWrong (Exception):
    MESSAGE_DEFAULT = 'Value is WRONG'
    def __init__ (self, value=None, message_additional='', message_main=MESSAGE_DEFAULT):
        print(f'{value = }')
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_ERROR+message_additional) if (message_additional!='') else ('') ) +
            ( (DIVIDER_ERROR+str(value)) if (value!=None) else ('') )
        )



class ErrorDeprecated (Exception):
    MESSAGE_DEFAULT = 'This is DEPREATED' 
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_ERROR+message_additional) if (message_additional!='') else ('') )
        )



class ErrorNotImpemented (Exception):
    MESSAGE_DEFAULT ='This is NOT IMPLEMENTED yet' 
    def __init__ (self, message_additional='', message_main=MESSAGE_DEFAULT):
        super().__init__(
            ( message_main ) +
            ( (DIVIDER_ERROR+message_additional) if (message_additional!='') else ('') )
        )



class ErrorWrongType (Exception):
    MESSAGE_DEFAULT = 'Var \'{1}\' must be of type {2}, but:\n  type({1}) = {3}'
    def __init__ (self, var, var_name, var_type_expected, message_main=MESSAGE_DEFAULT):
        super().__init__( message_main.format(var, var_name, type_expected, type(var)) )



class ErrorValuesNotEqualTypes (Exception):
    MESSAGE_DEFAULT = 'Vars \'{2}\' and \'{3}\' must have equal types, but:\n  type({2}) = {4}\n  type({3}) = {5}'
    def __init__ (self, var1, var2, var1_name, var2_name, message_main=MESSAGE_DEFAULT):
        super().__init__( message_main.format(var1, var2, var1_name, var2_name, type(var1), type(var2)) )



class ErrorValuesNotEqual (Exception):
    MESSAGE_DEFAULT = 'Vars \'{2}\' and \'{3}\' must be equal, but:\n  {2} = {0}\n  {3} = {1}'
    def __init__ (self, var1, var2, var1_name, var2_name, message_main=MESSAGE_DEFAULT):
        super().__init__( message_main.format(var1, var2, var1_name, var2_name) )




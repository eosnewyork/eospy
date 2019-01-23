
class InvalidKeyFile(Exception):
    ''' Raised when the key file format is invalid '''
    pass

class InvalidPermissionFormat(Exception):
    ''' Raised when the permission format is invalid'''
    pass

class EOSKeyError(Exception):
    ''' Raised when there is an EOSKey error '''
    pass
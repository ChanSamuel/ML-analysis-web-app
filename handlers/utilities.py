class UnsupportedMethodException(Exception):
    def __init__(self, message):
        if ~(isinstance(message, str)):
            raise ValueError('Parameter \'message\' is not a string!')
        super().__init__(message)

class FileLoadingException(Exception):
    def __init__(self, message):
        if ~(isinstance(message, str)):
            raise ValueError('Parameter \'message\' is not a string!')
        super().__init__(message)

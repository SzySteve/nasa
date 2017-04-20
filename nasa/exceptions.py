class NASAValidationError(Exception):
    """Raised when request parameters are invalid"""
    pass


class NASAResponseError(Exception):
    """Raised when NASA returns anything but a 200"""
    pass

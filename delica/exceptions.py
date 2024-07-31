class DelicaException(Exception):
    """Base Exception For API"""


class MissingRequiredException(DelicaException):
    """Exception Raised When You're Missing Something That Is Required"""

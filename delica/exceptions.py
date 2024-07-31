from typing import Any


class DelicaException(Exception):
    """Base Exception For API"""


class MissingRequiredException(DelicaException):
    """Exception Raised When You're Missing Something That Is Required"""


class RequestException(DelicaException):
    def __init__(self, og_exception: Exception, request_args: tuple[Any, ...], request_kwargs: Any):
        self.og_exception = og_exception
        self.request_args = request_args
        self.request_kwargs = request_kwargs

        super().__init__(f"Error Making Request: {og_exception}")


class VanApiException(DelicaException):
    """Error Messages from VAN API"""

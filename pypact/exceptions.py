"""
PyPact exception classes
"""


class PyPactException(Exception):
    """
    Base PyPact exception.
    """
    pass


class PyPactServiceException(PyPactException):
    """
    Raised by MockService.
    """
    pass


class PyPactNullConsumerException(PyPactException):
    """
    Raised by the Builder if there is a null consumer.
    """
    pass


class PyPactNullProviderException(PyPactException):
    """
    Raised by the Builder if there is a null provider.
    """
    pass

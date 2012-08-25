"""Exceptions are defined in billdotcom for ease of use."""


class BilldotcomError(Exception):
    """The base class for billdotcom exceptions."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ConfigurationError(BilldotcomError):
    """An exception raised when the configuration is incorrect."""


class HTTPError(BilldotcomError):
    """An exception raised when an HTTP request returns with a bad code."""


class ServerResponseError(BilldotcomError):
    """An exception raised when the server reponds that a request failed."""


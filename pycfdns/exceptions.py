"""pycfdns exceptions."""


class CloudflareException(Exception):
    """Base exception class for pycfdns."""


class CloudflareConnectionException(CloudflareException):
    """Error to indicate we cant connect to API."""


class CloudflareAuthenticationException(CloudflareException):
    """Error to indicate we cant authenticate against API."""

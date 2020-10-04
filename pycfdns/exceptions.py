"""pycfdns exceptions."""


class CloudflareException(Exception):
    """Base exception class for pycfdns."""


class CloudflareAuthenticationException(CloudflareException):
    """Error to indicate we cant authenticate against API."""


class CloudflareConnectionException(CloudflareException):
    """Error to indicate we cant connect to API."""


class CloudflareZoneException(CloudflareException):
    """Error to indicate we couldnt find zone via API."""


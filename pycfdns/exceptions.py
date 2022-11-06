"""pycfdns exceptions."""


class CloudflareException(Exception):
    """Base exception class for pycfdns."""


class CloudflareAuthenticationException(CloudflareException):
    """Error to indicate we cannot authenticate against API."""


class CloudflareConnectionException(CloudflareException):
    """Error to indicate we cannot connect to API."""


class CloudflareZoneException(CloudflareException):
    """Error to indicate we cannot find zone via API."""

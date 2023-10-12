"""pycfdns exceptions."""


class AuthenticationException(Exception):
    """Error to indicate we cannot authenticate against API."""


class ComunicationException(Exception):
    """Error to indicate we cannot connect to API."""

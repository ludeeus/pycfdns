"""pycfdns models."""
# pylint: disable=missing-docstring
import asyncio
import logging
import socket
from typing import TypedDict
import aiohttp
import async_timeout

from pycfdns.const import NAME
from pycfdns.exceptions import (
    CloudflareAuthenticationException,
    CloudflareConnectionException,
    CloudflareException,
)

_LOGGER = logging.getLogger(NAME)


class CFAPI:
    """Class used to call the API."""

    def __init__(self, session, auth, timeout):
        """Initialize."""
        self.session = session
        self.auth = auth
        self.timeout = timeout

    async def get_json(self, url):
        """Return JSON response from the API."""
        data = None
        try:
            async with async_timeout.timeout(self.timeout):
                response = await self.session.get(url, headers=self.auth.header)
        except asyncio.TimeoutError as error:
            raise CloudflareConnectionException(
                f"Timeout error fetching information from {url}, {error}"
            ) from error
        except (KeyError, TypeError) as error:
            raise CloudflareException(
                f"Error parsing information from {url}, {error}"
            ) from error
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise CloudflareConnectionException(
                f"Error fetching information from {url}, {error}"
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise CloudflareException(
                f"Something really wrong happend! - {error}"
            ) from error
        else:
            if response.status == 403:
                raise CloudflareAuthenticationException(
                    "Access forbidden. Please ensure valid API Key is provided"
                )

            data = await response.json()
            _LOGGER.debug(data)

            if not data.get("success"):
                for error in data.get("errors"):
                    raise CloudflareException(
                        f"[{error.get('code')}] {error.get('message')}"
                    )

        return data

    async def put_json(self, url, json_data):
        """PUT JSON on the API."""
        data = None
        try:
            async with async_timeout.timeout(self.timeout):
                response = await self.session.put(
                    url, headers=self.auth.header, data=json_data
                )
        except asyncio.TimeoutError as error:
            raise CloudflareConnectionException(
                f"Timeout error fetching information from {url}, {error}"
            ) from error
        except (KeyError, TypeError) as error:
            raise CloudflareException(
                f"Error parsing information from {url}, {error}"
            ) from error
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise CloudflareConnectionException(
                f"Error fetching information from {url}, {error}"
            ) from error
        except Exception as error:  # pylint: disable=broad-except
            raise CloudflareException(
                f"Something really wrong happend! - {error}"
            ) from error
        else:
            if response.status == 403:
                raise CloudflareAuthenticationException(
                    "Access forbidden. Please ensure valid API Key is provided"
                )

            data = await response.json()
            _LOGGER.debug(data)

        return data


class CFAuth:
    """CF Auth."""

    def __init__(self, token):
        """Initialize."""
        self.token = token

    @property
    def header(self):
        """Return auth headers."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }


class CFRecord:
    """CFRecord."""

    def __init__(self, record):
        """Initialize."""
        self.record = record

    @property
    def record_id(self):
        return self.record.get("id")

    @property
    def record_type(self):
        return self.record.get("type")

    @property
    def record_name(self):
        return self.record.get("name")

    @property
    def record_proxied(self):
        return self.record.get("proxied")

    @property
    def record_content(self):
        return self.record.get("content")


class DNSRecord(TypedDict):
    """Dictionary representation of a DNS record"""

    content: str
    id: str
    name: str
    proxied: bool
    type: str

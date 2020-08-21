"""pycfdns models."""
# pylint: disable=missing-docstring
import asyncio
import logging
import socket
import aiohttp
import async_timeout

from pycfdns.const import GET_EXT_IP_URL, NAME
from pycfdns.exceptions import CloudflareException

_LOGGER = logging.getLogger(NAME)


class CFAPI:
    """Class used to call the API."""

    def __init__(self, session, auth):
        """Initialize."""
        self.session = session
        self.auth = auth

    async def get_json(self, url):
        """Return JSON response from the API."""
        data = None
        try:
            async with async_timeout.timeout(5, loop=asyncio.get_event_loop()):
                response = await self.session.get(url, headers=self.auth.header)
                data = await response.json()
            _LOGGER.debug(data)

            if not data.get("success"):
                for error in data.get("errors"):
                    raise CloudflareException(
                        f"[{error.get('code')}] {error.get('message')}"
                    )

        except asyncio.TimeoutError as error:
            raise CloudflareException(
                f"Timeouterror fetching information from {url}, {error}"
            )
        except (KeyError, TypeError) as error:
            raise CloudflareException(f"Error parsing information from {url}, {error}")
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise CloudflareException(f"Error fetching information from {url}, {error}")
        except Exception as error:  # pylint: disable=broad-except
            raise CloudflareException(f"Something really wrong happend! - {error}")
        return data

    async def get_external_ip(self):
        """Return the external IP."""
        data = None
        try:
            async with async_timeout.timeout(5, loop=asyncio.get_event_loop()):
                response = await self.session.get(GET_EXT_IP_URL)
                data = await response.text()
            _LOGGER.debug(data)

        except asyncio.TimeoutError as error:
            raise CloudflareException(
                f"Timeouterror fetching information from {GET_EXT_IP_URL}, {error}"
            )
        except (KeyError, TypeError) as error:
            raise CloudflareException(
                f"Error parsing information from {GET_EXT_IP_URL}, {error}"
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise CloudflareException(
                f"Error fetching information from {GET_EXT_IP_URL}, {error}"
            )
        except Exception as error:  # pylint: disable=broad-except
            raise CloudflareException(f"Something really wrong happend! - {error}")
        return data

    async def put_json(self, url, json_data):
        """PUT JSON on the API."""
        data = None
        try:
            async with async_timeout.timeout(5, loop=asyncio.get_event_loop()):
                response = await self.session.put(
                    url, headers=self.auth.header, data=json_data
                )
                data = await response.json()
            _LOGGER.debug(data)

        except asyncio.TimeoutError as error:
            raise CloudflareException(
                f"Timeouterror fetching information from {url}, {error}"
            )
        except (KeyError, TypeError) as error:
            raise CloudflareException(f"Error parsing information from {url}, {error}")
        except (aiohttp.ClientError, socket.gaierror) as error:
            raise CloudflareException(f"Error fetching information from {url}, {error}")
        except Exception as error:  # pylint: disable=broad-except
            raise CloudflareException(f"Something really wrong happend! - {error}")
        return data


class CFAuth:
    """CF Auth."""

    def __init__(self, email, token, api_token=None):
        """Initialize."""
        self.email = email
        self.token = token
        self.api_token = api_token

    @property
    def header(self):
        """Return auth headers."""
        if not self.api_token:
            return {
                "X-Auth-Email": self.email,
                "X-Auth-Key": self.token,
                "Content-Type": "application/json",
            }
        else:
            return {"Authorization": " Bearer " + self.api_token}


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
        return str(self.record.get("proxied"))

    @property
    def record_content(self):
        return self.record.get("content")

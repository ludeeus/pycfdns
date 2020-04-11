"""pycfdns models."""
# pylint: disable=missing-docstring
import asyncio
import logging
import socket
import aiohttp
import async_timeout

from pycfdns.const import GET_EXT_IP_URL, NAME

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
                    _LOGGER.error("[%s] %s", error.get("code"), error.get("message"))

        except asyncio.TimeoutError as error:
            _LOGGER.error("Timeouterror fetching information from %s, %s", url, error)
        except (KeyError, TypeError) as error:
            _LOGGER.error("Error parsing information from %s, %s", url, error)
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error("Error fetching information from %s, %s", url, error)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)
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
            _LOGGER.error(
                "Timeouterror fetching information from %s, %s", GET_EXT_IP_URL, error
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing information from %s, %s", GET_EXT_IP_URL, error
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching information from %s, %s", GET_EXT_IP_URL, error
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)
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

        except asyncio.TimeoutError as error:
            _LOGGER.error("Timeouterror putting information to %s, %s", url, error)
        except (KeyError, TypeError) as error:
            _LOGGER.error("Error putting information to %s, %s", url, error)
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error("Error putting information to %s, %s", url, error)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("Something really wrong happend! - %s", error)
        return data


class CFAuth:
    """CF Auth."""

    def __init__(self, email, token):
        """Initialize."""
        self.email = email
        self.token = token

    @property
    def header(self):
        """Return auth headers."""
        return {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.token,
            "Content-Type": "application/json",
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
        return str(self.record.get("proxied"))

    @property
    def record_content(self):
        return self.record.get("content")

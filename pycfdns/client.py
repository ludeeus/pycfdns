"""Clouflare DNS API client."""
import asyncio
from socket import gaierror
from typing import Any

import async_timeout
from aiohttp import ClientError, ClientSession

from .exceptions import (
    CloudflareAuthenticationException,
    CloudflareConnectionException,
    CloudflareException,
)
from .logger import LOGGER


class CloudflareApiClient:
    """Class used to call the API."""

    def __init__(
        self,
        session: ClientSession,
        token: str,
        timeout: float,
    ) -> None:
        """Initialize."""
        self.session = session
        self.token = token
        self.timeout = timeout

    async def get(self, url: str) -> dict[str, Any]:
        """Return JSON response from the API."""
        return await self._do_request(url=url, method="GET")

    async def put(self, url: str, json_data: dict[str, Any]) -> dict[str, Any]:
        """PUT JSON on the API."""
        return await self._do_request(url=url, method="PUT", data=json_data)

    async def _do_request(
        self,
        url: str,
        *,
        method: str = "GET",
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Call the Cloudflare API."""
        try:
            async with async_timeout.timeout(self.timeout):
                response = await self.session.request(
                    method=method,
                    url=url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}",
                    },
                    data=data,
                )
        except asyncio.TimeoutError as exception:
            raise CloudflareConnectionException(
                f"Timeout error fetching information from {url}, {exception}"
            ) from exception
        except (KeyError, TypeError) as exception:
            raise CloudflareException(
                f"Error parsing information from {url}, {exception}"
            ) from exception
        except (ClientError, gaierror) as exception:
            raise CloudflareConnectionException(
                f"Error fetching information from {url}, {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise CloudflareException(
                f"Something really wrong happend! - {exception}"
            ) from exception
        else:
            if response.status == 403:
                raise CloudflareAuthenticationException(
                    "Access forbidden. Please ensure valid API Key is provided"
                )

            result: dict[str, Any] = await response.json()
            LOGGER.debug(result)

            if not result.get("success"):
                for entry in result.get("errors", []):
                    raise CloudflareException(
                        f"[{entry.get('code')}] {entry.get('message')}"
                    )

        return result

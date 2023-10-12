"""Here lives the Client."""
from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from json import dumps as json_dumps
from typing import Any as TypingAny

from aiohttp.client import (
    ClientSession as AioHttpClientSession,
    ClientTimeout as AioHttpClientTimeout,
)
from aiohttp.client_exceptions import ClientError as AioHttpClientError
from aiohttp.hdrs import CONTENT_TYPE, AUTHORIZATION

from .exceptions import AuthenticationException, ComunicationException
from .models import RecordModel, ResponseModel, ZoneModel


class Client:
    """This is the main client class."""

    def __init__(
        self,
        *,
        api_token: str,
        client_session: AioHttpClientSession,
        timeout: float | None = None,
        **kwargs: TypingAny,
    ) -> None:
        """Initialize the Client."""
        self.client_session = client_session
        self.timeout = AioHttpClientTimeout(total=timeout or 10)
        self.api_token = api_token

    async def _do_api_request(
        self,
        url: str,
        *,
        method: str = "GET",
        data: str | None = None,
        **kwargs: TypingAny,
    ) -> ResponseModel[TypingAny]:
        """Call the Cloudflare API."""
        try:
            response = await self.client_session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                headers={
                    CONTENT_TYPE: "application/json",
                    AUTHORIZATION: f"Bearer {self.api_token}",
                },
                data=data,
            )
        except AsyncioTimeoutError as exception:
            raise ComunicationException(
                f"Timeout error fetching information from {url}, {exception}"
            ) from exception
        except (AioHttpClientError, OSError) as exception:
            raise ComunicationException(
                f"Error fetching information from {url}, {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ComunicationException(
                f"Something really wrong happend! - {exception}"
            ) from exception
        else:
            if response.status == 403:
                raise AuthenticationException(
                    f"{response.reason}. Please ensure a valid API Key is provided"
                )

            result: ResponseModel[TypingAny] = await response.json()

            if not result.get("success"):
                for entry in result.get("errors", []):
                    raise ComunicationException(
                        f"[{entry.get('code')}] {entry.get('message')}"
                    )
        return result

    def _api_url(
        self,
        *,
        endpoint: str = "",
        query: dict[str, str | None] | None = None,
        **kwargs: TypingAny,
    ) -> str:
        """Return the full URL to a endpoint."""
        url = f"https://api.cloudflare.com/client/v4{endpoint}"
        if query is None:
            return url
        return (
            f"{url}?{'&'.join(f'{k}={v}' for k, v in query.items() if v is not  None)}"
        )

    async def list_zones(self, **kwargs: TypingAny) -> list[ZoneModel]:
        """
        Get the zones linked to account.

        https://developers.cloudflare.com/api/operations/zones-get
        """
        response: ResponseModel[list[ZoneModel]] = await self._do_api_request(
            url=self._api_url(endpoint="/zones", query={"per_page": "100"})
        )
        return response["result"]

    async def list_dns_records(
        self,
        zone_id: str,
        *,
        type: str | None = None,
        name: str | None = None,
        **kwargs: TypingAny,
    ) -> list[RecordModel]:
        """
        Get the records of a zone.

        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
        """
        response: ResponseModel[list[RecordModel]] = await self._do_api_request(
            url=self._api_url(
                endpoint=f"/zones/{zone_id}/dns_records",
                query={"per_page": "100", "type": type, "name": name},
            )
        )
        return response["result"]

    async def update_dns_record(
        self,
        *,
        zone_id: str,
        id: str,
        type: str,
        content: str,
        name: str,
        comment: str | None = None,
        proxied: bool | None = None,
        tags: list[str] | None = None,
        ttl: int | None = None,
        **args: dict[str, TypingAny],
    ) -> RecordModel:
        """
        Update a DNS record.

        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record
        """
        response: ResponseModel[RecordModel] = await self._do_api_request(
            url=self._api_url(endpoint=f"/zones/{zone_id}/dns_records/{id}"),
            method="PUT",
            data=json_dumps(
                {
                    k: v
                    for k, v in {
                        "type": type,
                        "name": name,
                        "content": content,
                        "proxied": proxied,
                        "comment": comment,
                        "tags": tags,
                        "ttl": ttl,
                    }.items()
                    if v is not None
                }
            ),
        )
        return response["result"]

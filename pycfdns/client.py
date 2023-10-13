"""Here lives the Client."""
from asyncio import gather as AsyncioGather, TimeoutError as AsyncioTimeoutError
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
        **_: TypingAny,
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
        **_: TypingAny,
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

        if response.status == 403:
            raise AuthenticationException(
                f"{response.reason}. Please ensure a valid API Key is provided"
            )

        result: ResponseModel[TypingAny] = await response.json()

        if not result.get("success"):
            for entry in result.get("errors", []):
                raise ComunicationException(f"[{entry.get('code')}] {entry.get('message')}")

        return result

    def _api_url(
        self,
        *,
        endpoint: str = "",
        query: dict[str, str | None] | None = None,
        **_: TypingAny,
    ) -> str:
        """Return the full URL to a endpoint."""
        url = f"https://api.cloudflare.com/client/v4{endpoint}"
        if query is None:
            return url
        return f"{url}?{'&'.join(f'{k}={v}' for k, v in query.items() if v is not  None)}"

    async def list_zones(self, **_: TypingAny) -> list[ZoneModel]:
        """
        Get the zones linked to account.

        https://developers.cloudflare.com/api/operations/zones-get
        """

        async def _list(page: int = 1) -> ResponseModel[list[ZoneModel]]:
            return await self._do_api_request(
                url=self._api_url(endpoint="/zones", query={"per_page": "100", "page": f"{page}"})
            )

        response = await _list()
        [zones, result_info] = response["result"], response["result_info"]
        if (total_pages := result_info["total_pages"]) == 1:
            return zones

        for response in await AsyncioGather(*[_list(page) for page in range(2, (total_pages + 1))]):
            zones.extend(response["result"])
        return zones

    async def list_dns_records(
        self,
        zone_id: str,
        *,
        type: str | None = None,
        name: str | None = None,
        **_: TypingAny,
    ) -> list[RecordModel]:
        """
        Get the records of a zone.

        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records
        """

        async def _list(page: int = 1) -> ResponseModel[list[RecordModel]]:
            return await self._do_api_request(
                url=self._api_url(
                    endpoint=f"/zones/{zone_id}/dns_records",
                    query={"per_page": "100", "page": f"{page}", "type": type, "name": name},
                )
            )

        response = await _list()
        [records, result_info] = response["result"], response["result_info"]
        if (total_pages := result_info["total_pages"]) == 1:
            return records

        for response in await AsyncioGather(*[_list(page) for page in range(2, (total_pages + 1))]):
            records.extend(response["result"])

        return records

    async def update_dns_record(
        self,
        *,
        zone_id: str,
        record_id: str,
        record_type: str,
        record_content: str,
        record_name: str,
        record_comment: str | None = None,
        record_proxied: bool | None = None,
        record_tags: list[str] | None = None,
        record_ttl: int | None = None,
        **_: dict[str, TypingAny],
    ) -> RecordModel:
        """
        Update a DNS record.

        https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-update-dns-record
        """
        response: ResponseModel[RecordModel] = await self._do_api_request(
            url=self._api_url(endpoint=f"/zones/{zone_id}/dns_records/{record_id}"),
            method="PUT",
            data=json_dumps(
                {
                    k: v
                    for k, v in {
                        "type": record_type,
                        "name": record_name,
                        "content": record_content,
                        "proxied": record_proxied,
                        "comment": record_comment,
                        "tags": record_tags,
                        "ttl": record_ttl,
                    }.items()
                    if v is not None
                }
            ),
        )
        return response["result"]

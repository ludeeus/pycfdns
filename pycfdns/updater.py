"""Cloudflare DNS Updater."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession

from .client import CloudflareApiClient
from .exceptions import CloudflareException, CloudflareZoneException
from .logger import LOGGER
from .models import CloudflareDNSRecord


class CloudflareUpdater:
    """This class is used to update Cloudflare DNS records."""

    def __init__(
        self,
        session: ClientSession,
        token: str,
        zone: str,
        *,
        records: list[str] | None = None,
        timeout: float = 10,
        **_: Any,
    ) -> None:
        """Initialize the CloudflareUpdater object.

        Args:
            session (ClientSession): An instance of the `aiohttp.ClientSession` class.
            token (str): The Cloudflare API token.
            zone (str): The zone name for the Cloudflare DNS records (i.e. example.com).

            records (list[str], optional): A list of record IDs to be updated.
                If not provided, all records in the zone will be updated.
            timeout (float, optional): The number of seconds to wait for
                a response from the Cloudflare API before timing out. Defaults to 10.
        """
        self.api = CloudflareApiClient(session, token, timeout)
        self.zone = zone
        self.records = records

    def _endpoint(
        self,
        *,
        path: str = "",
        query: dict[str, str | None] | None = None,
    ) -> str:
        """Return the full URL to a endpoint."""
        endpoint = f"https://api.cloudflare.com/client/v4/zones/{path}"
        if query is None:
            return endpoint
        return f"{endpoint}?{'&'.join(f'{k}={v}' for k, v in query.items() if v is not  None)}"

    async def get_zones(self) -> list[str] | None:
        """Get the zones linked to account."""
        data: list[dict[str, str]] | None = await self.api.get(self._endpoint())

        if data is None:
            return None

        return [zone["name"] for zone in data]

    async def get_zone_id(self) -> str:
        """Get the zone id for the zone."""
        try:
            data: list[dict[str, str]] = await self.api.get(
                url=self._endpoint(query={"name": self.zone})
            )
            return data[0]["id"]
        except Exception as error:
            raise CloudflareZoneException("Could not get zone ID") from error

    async def get_zone_records(
        self,
        zone_id: str,
        *,
        record_type: str | None = None,
    ) -> list[str] | None:
        """Get the records of a zone."""
        data: list[dict[str, str]] | None = await self.api.get(
            self._endpoint(
                path=f"{zone_id}/dns_records",
                query={"per_page": "100", "type": record_type},
            )
        )

        if data is None:
            return None

        return [record["name"] for record in data]

    async def get_record_info(self, zone_id: str) -> list[CloudflareDNSRecord]:
        """Get the information of the records."""
        record_information: list[CloudflareDNSRecord] = []
        if self.records is None:
            self.records = []
            data = await self.get_zone_records(zone_id)

            if data is None:
                raise CloudflareException(f"No records found for {zone_id}")

            self.records = data

        if not self.records:
            return record_information

        for record in self.records:
            if self.zone not in record:
                record = f"{record}.{self.zone}"

            recorddata: list[dict[str, Any]] = await self.api.get(
                self._endpoint(
                    path=f"{zone_id}/dns_records",
                    query={"name": record},
                )
            )

            first_record = recorddata[0]
            record_information.append(
                CloudflareDNSRecord(
                    content=first_record["content"],
                    id=first_record["id"],
                    name=first_record["name"],
                    proxied=first_record["proxied"],
                    type=first_record["type"],
                )
            )
        return record_information

    async def update_records(
        self,
        zone_id: str,
        records: list[CloudflareDNSRecord],
        content: str,
    ) -> None:
        """Update DNS records."""
        success, error = [], []

        if content is None:
            raise CloudflareException("No content provided, skipping update")

        for record in records:
            if record["content"] == content:
                LOGGER.debug(
                    "No need to update record (%s) content did not change",
                    record["name"],
                )
                continue

            if (
                record["id"] is None
                or record["type"] is None
                or record["name"] is None
                or record["proxied"] is None
            ):
                LOGGER.debug(
                    "Skipping record (%s) as it is not supported by the API",
                    record["name"],
                )
                continue

            result = await self.update_dns_record(
                zone_id=zone_id,
                record=record,
            )

            if result["success"]:
                success.append(record["name"])
            else:
                error.append(record["name"])

            if success:
                LOGGER.debug("Updated DNS records %s", success)
            if error:
                raise CloudflareException(f"Failed updating DNS records {error}")

    async def update_dns_record(
        self,
        *,
        zone_id: str,
        record: CloudflareDNSRecord,
    ) -> dict[str, Any]:
        """Update a DNS record."""
        result: dict[str, Any] = await self.api.put(
            url=self._endpoint(path=f"{zone_id}/dns_records/{record['id']}"),
            json_data={
                "type": record["type"],
                "name": record["name"],
                "content": record["content"],
                "proxied": record["proxied"],
            },
        )
        return result

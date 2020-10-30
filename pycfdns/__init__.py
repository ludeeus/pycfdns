"""Update Cloudflare DNS A-records."""
# pylint: disable=broad-except
import json
import logging
from pycfdns.models import CFAPI, CFAuth, CFRecord
from pycfdns.const import BASE_URL, NAME
from pycfdns.exceptions import CloudflareException, CloudflareZoneException

_LOGGER = logging.getLogger(NAME)


class CloudflareUpdater:
    """This class is used to update Cloudflare DNS records."""

    def __init__(self, session, token, zone, records=None, timeout=10):
        """Initialize"""
        self.api = CFAPI(session, CFAuth(token), timeout)
        self.zone = zone
        self.records = records

    async def get_zones(self):
        """Get the zones linked to account."""
        zones = []

        url = BASE_URL.format("")
        data = await self.api.get_json(url)
        data = data["result"]

        if data is None:
            return None

        for zone in data:
            zones.append(zone["name"])

        return zones

    async def get_zone_id(self):
        """Get the zone id for the zone."""
        zone_id = None
        endpoint = f"?name={self.zone}"
        url = BASE_URL.format(endpoint)
        data = await self.api.get_json(url)
        try:
            zone_id = data["result"][0]["id"]
        except Exception as error:
            raise CloudflareZoneException("Could not get zone ID") from error
        return zone_id

    async def get_zone_records(self, zone_id, record_type=None):
        """Get the records of a zone."""
        records = []

        endpoint = f"{zone_id}/dns_records?per_page=100"
        if record_type:
            endpoint += f"&type={record_type}"

        url = BASE_URL.format(endpoint)
        data = await self.api.get_json(url)
        data = data["result"]

        if data is None:
            return None

        for record in data:
            records.append(record["name"])

        return records

    async def get_record_info(self, zone_id):
        """Get the information of the records."""
        record_information = []
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

            endpoint = f"{zone_id}/dns_records?name={record}"
            url = BASE_URL.format(endpoint)
            data = await self.api.get_json(url)
            if data.get("result") is None:
                continue
            record_information.append(CFRecord(data["result"][0]))
        return record_information

    async def update_records(self, zone_id, records, external_ip=None):
        """Update DNS records."""
        if external_ip is None:
            external_ip = await self.api.get_external_ip()
        success, error = [], []

        if external_ip is None:
            raise CloudflareException("No external IP, skipping update")

        for record in records:
            if record.record_content == external_ip:
                _LOGGER.debug(
                    "No need to update record (%s) IP did not change",
                    record.record_name,
                )
                continue
            if record.record_type != "A":
                raise CloudflareException(
                    f"Record type {record.record_type}, is not supported"
                )
            endpoint = f"{zone_id}/dns_records/{record.record_id}"
            url = BASE_URL.format(endpoint)

            data = {
                "type": record.record_type,
                "name": record.record_name,
                "content": external_ip,
                "proxied": record.record_proxied,
            }

            result = await self.api.put_json(url, json.dumps(data))

            if result["success"]:
                success.append(record.record_name)
            else:
                error.append(record.record_name)

            if success:
                _LOGGER.debug("Updated DNS records %s", success)
            if error:
                raise CloudflareException(f"Failed updating DNS records {error}")

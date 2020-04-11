"""Update Cloudflare DNS A-records."""
# pylint: disable=broad-except
import json
import logging
from pycfdns.models import CFAPI, CFAuth, CFRecord
from pycfdns.const import BASE_URL, NAME

_LOGGER = logging.getLogger(NAME)


class CloudflareUpdater:
    """This class is used to update Cloudflare DNS records."""

    def __init__(self, session, email, token, zone, records=None):
        """Initialize"""
        self.api = CFAPI(session, CFAuth(email, token))
        self.zone = zone
        self.records = records

    async def get_zone_id(self):
        """Get the zone id for the zone."""
        zone_id = None
        endpoint = f"?name={self.zone}"
        url = BASE_URL.format(endpoint)
        data = await self.api.get_json(url)
        try:
            zone_id = data["result"][0]["id"]
        except Exception:
            pass
        return zone_id

    async def get_record_info(self, zone_id):
        """Get the information of the records."""
        record_information = []
        if self.records is None:
            self.records = []
            endpoint = f"{zone_id}/dns_records&per_page=100"
            url = BASE_URL.format(endpoint)
            data = await self.api.get_json(url)
            data = data["result"]

            if data is None:
                _LOGGER.error("No records found for %s", zone_id)
                return record_information

            for record in data:
                self.records.append(record["name"])

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

    async def update_records(self, zone_id, records):
        """Update DNS records."""
        external_ip = await self.api.get_external_ip()
        success, error = [], []

        if external_ip is None:
            _LOGGER.error("No external IP, skipping update")

        for record in records:
            if record.record_content == external_ip:
                continue
            elif record.record_type != "A":
                continue
            endpoint = f"{zone_id}/dns_records/{record.record_id}"
            url = BASE_URL.format(endpoint)
            data = {
                "type": record.record_type,
                "name": record.record_name,
                "content": external_ip,
                "proxied": bool(record.record_proxied),
            }

            result = await self.api.put_json(url, json.dumps(data))

            if result["success"]:
                success.append(record.record_name)
            else:
                error.append(record.record_name)

            if success:
                _LOGGER.info("Updated DNS records %s", success)
            if error:
                _LOGGER.error("Failed updating DNS records %s", error)

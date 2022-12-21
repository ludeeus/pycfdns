"""pycfdns models."""
# pylint: disable=missing-docstring
from typing import TypedDict


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

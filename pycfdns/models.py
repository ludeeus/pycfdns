"""pycfdns models."""
from __future__ import annotations

from typing import TypedDict


class CFRecord:
    """CFRecord represents a Cloudflare DNS record."""

    def __init__(self, record: dict[str, str]) -> None:
        """Initialize the CFRecord object with a dictionary representation of the Cloudflare DNS record.

        Args:
            record (Dict[str, str]): A dictionary representation of the Cloudflare DNS record.
        """
        self.record = record

    @property
    def record_id(self) -> str | None:
        """Return the unique identifier for the Cloudflare DNS record."""
        return self.record.get("id")

    @property
    def record_type(self) -> str | None:
        """Return the type of the Cloudflare DNS record (e.g. A, AAAA, CNAME, etc)."""
        return self.record.get("type")

    @property
    def record_name(self) -> str | None:
        """Return the name of the Cloudflare DNS record (e.g. the domain name)."""
        return self.record.get("name")

    @property
    def record_proxied(self) -> bool | None:
        """Return a boolean value indicating whether the Cloudflare DNS record is proxied or not."""
        return self.record.get("proxied")

    @property
    def record_content(self) -> str | None:
        """Return the content of the Cloudflare DNS record (e.g. the IP address for an A record)."""
        return self.record.get("content")


class DNSRecord(TypedDict):
    """Dictionary representation of a DNS record

    Attributes:
        content (str): The content of the DNS record.
        id (str): The unique identifier for the DNS record.
        name (str): The name of the DNS record.
        proxied (bool): Whether the DNS record is proxied or not.
        type (str): The type of the DNS record (e.g. A, AAAA, CNAME, etc).
    """

    content: str
    id: str
    name: str
    proxied: bool
    type: str

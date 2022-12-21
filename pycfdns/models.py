"""pycfdns models."""
from __future__ import annotations

from typing import TypedDict


class CloudflareDNSRecord(TypedDict):
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

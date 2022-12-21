"""Update Cloudflare DNS A-records."""
from .models import DNSRecord as CloudflareDNSRecord
from .updater import CloudflareUpdater

__all__ = ["CloudflareUpdater", "CloudflareDNSRecord"]

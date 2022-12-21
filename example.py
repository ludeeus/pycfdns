"""Example usage of pycfdns."""
import asyncio
import aiohttp
from pycfdns import CloudflareUpdater

API_TOKEN = "token from https://developers.cloudflare.com/api/tokens/create"
ZONE = "example.com"


async def example():
    """Example usage of pycfdns with api token."""
    async with aiohttp.ClientSession() as session:
        cfupdate = CloudflareUpdater(
            session=session,
            token=API_TOKEN,
            zone="example.com",
            records=["test"],
        )
        zone_id = await cfupdate.get_zone_id()
        records = await cfupdate.get_record_info(zone_id)
        for record in records:
            print(record.record_name)
        await cfupdate.update_records(zone_id, records, "127.0.0.1")


asyncio.get_event_loop().run_until_complete(example())

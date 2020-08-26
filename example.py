"""Example usage of pycfdns."""
import asyncio
import aiohttp
from pycfdns import CloudflareUpdater

API_TOKEN = "token from https://developers.cloudflare.com/api/tokens/create"
ZONE = "example.com"
UPDATE_RECORDS = ["test"]


async def example():
    """Example usage of pycfdns with api token."""
    async with aiohttp.ClientSession() as session:
        cfupdate = CloudflareUpdater(session, API_TOKEN, ZONE, UPDATE_RECORDS)
        zone_id = await cfupdate.get_zone_id()
        records = await cfupdate.get_record_info(zone_id)
        for record in records:
            print(record.record_name)
        await cfupdate.update_records(zone_id, records)


asyncio.get_event_loop().run_until_complete(example())

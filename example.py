"""Example usage of pycfdns."""
import asyncio
import aiohttp
from pycfdns import CloudflareUpdater

EMAIL = "example@example.com"
TOKEN = "5cdba21d55cdba21d55cdba21d5"
API_TOKEN = "token from https://developers.cloudflare.com/api/tokens/create"
ZONE = "example.com"
UPDATE_RECORDS = ["test"]


async def example():
    """Example usage of pycfdns."""
    async with aiohttp.ClientSession() as session:
        cfupdate = CloudflareUpdater(session, EMAIL, TOKEN, ZONE, UPDATE_RECORDS)
        zone_id = await cfupdate.get_zone_id()
        records = await cfupdate.get_record_info(zone_id)
        for record in records:
            print(record.record_name)
        await cfupdate.update_records(zone_id, records)


async def exampleApiToken():
    """Example usage of pycfdns with api token."""
    async with aiohttp.ClientSession() as session:
        cfupdate = CloudflareUpdater(session, "", "", ZONE, UPDATE_RECORDS, API_TOKEN)
        zone_id = await cfupdate.get_zone_id()
        records = await cfupdate.get_record_info(zone_id)
        for record in records:
            print(record.record_name)
        await cfupdate.update_records(zone_id, records)


asyncio.get_event_loop().run_until_complete(example())
asyncio.get_event_loop().run_until_complete(exampleApiToken())

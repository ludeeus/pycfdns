"""Example usage of pycfdns."""
import os
import asyncio

import aiohttp
from pycfdns import Client

async def example():
    """Example usage of pycfdns."""
    async with aiohttp.ClientSession() as client_session:
        client = Client(api_token=os.getenv("CF_API_TOKEN"), client_session=client_session)
        zones = await client.list_zones()
        print(zones)

asyncio.get_event_loop().run_until_complete(example())

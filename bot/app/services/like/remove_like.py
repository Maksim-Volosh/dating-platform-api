import logging

import aiohttp
from config import API_KEY, API_URL


async def remove_like(liked_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
                f"{API_URL}/likes/pending/{liked_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 204:
                    return None

                return True
            
        except Exception as e:
            logging.error(f"API error: {e}")
            return None
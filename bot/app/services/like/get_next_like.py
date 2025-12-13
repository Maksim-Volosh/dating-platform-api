import logging

import aiohttp
from config import API_KEY, API_URL


async def get_next_like(liked_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/likes/pending/{liked_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 200:
                    return None

                data = await resp.json()
                liker_id: int = data.get("liker_id")
                return liker_id if liker_id else None
            
        except Exception as e:
            logging.error(f"API error: {e}")
            return None
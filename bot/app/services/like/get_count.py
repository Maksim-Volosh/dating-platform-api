import logging

import aiohttp
from config import API_KEY, API_URL


async def get_like_count(liked_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/likes/pending/count/{liked_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 200:
                    return None

                data = await resp.json()
                count: int = data.get("count")
                return count if count else None
            
        except Exception as e:
            logging.error(f"API error: {e}")
            return None
import logging
import time

import aiohttp
from config import API_KEY, API_URL


async def create_like(liker_id: int, liked_id: int) -> None | int:
    like_payload = {
        "liker_id": liker_id,
    }
    
    logging.info(f"Creating like at {time.time()}: {like_payload}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/likes/add_like/{liked_id}",
                headers={"x-api-key": API_KEY},
                json=like_payload,
            ) as resp:
                if resp.status != 201:
                    logging.error(f"CREATE LIKE API {resp.status}: {await resp.text()}")
                    return
                
                data = await resp.json()
                count: int = data.get("count")
                return count if count else None

        except Exception as e:
            logging.error(f"API error: {e}")

    return



import logging
import time

import aiohttp
from config import API_KEY, API_URL

async def create_swipe(liker_id: int, liked_id: int, decision: bool) -> bool:
    swipe_payload = {
        "liker_id": liker_id,
        "liked_id": liked_id,
        "decision": decision
    }
    
    logging.info(f"Creating swipe at {time.time()}: {swipe_payload}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/swipes/",
                headers={"x-api-key": API_KEY},
                json=swipe_payload,
            ) as resp:
                if resp.status != 201:
                    logging.error(f"CREATE SWIPE API {resp.status}: {await resp.text()}")
                    return False


        except Exception as e:
            logging.error(f"API error: {e}")

    return False

import logging

import aiohttp
from config import API_KEY, API_URL


async def is_match(user1_id: int, user2_id: int):
    match_payload = {
        "user1_id": user1_id,
        "user2_id": user2_id
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{API_URL}/swipes/is_match",
                headers={"x-api-key": API_KEY},
                json=match_payload,
            ) as resp:
                if resp.status != 200:
                    return False

                result = await resp.json()
                if isinstance(result, bool):
                    return result
                return False
            
        except Exception as e:
            logging.error(f"API error: {e}")
            return None
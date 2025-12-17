import logging

import aiohttp
from config import API_KEY, API_URL


async def ack_inbox_item(owner_id: int, candidate_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/inbox/ack/{owner_id}",
                headers={"x-api-key": API_KEY},
                json={
                    "candidate_id": candidate_id
                }
                
            ) as resp:
                if resp.status != 204:
                    return None

                return True
            
        except Exception as e:
            logging.error(f"API error: {e}")
            return None
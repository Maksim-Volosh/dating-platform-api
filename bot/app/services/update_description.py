import logging
import time

import aiohttp
from config import API_KEY, API_URL


async def update_description(description: str, telegram_id: int) -> bool:
    description_payload = {
        "description": description
    }

    logging.info(f"Updating description for user at {time.time()}: {description_payload}") 
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(
                f"{API_URL}/users/{telegram_id}/description/",
                headers={"x-api-key": API_KEY},
                json=description_payload,
            ) as resp:
                if resp.status == 200:
                    return True
                else:
                    logging.error(f"UPDATE DESCRIPTION API error: {await resp.text()}")
                    return False


        except Exception as e:
            logging.error(f"API error: {e}")
    return False
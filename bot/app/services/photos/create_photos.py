import logging
import time

import aiohttp
from config import API_KEY, API_URL


async def create_photos_for_user(data: dict, telegram_id: int) -> bool:
    photo_payload = [
        {"file_id": file_id} for file_id in data["photo_ids"]
    ]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/users/{telegram_id}/photos/",
                headers={"x-api-key": API_KEY},
                json=photo_payload,
            ) as resp:
                if resp.status == 201:
                    return True
                else:
                    logging.error(f"CREATE PHOTO API {resp.status}: {await resp.text()}")
                    return False


        except Exception as e:
            logging.error(f"API error: {e}")
    return False
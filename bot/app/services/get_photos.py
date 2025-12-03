import logging

import aiohttp
from config import API_KEY, API_URL


async def get_user_photos(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    f"{API_URL}/users/{telegram_id}/photos",
                    headers={"x-api-key": API_KEY}
                ) as photo_resp:

                    if photo_resp.status != 200:
                        logging.error(f"GET PHOTO API error: {await photo_resp.text()}")
                        return

                    photos_data = await photo_resp.json()
                    photos = photos_data.get("photos", [])
                    
                    return photos
        except Exception as e:
            logging.error(f"API error: {e}")
            return
import logging

import aiohttp
from config import API_KEY, API_URL


async def get_next_user(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    f"{API_URL}/decks/next/{telegram_id}",
                    headers={"x-api-key": API_KEY}
                ) as resp:

                    if resp.status == 404:
                        return None

                    if resp.status != 200:
                        logging.error(f"GET PHOTO API {resp.status}: {await resp.text()}")
                        return None

                    user_data = await resp.json()
                    if user_data:
                        return user_data
                    return
                
        except Exception as e:
            logging.error(f"API error: {e}")
            return
import logging

import aiohttp
from config import API_KEY, API_URL


async def get_user(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        try:
            # --- 1. Get user data ---
            async with session.get(
                f"{API_URL}/users/{telegram_id}",
                headers={"x-api-key": API_KEY}
            ) as resp:
                if resp.status != 200:
                    return None

                data = await resp.json()
                return data if data else None
        except Exception as e:
            logging.error(f"API error: {e}")
            return False
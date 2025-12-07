import logging
import time

import aiohttp
from config import API_KEY, API_URL

GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
}
PREFER_GENDER_MAP = {
    "Мужской": "male",
    "Женский": "female",
    "Неважно": "anyone",
}

async def update_user_profile(data: dict, telegram_id: int) -> bool:
    user_payload = {
        "name": data["name"],
        "age": int(data["age"]),
        "city": data["city"],
        "description": data["description"],
        "gender": GENDER_MAP[data["gender"]],
        "prefer_gender": PREFER_GENDER_MAP[data["prefer_gender"]],
    }
    
    logging.info(f"Updating user at {time.time()}: {user_payload}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(
                f"{API_URL}/users/{telegram_id}/",
                headers={"x-api-key": API_KEY},
                json=user_payload,
            ) as resp:
                if resp.status != 201:
                    logging.error(f"UPDATE USER API error: {await resp.text()}")
                    return False

        except Exception as e:
            logging.error(f"API error: {e}")

    return False

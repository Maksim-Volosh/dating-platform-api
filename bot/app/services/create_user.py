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

async def create_user(data: dict, telegram_id: int) -> bool:
    payload = {
        "telegram_id": telegram_id,
        "name": data["name"],
        "age": int(data["age"]),
        "city": data["city"],
        "description": data["description"],
        "gender": GENDER_MAP[data["gender"]],
        "prefer_gender": PREFER_GENDER_MAP[data["prefer_gender"]],
    }
    logging.info(f"Creating user at {time.time()}: {payload}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}/users/",
                headers={"x-api-key": API_KEY},
                json=payload,
            ) as resp:
                if resp.status == 201:
                    return True
                else:
                    logging.error(f"API error: {await resp.text()}")
                    return False


        except Exception as e:
            logging.error(f"API error: {e}")
    return False

from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN", "key")
API_URL = getenv("API_URL", "http://localhost:8000/api/v1")
API_KEY = getenv("API_KEY", "key")
from aiogram import Dispatcher
from . import start, registration, profile

def register_all_handlers(dp: Dispatcher):
    start.register(dp)
    registration.register(dp)
    profile.register(dp)

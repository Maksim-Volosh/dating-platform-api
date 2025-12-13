from aiogram import Dispatcher
from . import start, registration, profile, change_profile, swipe, like

def register_all_handlers(dp: Dispatcher):
    start.register(dp)
    registration.register(dp)
    profile.register(dp)
    change_profile.register(dp)
    swipe.register(dp)
    like.register(dp)

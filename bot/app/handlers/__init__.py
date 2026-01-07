from aiogram import Dispatcher

from . import change_profile, like, profile, registration, start, swipe


def register_all_handlers(dp: Dispatcher):
    start.register(dp)
    registration.register(dp)
    profile.register(dp)
    change_profile.register(dp)
    swipe.register(dp)
    like.register(dp)

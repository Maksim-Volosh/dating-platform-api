from aiogram.types import Message

from app.keyboards.keyboards import (get_name_keyboard, main_kb, photo_kb,
                                     swipe_kb)


class ChangeProfilePresenter:
    async def start_swiping(self, message: Message) -> None:
        await message.answer("✨🔍", reply_markup=swipe_kb)
        
    async def restart_registration(self, message: Message) -> None:
        await message.answer("Ну давай по новой ✨")
        
    async def ask_name(self, message: Message) -> None:
        await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))
        
    async def ask_photos(self, message: Message) -> None:
        await message.answer(
            "Отлично, теперь пришли мне свои фотографии (до 3х)",
            reply_markup=photo_kb
        )
        
    async def ask_description(self, message: Message) -> None:
        await message.answer("Окей, давай по новой! Расскажи немного о себе.")
        
    async def photo_added(self, message: Message, count: int):
        await message.answer(f"Фото добавлено ({count}/3).", reply_markup=photo_kb)

    async def no_photos(self, message: Message) -> None:
        await message.answer("Ты не отправил ни одной фотографии 🙃")
        
    async def finish_photo_update(self, message: Message) -> None:
        await message.answer("Отлично! Фотографии обновлены! 🎉", reply_markup=main_kb)
        
    async def send_error(self, message: Message, error: str) -> None:
        await message.answer(error)
        
    async def finish_description_update(self, message: Message) -> None:
        await message.answer("Описание обновлено! 🎉", reply_markup=main_kb)
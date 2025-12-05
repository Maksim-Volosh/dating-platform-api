import asyncio

from aiogram import Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.keyboards import get_name_keyboard, main_kb, photo_kb
from app.services import update_photos_for_user
from app.states import Registration, UpdatePhotos

router = Router()
            
@router.message(F.text == "2")
async def restart_registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Ну давай по новой ✨")
    await state.set_state(Registration.name)
    await state.update_data(update=True)
    await message.answer("Как тебя зовут?", reply_markup=await get_name_keyboard(message))
    
@router.message(F.text == "3")
async def update_photos(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Окей, пришли мне свои фотографии где можно увидеть твою красоту!) Фотографий не должно быть больше 3х")
    await state.set_state(UpdatePhotos.photos)

@router.message(UpdatePhotos.photos, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])


    if len(photo_ids) < 3:
        file_id = message.photo[-1].file_id # type: ignore
        # take the highest quality photo
        photo_ids.append(file_id)

        await state.update_data(photo_ids=photo_ids)
        if len(photo_ids) == 3:
            await message.answer(
                f"Фото добавлено ({len(photo_ids)}/3)."
            )
            await finish_photo_upload(message, state)
        elif len(photo_ids) < 3:
            await message.answer(
                f"Фото добавлено ({len(photo_ids)}/3). Отправь ещё или нажми «Завершить», когда закончишь.", reply_markup=photo_kb
            )
      
@router.message(UpdatePhotos.photos, F.text.lower() == "завершить")
async def finish_photo_upload(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])

    if not photo_ids:
        await message.answer("Ты не отправил ни одной фотографии 🙃")
        return
    
    await asyncio.sleep(0.5)
    await message.answer("Отлично! Фотографии обновлены! 🎉", reply_markup=main_kb)
    
    if message.from_user is not None:
        await update_photos_for_user(data, message.from_user.id)

    await state.clear()
            
def register(dp: Dispatcher) -> None:
    dp.include_router(router)
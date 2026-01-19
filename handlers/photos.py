from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from config_data.config import CAT_PHOTOS
from handlers.keyboards import photos_menu_keyboard
from services.cat_random_image_api import fetch_random_cat_image
from utils.concurrency import acquire_or_notify


router = Router()


async def _send_local_album(call: CallbackQuery, photo_list, title):
    media = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_list]
    await call.message.answer(f"📸 {title}")
    await call.bot.send_media_group(chat_id=call.message.chat.id, media=media)
    await call.message.answer("Хочешь еще?", reply_markup=photos_menu_keyboard())


@router.callback_query(F.data == "photo:manechka")
async def photo_manechka(call: CallbackQuery):
    await _send_local_album(call, CAT_PHOTOS["Манечка"], "Манечка")
    await call.answer()


@router.callback_query(F.data == "photo:cezar")
async def photo_cezar(call: CallbackQuery):
    await _send_local_album(call, CAT_PHOTOS["Цезарь"], "Цезарь")
    await call.answer()


@router.callback_query(F.data == "photo:scottish")
async def photo_scottish(call: CallbackQuery):
    await _send_local_album(call, CAT_PHOTOS["Шотландец"], "Шотландец")
    await call.answer()


@router.callback_query(F.data == "photo:random")
async def photo_random(call: CallbackQuery, session, settings, semaphore):
    if not await acquire_or_notify(semaphore, call):
        return
    try:
        image_url = await fetch_random_cat_image(session, settings)
    finally:
        semaphore.release()
    if image_url:
        await call.message.answer_photo(
            image_url,
            caption="Вот тебе котик. Еще?",
            reply_markup=photos_menu_keyboard(),
        )
    else:
        await call.message.answer(
            "Не удалось получить фото. Попробуй чуть позже.",
            reply_markup=photos_menu_keyboard(),
        )
    await call.answer()

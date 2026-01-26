from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from config_data.config import CAT_PHOTOS
from services.cat_random_image_api import fetch_random_cat_image
from utils.concurrency import acquire_or_notify
from utils.i18n import t, resolve_user_lang


router = Router()

async def _send_local_album(call: CallbackQuery, photo_list: list[str]):
    media = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_list]
    await call.bot.send_media_group(chat_id=call.message.chat.id, media=media)


@router.callback_query(F.data == "photo:manechka")
async def photo_manechka(call: CallbackQuery, ui_state):
    await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Манечка"])
    await call.answer()


@router.callback_query(F.data == "photo:cezar")
async def photo_cezar(call: CallbackQuery, ui_state):
    await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Цезарь"])
    await call.answer()


@router.callback_query(F.data == "photo:scottish")
async def photo_scottish(call: CallbackQuery, ui_state):
    await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Шотландец"])
    await call.answer()


@router.callback_query(F.data == "photo:random")
async def photo_random(call: CallbackQuery, session, settings, semaphore, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    if not await acquire_or_notify(semaphore, call, lang):
        return
    try:
        image_url = await fetch_random_cat_image(session, settings)
    finally:
        semaphore.release()

    if image_url:
        await call.message.answer_photo(
            image_url,
            caption=t(lang, "photos.random_caption"),
        )
    else:
        await call.message.answer(
            t(lang, "photos.random_error"),
        )
    await call.answer()

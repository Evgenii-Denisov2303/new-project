from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from config_data.config import CAT_PHOTOS
from handlers.keyboards import action_menu_keyboard, photos_menu_keyboard
from handlers.ui import send_or_update_hub
from services.cat_random_image_api import fetch_random_cat_image
from utils.concurrency import acquire_or_notify
from utils.i18n import t, resolve_user_lang


router = Router()

async def _send_local_album(call: CallbackQuery, photo_list: list[str], title: str, lang: str):
    media = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_list]
    await call.bot.send_media_group(chat_id=call.message.chat.id, media=media)

    await call.message.answer(
        t(lang, "photos.album_done").format(title=title),
        reply_markup=action_menu_keyboard(t(lang, "btn.more_photo"), "menu:photos", lang=lang),
    )


@router.callback_query(F.data == "photo:manechka")
async def photo_manechka(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Манечка"], "Манечка", lang)
    await send_or_update_hub(call.message, t(lang, "photos.hub"), photos_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "photo:cezar")
async def photo_cezar(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Цезарь"], "Цезарь", lang)
    await send_or_update_hub(call.message, t(lang, "photos.hub"), photos_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "photo:scottish")
async def photo_scottish(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await _send_local_album(call, CAT_PHOTOS["Шотландец"], "Шотландец", lang)
    await send_or_update_hub(call.message, t(lang, "photos.hub"), photos_menu_keyboard(lang), ui_state, repost=True)
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
            reply_markup=action_menu_keyboard(t(lang, "btn.more_random"), "photo:random", lang=lang),
        )
    else:
        await call.message.answer(
            t(lang, "photos.random_error"),
            reply_markup=action_menu_keyboard(t(lang, "btn.more_random"), "photo:random", lang=lang),
        )

    await send_or_update_hub(call.message, t(lang, "photos.hub"), photos_menu_keyboard(lang), ui_state, repost=True)
    await call.answer()

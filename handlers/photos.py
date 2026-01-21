from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from config_data.config import CAT_PHOTOS
from handlers.keyboards import action_menu_keyboard, photos_menu_keyboard
from handlers.ui import send_or_update_hub
from services.cat_random_image_api import fetch_random_cat_image
from utils.concurrency import acquire_or_notify


router = Router()

PHOTOS_HUB_TEXT = (
    "📸 <b>Фото котиков</b>\n"
    "Выбери любимчика или нажми случайный кадр.\n"
    "────────"
)


async def _send_local_album(call: CallbackQuery, photo_list: list[str], title: str):
    media = [InputMediaPhoto(media=FSInputFile(path)) for path in photo_list]
    await call.bot.send_media_group(chat_id=call.message.chat.id, media=media)

    await call.message.answer(
        f"📸 <b>{title}</b>\n────────\nГотово. Хочешь еще?",
        reply_markup=action_menu_keyboard("Еще фото", "menu:photos"),
    )


@router.callback_query(F.data == "photo:manechka")
async def photo_manechka(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Манечка"], "Манечка")
    await send_or_update_hub(call.message, PHOTOS_HUB_TEXT, photos_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "photo:cezar")
async def photo_cezar(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Цезарь"], "Цезарь")
    await send_or_update_hub(call.message, PHOTOS_HUB_TEXT, photos_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "photo:scottish")
async def photo_scottish(call: CallbackQuery, ui_state):
    await _send_local_album(call, CAT_PHOTOS["Шотландец"], "Шотландец")
    await send_or_update_hub(call.message, PHOTOS_HUB_TEXT, photos_menu_keyboard(), ui_state, repost=True)
    await call.answer()


@router.callback_query(F.data == "photo:random")
async def photo_random(call: CallbackQuery, session, settings, semaphore, ui_state):
    if not await acquire_or_notify(semaphore, call):
        return
    try:
        image_url = await fetch_random_cat_image(session, settings)
    finally:
        semaphore.release()

    if image_url:
        await call.message.answer_photo(
            image_url,
            caption="🎲 <b>Случайный котик</b>\n────────\nВот тебе котик 🐾",
            reply_markup=action_menu_keyboard("🎲 Еще случайный", "photo:random"),
        )
    else:
        await call.message.answer(
            "🎲 <b>Случайный котик</b>\n────────\n"
            "Не удалось получить фото. Попробуй чуть позже.",
            reply_markup=action_menu_keyboard("🎲 Еще случайный", "photo:random"),
        )

    await send_or_update_hub(call.message, PHOTOS_HUB_TEXT, photos_menu_keyboard(), ui_state, repost=True)
    await call.answer()
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
            caption="Вот тебе котик 🐾",
            reply_markup=action_menu_keyboard("🎲 Еще случайный", "photo:random"),
        )
    else:
        await call.message.answer(
            "🎲 <b>Случайный котик</b>\n────────\n"
            "Не удалось получить фото. Попробуй чуть позже.",
            reply_markup=action_menu_keyboard("🎲 Еще случайный", "photo:random"),
        )
    await call.answer()

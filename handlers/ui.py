from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


async def send_or_update_hub(
    message,
    text: str,
    markup: InlineKeyboardMarkup | None,
    ui_state: dict,
    *,
    reply_keyboard: ReplyKeyboardMarkup | None = None,
    force_new: bool = False,
    repost: bool = False,
):
    """
    Hub = одно "меню-сообщение" с InlineKeyboard под ним.

    - По умолчанию: редактируем прошлый hub (чтобы не спамить).
    - repost=True: удаляем прошлый hub и отправляем новый (перемещаем вниз).
    - force_new=True: не редактируем, а всегда отправляем новый hub.

    Важно:
    - ReplyKeyboard (нижние кнопки) НЕЛЬЗЯ надежно включить через editMessageText.
      Поэтому, если reply_keyboard передан — мы всегда отправляем отдельное "пустое"
      сообщение, чтобы Telegram показал клавиатуру.
    """

    chat_id = message.chat.id
    user_id = message.from_user.id

    # 1) "Будим" ReplyKeyboard отдельным sendMessage (это единственный надежный способ)
    if reply_keyboard is not None:
        try:
            await message.answer("\u200b", reply_markup=reply_keyboard)  # zero-width space
        except Exception:
            pass

    hub_message_id = ui_state.get(user_id)

    # 2) repost: удалить предыдущий hub, чтобы меню было снизу
    if repost and hub_message_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=hub_message_id)
        except TelegramBadRequest:
            pass
        ui_state.pop(user_id, None)
        hub_message_id = None

    # 3) Попытка редактировать hub (если можно)
    if (not force_new) and hub_message_id:
        try:
            await message.bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=hub_message_id,
                reply_markup=markup,
            )
            return
        except TelegramBadRequest as exc:
            if "message is not modified" in str(exc):
                return
            # если не получилось — забудем старый id и отправим новый hub
            ui_state.pop(user_id, None)

    # 4) Отправить новый hub (InlineKeyboard под сообщением)
    sent = await message.answer(text, reply_markup=markup)
    ui_state[user_id] = sent.message_id
from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


async def send_or_update_hub(
    message,
    text: str,
    markup: InlineKeyboardMarkup | None = None,
    ui_state: dict | None = None,
    reply_keyboard: ReplyKeyboardMarkup | None = None,
    *,
    force_new: bool = False,
    repost: bool = False,
    # backward-compat:
    inline_keyboard: InlineKeyboardMarkup | None = None,
    **_kwargs,
):
    """
    Backward-compatible hub sender/updater.

    Supports old calls:
      - send_or_update_hub(message, text, inline_kb, ui_state, repost=True, reply_keyboard=...)
      - send_or_update_hub(message, text, markup=..., ui_state=...)
      - send_or_update_hub(..., inline_keyboard=...)
    """

    # ---- normalize args ----
    if ui_state is None:
        ui_state = {}

    if markup is None and inline_keyboard is not None:
        markup = inline_keyboard

    chat_id = message.chat.id
    user_id = message.from_user.id

    # 1) Wake ReplyKeyboard reliably (only sendMessage can show it)
    if reply_keyboard is not None:
        try:
            await message.answer("\u200b", reply_markup=reply_keyboard)
        except Exception:
            pass

    hub_message_id = ui_state.get(user_id)

    # 2) repost: delete previous hub to move to bottom
    if repost and hub_message_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=hub_message_id)
        except TelegramBadRequest:
            pass
        ui_state.pop(user_id, None)
        hub_message_id = None

    # 3) edit existing hub if possible
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
            ui_state.pop(user_id, None)

    # 4) send new hub
    sent = await message.answer(text, reply_markup=markup)
    ui_state[user_id] = sent.message_id
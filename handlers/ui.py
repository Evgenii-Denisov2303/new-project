from aiogram.exceptions import TelegramBadRequest


async def send_or_update_hub(
    message,
    text,
    markup,
    ui_state,
    reply_keyboard=None,
    *,
    force_new: bool = False,
    repost: bool = False,
):
    """Send or update the 'hub' message.

    - Default: tries to edit the previous hub message (so menu stays in one place).
    - force_new=True: always send a new message (useful for results that must appear at the bottom).
    - repost=True: delete the previous hub message (if any) and send a new hub message (moves hub to bottom).
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = ui_state.get(user_id)

    # Optionally replace the hub message to move it to the bottom of the chat.
    if repost and message_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except TelegramBadRequest:
            pass
        message_id = None
        ui_state.pop(user_id, None)

    if (not force_new) and message_id:
        try:
            await message.bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup,
            )
            return
        except TelegramBadRequest as exc:
            if "message is not modified" in str(exc):
                return

    reply_markup = markup if markup is not None else reply_keyboard
    sent = await message.answer(text, reply_markup=reply_markup)
    ui_state[user_id] = sent.message_id

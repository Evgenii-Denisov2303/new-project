from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardMarkup

async def send_or_update_hub(
    message,
    text,
    inline_keyboard,
    ui_state,
    repost=False,
    reply_keyboard: ReplyKeyboardMarkup | None = None,
):
    # ✅ ВСЕГДА "будим" нижнюю клавиатуру отдельным sendMessage,
    # потому что editMessageText не умеет выставлять ReplyKeyboard.
    if reply_keyboard is not None:
        try:
            await message.answer("\u200b", reply_markup=reply_keyboard)  # zero-width space
        except Exception:
            pass


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
    """Send or update the 'hub' message (menu message).

    Default behavior:
      - Edit the previous hub message (keeps a single menu message).

    Options:
      - force_new=True: always send a new message (use for results that must appear as a new message).
      - repost=True: delete the previous hub message (if any) and send a new one.
        This effectively 'moves' the hub to the bottom of the chat.
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    hub_message_id = ui_state.get(user_id)

    # Move hub to bottom by deleting the previous hub message and sending a fresh one.
    if repost and hub_message_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=hub_message_id)
        except TelegramBadRequest:
            pass
        ui_state.pop(user_id, None)
        hub_message_id = None

    # Update in place (keeps hub in the same position in chat history)
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
            # Safe to ignore "not modified"
            if "message is not modified" in str(exc):
                return
            # Any other edit error -> fall back to sending a new hub below
            ui_state.pop(user_id, None)

    # Send new hub
    reply_markup = markup if markup is not None else reply_keyboard
    sent = await message.answer(text, reply_markup=reply_markup)
    ui_state[user_id] = sent.message_id

import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from handlers.keyboards import survey_keyboard
from handlers.ui import send_or_update_hub
from utils.i18n import t, resolve_user_lang


router = Router()


class CommentState(StatesGroup):
    waiting_for_comment = State()


@router.message(Command("survey"))
async def survey_command(message: Message, ui_state):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    await send_or_update_hub(
        message,
        t(lang, "survey.title"),
        survey_keyboard(lang),
        ui_state, repost=True
    )


@router.callback_query(F.data == "survey:open")
async def survey_open(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await call.message.answer(
        t(lang, "survey.title"),
        reply_markup=survey_keyboard(lang),
    )
    await call.answer()


@router.callback_query(F.data == "survey:rate")
async def survey_rate(call: CallbackQuery, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await call.message.answer_poll(
        question=t(lang, "survey.poll_question"),
        options=["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"],
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    await call.message.answer(t(lang, "survey.thanks"))
    await call.answer()


@router.callback_query(F.data == "survey:comment")
async def survey_comment(call: CallbackQuery, state: FSMContext, ui_state):
    lang = await resolve_user_lang(call.from_user.id, call.from_user.language_code)
    await state.set_state(CommentState.waiting_for_comment)
    await call.message.answer(t(lang, "survey.ask_comment"))
    await call.answer()


@router.message(CommentState.waiting_for_comment)
async def handle_comment(message: Message, state: FSMContext):
    lang = await resolve_user_lang(message.from_user.id, message.from_user.language_code)
    comment = message.text.strip() if message.text else ""
    if not comment:
        await message.answer(t(lang, "survey.empty_comment"))
        return

    await asyncio.to_thread(_append_comment, message.from_user.id, comment)
    await state.clear()
    await message.answer(
        t(lang, "survey.thanks_comment"),
        reply_markup=None,
    )


def _append_comment(user_id: int, comment: str) -> None:
    with open("comments.txt", "a", encoding="utf-8") as file:
        file.write(f"User {user_id}: {comment}\n")

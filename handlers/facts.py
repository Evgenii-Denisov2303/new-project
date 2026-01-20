import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from database.db_setup import get_user_facts, update_user_facts
from handlers.keyboards import facts_nav_keyboard
from handlers.ui import send_or_update_hub
from services.cat_fact_api import fetch_cat_fact
from services.translate_api import translate_text
from utils.concurrency import acquire_or_notify


router = Router()
MAX_FACTS_PER_USER = 80


def _format_fact(original: str, translation: str | None) -> str:
    header = "🧠 <b>Кошачий факт</b>"
    if not translation:
        return (
            f"{header}\n────────\n"
            f"🇬🇧 {original}\n\n"
            "❌ Перевод временно недоступен"
        )
    return f"{header}\n────────\n🇬🇧 {original}\n\n🇷🇺 {translation}"


async def _show_fact(call: CallbackQuery, facts: list, current_index: int):
    current = facts[current_index]
    text = current.get("display_text") or _format_fact(
        current.get("text", ""), current.get("translation")
    )
    markup = facts_nav_keyboard(
        has_prev=current_index > 0,
        has_next=current_index < len(facts) - 1,
    )
    try:
        await call.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=markup)


@router.callback_query(F.data == "menu:facts")
async def menu_facts(call: CallbackQuery, session, settings, cache, semaphore):
    if not await acquire_or_notify(semaphore, call):
        return
    try:
        fact = await fetch_cat_fact(session, settings, cache)
        if not fact:
            await call.message.answer(
                "Не удалось получить факт. Попробуй чуть позже."
            )
            await call.answer()
            return

        translation = await translate_text(session, settings, cache, fact)
    finally:
        semaphore.release()
    display_text = _format_fact(fact, translation)

    data = await get_user_facts(call.from_user.id)
    facts = data["facts"]
    facts.append(
        {
            "text": fact,
            "translation": translation,
            "display_text": display_text,
        }
    )
    if len(facts) > MAX_FACTS_PER_USER:
        facts = facts[-MAX_FACTS_PER_USER:]
    current_index = len(facts) - 1
    await update_user_facts(call.from_user.id, facts, current_index)

    await _show_fact(call, facts, current_index)
    await call.answer()


@router.message(F.text == "Факты")
async def menu_facts_message(
    message: Message,
    session,
    settings,
    cache,
    semaphore,
    ui_state,
):
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=0.1)
    except asyncio.TimeoutError:
        await message.answer("Бот сейчас занят, попробуй чуть позже.")
        return
    try:
        fact = await fetch_cat_fact(session, settings, cache)
        if not fact:
            await message.answer("Не удалось получить факт. Попробуй чуть позже.")
            return
        translation = await translate_text(session, settings, cache, fact)
    finally:
        semaphore.release()

    display_text = _format_fact(fact, translation)
    data = await get_user_facts(message.from_user.id)
    facts = data["facts"]
    facts.append(
        {
            "text": fact,
            "translation": translation,
            "display_text": display_text,
        }
    )
    if len(facts) > MAX_FACTS_PER_USER:
        facts = facts[-MAX_FACTS_PER_USER:]
    current_index = len(facts) - 1
    await update_user_facts(message.from_user.id, facts, current_index)

    await send_or_update_hub(
        message,
        display_text,
        facts_nav_keyboard(
            has_prev=current_index > 0,
            has_next=current_index < len(facts) - 1,
        ),
        ui_state,
    )


@router.callback_query(F.data.in_({"facts:new", "facts:prev", "facts:next"}))
async def facts_nav(call: CallbackQuery, session, settings, cache, semaphore):
    data = await get_user_facts(call.from_user.id)
    facts = data["facts"]
    current_index = data["current_index"]

    if call.data == "facts:new":
        if not await acquire_or_notify(semaphore, call):
            return
        try:
            fact = await fetch_cat_fact(session, settings, cache)
            if not fact:
                await call.answer("Не удалось получить факт.", show_alert=True)
                return
            translation = await translate_text(session, settings, cache, fact)
        finally:
            semaphore.release()
        display_text = _format_fact(fact, translation)
        facts.append(
            {
                "text": fact,
                "translation": translation,
                "display_text": display_text,
            }
        )
        if len(facts) > MAX_FACTS_PER_USER:
            facts = facts[-MAX_FACTS_PER_USER:]
        current_index = len(facts) - 1
    elif call.data == "facts:prev" and current_index > 0:
        current_index -= 1
    elif call.data == "facts:next" and current_index < len(facts) - 1:
        current_index += 1

    if not facts:
        await call.message.answer("Фактов пока нет. Нажми «Новый».")
        await call.answer()
        return

    await update_user_facts(call.from_user.id, facts, current_index)
    await _show_fact(call, facts, current_index)
    await call.answer()


@router.callback_query(F.data == "noop")
async def noop(call: CallbackQuery):
    await call.answer()

"""
Miscellaneous helper handlers for OynaIQ.bot.

This module contains stubs for bonus features such as:

* referral system;
* post‑match feedback prompts;
* simple reaction commands (for future group integrations).
"""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="utils")


@router.message(F.text.regexp(r"(?i)^\s*/?nurlan\s*$"))
async def secret_nurlan_command(message: Message) -> None:
    """
    Secret command handler for `/Nurlan` (or `Nurlan` in any case).

    Matches:
        - /Nurlan
        - /nurlan
        - Nurlan
        - nurlan
    """

    await message.answer("Люблю тебя, пусанай!")


@router.message(Command("referral"))
async def cmd_referral(message: Message) -> None:
    """
    Generate a referral link stub for the current user.

    In MVP this simply shows a link of the form:
    ``t.me/playqbot?start=ref_<username>``.
    """

    username = message.from_user.username or str(message.from_user.id)
    link = f"t.me/playqbot?start=ref_{username}"
    await message.answer(
        "Пригласи друга → получите бонус (в будущем здесь будут реальные бонусы).\n\n"
        f"Твоя реферальная ссылка:\n{link}",
    )


@router.message(Command("feedback"))
async def cmd_feedback_stub(message: Message) -> None:
    """
    Stub for automatic post‑match feedback.

    In production this could be triggered after the scheduled match time.
    Currently it can be called manually via /feedback.
    """

    await message.answer(
        "🏁 Игра прошла 🔥\n"
        "Команда уже планирует следующую встречу...\n"
        "Скоро здесь появится опрос про качество площадки и уровень соперников.",
    )


@router.message(F.text.in_(["👍 Пойду", "🤔 Думаю", "👎 Не смогу"]))
async def reaction_stub(message: Message) -> None:
    """
    Simple text‑based emulation of reaction buttons in groups.

    In real chats these could be inline buttons under a match announcement.
    """

    if message.text == "👍 Пойду":
        reply = "Отлично! Добавим тебя в условный список участников 👍"
    elif message.text == "🤔 Думаю":
        reply = "Окей, подумай ещё немного. Места быстро разбирают 😉"
    else:
        reply = "Жаль, что не получится в этот раз. Надеюсь, присоединишься к следующей игре!"

    await message.reply(reply)




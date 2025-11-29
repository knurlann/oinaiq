"""
Match details keyboard.

Provides different button sets depending on the match status
(`ACTIVE`, `ALMOST_FULL`, `LOW_PLAYERS`).
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from oynaiq_bot.data.matches import Match, MatchStatus
from oynaiq_bot.utils.navigator import BookingCallback


def build_match_details_keyboard(match: Match) -> InlineKeyboardMarkup:
    """
    Build an inline keyboard for the match details screen.

    The layout depends on :attr:`Match.status`:

    * ACTIVE:
        - ✅ Подтвердить участие
        - 💳 Забронировать место (депозит N ₸)
        - 💬 Написать организатору
        - ↩ Назад к списку матчей
    * ALMOST_FULL:
        - 🚀 Подтвердить
        - 💳 Забронировать
        - 🔔 Получить напоминание, если появится место
    * LOW_PLAYERS:
        - 🔔 Уведомить
        - 💬 Написать организатору
        - ↩ Назад

    Args:
        match: Match for which to build the keyboard.

    Returns:
        :class:`InlineKeyboardMarkup` instance.
    """

    rows: list[list[InlineKeyboardButton]] = []

    if match.status is MatchStatus.ACTIVE:
        rows.append(
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить участие",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="confirm",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"💳 Забронировать место (депозит {match.deposit} ₸)",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="deposit",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="💬 Написать организатору",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="contact",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="↩ Назад к списку матчей",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="back_list",
                    ).pack(),
                )
            ]
        )

    elif match.status is MatchStatus.ALMOST_FULL:
        rows.append(
            [
                InlineKeyboardButton(
                    text="🚀 Подтвердить",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="confirm",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="💳 Забронировать",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="deposit",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="🔔 Получить напоминание, если появится место",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="waitlist",
                    ).pack(),
                )
            ]
        )

    else:  # LOW_PLAYERS and any other custom statuses fallback
        rows.append(
            [
                InlineKeyboardButton(
                    text="🔔 Уведомить",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="notify",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="💬 Написать организатору",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="contact",
                    ).pack(),
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="↩ Назад",
                    callback_data=BookingCallback(
                        match_id=match.id,
                        action="back_list",
                    ).pack(),
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)




"""
Booking and payment confirmation keyboards.

In the MVP implementation payments are mocked and always succeed.
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from oynaiq_bot.data.matches import Match
from oynaiq_bot.utils.navigator import PaymentCallback


def build_booking_keyboard(match: Match) -> InlineKeyboardMarkup:
    """
    Build an inline keyboard for confirming the booking payment.

    Buttons:
        - 💳 Оплатить через Kaspi Pay (кнопка-ссылка)
        - ✅ Я оплатил через Kaspi
        - ❌ Отмена

    Args:
        match: Match for which the booking is being made.

    Returns:
        :class:`InlineKeyboardMarkup` instance.
    """

    rows = [
        [
            InlineKeyboardButton(
                text="💳 Оплатить через Kaspi Pay",
                url="https://pay.kaspi.kz/pay/df3xuh5c",
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Я оплатил через Kaspi",
                callback_data=PaymentCallback(match_id=match.id, action="pay").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data=PaymentCallback(match_id=match.id, action="cancel").pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)




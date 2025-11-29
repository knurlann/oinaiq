"""
Sport selection keyboard for the "Найти команду" flow.

The keyboard presents four sport options as inline buttons.
"""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from oynaiq_bot.utils.navigator import SportCallback, SPORTS


def build_sport_choice_keyboard() -> InlineKeyboardMarkup:
    """
    Build an inline keyboard that lets the user choose a sport.

    Returns:
        :class:`InlineKeyboardMarkup` with four buttons:
        football, basketball, volleyball and other.
    """

    buttons = [
        [
            InlineKeyboardButton(
                text=SPORTS["football"],
                callback_data=SportCallback(sport="football").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=SPORTS["basketball"],
                callback_data=SportCallback(sport="basketball").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=SPORTS["volleyball"],
                callback_data=SportCallback(sport="volleyball").pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=SPORTS["other"],
                callback_data=SportCallback(sport="other").pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)




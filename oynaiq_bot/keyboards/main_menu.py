"""
Main menu keyboard for OynaIQ.bot.

This module contains a single helper function that returns the reply
keyboard shown after /start and for navigation back to the main screen.
"""

from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Create the main menu reply keyboard.

    Buttons:
        - 🧑‍🤝‍🧑 Найти команду
        - ⚡ Создать игру
        - 💬 Узнать, как это работает

    Returns:
        An instance of :class:`ReplyKeyboardMarkup`.
    """

    keyboard = [
        [
            KeyboardButton(text="🧑‍🤝‍🧑 Найти команду"),
        ],
        [
            KeyboardButton(text="⚡ Создать игру"),
        ],
        [
            KeyboardButton(text="💬 Узнать, как это работает"),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выбери действие…",
    )




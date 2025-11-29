"""
Keyboards for the \"Создать игру\" (create game) flow.
"""

from __future__ import annotations

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from oynaiq_bot.utils.navigator import SPORTS


def build_create_game_sport_keyboard() -> ReplyKeyboardMarkup:
    """
    Build a reply keyboard to choose sport when creating a match.

    Returns:
        :class:`ReplyKeyboardMarkup` with sport options.
    """

    keyboard = [
        [KeyboardButton(text=SPORTS["football"])],
        [KeyboardButton(text=SPORTS["basketball"])],
        [KeyboardButton(text=SPORTS["volleyball"])],
        [KeyboardButton(text=SPORTS["other"])],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выбери вид спорта…",
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    """
    Small helper to remove the custom reply keyboard.
    """

    return ReplyKeyboardRemove()




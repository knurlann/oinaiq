"""
Inline keyboard with a list of matches for a given sport.

Each match is represented as a separate button. The last row contains
an option to create a new match (stub in MVP).
"""

from __future__ import annotations

from typing import Iterable, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from oynaiq_bot.data.matches import Match
from oynaiq_bot.utils.formatter import format_match_list_item
from oynaiq_bot.utils.navigator import CreateMatchCallback, MatchCallback


def build_matches_list_keyboard(sport: str, matches: Iterable[Match]) -> InlineKeyboardMarkup:
    """
    Build an inline keyboard with all matches for the chosen sport.

    Args:
        sport: Internal sport code.
        matches: Iterable of :class:`Match` instances belonging to that sport.

    Returns:
        :class:`InlineKeyboardMarkup` instance with one button per match and
        an extra button "Создать свой матч".
    """

    inline_rows: List[List[InlineKeyboardButton]] = []

    for idx, match in enumerate(matches, start=1):
        inline_rows.append(
            [
                InlineKeyboardButton(
                    text=format_match_list_item(match, idx),
                    callback_data=MatchCallback(match_id=match.id).pack(),
                )
            ]
        )

    # Extra button for creating a custom match (stub)
    inline_rows.append(
        [
            InlineKeyboardButton(
                text="➕ Создать свой матч",
                callback_data=CreateMatchCallback(sport=sport).pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_rows)




"""
Handlers for the sport selection step in the \"Найти команду\" flow.
"""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery

from oynaiq_bot.data.matches import get_matches_by_sport
from oynaiq_bot.keyboards.matches_list import build_matches_list_keyboard
from oynaiq_bot.utils.formatter import format_matches_intro
from oynaiq_bot.utils.navigator import SportCallback


router = Router(name="find_team")


@router.callback_query(SportCallback.filter())
async def on_sport_chosen(callback: CallbackQuery, callback_data: SportCallback) -> None:
    """
    Handle sport selection from the inline keyboard.

    Shows a list of upcoming matches for the chosen sport.
    """

    sport = callback_data.sport
    matches = get_matches_by_sport(sport)

    if not matches:
        await callback.message.edit_text(
            format_matches_intro(sport)
            + "\n\nПока нет доступных матчей по этому виду спорта. "
            "Скоро здесь появятся новые игры!",
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        format_matches_intro(sport),
        reply_markup=build_matches_list_keyboard(sport=sport, matches=matches),
    )
    await callback.answer()




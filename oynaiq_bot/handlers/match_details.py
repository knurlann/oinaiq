"""
Handlers for the match details screen.
"""

from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from oynaiq_bot.data.matches import get_match_by_id, get_matches_by_sport
from oynaiq_bot.keyboards.match_details import build_match_details_keyboard
from oynaiq_bot.keyboards.matches_list import build_matches_list_keyboard
from oynaiq_bot.utils.formatter import format_match_details, format_matches_intro
from oynaiq_bot.utils.navigator import BookingCallback, MatchCallback


router = Router(name="match_details")


@router.callback_query(MatchCallback.filter())
async def show_match_details(callback: CallbackQuery, callback_data: MatchCallback) -> None:
    """
    Show detailed information for the selected match.

    Args:
        callback: Incoming callback query.
        callback_data: Decoded :class:`MatchCallback` payload.
    """

    match = get_match_by_id(callback_data.match_id)
    if not match:
        await callback.answer("Матч не найден. Возможно, он был удалён.", show_alert=True)
        return

    await callback.message.edit_text(
        format_match_details(match),
        reply_markup=build_match_details_keyboard(match),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(
    BookingCallback.filter(
        F.action.in_({"confirm", "contact", "waitlist", "notify", "back_list"})
    )
)
async def handle_match_details_actions(
    callback: CallbackQuery,
    callback_data: BookingCallback,
) -> None:
    """
    Handle non‑payment actions from the match details keyboard.

    Actions processed here:
        - ``confirm``: Confirm participation without deposit.
        - ``contact``: Provide organizer username.
        - ``waitlist`` / ``notify``: Stub subscription to notifications.
        - ``back_list``: Return to the list of matches for the same sport.
    """

    match = get_match_by_id(callback_data.match_id)
    if not match:
        await callback.answer("Матч не найден.", show_alert=True)
        return

    action = callback_data.action

    if action == "confirm":
        # Условно увеличиваем количество подтверждённых игроков
        if match.players_current < match.players_total:
            match.players_current += 1
        await callback.answer("Участие подтверждено ✅")
        await callback.message.answer(
            "Отлично! Мы записали тебя в список игроков.\n"
            "Не забудь прийти вовремя — хорошей игры! ⚽",
        )
        return

    if action == "contact":
        await callback.answer()
        await callback.message.answer(
            f"Написать организатору: @{match.organizer_username}\n"
            "Скоро здесь появится удобная кнопка для быстрого чата.",
        )
        return

    if action in {"waitlist", "notify"}:
        await callback.answer("Мы отправим уведомление, когда появятся места 🔔", show_alert=True)
        return

    if action == "back_list":
        matches = get_matches_by_sport(match.sport)
        await callback.message.edit_text(
            format_matches_intro(match.sport),
            reply_markup=build_matches_list_keyboard(match.sport, matches),
        )
        await callback.answer()
        return

    # For actions not handled here (e.g. \"deposit\") we simply acknowledge.
    await callback.answer()




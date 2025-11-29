"""
Handlers related to listing matches and simple stubs for creating games.
"""

from __future__ import annotations

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from oynaiq_bot.utils.navigator import CreateMatchCallback
from .start import CreateMatchForm


router = Router(name="matches")


@router.callback_query(CreateMatchCallback.filter())
async def on_create_match_from_list(
    callback: CallbackQuery,
    callback_data: CreateMatchCallback,
    state: FSMContext,
) -> None:
    """
    Start the \"Создать свой матч\" wizard directly from the matches list.

    Sport is already known from :class:`CreateMatchCallback`, so we skip
    the sport selection step and go straight to entering the title.
    """

    await state.update_data(sport=callback_data.sport)
    await state.set_state(CreateMatchForm.title)

    await callback.message.answer("Как назовём матч? Например: «Футбол 5×5»")
    await callback.answer()


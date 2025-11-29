"""
Navigation helpers and callback data definitions for OynaIQ.bot.

This module centralizes all callback_data schemas and sport metadata so that
keyboards and handlers can share the same navigation logic.
"""

from __future__ import annotations

from typing import Dict, Optional

from aiogram.filters.callback_data import CallbackData


# Mapping of internal sport codes to user-facing labels
SPORTS: Dict[str, str] = {
    "football": "⚽ Футбол",
    "basketball": "🏀 Баскетбол",
    "volleyball": "🏐 Волейбол",
    "other": "🎯 Другое",
}


class SportCallback(CallbackData, prefix="sport"):
    """
    Callback data for choosing a sport.

    Attributes:
        sport: Internal code of the sport (e.g. ``football``).
    """

    sport: str


class MatchCallback(CallbackData, prefix="match"):
    """
    Callback data for selecting a specific match.

    Attributes:
        match_id: Unique identifier of the match in mock data.
    """

    match_id: int


class BookingCallback(CallbackData, prefix="booking"):
    """
    Callback data for actions on the match details screen.

    Attributes:
        match_id: Identifier of the match.
        action: Action type (e.g. ``confirm``, ``deposit``, ``notify``, ``back``,
            ``contact``, ``waitlist``).
    """

    match_id: int
    action: str


class PaymentCallback(CallbackData, prefix="payment"):
    """
    Callback data used in the booking/payment confirmation flow.

    Attributes:
        match_id: Identifier of the match.
        action: Payment action (e.g. ``pay`` or ``cancel``).
    """

    match_id: int
    action: str


class CreateMatchCallback(CallbackData, prefix="create_match"):
    """
    Callback data for the "Создать свой матч" button.

    This is only a stub in the MVP and does not actually create matches.

    Attributes:
        sport: Internal sport code for which the match would be created.
    """

    sport: str


def get_sport_label(sport: str) -> str:
    """
    Return a human‑readable label for the sport.

    Args:
        sport: Internal sport code.

    Returns:
        Label from :data:`SPORTS` if present, otherwise the input value.
    """

    return SPORTS.get(sport, sport)






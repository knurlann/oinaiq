"""
Formatting helpers for OynaIQ.bot.

This module contains small, focused functions that build user-facing text
for match lists and match details screens.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from oynaiq_bot.data.matches import Match, MatchStatus
from oynaiq_bot.utils.navigator import SPORTS


INDEX_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def sport_emoji(sport: str) -> str:
    """
    Extract the emoji for the given internal sport code.

    Args:
        sport: Internal sport code (e.g. ``football``).

    Returns:
        Emoji representing the sport (e.g. ``⚽``).
    """

    label = SPORTS.get(sport, sport)
    # Expect labels like "⚽ Футбол"
    return label.split()[0] if label else sport


def format_match_list_item(match: Match, index: int) -> str:
    """
    Build a compact text for a single match row in the list keyboard,
    focusing on how many slots are left.

    Example:
        ``1️⃣ ⚽ Футбол 5×5 (осталось 2 мест)``

    Args:
        match: Match instance to format.
        index: Position of the match in the list (1-based).

    Returns:
        Human‑readable description string.
    """

    icon = INDEX_EMOJIS[index - 1] if 0 < index <= len(INDEX_EMOJIS) else "•"
    sport_label = SPORTS.get(match.sport, match.sport)

    free = max(match.players_total - match.players_current, 0)
    if free == 0:
        remaining_text = "мест нет"
    elif free == 1:
        remaining_text = "осталось 1 место"
    else:
        remaining_text = f"осталось {free} мест"

    return f"{icon} {sport_label} {match.title} ({remaining_text})"


def format_matches_intro(sport: str) -> str:
    """
    Format the intro text shown before the matches list.

    Args:
        sport: Internal sport code.

    Returns:
        Intro message ready to send to the user.
    """

    emoji = sport_emoji(sport)
    return f"Отлично! Вот ближайшие матчи по {emoji}"


def format_match_details(match: Match) -> str:
    """
    Format a detailed description of a match depending on its status.

    The function covers three variants required by the specification:
    active, almost full and low players.

    Args:
        match: Match instance to describe.

    Returns:
        Multi‑line message in Russian, ready to send as HTML.
    """

    if match.time_human:
        datetime_line = f"🕖 {match.date_human}, {match.time_human}\n"
    else:
        datetime_line = f"🕖 {match.date_human}\n"

    base_header = (
        f"{sport_emoji(match.sport)} {match.title} — {match.location}\n"
        f"{datetime_line}"
        f"📍 Локация: <a href=\"{match.google_maps_url}\">Открыть в Google Maps</a>\n\n"
    )

    players_line = f"👥 {match.players_current} из {match.players_total} мест занято"
    deposit_line = f"💸 Депозит: {match.deposit} ₸ (возвращается при явке)\n\n"
    meta_block = (
        f"Уровень: {match.level}\n"
        f"Организатор: @{match.organizer_username}\n"
        f"🔸 Правила: {match.rules}\n"
        f"🔸 {match.refund_policy}\n"
    )

    if match.status is MatchStatus.ALMOST_FULL:
        free = max(match.players_total - match.players_current, 0)
        return (
            base_header
            + f"🕑 Осталось {free} мест!\n"
            + f"👥 {match.players_current}/{match.players_total} подтверждено\n"
            + f"🔥 Игра уже {match.date_human} в {match.time_human}\n\n"
            + meta_block
        )

    if match.status is MatchStatus.LOW_PLAYERS:
        return (
            base_header
            + "Пока в команде мало игроков, но скоро соберём остальных 💪\n"
            + f"Сейчас в списке: {match.players_current} человек(а).\n"
            + "Хочешь уведомление, когда будет 6+ игроков?\n\n"
            + meta_block
        )

    # Default: ACTIVE
    return base_header + players_line + "\n" + deposit_line + meta_block


def debug_match_as_dict(match: Match) -> dict:
    """
    Convert a match to a serializable dictionary.

    This is used only for logging / debugging and not exposed to users.

    Args:
        match: Match instance.

    Returns:
        Dictionary representation of the match.
    """

    return asdict(match)




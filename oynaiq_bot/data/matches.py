"""
Mock match data for OynaIQ.bot.

This module defines a simple in‑memory list of matches that emulate
what will later be stored in a real database.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class MatchStatus(str, Enum):
    """
    Enumeration of supported match states.

    Attributes:
        ACTIVE: Match has enough players, still accepting.
        ALMOST_FULL: Only a few spots left.
        LOW_PLAYERS: Not enough players yet.
    """

    ACTIVE = "active"
    ALMOST_FULL = "almost_full"
    LOW_PLAYERS = "low_players"


@dataclass
class Match:
    """
    Data model representing a single sport match.

    Attributes:
        id: Unique identifier for internal navigation.
        sport: Internal sport code (e.g. ``football``).
        title: Short title such as ``Футбол 5×5``.
        location: Human‑readable location name.
        date_human: Human‑friendly date description (e.g. ``сегодня``).
        time_human: Human‑friendly time (e.g. ``19:00``).
        google_maps_url: Link to open the location in Google Maps.
        players_current: Number of already confirmed players.
        players_total: Maximum number of players allowed.
        deposit: Deposit in tenge.
        level: Skill level description.
        organizer_username: Telegram username of organizer (without @).
        rules: Description of match rules.
        refund_policy: Short explanation of refund policy.
        status: One of :class:`MatchStatus` values.
    """

    id: int
    sport: str
    title: str
    location: str
    date_human: str
    time_human: str
    google_maps_url: str
    players_current: int
    players_total: int
    deposit: int
    level: str
    organizer_username: str
    rules: str
    refund_policy: str
    status: MatchStatus


# Simple in‑memory list of sample matches
MOCK_MATCHES: List[Match] = [
    Match(
        id=1,
        sport="football",
        title="Футбол 5×5",
        location="Астана Арена",
        date_human="сегодня",
        time_human="19:00",
        google_maps_url="https://maps.app.goo.gl/7Tv5Yv8CpmNSdanY8",
        players_current=8,
        players_total=10,
        deposit=200,
        level="любители",
        organizer_username="ttttokzhn",
        rules="5×5, 2 тайма по 25 минут",
        refund_policy="Возврат депозита при отмене за 24+ ч",
        status=MatchStatus.ACTIVE,
    ),
    Match(
        id=2,
        sport="football",
        title="Футбол 5×5",
        location="Алау",
        date_human="завтра",
        time_human="18:30",
        google_maps_url="https://maps.app.goo.gl/CLXuEm5uT9CMvkcS8",
        players_current=8,
        players_total=10,
        deposit=200,
        level="любители",
        organizer_username="ttttokzhn",
        rules="5×5, 2 тайма по 20 минут",
        refund_policy="Возврат депозита при отмене за 24+ ч",
        status=MatchStatus.ALMOST_FULL,
    ),
    Match(
        id=3,
        sport="basketball",
        title="Баскетбол 3×3",
        location="Центральный Спортзал",
        date_human="послезавтра",
        time_human="20:00",
        google_maps_url="https://maps.app.goo.gl/sSsgJsmRwwF3Ujga8",
        players_current=2,
        players_total=6,
        deposit=0,
        level="новички/любители",
        organizer_username="ttttokzhn",
        rules="3×3, до 21 очка",
        refund_policy="Без депозита — просто приходи",
        status=MatchStatus.LOW_PLAYERS,
    ),
    Match(
        id=4,
        sport="volleyball",
        title="Волейбол 6×6",
        location="City Arena",
        date_human="в субботу",
        time_human="17:00",
        google_maps_url="https://maps.google.com/?q=City+Arena",
        players_current=10,
        players_total=12,
        deposit=150,
        level="любители",
        organizer_username="ttttokzhn",
        rules="6×6, 3 партии до 25 очков",
        refund_policy="Возврат депозита при отмене за 24+ ч",
        status=MatchStatus.ALMOST_FULL,
    ),
]


def get_matches_by_sport(sport: str) -> List[Match]:
    """
    Retrieve all matches for a particular sport.

    Args:
        sport: Internal sport code to filter by.

    Returns:
        List of :class:`Match` objects.
    """

    return [m for m in MOCK_MATCHES if m.sport == sport]


def get_match_by_id(match_id: int) -> Optional[Match]:
    """
    Find a match by its identifier.

    Args:
        match_id: Numeric match identifier.

    Returns:
        Match instance if found, otherwise ``None``.
    """

    return next((m for m in MOCK_MATCHES if m.id == match_id), None)




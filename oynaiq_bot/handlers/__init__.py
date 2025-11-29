"""
Handlers subpackage for OynaIQ.bot.

This module aggregates all routers so they can be easily included
in the main dispatcher.
"""

from __future__ import annotations

from aiogram import Router

from . import booking, find_team, match_details, matches, start, utils as handlers_utils


def get_routers() -> list[Router]:
    """
    Collect all routers used in the application.

    Returns:
        A list of configured `Router` instances.
    """

    return [
        start.router,
        find_team.router,
        matches.router,
        match_details.router,
        booking.router,
        handlers_utils.router,
    ]




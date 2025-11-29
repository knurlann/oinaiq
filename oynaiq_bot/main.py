"""
Main entry point for running OynaIQ.bot as a module.

You can also use the project‑root :mod:`main` which simply forwards to
this module.
"""

from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher

from oynaiq_bot.config import get_settings
from oynaiq_bot.handlers import get_routers


async def main() -> None:
    """
    Bootstrap and start the Telegram bot.

    This function:
        * loads settings from environment;
        * creates :class:`Bot` and :class:`Dispatcher` instances;
        * includes all routers;
        * starts long‑polling.
    """

    settings = get_settings()

    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    for router in get_routers():
        dp.include_router(router)

    await dp.start_polling(bot)


def run() -> None:
    """
    Convenience wrapper to run the bot using :func:`asyncio.run`.
    """

    asyncio.run(main())


if __name__ == "__main__":
    run()




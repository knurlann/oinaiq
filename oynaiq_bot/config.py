"""
Configuration module for OynaIQ.bot.

This module is responsible for loading environment variables and exposing
typed settings that can be reused across the project.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """
    Application settings loaded from environment variables.

    Attributes:
        bot_token: Telegram bot token obtained from BotFather.
    """

    bot_token: str


def get_settings() -> Settings:
    """
    Load settings from environment variables.

    Returns:
        An instance of `Settings` containing validated configuration.

    Raises:
        RuntimeError: If required environment variables are missing.
    """

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError(
            "BOT_TOKEN is not set. "
            "Create a .env file (see .env.example) and define BOT_TOKEN."
        )

    return Settings(bot_token=bot_token)




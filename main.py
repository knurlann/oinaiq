"""
Root entry point that runs OynaIQ.bot.

This file is kept extremely small and simply forwards execution
to :mod:`oynaiq_bot.main`, so that ``python main.py`` works from
the project root as requested.
"""

from __future__ import annotations

from oynaiq_bot.main import run


if __name__ == "__main__":
    run()


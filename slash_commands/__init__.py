"""Slash command package for Rahbot."""

from .leaderboard import leaderboard_slash
from .rank import rank_slash
from .warnings import warnings_slash
from .setup import setup_slash
from .getdiv import getdiv_slash
from .medicpicker import medicpicker_slash
from .getserver import getserver_slash

__all__ = [
    "leaderboard_slash",
    "rank_slash",
    "warnings_slash",
    "setup_slash",
    "getdiv_slash",
    "medicpicker_slash",
    "getserver_slash",
]

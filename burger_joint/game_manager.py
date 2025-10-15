
"""Manipulates game state, player data, etc.x"""

from utils import database
from model import Player 
import discord

players : list[Player] = []

"""Load player data from the database on startup"""
def on_startup() -> None:
    global players
    players = database.load_players_data()
    print(f"Loaded {len(players)} players from database")

"""Add a new player and initialize their data"""
def init_player(discord_user : discord.User) -> None:
    players.append(Player(
        user_id=discord_user.id,
        username=discord_user.name,
        shop_name=f"{discord_user.name}'s Burger Joint",
        balance=100,
        level=1,
        xp=0,
        burgers_sold=0,
        upgrades=[],
        employees=[],
        badges=[],
        prestige=0
    ))
    print(f"Initialized player data for {discord_user.name}")

    database.save_players_data(players)
   
def get_player(user_id : int) -> Player | None:
    for player in players:
        if player.user_id == user_id:
            return player
    return None
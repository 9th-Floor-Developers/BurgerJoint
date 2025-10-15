
"""Manipulates game state, player data, etc.x"""

from model import Player 
import discord

players : list[Player] = []

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

def get_player(user_id : int) -> Player | None:
    for player in players:
        if player.user_id == user_id:
            return player
    return None
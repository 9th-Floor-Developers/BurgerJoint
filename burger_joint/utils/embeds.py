"""Display various information as embeds."""

import discord
from discord import Embed

from burger_joint.model import Player


def get_status_embed(player: Player) -> Embed:
    """Returns an embed displaying the player's stats with emojis."""

    embed = discord.Embed(
        title=f"🍔 {player.shop_name} Status",
        description=
            f"🏆 Level: {player.level} | ✨ XP: {player.xp} | 💰 Balance: ${player.balance}"
        ,
        color=discord.Color.green()
    )
    
    embed.add_field(
	    name="💵 Burgers Sold",
	    value=str(player.burgers_sold)
    ).add_field(
	    name="🛠️ Upgrades",
	    value=str(len(player.upgrades))
    ).add_field(
	    name="👨‍🍳 Employees",
	    value=str(len(player.employees))
    ).set_footer(
	    text=f"⭐ Prestige Level: {player.prestige}"
    )
    
    return embed
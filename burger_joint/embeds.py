"""Display various information as embeds."""

import discord
from model import Player

def get_player_status_embed(player: Player) -> discord.Embed:
    """Returns an embed displaying the player's status with emojis."""

    embed = discord.Embed(
        title=f"🍔 {player.shop_name} Status",
        description=(
            f"🏆 Level: {player.level} | ✨ XP: {player.xp} | 💰 Balance: ${player.balance}"
        ),
        color=discord.Color.green()
    )
    embed.add_field(name="🍟 Burgers Sold", value=str(player.burgers_sold), inline=True)
    embed.add_field(name="🛠️ Upgrades", value=str(len(player.upgrades)), inline=True)
    embed.add_field(name="👨‍🍳 Employees", value=str(len(player.employees)), inline=True)
    embed.set_footer(text=f"⭐ Prestige Level: {player.prestige}")
    return embed
"""Display various information as embeds."""

import discord
from discord import Color, Embed, User

from burger_joint.model import Player


def simple_embed(
	title_text: str,
	description_text: str = None,
	embed_color: Color = Color.green()
) -> Embed:
	return Embed(
		title=title_text,
		description=description_text,
		color=embed_color
	)


def status_embed(player: Player) -> Embed:
	"""Returns an embed displaying the player's stats with emojis."""
	
	embed = Embed(
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


"""Bot initialization, event loop, command loader"""

import game_manager
import embeds
import discord


def setup(bot):
	@bot.event
	async def on_ready():
		print('Burger Joint Bot Online')
		
		for guild in bot.guilds:
			channel = guild.system_channel
			await channel.send('Burger Joint Bot Online')

	@bot.command(description="Display your joint's status.")
	async def status(ctx : discord.ApplicationContext): 
		if (game_manager.get_player(ctx.user.id) is None):
			game_manager.init_player(ctx.user)
		
		await ctx.respond("", embed=embeds.get_player_status_embed(game_manager.get_player(ctx.user.id)))
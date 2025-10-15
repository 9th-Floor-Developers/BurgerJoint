"""Bot initialization, event loop, command loader"""

import discord
from discord import Bot, Intents

import game_manager
from utils.embeds import get_status_embed

bot = Bot(intents=Intents.all())


def setup() -> Bot:
	return bot


@bot.event
async def on_ready():
	game_manager.on_startup()
	print('Burger Joint Bot Online')


# for guild in bot.guilds:
#	channel = guild.system_channel
#	await channel.send('Burger Joint Bot Online')

@bot.command(description="Display your joint's status.")
async def status(ctx: discord.ApplicationContext):
	if not game_manager.get_player(ctx.user.id):
		game_manager.init_player(ctx.user)
	
	await ctx.respond(
		embed=get_status_embed(
			game_manager.get_player(ctx.user.id)
		)
	)

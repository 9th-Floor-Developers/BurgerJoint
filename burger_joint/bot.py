"""Bot initialization, event loop, command loader"""

import discord
from discord import Bot, Intents

from burger_joint.cogs.player_commands import PlayerCommands
from burger_joint.model import Player
from burger_joint.utils import database
from utils.embeds import get_status_embed

bot = Bot(intents=Intents.all())
player_commands = PlayerCommands()
bot.add_cog(player_commands)


def setup() -> Bot:
	return bot


@bot.event
async def on_ready():
	print('Burger Joint Bot Online')


# for guild in bot.guilds:
#	channel = guild.system_channel
#	await channel.send('Burger Joint Bot Online')

@bot.slash_command(description="Display your joint's status.")
async def status(ctx: discord.ApplicationContext):
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		player = player_commands.create_new_player(ctx.author)
	
	await ctx.respond(embed=get_status_embed(player))

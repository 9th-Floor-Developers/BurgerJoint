"""Bot initialization, event loop, command loader"""

import discord
from discord import ApplicationContext, Bot, Intents

from burger_joint.model import Player
from burger_joint.utils import database
from utils import embeds

bot = Bot(intents=Intents.all())


def setup() -> Bot:
	return bot


@bot.event
async def on_ready():
	print('Burger Joint Bot Online')


# for guild in bot.guilds:
#	channel = guild.system_channel
#	await channel.send('Burger Joint Bot Online')

@bot.slash_command(description='')
async def start(ctx: ApplicationContext):
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		database.create_new_player(ctx.author)
		await ctx.respond(
			embed=embeds.simple_embed(
				'✅ You have successfully established your very own burger joint!'
			)
		)
	else:
		await ctx.respond(
			embed=embeds.simple_embed(
				f'🍔 {player.username} already owns a burger joint called "{player.shop_name}".',
				embed_color=discord.Color.yellow()
			)
		)


@bot.slash_command(description="Display your joint's status.")
async def status(ctx: ApplicationContext):
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		await ctx.respond(
			embed=embeds.simple_embed(
				'❌ You do not own a burger joint!',
				'Use the `/start` command to start your very own burger joint!',
				discord.Color.red()
			)
		)
		return
	
	await ctx.respond(embed=embeds.status_embed(player))


@bot.slash_command(description='Rename your burger joint.')
async def rename(ctx: ApplicationContext, new_name: str):
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		await ctx.respond(
			embed=embeds.simple_embed(
				'❌ You do not own a burger joint!',
				'Use the `/start` command to start your very own burger joint!',
				discord.Color.red()
			)
		)
		return
	
	player.shop_name = new_name
	database.save_data(player)
	await ctx.respond(
		embed=embeds.simple_embed(
			f'✅ Changed burger joint name to: {player.shop_name}!'
		)
	)

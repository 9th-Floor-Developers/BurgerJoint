import asyncio
import os
from pathlib import Path
from typing import Any

import discord
from discord import ApplicationContext, Bot, ButtonStyle, Color, Embed, File, \
	Guild, Intents, Message, TextChannel

from burger_joint.model import BadgeID, Player
from burger_joint.utils import ChoiceButtons, database
from model import ALL_BADGES
from utils import embeds
from utils.decorators import player_check
from utils.embeds import simple_embed

bot = Bot(intents=Intents.all())
all_guilds: dict[int, dict[str, Any]] = {}


def setup() -> Bot:
	all_cogs = [
		'leaderboards',
		'work_commands',
		'upgrades',
		'minigames',
		'menu_commands',
	]
	for cog in all_cogs:
		bot.load_extension(f'cogs.{cog}')
	return bot


@bot.event
async def on_ready() -> None:
	print('Burger Joint Bot Online')


# uncomment in final version
# for guild in bot.guilds:
# 	all_guilds[guild.id] = {
# 		'last_clicked': True,
# 		'spawn_channel': guild.system_channel.id
# 	}
# 	asyncio.create_task(spawn_upgrade_loop(guild))

@bot.event
async def on_message(message: Message) -> None:
	if message.author.bot:
		return
	
	if not message.content.startswith('$secret'):
		return
	
	player: Player | None = database.get_player(message.author.id)
	
	if not player:
		await message.reply(
			embed=embeds.simple_embed(
				f'{message.author.mention} '
				f'❌ You do not own a burger joint!',
				'Use the `/start` command to '
				'start your very own burger joint!',
				Color.red()
			)
		)
		return
	
	await player.unlock_badge(BadgeID.SECRET, message.channel)
	
	database.save_data(player)

@bot.event
async def on_guild_join(guild: Guild):
	await guild.system_channel.send(embed=Embed(
		title="Welcome to burger joint ",
		description="Utilize commands to run your very own burger joint \n Type `/start` to begin your journey",
		color=discord.Color.green()
	))


@bot.slash_command(description='')
async def set_spawn_channel(
	ctx: ApplicationContext,
	channel: TextChannel
) -> None:
	all_guilds[channel.guild.id]['spawn_channel'] = channel.id
	await ctx.respond(f'Item spawn channel changed to: {channel.name}')


async def spawn_upgrade_loop(guild: Guild) -> None:
	while True:
		guild_status: dict[str, Any] | None = all_guilds[guild.id]
		if not guild_status or not guild_status['last_clicked']:
			break
		
		await spawn_upgrade_message(
			guild.get_channel(guild_status['spawn_channel']), guild_status
		)
		await asyncio.sleep(10)
	
	all_guilds.pop(guild.id, None)


async def spawn_upgrade_message(
	channel: TextChannel,
	guild_status: dict[str, Any]
) -> None:
	guild_status['last_clicked'] = False
	
	buttons = ChoiceButtons(
		{'🎁 Claim!': ButtonStyle.green},
		player=None,
		timeout=None
	)
	
	base_dir = Path(__file__).resolve().parent
	data_path = os.path.join(base_dir, 'assets', 'images', 'burger.png')
	
	message: Message = await channel.send(file=File(data_path), view=buttons)
	await buttons.wait()
	
	player: Player | None = database.get_player(buttons.player_clicked.id)
	if not player:
		await channel.send(
			embed=embeds.simple_embed(
				f'{buttons.player_clicked.mention} '
				f'❌ You do not own a burger joint!',
				'Use the `/start` command to '
				'start your very own burger joint!',
				Color.red()
			)
		)
		return
	
	await message.edit(
		content=f'{player.username} claimed this spawn!', view=None
	)
	guild_status['last_clicked'] = True
	
	player.balance += 1000
	database.save_data(player)


@bot.slash_command(description='')
async def start(ctx: ApplicationContext) -> None:
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		database.create_new_player(ctx.author)
		await ctx.respond(
			embed=embeds.simple_embed(
				description_text='✅ You have successfully established '
				                 'your very own burger joint!'
			).add_field(name='basic commands',
			   value='`/status` in order to check how your joint is doing \n'
			   '`/work` earn some money \n'
			   '`/upgrade` see your joint\'s upgrades and buy new ones')
		)
	else:
		await ctx.respond(
			embed=embeds.simple_embed(
				description_text=f'🍔 {player.username} already owns '
				                 f'a burger joint called "{player.shop_name}".',
				embed_color=discord.Color.yellow()
			)
		)


def status_embed(player: Player) -> Embed:
	"""Returns an embed displaying the player's stats with emojis."""
	
	embed = Embed(
		title=f'🍔 {player.shop_name} Status:',
		description=
		f'🏆 Level: {player.level} | ✨ XP: {player.xp} '
		f'| 💰 Balance: ${player.balance}',
		color=discord.Color.green()
	)
	
	embed.add_field(
		name='💵 Burgers Sold',
		value=str(player.burgers_sold)
	).add_field(
		name='🛠️ Upgrades',
		value=str(len(player.upgrades))
	).add_field(
		name='👨‍🍳 Employees',
		value=str(len(player.employees))
	).set_footer(
		text=f'⭐ Prestige Level: {player.prestige}'
	)
	
	return embed


@bot.slash_command(description='Display your joint\'s status.')
@player_check
async def status(ctx: ApplicationContext) -> None:
	await ctx.respond(embed=status_embed(ctx.player))  # type: ignore


@bot.slash_command(description='Rename your burger joint.')
@player_check
async def rename(ctx: ApplicationContext, new_name: str) -> None:
	player: Player = ctx.player  # type: ignore
	
	if player.shop_name == new_name:
		await ctx.respond(
			embed=embeds.simple_embed(
				description_text=f'{new_name} is already the name '
				                 f'of {ctx.author}\'s burger joint.'
			)
		)
		return
	
	player.shop_name = new_name
	await ctx.respond(
		embed=embeds.simple_embed(
			description_text=f'✅ Changed burger joint '
			                 f'name to: "{player.shop_name}"!'
		)
	)
	await player.unlock_badge(BadgeID.RENAME_JOINT, ctx.channel)


def badges_embed(player: Player) -> Embed:
	embed: Embed = simple_embed(f'{player.shop_name}\'s Badges:')
	
	for badge_id in ALL_BADGES:
		badge_obj = ALL_BADGES[badge_id]
		
		if player.has_badge(badge_id):
			embed.add_field(
				name=f'✅ {badge_obj.name}',
				value=f'~~Reward: {badge_obj.reward}~~',
				inline=False
			)
		else:
			embed.add_field(
				name=f'🔒 {badge_obj.name}',
				value=f'Reward: ${badge_obj.reward}',
				inline=False
			)
	
	embed.set_footer(
		text=f'Total Progress: {len(player.badges) // len(ALL_BADGES)}%'
	)
	
	return embed


@bot.slash_command(description='')
@player_check
async def badges(ctx: ApplicationContext) -> None:
	await ctx.respond(embed=badges_embed(ctx.player))  # type: ignore

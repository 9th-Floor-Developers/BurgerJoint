"""Bot initialization, event loop, command loader"""

import discord
from discord import ApplicationContext, Bot, Embed, Intents

from burger_joint.model import BadgeID, Player
from burger_joint.utils import database
from model import ALL_BADGES
from utils import embeds
from utils.decorators import player_check
from utils.embeds import simple_embed

bot = Bot(intents=Intents.all())


def setup() -> Bot:
	all_cogs = [
		'leaderboards',
		'work_commands',
		'minigames',
		'menu_commands',
	]
	for cog in all_cogs:
		bot.load_extension(f'cogs.{cog}')
	return bot


@bot.event
async def on_ready():
	print('Burger Joint Bot Online')


@bot.slash_command(description='')
async def start(ctx: ApplicationContext):
	player: Player | None = database.get_player(ctx.author.id)
	if not player:
		database.create_new_player(ctx.author)
		await ctx.respond(
			embed=embeds.simple_embed(
				description_text='✅ You have successfully established '
				                 'your very own burger joint!'
			)
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
		title=f"🍔 {player.shop_name} Status:",
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

@bot.slash_command(description="Display your joint's status.")
@player_check
async def status(ctx: ApplicationContext):
	await ctx.respond(embed=status_embed(ctx.player))  # type: ignore


@bot.slash_command(description='Rename your burger joint.')
@player_check
async def rename(ctx: ApplicationContext, new_name: str):
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
			description_text=f'✅ Changed burger joint name to: "{player.shop_name}"!'
		)
	)
	await player.unlock_badge(BadgeID.RENAME_JOINT, ctx)


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
async def badges(ctx: ApplicationContext):
	await ctx.respond(embed=badges_embed(ctx.player))  # type: ignore

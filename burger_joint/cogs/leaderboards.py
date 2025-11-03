from discord import ApplicationContext, Bot, Cog, Color, Embed, \
	SlashCommandGroup

from burger_joint.model.enums import LeaderboardID
from burger_joint.model.player import Player
from burger_joint.utils.decorators import leaderboard_command


class Leaderboards(Cog):
	_leaderboards = SlashCommandGroup(
		'leaderboard', 'Display Various Leaderboards'
	)
	
	@_leaderboards.command(description='Displays the Balance Leaderboard')
	@leaderboard_command('balance', LeaderboardID.BALANCE)
	async def balance(self, ctx: ApplicationContext) -> None:
		...
	
	@_leaderboards.command(description='Displays the XP Leaderboard')
	@leaderboard_command('xp', LeaderboardID.XP)
	async def xp(self, ctx: ApplicationContext) -> None:
		...
	
	@_leaderboards.command(description='Displays the Burgers Sold Leaderboard')
	@leaderboard_command('burgers_sold', LeaderboardID.BURGERS_SOLD)
	async def burgers(self, ctx: ApplicationContext) -> None:
		...
	
	@_leaderboards.command(description='Displays the Prestige Leaderboard')
	@leaderboard_command('prestige', LeaderboardID.PRESTIGE)
	async def prestige(self, ctx: ApplicationContext) -> None:
		...


def leaderboard_embed(
	players: list[Player],
	leaderboard_type: LeaderboardID
) -> Embed:
	embed = Embed(
		title=f'🍔 {leaderboard_type.value[0]} Leaderboard 🍔',
		color=Color.purple()
	)
	
	for i, player in enumerate(players):
		embed.add_field(
			name=f'{i + 1}. {player.shop_name} - '
			     f'{getattr(player, leaderboard_type.value[1])} '
			     f'{leaderboard_type.value[0]}',
			value='',
			inline=False
		)
	
	return embed


def setup(bot: Bot) -> None:
	bot.add_cog(Leaderboards())

import functools

from discord import ApplicationContext, Bot, Cog, SlashCommandGroup

from burger_joint.model import Player
from burger_joint.utils import database, embeds
from burger_joint.utils.enums import LeaderboardID


class Leaderboards(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@staticmethod
	def leaderboard_command(attr: str, leaderboard_id: LeaderboardID):
		def decorator(func):
			@functools.wraps(func)
			async def wrapper(self, ctx: ApplicationContext, *args, **kwargs):
				players: list[Player] = database.get_all_players()
				players.sort(key=lambda p: getattr(p, attr), reverse=True)
				await ctx.respond(
					embed=embeds.leaderboard_embed(players, leaderboard_id)
				)
			
			return wrapper
		
		return decorator
	
	_leaderboards = SlashCommandGroup(
		'leaderboard', 'Display Various Leaderboards'
	)
	
	@_leaderboards.command(description='Displays the Balance Leaderboard')
	@leaderboard_command('balance', LeaderboardID.BALANCE)
	async def balance(self, ctx: ApplicationContext):
		pass
	
	@_leaderboards.command(description='Displays the XP Leaderboard')
	@leaderboard_command('xp', LeaderboardID.XP)
	async def xp(self, ctx: ApplicationContext):
		pass
	
	@_leaderboards.command(description='Displays the Burgers Sold Leaderboard')
	@leaderboard_command('burgers_sold', LeaderboardID.BURGERS_SOLD)
	async def burgers(self, ctx: ApplicationContext):
		pass
	
	@_leaderboards.command(description='Displays the Prestige Leaderboard')
	@leaderboard_command('prestige', LeaderboardID.PRESTIGE)
	async def prestige(self, ctx: ApplicationContext):
		pass


def setup(bot: Bot):
	bot.add_cog(Leaderboards(bot))

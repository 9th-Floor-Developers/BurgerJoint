from discord import ApplicationContext, Bot, Cog, SlashCommandGroup

from burger_joint.model.enums import LeaderboardID
from utils.decorators import leaderboard_command


class Leaderboards(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	_leaderboards = SlashCommandGroup(
		'leaderboard', 'Display Various Leaderboards'
	)
	
	@_leaderboards.command(description='Displays the Balance Leaderboard')
	@leaderboard_command('balance', LeaderboardID.BALANCE)
	async def balance(self, ctx: ApplicationContext):
		...
	
	@_leaderboards.command(description='Displays the XP Leaderboard')
	@leaderboard_command('xp', LeaderboardID.XP)
	async def xp(self, ctx: ApplicationContext):
		...
	
	@_leaderboards.command(description='Displays the Burgers Sold Leaderboard')
	@leaderboard_command('burgers_sold', LeaderboardID.BURGERS_SOLD)
	async def burgers(self, ctx: ApplicationContext):
		...
	
	@_leaderboards.command(description='Displays the Prestige Leaderboard')
	@leaderboard_command('prestige', LeaderboardID.PRESTIGE)
	async def prestige(self, ctx: ApplicationContext):
		...


def setup(bot: Bot):
	bot.add_cog(Leaderboards(bot))

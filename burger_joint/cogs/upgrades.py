import random

from discord import ApplicationContext, Bot, Cog, Color, Option, slash_command

from burger_joint.bot import player_check
from burger_joint.cogs.mini_games.blackjack import BlackJack
from burger_joint.model.player import Player
from burger_joint.utils import embeds
from burger_joint.utils.decorators import cost_check


class UpgradesCommands(Cog):
	@slash_command(description='View your upgrades')
	@player_check
	async def upgrades(self, ctx: ApplicationContext):
		pass
		


def setup(bot: Bot):
	bot.add_cog(UpgradesCommands(bot))


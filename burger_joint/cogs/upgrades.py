import random

from discord import ApplicationContext, Bot, Cog, Color, Embed, Option, slash_command

from burger_joint.bot import player_check
from burger_joint.cogs.mini_games.blackjack import BlackJack
from burger_joint.model import Player, ALL_UPGRADES, Upgrade, Employee
from burger_joint.utils import embeds
from burger_joint.utils.decorators import cost_check


class UpgradesCommands(Cog):
	@slash_command(description='View your upgrades')
	@player_check
	async def upgrades(self, ctx: ApplicationContext):
		self.player: Player = ctx.player

		embed = Embed(
			title='Player upgrades 🛠️',
			color=Color.green()
		)

		for upgradeID in self.player.upgrades:
			upgrade: Upgrade = ALL_UPGRADES[upgradeID]
			if (upgrade.level > 0):
				description: str = f"Level: {upgrade.level} \n {upgrade.description}" if upgrade is Employee else f"Number: {upgrade.level} \n {upgrade.description}"

				embed.add_field(
					name=upgrade.name,
					value=description,
					inline=False
				)

		await ctx.respond(embed=embed)
		


def setup(bot: Bot):
	bot.add_cog(UpgradesCommands(bot))


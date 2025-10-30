from discord import ApplicationContext, Bot, Cog, Color, Embed, slash_command

from burger_joint.bot import player_check
from burger_joint.model import Employee, Player


class UpgradesCommands(Cog):
	def __init__(self):
		self.player: Player | None = None
	
	@slash_command(description='View your upgrades')
	@player_check
	async def upgrades(self, ctx: ApplicationContext):
		self.player: Player = ctx.player  # type: ignore
		
		embed = Embed(
			title='Player upgrades 🛠️',
			color=Color.green()
		)
		
		for upgrade in self.player.upgrades:
			if not upgrade.level:
				continue
			
			description: str = f'Level: {upgrade.level}`\n{upgrade.description}' \
				if upgrade is Employee \
				else f'Number: {upgrade.level}\n{upgrade.description}'
			
			embed.add_field(
				name=upgrade.name,
				value=description,
				inline=False
			)
		
		await ctx.respond(embed=embed)


def setup(bot: Bot):
	bot.add_cog(UpgradesCommands())

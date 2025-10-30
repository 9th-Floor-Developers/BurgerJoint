from discord import ApplicationContext, Bot, Cog, Color, Embed, slash_command
import discord

from burger_joint.utils import database, player_check, cost_check
from burger_joint.model import Employee, Player, ALL_UPGRADES, UpgradeID
from burger_joint.utils.inputs import PerPersonView


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
		
		await ctx.respond(embed=embed, view=UpgradesView(player=self.player, ctx=ctx))

class UpgradesView(PerPersonView):
	@discord.ui.button(
		label='Buy upgrades',
		style=discord.ButtonStyle.success  # type: ignore
	)
	async def add_item_button_callback(self, _, interaction):
		await interaction.respond(
			view=SelectUpgrades(player=self.player, ctx=self.ctx)
		)

class SelectUpgrades(PerPersonView):
	def __init__(self, ctx: ApplicationContext, player: Player = None):
		super().__init__(player)
		self.ctx = ctx

		options = []
		for index, data in enumerate(player.upgrades):
			options.append(
				discord.SelectOption(
					value=str(index),
					label=data.name,
					description=f'Cost: {data.cost}'
				)
			)

		if not options:
			return
		
		select = discord.ui.Select(
			placeholder='Choose an upgrade!',
			min_values=1,
			max_values=1,
			options=options
		)

		async def _select_callback(interaction):
			index: int = int(select.values[0])
			await self.buy_upgrade(self.ctx, index, cost=self.player.upgrades[index].cost)
			await interaction.response.defer()

		select.callback = _select_callback
		self.add_item(select)

	@cost_check(extra=True)
	async def buy_upgrade(self, ctx: discord.ApplicationContext, index: int, cost: int):
		self.player.balance -= cost
		self.player.upgrades[index].upgrade()

		database.save_data(self.player)
		
		await ctx.respond(embed=Embed(
			title=f"{self.player.upgrades[index].name} Bought", 
			description="This addition will help your joint grow", 
			color=discord.Color.green()))





def setup(bot: Bot):
	bot.add_cog(UpgradesCommands())

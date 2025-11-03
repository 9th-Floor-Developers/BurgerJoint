from discord import ApplicationContext, Bot, ButtonStyle, Cog, Color, Embed, \
	Interaction, SelectOption, slash_command, ui

from burger_joint.model import Employee, Player
from burger_joint.utils import cost_check, database, player_check
from burger_joint.utils.inputs import PerPersonView


class UpgradesCommands(Cog):
	def __init__(self) -> None:
		self.player: Player | None = None
	
	@slash_command(description='View your upgrades')
	@player_check
	async def upgrades(self, ctx: ApplicationContext) -> None:
		self.player: Player = ctx.player  # type: ignore
		embed = Embed(
			title='Player Upgrades 🛠️',
			color=Color.green()
		)
		
		for upgrade in self.player.upgrades:
			if not upgrade.level:
				continue
			
			description: str = \
				f'Level: {upgrade.level}`\n{upgrade.description}' \
					if upgrade is Employee \
					else f'Number: {upgrade.level}\n{upgrade.description}'
			
			embed.add_field(
				name=upgrade.name,
				value=description,
				inline=False
			)
		
		await ctx.respond(
			embed=embed, view=UpgradesView(player=self.player, ctx=ctx)
		)


class UpgradesView(PerPersonView):
	@ui.button(
		label='Buy upgrades',
		style=ButtonStyle.success  # type: ignore
	)
	async def add_item_button_callback(
		self,
		_,
		interaction: Interaction
	) -> None:
		await interaction.respond(
			view=SelectUpgrades(player=self.player, ctx=self.ctx)
		)


class SelectUpgrades(PerPersonView):
	def __init__(self, ctx: ApplicationContext, player: Player = None) -> None:
		super().__init__(player)
		
		self.ctx = ctx
		options: list[SelectOption] = []
		
		for i, data in enumerate(player.upgrades):
			options.append(
				SelectOption(
					value=str(i),
					label=data.name,
					description=f'Cost: {data.cost}'
				)
			)
		
		if not options:
			return
		
		select = ui.Select(
			placeholder='Choose an upgrade!',
			options=options
		)
		
		async def _select_callback(interaction) -> None:
			index: int = int(select.values[0])
			await self.buy_upgrade(
				self.ctx, index, cost=self.player.upgrades[index].cost
			)
			await interaction.response.defer()
		
		select.callback = _select_callback
		self.add_item(select)
	
	@cost_check(extra=True)
	async def buy_upgrade(
		self,
		ctx: ApplicationContext,
		index: int,
		cost: int
	) -> None:
		self.player.balance -= cost
		self.player.upgrades[index].upgrade()
		
		database.save_data(self.player)
		
		await ctx.respond(
			embed=Embed(
				title=f'{self.player.upgrades[index].name} Bought',
				description='This addition will help your joint grow',
				color=Color.green()
			)
		)


def setup(bot: Bot) -> None:
	bot.add_cog(UpgradesCommands())

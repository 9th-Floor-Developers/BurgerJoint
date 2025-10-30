import discord
from discord import ApplicationContext, Bot, Cog, Color, Embed, slash_command

from burger_joint.bot import player_check
from burger_joint.model import ALL_FOOD_ITEMS, FoodCategoryID, FoodItemID, \
	Player
from burger_joint.utils import database, EditingMenuItemModal, embeds, \
	PerPersonView, SettingAddedMenuItemModal


class MenuCommands(Cog):
	@slash_command(description='View and edit you joint\'s menu')
	@player_check
	async def menu(self, ctx: ApplicationContext):
		await ctx.respond(
			embed=menu_embed(ctx.player),  # type: ignore
			view=MenuView(player=ctx.player)  # type: ignore
		)


def menu_embed(player: Player) -> Embed:
	embed = Embed(
		title=f'🍔 {player.shop_name} Menu:', color=Color.lighter_grey()
	)
	
	menu_item_categories: set[FoodCategoryID] = {
		ALL_FOOD_ITEMS[item.food_item_ID].category
		for item in player.menu_items
	}
	
	for category in menu_item_categories:
		items_text = '\n'.join(
			f'{item.name} — ${item.price}'
			for item in player.menu_items
			if ALL_FOOD_ITEMS[item.food_item_ID].category == category
		)
		
		embed.add_field(name=category.value, value=items_text, inline=False)
	
	return embed


class MenuView(PerPersonView):
	@discord.ui.button(
		label='Add Item',
		style=discord.ButtonStyle.success  # type: ignore
	)
	async def add_item_button_callback(self, _, interaction):
		await interaction.response.send_message(
			view=SelectAllFoodItemView(player=self.player)
		)
	
	@discord.ui.button(
		label='Remove Item',
		style=discord.ButtonStyle.red  # type: ignore
	)
	async def remove_item_button_callback(self, _, interaction):
		await interaction.response.send_message(
			view=SelectPlayerFoodItemView(player=self.player, mode='remove')
		)
	
	@discord.ui.button(
		label='Edit Item',
		style=discord.ButtonStyle.primary  # type: ignore
	)
	async def edit_item_button_callback(self, _, interaction):
		await interaction.response.send_message(
			view=SelectPlayerFoodItemView(player=self.player, mode='edit')
		)


class SelectAllFoodItemView(PerPersonView):
	@discord.ui.select(
		placeholder='Choose a food!',
		min_values=1,
		max_values=1,
		options=[
			discord.SelectOption(
				value=ID.value,
				label=data.name,
				description='Pick this if you like '
				            f'to put a {data.name} in your menu!'
			)
			for ID, data in ALL_FOOD_ITEMS.items()
		]
	)
	async def select_callback(self, select, interaction):
		await interaction.response.send_modal(
			SettingAddedMenuItemModal(
				self.player, FoodItemID(select.values[0])
			)
		)


class SelectPlayerFoodItemView(PerPersonView):
	def __init__(self, mode: str, player: Player =None):
		super().__init__(player)
		self.mode = mode
		
		options = []
		for index, menu_item in enumerate(self.player.menu_items):
			options.append(
				discord.SelectOption(
					value=str(index),
					label=menu_item.name,
					description=f'Edit the {menu_item.name} in your menu'
				)
			)
		
		if not options:
			return
		
		select = discord.ui.Select(
			placeholder='Choose a food!',
			min_values=1,
			max_values=1,
			options=options
		)
		
		async def _select_callback(interaction):
			if mode == 'edit':
				await interaction.response.send_modal(
					EditingMenuItemModal(self.player, int(select.values[0]))
				)
			elif mode == 'remove':
				await interaction.respond(
					embed=embeds.simple_embed(
						description_text=f'Removing item from menu'
					),
				)
				self.player.menu_items.pop(int(select.values[0]))
				database.save_data(self.player)
		
		select.callback = _select_callback
		self.add_item(select)


def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))

from discord import ApplicationContext, Bot, ButtonStyle, Cog, SelectOption, \
	slash_command
from discord.ui import button, select, View

from burger_joint.bot import player_check
from utils import embeds
from utils.constants import ALL_FOOD_ITEMS


class MenuCommands(Cog):
	@slash_command(description="View and edit you joint's menu")
	@player_check
	async def menu(self, ctx: ApplicationContext):
		await ctx.respond(
			embed=embeds.menu_embed(ctx.player),  # type: ignore
			view=MenuView()
		)


class MenuView(View):
	@button(
		label="Add Item", style=ButtonStyle.success  # type: ignore
	)
	async def add_item_button_callback(self, _, interaction):
		await interaction.response.send_message(view=SelectFoodItemView())
	
	@button(label="Remove Item", style=ButtonStyle.red)  # type: ignore
	async def remove_item_button_callback(self, _, interaction):
		await interaction.response.send_message("You clicked the button2!")
	
	@button(
		label="Edit Item", style=ButtonStyle.primary  # type: ignore
	)
	async def edit_item_button_callback(self, _, interaction):
		await interaction.response.send_message("You clicked the button3!")


class SelectFoodItemView(View):
	@select(
		placeholder="Choose a Flavor!",
		min_values=1,
		max_values=1,
		options=[
			SelectOption(
				label=food_item.name,
				description=f"Pick this if you like {food_item.name}!"
			)
			for food_item in ALL_FOOD_ITEMS
		]
	)
	async def select_callback(
		self,
		select,
		interaction
	):  # the function called when the user is done selecting options
		await interaction.response.send_message(
			f"Awesome! I like {select.values[0]} too!"
		)


def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))

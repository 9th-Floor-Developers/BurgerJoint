from discord import ApplicationContext, Bot, Cog, slash_command
import discord
import discord
from discord import ApplicationContext, Bot, Cog, Color, Embed, slash_command

from burger_joint.bot import player_check
from burger_joint.model import Player
from burger_joint.utils import ALL_FOOD_ITEMS, FoodCategoryID


class MenuCommands(Cog):
	@slash_command(description="View and edit you joint's menu")
	@player_check
	async def menu(self, ctx: ApplicationContext):
		await ctx.respond(embed=menu_embed(ctx.player), view=MenuView())


def menu_embed(player: Player) -> Embed:
	embed = Embed(
		title=f"🍔 {player.shop_name} Menu:", color=Color.lighter_grey()
	)
	
	menu_item_categories: set[FoodCategoryID] = {
		ALL_FOOD_ITEMS[item.food_item_ID].category for item in
		player.menu_items}
	
	for category in menu_item_categories:
		items_text = "\n".join(
			f"{item.name} — ${item.price}"
				for item in player.menu_items if
				ALL_FOOD_ITEMS[item.food_item_ID].category == category
		)
		
		embed.add_field(name=category.value, value=items_text, inline=False)
	
	return embed


class MenuView(discord.ui.View):
	@discord.ui.button(label="Add Item", style=discord.ButtonStyle.success)
	async def add_item_button_callback(self, button, interaction):
		await interaction.response.send_message(view=SelectFoodItemView())
	
	@discord.ui.button(label="Remove Item", style=discord.ButtonStyle.red)
	async def remove_item_button_callback(self, button, interaction):
		await interaction.response.send_message("You clicked the button2!")
	
	@discord.ui.button(label="Edit Item", style=discord.ButtonStyle.primary)
	async def edit_item_button_callback(self, button, interaction):
		await interaction.response.send_message("You clicked the button3!")


class SelectFoodItemView(discord.ui.View):
	@discord.ui.select(
		placeholder="Choose a Flavor!",
		min_values=1,
		max_values=1,
		options=[
			discord.SelectOption(
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

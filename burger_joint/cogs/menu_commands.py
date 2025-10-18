import random
from discord import ApplicationContext, Bot, Cog, slash_command, SlashCommandGroup
import discord
from discord.ext import tasks
from burger_joint.bot import player_check
from burger_joint.utils import FoodItemID, FoodCategoryID, database, ALL_FOOD_ITEMS
from burger_joint.model import FoodItem, MenuItem, Player
from discord import Embed, Message, Color

class MenuCommands(Cog):
	@slash_command(description="View and edit you joint's menu")
	@player_check
	async def menu(self, ctx: ApplicationContext):
		await ctx.respond(
			embed=embeds.menu_embed(ctx.player), view=MenuView()
			# type: ignore
		)


    for category in menu_item_categories:
        items_text = "\n".join(
            f"{item.name} — ${item.price}"
            for item in player.menu_items if ALL_FOOD_ITEMS[item.food_item_ID].category == category
        )

        embed.add_field(name=category.value, value=items_text, inline=False)

    return embed
          
class MenuView(discord.ui.View):
    @discord.ui.button(label="Add Item", style=discord.ButtonStyle.success) 
    async def add_item_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button1!")

    @discord.ui.button(label="Remove Item", style=discord.ButtonStyle.red) 
    async def remove_item_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button2!")

    @discord.ui.button(label="Edit Item", style=discord.ButtonStyle.primary) 
    async def edit_item_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button3!")


def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))

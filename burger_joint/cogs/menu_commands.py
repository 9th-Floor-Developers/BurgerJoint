import random
from discord import ApplicationContext, Bot, Cog, slash_command, SlashCommandGroup
import discord
from discord.ext import tasks
from burger_joint.bot import player_check
from burger_joint.utils import FoodItemID, FoodCategoryID, database, ALL_FOOD_ITEMS, SettingAddedMenuItemModal
from burger_joint.model import FoodItem, MenuItem, Player
from discord import Embed, Message, Color

class MenuCommands(Cog):
    @slash_command(description="View and edit you joint's menu")
    @player_check
    async def menu(self, ctx: ApplicationContext):
        await ctx.respond(embed=menu_embed(ctx.player), view=MenuView(player=ctx.player))

def menu_embed(player : Player) -> Embed:
    embed = Embed(title=f"🍔 {player.shop_name} Menu:", color=Color.lighter_grey())

    menu_item_categories : set[FoodCategoryID] = {ALL_FOOD_ITEMS[item.food_item_ID].category for item in player.menu_items}


    for category in menu_item_categories:
        items_text = "\n".join(
            f"{item.name} — ${item.price}"
            for item in player.menu_items if ALL_FOOD_ITEMS[item.food_item_ID].category == category
        )

        embed.add_field(name=category.value, value=items_text, inline=False)

    return embed
          
class MenuView(discord.ui.View):
    def __init__(self, *items, timeout = 180, disable_on_timeout = False, player: Player):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.player = player

    @discord.ui.button(label="Add Item", style=discord.ButtonStyle.success) 
    async def add_item_button_callback(self, button, interaction):
        await interaction.response.send_message(view=SelectAllFoodItemView(player=self.player))

    @discord.ui.button(label="Remove Item", style=discord.ButtonStyle.red) 
    async def remove_item_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button2!")

    @discord.ui.button(label="Edit Item", style=discord.ButtonStyle.primary) 
    async def edit_item_button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button3!")

class SelectAllFoodItemView(discord.ui.View):
    def __init__(self, *items, timeout = 180, disable_on_timeout = False, player: Player):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.player = player


    @discord.ui.select( 
        placeholder = "Choose a Flavor!",
        min_values = 1,
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                value=ID.value,
                label=data.name,
                description=f"Pick this if you like {data.name}!"
            )
            for ID, data in ALL_FOOD_ITEMS.items()
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_modal(SettingAddedMenuItemModal(
            self.player, FoodItemID(select.values[0]), ALL_FOOD_ITEMS[FoodItemID(select.values[0])]))


def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))
import random
from discord import ApplicationContext, Bot, Cog, slash_command, SlashCommandGroup
from discord.ext import tasks
from burger_joint.bot import player_check
from burger_joint.utils import FoodItemID, database, ALL_FOOD_ITEMS
from burger_joint.model import FoodItem, MenuItem, Player
from discord import Embed, Message, Color

class MenuCommands(Cog):
    @slash_command(description="View and edit you joint's menu")
    @player_check
    async def menu(self, ctx: ApplicationContext):
        await ctx.respond(embed=menu_embed(ctx.player))

def menu_embed(player : Player) -> Embed:
    embed = Embed(title=f"🍔 {player.shop_name} Menu:", color=Color.lighter_grey())



    for menu_item in player.menu_items:
        embed.add_field(name=menu_item.name, value=f"{menu_item.price}$")

    return embed
          

def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))
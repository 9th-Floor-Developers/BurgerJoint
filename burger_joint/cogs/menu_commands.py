import random
from discord import ApplicationContext, Bot, Cog, slash_command, SlashCommandGroup
from discord.ext import tasks
from burger_joint.bot import player_check
from burger_joint.utils import FoodItemID, database, ALL_FOOD_ITEMS
from burger_joint.model import FoodItem
from discord import Embed, Message, Color

class MenuCommands(Cog):
    @slash_command(description="View and edit you joint's menu")
    @player_check
    async def menu(self, ctx: ApplicationContext):
        await ctx.respond("menu")

def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))
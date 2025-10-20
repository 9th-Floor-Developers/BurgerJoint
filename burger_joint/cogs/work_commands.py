import random
from discord import ApplicationContext, Bot, Cog, slash_command
from discord.ext import tasks
from burger_joint.bot import player_check
from burger_joint.utils import database
from burger_joint.model import FoodItem, FoodItemID, ALL_FOOD_ITEMS
from discord import Embed, Message, Color

        
class WorkCommands(Cog):
    @slash_command(description="Work to earn money and XP")
    @player_check
    async def work(self, ctx: ApplicationContext):
        await ctx.respond("work in progress")
        WorkSession(ctx)


class WorkSession:
    def __init__(self, ctx: ApplicationContext):
        self.ctx = ctx

        self.updater.start()
        self.ordered_items : list[FoodItem] = [] 
        self.money_earned : int = 0

        self.counter : int = 0
  
    @tasks.loop(seconds=0.1, count=50)
    async def updater(self):
        self.counter += 1
        if self.counter > 5:
            if random.random() < 0.2:
                await self.on_order_item()

    async def on_order_item(self):
        menu_item : FoodItem = ALL_FOOD_ITEMS[random.choice(list(self.ctx.player.menu_items))]

        self.ordered_items.append(menu_item)
        self.money_earned += menu_item.price

        await self.message_display.edit(embed=await self.work_session_embed())


    @updater.before_loop
    async def start_session(self):
        self.message_display : Message = await self.ctx.respond(embed=await self.work_session_embed())


    @updater.after_loop
    async def finnish_session(self):
        self.ctx.player.balance += self.money_earned
        database.save_data(self.ctx.player)
        
        await self.message_display.edit(embed=await self.work_session_embed(True))

    async def work_session_embed(self, is_finnish : bool = False) -> Embed:
        if self.counter < 5:
            return Embed(title="Work Session Starting...", description="Geting ready to serve some customers!", color=Color.yellow())
        if len(self.ordered_items) == 0:
            return Embed(title="Work Session In Progress", description="No items served yet...", color=Color.yellow())
        
        items_text = "\n".join(
            f"{i+1}. {item.name} — ${item.price}"
            for i, item in enumerate(self.ordered_items)
        )

        if (is_finnish):
            embed = Embed(title="Work Session Finished!", color=Color.green())
        else:
            embed = Embed(title="Work Session In Progress", color=Color.green())
        
        embed.add_field(name="Served Items", value=items_text, inline=False)
        embed.add_field(name="Total Items", value=str(len(self.ordered_items)), inline=True)
        embed.add_field(name="Money Earned", value=f"${self.money_earned}", inline=True)
        return embed
    

		
def setup(bot: Bot):
	bot.add_cog(WorkCommands(bot))

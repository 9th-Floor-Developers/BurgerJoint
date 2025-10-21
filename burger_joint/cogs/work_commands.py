import random

from discord import ApplicationContext, Bot, Cog, Color, Embed, Message, \
	slash_command
from discord.ext import tasks

from burger_joint.bot import player_check
from burger_joint.model import ALL_FOOD_ITEMS, FoodItem
from burger_joint.utils import database


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
		self.ordered_items: list[FoodItem] = []
		self.money_earned: int = 0
		self.message_display: Message | None = None
		
		self.counter: int = 0
	
	@tasks.loop(seconds=0.1, count=50)
	async def updater(self):
		self.counter += 1
		if self.counter > 5:
			if random.random() < 0.2:
				await self.on_order_item()
	
	async def on_order_item(self):
		menu_item: FoodItem = ALL_FOOD_ITEMS[
			random.choice(list(self.ctx.player.menu_items))  # type: ignore
		]
		
		self.ordered_items.append(menu_item)
		self.money_earned += menu_item.price
		
		await self.message_display.edit(embed=await self.work_session_embed())
	
	@updater.before_loop
	async def start_session(self):
		self.message_display: Message = await self.ctx.respond(
			embed=await self.work_session_embed()
		)
	
	@updater.after_loop
	async def finnish_session(self):
		self.ctx.player.balance += self.money_earned  # type: ignore
		database.save_data(self.ctx.player)  # type: ignore
		
		await self.message_display.edit(
			embed=await self.work_session_embed(True)
		)
	
	async def work_session_embed(self, is_finished: bool = False) -> Embed:
		if self.counter < 5:
			return Embed(
				title="Work Session Starting...",
				description="Getting ready to serve some customers!",
				color=Color.yellow()
			)
		if not self.ordered_items:
			return Embed(
				title="Work Session In Progress",
				description="No items served yet...", color=Color.yellow()
			)
		
		items_text = "\n".join(
			f"{i + 1}. {item.name} — ${item.price}"
				for i, item in enumerate(self.ordered_items)
		)
		
		embed = Embed(
			title=(
				"Work Session Finished!" if is_finished else "Work Session In Progress"),
			color=Color.green()
		).add_field(
			name="Served Items", value=items_text, inline=False
		).add_field(
			name="Total Items", value=str(len(self.ordered_items)), inline=True
		).add_field(
			name="Money Earned", value=f"${self.money_earned}", inline=True
		)
		
		return embed


def setup(bot: Bot):
	bot.add_cog(WorkCommands(bot))

import random

from discord import ApplicationContext, Bot, Cog, Color, Embed, Message, \
	slash_command
from discord.ext import tasks

from burger_joint.bot import player_check
from burger_joint.model import ALL_FOOD_ITEMS, FoodItem, Order, MenuItem, OrderedItem
from burger_joint.utils import database


class WorkCommands(Cog):
	@slash_command(description="Work to earn money and XP")
	@player_check
	async def work(self, ctx: ApplicationContext):
		WorkSession(ctx)


class WorkSession:
	def __init__(self, ctx: ApplicationContext):
		self.ctx = ctx
		self.player = ctx.player
		
		self.updater.start()
		self.orders: list[Order] = []
		self.money_earned: int = 0
		self.message_display: Message | None = None
		
		self.counter: int = 0

	async def generate_order(self) -> Order:
		ordering_items: list[OrderedItem] = []
		for menu_item in self.player.menu_items:
			ordering_items.append(OrderedItem(
				menu_item=menu_item,
				amount=random.randint(1, 4),))

		self.orders.append(Order(
			ordered_items=ordering_items
		))

	
	@tasks.loop(seconds=0.5, count=50)
	async def updater(self):
		self.counter += 1
		if self.counter > 5:
			if random.random() < 0.2:
				await self.generate_order()

		await self.message_display.edit(
			embed=await self.work_session_embed()
		)
	
	@updater.before_loop
	async def start_session(self):
		self.message_display: Message = await self.ctx.respond(
			embed=await self.work_session_embed()
		)
	
	@updater.after_loop
	async def finnish_session(self):
		self.player.balance += self.money_earned  # type: ignore
		database.save_data(self.player)  # type: ignore
		
		await self.message_display.edit(
			embed=await self.work_session_embed(True)
		)
	
	async def work_session_embed(self, is_finished: bool = False) -> Embed:
		if self.counter < 5:
			return Embed(
				title="Preparing the joint",
				description="Getting ready to serve some customers!",
				color=Color.yellow()
			)
		if not self.orders:
			return Embed(
				title="Waiting for customers",
				description="No items served yet...", color=Color.yellow()
			)
		
		orders_text = "\n-------\n".join(
			f"{order.display_item_string()}"
				for i, order in enumerate(self.orders)
		)
		
		embed = Embed(
			title=(
				"Work Session Finished!" if is_finished else "Work Session In Progress"),
			color=Color.green()
		).add_field(
			name="Current orders", value=orders_text, inline=False
		).add_field(
			name="Total orders", value=str(len(self.orders)), inline=True
		).add_field(
			name="Money Earned", value=f"${self.money_earned}", inline=True
		)
		
		return embed


def setup(bot: Bot):
	bot.add_cog(WorkCommands(bot))

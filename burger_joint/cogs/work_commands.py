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

		self.finished_orders:int = 0
		self.total_orders:int = 0

		self.money_earned: int = 0
		self.message_display: Message | None = None
		
		self.counter: int = 0

	async def generate_order(self) -> Order:
		ordering_items: list[OrderedItem] = []
		for menu_item in self.player.menu_items:
			ordering_items.append(OrderedItem(
				menu_item=menu_item,
				amount=random.randint(1, 3),
				state="waiting"))

		self.orders.append(Order(
			ordered_items=ordering_items
		))
		self.total_orders += 1

	
	@tasks.loop(seconds=0.5)
	async def updater(self):
		self.counter += 1
		if self.counter > 3 and self.counter < 100 and len(self.orders) < 5:
			if random.random() < 0.2:
				await self.generate_order()

		await self.update_work_progress()
		await self.update_finished_orders()

		await self.message_display.edit(
			embed=await self.work_session_embed()
		)

		if self.counter >= 100 and not self.orders:
			self.updater.cancel()

		

	async def update_work_progress(self):
		worker_amount: int = 5 #TODO link this to amount of employees

		all_ordered_items: list[OrderedItem] = []
		for order in self.orders:
			all_ordered_items.extend([item for item in order.ordered_items if not item.state == "finished"])

		working_on_items: list[OrderedItem] = all_ordered_items[:worker_amount]
		for item in working_on_items:
			item.progress += 2 #TODO link this to updgrades
			
			if item.progress >= item.get_required_progress():
				item.state = "finished"
			else:
				item.state = "working"

		

	async def update_finished_orders(self):
		for order in self.orders:
			if order.is_finished():
				self.orders.remove(order)
				self.money_earned += order.get_total_price()
				self.finished_orders += 1
	
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
		if not is_finished:
			if self.counter < 5:
				return Embed(
					title="Preparing the joint",
					description="Getting ready to serve some customers!",
					color=Color.yellow()
				)
			if not self.orders:
				return Embed(
					title="Waiting for customers",
					description="No orders currently", color=Color.yellow()
				)

		embed = Embed(
			title=(
				"Work Session Finished!" if is_finished else "Work Session In Progress"),
			color=Color.green()
		)
		
		for i, order in enumerate(self.orders):
			embed.add_field(
				name=f"Order {i}:", value=order.get_items_display_string(), inline=True
			).add_field(
				name="Progress", value=order.get_progresses_display_string(), inline=True
			).add_field(name = chr(173), value = chr(173), inline=False)
		
		embed.add_field(
			name="Finished orders", value=f"{self.finished_orders}/{self.total_orders}", inline=True
		).add_field(
			name="Money Earned", value=f"${self.money_earned}", inline=True
		)
		
		return embed


def setup(bot: Bot):
	bot.add_cog(WorkCommands(bot))

import random

from discord import ApplicationContext, Bot, Cog, Color, Embed, Message, \
	slash_command
from discord.ext import tasks

from burger_joint.bot import player_check
from burger_joint.model import ALL_FOOD_ITEMS, FoodItem, Order, MenuItem, OrderedItem, Player, FoodCategoryID
from burger_joint.utils import database

ON_START_TAKING_ORDERS = 3
ON_END_TAKING_ORDERS = 100


class WorkCommands(Cog):
	@slash_command(description="Work to earn money and XP")
	@player_check
	async def work(self, ctx: ApplicationContext):
		WorkSession(ctx)


class WorkSession:
	def __init__(self, ctx: ApplicationContext):
		self.ctx = ctx
		self.player: Player = ctx.player
		
		self.updater.start()
		self.orders: list[Order] = []

		self.finished_orders: int = 0
		self.total_orders: int = 0

		self.money_earned: int = 0
		self.message_display: Message | None = None

		self.avg_waiting_time: float = 0
		self.avg_quality: float = 0

		self.counter: int = 0


	def get_items_desires(self) -> list[list[MenuItem, float]]:
		desires: list[list[MenuItem, float]] = []
		for menu_item in self.player.menu_items:
			desire: float = 0.6
			default_price = ALL_FOOD_ITEMS[menu_item.food_item_ID].default_price

			desire -= (menu_item.price/default_price - 1)

			desires.append([menu_item, desire])

		return desires

	def apply_loss_leader_effect(self, desires: list[list[MenuItem, float]], exception: MenuItem) -> list[list[MenuItem, float]]:
		for desire in desires:
			if ALL_FOOD_ITEMS[desire[0].food_item_ID].category != ALL_FOOD_ITEMS[exception.food_item_ID].category:
				desire[1] += 0.3

		return desires


	async def generate_order(self) -> Order:
		ordering_items: list[OrderedItem] = []
		desires: list[list[MenuItem, float]] = self.get_items_desires()

		for desire in desires:
			desire[1] = min(0.9, desire[1])
			if (random.random() < desire[1]):
				amount: int = 1
				if (random.random() < desire[1] / 2):
					amount += 1

				ordering_items.append(OrderedItem(
					menu_item=desire[0],
					amount=amount,
					state="waiting"))

				if (len(ordering_items) == 1):
					desires = self.apply_loss_leader_effect(desires, desire[0])

		if ordering_items:
			self.orders.append(Order(
				ordered_items=ordering_items
			))
			self.total_orders += 1

	
	@tasks.loop(seconds=0.5)
	async def updater(self):
		self.counter += 1
		if self.counter > ON_START_TAKING_ORDERS and self.counter < ON_END_TAKING_ORDERS and len(self.orders) < 5: #TODO Remove hard limit
			await self.generate_order()

		for order in self.orders:
			order.timer += 1

		await self.update_work_progress()
		await self.update_finished_orders()

		await self.message_display.edit(
			embed=await self.work_session_embed()
		)

		if self.counter >= ON_END_TAKING_ORDERS and not self.orders:
			self.updater.cancel()

		

	async def update_work_progress(self):
		worker_amount: int = 5 #TODO link this to amount of employees

		all_ordered_items: list[OrderedItem] = []
		for order in self.orders:
			all_ordered_items.extend([item for item in order.ordered_items if not item.state == "finished"])

		working_on_items: list[OrderedItem] = all_ordered_items[:worker_amount]
		for item in working_on_items:
			item.progress += 1 #TODO link this to updgrades
			
			if item.progress >= item.get_required_progress():
				item.state = "finished"
			else:
				item.state = "working"

		

	async def update_finished_orders(self):
		for order in self.orders:
			if order.is_finished():
				self.avg_waiting_time += order.timer - order.get_expected_waiting_time()
				
				self.money_earned += order.get_total_price()
				self.finished_orders += 1
				self.orders.remove(order)
	
	@updater.before_loop
	async def start_session(self):
		self.message_display: Message = await self.ctx.respond(
			embed=await self.work_session_embed()
		)
	
	@updater.after_loop
	async def finnish_session(self):
		self.player.balance += self.money_earned  # type: ignore
		database.save_data(self.player)  # type: ignore

		if self.finished_orders > 0:
			self.avg_waiting_time = round(self.avg_waiting_time / self.finished_orders, 2)
		
		await self.message_display.edit(
			embed=await self.work_session_embed(True)
		)
	
	async def work_session_embed(self, is_finished: bool = False) -> Embed:
		if is_finished:
			return self.work_session_finish_orders_embed()
		else:
			if self.counter < ON_START_TAKING_ORDERS:
				return Embed(
					title="Preparing the joint",
					description="Getting ready to serve some customers!",
					color=Color.yellow()
				)
			if not self.orders:
				return Embed(
					title="Waiting for customers",
					description="No orders currently"
				)
			else:
				return self.work_session_orders_embed()



	
	def work_session_orders_embed(self):
		embed = Embed(
			title=("Work Session In Progress"),
			color=Color.green()
		)
		
		for i, order in enumerate(self.orders):
			embed.add_field(
				name=f"Order {i+1}:", value=order.get_items_display_string(), inline=True
			).add_field(
				name="Progress", value=order.get_progresses_display_string(), inline=True
			).add_field(name = chr(173), value = chr(173), inline=False)
		
		embed.add_field(
			name="Finished orders", value=f"{self.finished_orders}/{self.total_orders}", inline=True
		).add_field(
			name="Money Earned", value=f"${self.money_earned}", inline=True
		)
		
		return embed
	
	def work_session_finish_orders_embed(self):
		waiting_time_text: str
		if (self.avg_waiting_time >= 30):
			waiting_time_text = "Extemely long"
		elif (self.avg_waiting_time >= 20):
			waiting_time_text = "Very long"
		elif (self.avg_waiting_time >= 10):
			waiting_time_text = "Long"
		elif (self.avg_waiting_time >= 0):
			waiting_time_text = "Fine"
		elif (self.avg_waiting_time >= -10):
			waiting_time_text = "Good"
		else:
			waiting_time_text = "Great"

		embed = Embed(
			title=("Work Session Finished!"),
			color=Color.green()
		).add_field(
			name="Waiting time:", value=f"{waiting_time_text} | {str(self.avg_waiting_time)}"
		).add_field(
			name="Quality:", value=""
		).add_field(
			name="Money Earned:", value=f"${self.money_earned}", inline=False
		)
		return embed



def setup(bot: Bot):
	bot.add_cog(WorkCommands(bot))

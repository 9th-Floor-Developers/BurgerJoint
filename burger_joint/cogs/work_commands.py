import random

from discord import ApplicationContext, Bot, Cog, Color, Embed, Interaction, \
	slash_command
from discord.ext import tasks

from burger_joint.bot import player_check
from burger_joint.model import ALL_FOOD_ITEMS, BadgeID, FoodCategoryID, \
	FoodItem, FoodItemID, MenuItem, \
	Order, \
	OrderedItem, \
	Player, UpgradeID
from burger_joint.utils import database

ON_START_TAKING_ORDERS = 3
ON_END_TAKING_ORDERS = 100


class WorkCommands(Cog):
	@slash_command(description='Work to earn money and XP')
	@player_check
	async def work(self, ctx: ApplicationContext):
		WorkSession(ctx)


class WorkSession:
	def __init__(self, ctx: ApplicationContext) -> None:
		self.ctx = ctx
		self.player: Player = ctx.player  # type: ignore
		
		self.updater.start()
		self.orders: list[Order] = []
		
		self.finished_orders: int = 0
		self.total_orders: int = 0
		
		self.money_earned: int = 0
		self.message_display: Interaction | None = None
		
		self.avg_waiting_time: float = 0
		self.avg_quality: float = 0
		
		self.counter: int = 0
	
	def get_items_desires(self) -> dict[MenuItem, float]:
		desires: dict[MenuItem, float] = {}
		for menu_item in self.player.menu_items:
			desire: float = 0.1
			default_price = \
				ALL_FOOD_ITEMS[menu_item.food_item_ID].default_price
			
			desire -= (menu_item.price / default_price - 1)
			desire += self.player.get_upgrade(
				UpgradeID.ADVERTISEMENTS
			).mult - 1
			
			desires[menu_item] = desire
		
		return desires
	
	@staticmethod
	def apply_loss_leader_effect(
		desires: dict[MenuItem, float],
		exception: MenuItem
	) -> dict[MenuItem, float]:
		for menu_item in desires:
			food = ALL_FOOD_ITEMS[menu_item.food_item_ID]
			exception_food = ALL_FOOD_ITEMS[exception.food_item_ID]
			
			if food and exception_food and food.category != exception_food.category:
				desires[menu_item] += 0.3
		
		return desires
	
	async def generate_order(self) -> None:
		ordering_items: list[OrderedItem] = []
		desires: dict[MenuItem, float] = self.get_items_desires()
		
		for menu_item in desires:
			desires[menu_item] = min(0.9, desires[menu_item])
			desire = desires[menu_item]
			if random.random() > desire:
				continue
			
			amount: int = 1
			if random.random() < desire / 2:
				amount += 1
			
			ordering_items.append(
				OrderedItem(
					menu_item=menu_item,
					amount=amount,
					state='waiting'
				)
			)
			
			if len(ordering_items):
				desires = self.apply_loss_leader_effect(desires, menu_item)
		
		if ordering_items:
			self.orders.append(
				Order(
					ordered_items=ordering_items
				)
			)
			self.total_orders += 1
	
	@tasks.loop(seconds=0.5)
	async def updater(self) -> None:
		self.counter += 1
		if ON_START_TAKING_ORDERS < self.counter < ON_END_TAKING_ORDERS:
			await self.generate_order()
		
		for order in self.orders:
			order.timer += 1
		
		await self.update_work_progress()
		await self.update_finished_orders()
		
		await self.message_display.edit(
			embed=self.work_session_embed()
		)
		
		if self.counter >= ON_END_TAKING_ORDERS and not self.orders:
			self.updater.cancel()
	
	async def update_work_progress(self) -> None:
		worker_amount: int = self.player.get_upgrade(UpgradeID.COOK).level
		
		all_ordered_items: list[OrderedItem] = []
		for order in self.orders:
			all_ordered_items.extend(
				[
					item
					for item in order.ordered_items
					if not item.state == 'finished'
				]
			)
		
		working_on_items: list[OrderedItem] = all_ordered_items[:worker_amount]
		for item in working_on_items:
			if random.random() < 0.3:
				item.quality -= 10  # Cook makes a mistake
			else:
				food_item_id: FoodItem = \
					ALL_FOOD_ITEMS[item.menu_item.food_item_ID]
				
				food_type: UpgradeID = {
					FoodCategoryID.BURGERS: UpgradeID.GRILL,
					FoodCategoryID.SNACKS: UpgradeID.FRYER,
					FoodCategoryID.DRINKS: UpgradeID.FOUNTAIN
				}.get(food_item_id.category)
				
				item.progress += self.player.get_upgrade(food_type).mult
			
			item.state = \
				'finished' if item.progress >= item.get_required_progress() \
					else 'working'
	
	async def update_finished_orders(self) -> None:
		for order in self.orders:
			if not order.is_finished():
				continue
			
			burgers_sold: int = 0
			for item in order.ordered_items:
				if item.menu_item.food_item_ID == FoodItemID.CLASSIC_BURGER:
					burgers_sold += item.amount
			self.player.burgers_sold += burgers_sold
			
			self.avg_waiting_time += order.timer - order.get_expected_waiting_time()
			self.avg_quality += order.get_avg_quality()
			
			self.money_earned += order.get_total_price()
			self.finished_orders += 1
			self.orders.remove(order)
	
	@updater.before_loop
	async def start_session(self) -> None:
		self.message_display: Interaction = await self.ctx.respond(
			embed=self.work_session_embed(),
			ephemeral=True
		)
	
	@updater.after_loop
	async def finnish_session(self) -> None:
		self.player.balance += self.money_earned  # type: ignore
		
		await self.check_achievements()
		
		if self.finished_orders > 0:
			self.avg_waiting_time = round(
				self.avg_waiting_time / self.finished_orders, 2
			)
			self.avg_quality = round(
				self.avg_quality / self.finished_orders, 2
			)
		
		rewards_text: str = ''
		
		if self.avg_waiting_time > 30 > self.avg_quality:
			self.player.prestige -= 1
			rewards_text += '-1 Prestige'
		elif self.avg_waiting_time < 0 and self.avg_quality > 70:
			self.player.prestige += 1
			rewards_text += '+1 Prestige'
		else:
			rewards_text += '-'
		
		database.save_data(self.player)
		
		await self.message_display.delete_original_response()
		await self.message_display.channel.send(
			embed=self.work_session_finish_orders_embed(rewards_text),
		)
	
	async def check_achievements(self):
		channel = self.ctx.channel
		if self.player.balance >= 5_000:
			await self.player.unlock_badge(
				BadgeID.REACH_5K_INCOME, channel
			)
		
		burgers_sold: int = self.player.burgers_sold
		if burgers_sold >= 1:
			await self.player.unlock_badge(
				BadgeID.SELL_1_BURGER, channel
			)
		if burgers_sold >= 100:
			await self.player.unlock_badge(
				BadgeID.SELL_100_BURGERS, channel
			)
		if burgers_sold >= 1000:
			await self.player.unlock_badge(
				BadgeID.SELL_1000_BURGERS, channel
			)
		if burgers_sold >= 10_000:
			await self.player.unlock_badge(
				BadgeID.SELL_10000_BURGERS, channel
			)
	
	def work_session_embed(self) -> Embed:
		if self.counter < ON_START_TAKING_ORDERS:
			return Embed(
				title='Preparing the joint',
				description='Getting ready to serve some customers!',
				color=Color.yellow()
			)
		if not self.orders:
			return Embed(
				title='Waiting for customers',
				description='No orders currently',
				color=Color.green()
			)
		
		return self.work_session_orders_embed()
	
	def work_session_orders_embed(self) -> Embed:
		embed = Embed(
			title='Work Session In Progress :cook:',
			color=Color.green()
		)
		
		for i, order in enumerate(self.orders):
			embed.add_field(
				name=f'Order {i + 1}:',
				value=order.get_items_display_string(),
				inline=True
			).add_field(
				name='Progress',
				value=order.get_progresses_display_string(),
				inline=True
			)
			
			if i >= 4 and i + 1 < len(self.orders):
				embed.add_field(
					name=f'And {len(self.orders) - (i + 1)} more orders',
					value=chr(173),
					inline=False
				)
				break
			else:
				embed.add_field(
					name=chr(173),
					value=chr(173),
					inline=False
				)
		
		embed.add_field(
			name='Finished orders :checkered_flag:',
			value=f'{self.finished_orders}/{self.total_orders}', inline=True
		).add_field(
			name='Money Earned :moneybag::', value=f'${self.money_earned}',
			inline=True
		)
		
		return embed
	
	def work_session_finish_orders_embed(self, rewards_text: str) -> Embed:
		waiting_time_text: str = next(
			(text for limit, text in [
				(40, 'Extremely long ⏳'),
				(30, 'Very long 🐢'),
				(20, 'Long ⏲️'),
				(10, 'Fine 😐'),
				(0, 'Good ⏩'),
			] if self.avg_waiting_time >= limit),
			'Great ⚡'
		)
		
		quality_text: str = next(
			(text for limit, text in [
				(90, 'Awesome 🤩'),
				(70, 'Great ⭐'),
				(50, 'Good 👍'),
				(30, 'Fine 😐'),
				(10, 'Poor 👎'),
			] if self.avg_quality >= limit),
			'Puke 🤮'
		)
		
		embed = Embed(
			title='Work Session Finished! 🏁',
			color=Color.green()
		).add_field(
			name='Waiting time ⏳:',
			value=f'{waiting_time_text} | {str(self.avg_waiting_time)}'
		).add_field(
			name='Quality 👅:',
			value=f'{quality_text} | {str(self.avg_quality)}'
		).add_field(
			name='Money Earned 💰:',
			value=f'${self.money_earned}',
			inline=False
		).add_field(
			name='Rewards 🎁:',
			value=rewards_text,
			inline=False
		)
		return embed


def setup(bot: Bot):
	bot.add_cog(WorkCommands())

from typing import override

from discord import Embed, InputTextStyle, Interaction
from discord.ui import InputText, Modal

from burger_joint.model import ALL_FOOD_ITEMS, BadgeID, FoodItemID, MenuItem, \
	Player
from burger_joint.model.food_item import FoodItem
from burger_joint.utils.database import save_data
from burger_joint.utils.datacheck import is_positive_int


class EditingMenuItemModal(Modal):
	def __init__(self, player: Player, menu_item_index: int):
		super().__init__(title='Edit Item from menu')
		self.player: Player = player
		self.menu_item_index: int = menu_item_index
		self.food_item_ID: FoodItemID = \
			player.menu_items[menu_item_index].food_item_ID
		
		self.add_item(
			InputText(
				label='Name', value=player.menu_items[menu_item_index].name
			)
		)
		self.add_item(
			InputText(
				label='Price',
				value=str(player.menu_items[menu_item_index].price),
				style=InputTextStyle.short  # type: ignore
			)
		)
	
	@override
	async def callback(self, interaction: Interaction):
		temp_menu_item: MenuItem = \
			self.player.menu_items[self.menu_item_index]
		self.player.menu_items.pop(self.menu_item_index)
		
		name: str = self.children[0].value
		if await self.player.has_menu_item_name(name, interaction):
			self.player.menu_items.insert(
				self.menu_item_index, temp_menu_item
			)
			return
		
		if not await is_positive_int(
				self.children[1].value,
				interaction,
				var_name='price'
		):
			self.player.menu_items.insert(
				self.menu_item_index, temp_menu_item
			)
			return
		
		price: int = int(self.children[1].value)
		
		embed = Embed(
			title='Edited item on the menu'
		).add_field(
			name='Name', value=name
		).add_field(name='Price', value=str(price))
		
		await interaction.response.send_message(embeds=[embed])
		
		self.player.menu_items.insert(
			self.menu_item_index,
			MenuItem(
				food_item_ID=FoodItemID(self.food_item_ID.value),
				name=name,
				price=price,
				prestige=0
			)
		)
		
		save_data(self.player)


class SettingAddedMenuItemModal(Modal):
	def __init__(self, player: Player, food_item_id: FoodItemID):
		super().__init__(title='Add Item to menu')
		self.player: Player = player
		self.food_item_ID: FoodItemID = food_item_id
		self.food_item: FoodItem = ALL_FOOD_ITEMS[food_item_id]
		
		self.add_item(
			InputText(label='Name', value=self.food_item.name)
		)
		self.add_item(
			InputText(
				label='Price', value=str(self.food_item.default_price),
				style=InputTextStyle.short  # type: ignore
			)
		)
	
	@override
	async def callback(self, interaction: Interaction):
		name: str = self.children[0].value
		if await self.player.has_menu_item_name(name, interaction):
			return
		
		if not await is_positive_int(
				self.children[1].value,
				interaction,
				var_name='price'
		):
			return
		
		price: int = int(self.children[1].value)
		
		embed = Embed(
			title='Adding item to menu'
		).add_field(
			name='Name', value=name
		).add_field(name='Price', value=str(price))
		
		await interaction.response.send_message(embeds=[embed])
		
		self.player.menu_items.append(
			MenuItem(
				food_item_ID=FoodItemID(self.food_item_ID.value),
				name=name,
				price=price,
				prestige=0
			)
		)
		await self.player.unlock_badge(
			BadgeID.ADD_MENU_ITEM, interaction.channel
		)
		save_data(self.player)

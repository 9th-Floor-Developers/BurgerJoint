from typing import override

from discord import Embed, InputTextStyle, Interaction
from discord.ui import InputText, Modal

from burger_joint.model import ALL_FOOD_ITEMS, FoodItemID, MenuItem, Player
from model import FoodItem
from .database import save_data
from .datacheck import is_positive_int


class SettingAddedMenuItemModal(Modal):
	def __init__(self, player: Player, food_item_id: FoodItemID):
		super().__init__(title="Add Item to menu")
		self.player: Player = player
		self.food_item_ID: FoodItemID = food_item_id
		self.food_item: FoodItem = ALL_FOOD_ITEMS[food_item_id]
		
		self.add_item(
			InputText(label="Name", value=self.food_item.name)
		)
		self.add_item(
			InputText(
				label="Price", value=str(self.food_item.price),
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
				var_name="price"
		):
			return
		
		price: int = int(self.children[1].value)
		
		embed = Embed(
			title="Adding item to menu"
		).add_field(
			name="Name", value=name
		).add_field(name="Price", value=str(price))
		await interaction.response.send_message(embeds=[embed])
		
		self.player.menu_items.append(
			MenuItem(
				food_item_ID=FoodItemID(self.food_item_ID.value),
				name=name,
				price=price,
				prestige=0
			)
		)
		save_data(self.player)

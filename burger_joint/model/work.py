import math
from dataclasses import dataclass

from burger_joint.model.constants import ALL_FOOD_ITEMS
from burger_joint.model.food_item import MenuItem


@dataclass
class OrderedItem:
	menu_item: MenuItem
	amount: int = 1
	state: str = 'waiting'
	progress: float = 0
	quality: int = 100
	
	def get_required_progress(self) -> int:
		return ALL_FOOD_ITEMS[self.menu_item.food_item_ID].required_progress \
			* self.amount
	
	def get_progress_display_string(self) -> str:
		required_progress_per_piece: int = \
			ALL_FOOD_ITEMS[self.menu_item.food_item_ID].required_progress
		length: int = 8
		green_length: int = \
			math.floor(
				(self.progress % required_progress_per_piece) \
				/ required_progress_per_piece * length
			)
		
		display: str = '?'
		match self.state:
			case 'waiting':
				display = '🕒-'
			case 'working':
				display = '🍳-'
			case 'finished':
				display = '✅-'
				green_length = length
		
		display += '🟩' * green_length
		display += '🟥' * (length - green_length)
		
		display += (f' {int(self.progress // required_progress_per_piece)}'
		            f'/{self.amount}')
		return display
	
	def get_item_display_string(self) -> str:
		return f'{self.menu_item.name} : {self.amount}'


@dataclass
class Order:
	ordered_items: list[OrderedItem]
	timer: int = 0
	state: str = 'waiting'
	
	def get_expected_waiting_time(self) -> int:
		return max(item.get_required_progress() for item in self.ordered_items)
	
	def get_avg_quality(self) -> float:
		return sum(item.quality for item in self.ordered_items) / len(
			self.ordered_items
		)
	
	def get_items_display_string(self) -> str:
		return '\n'.join(
			f'{ordered_item.get_item_display_string()}'
				for ordered_item in self.ordered_items
		)
	
	def get_progresses_display_string(self) -> str:
		return '\n'.join(
			f'{ordered_item.get_progress_display_string()}'
				for ordered_item in self.ordered_items
		)
	
	def is_finished(self) -> bool:
		for ordered_item in self.ordered_items:
			if not ordered_item.state == 'finished':
				return False
		return True
	
	def get_total_price(self) -> int:
		return sum(
			item.menu_item.price * item.amount
				for item in self.ordered_items
		)

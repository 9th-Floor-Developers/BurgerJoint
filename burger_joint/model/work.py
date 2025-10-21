from dataclasses import dataclass
from burger_joint.model.food_item import MenuItem
from burger_joint.model.constants import ALL_FOOD_ITEMS
import math

@dataclass
class OrderedItem:
	menu_item: MenuItem
	amount: int = 1
	state: str = "waiting"
	progress: int = 0
	quality: int = 100
	
	def get_required_progress(self) -> int:
		return ALL_FOOD_ITEMS[self.menu_item.food_item_ID].required_progress * self.amount

	def get_progress_display_string(self) -> str:
		progress_per_peice: int = ALL_FOOD_ITEMS[self.menu_item.food_item_ID].required_progress 
		length: int = 8
		green_length: int = math.floor((self.progress%progress_per_peice)/progress_per_peice*length)

		display: str

		if self.state == "waiting":
			display = ":clock1:-"
		elif self.state == "working":
			display = ":cooking:-"
		elif self.state == "finished":
			display = ":white_check_mark:-"
			green_length = length

		display += ":green_square:" * green_length
		display += ":red_square:" * (length - green_length)

		display += f" {self.progress//progress_per_peice}/{self.amount}"
		return display
	
	def get_item_display_string(self) -> str:
		return f"{self.menu_item.name} : {self.amount}"
		



@dataclass
class Order:
	ordered_items: list[OrderedItem]
	timer: int = 0
	state: str = "waiting"
	expected_quality: int = 50
	expected_timer: int = 1

	def get_items_display_string(self) -> str:
		return "\n".join(f"{ordered_item.get_item_display_string()}" for ordered_item in self.ordered_items)
	
	def get_progresses_display_string(self) -> str:
		return "\n".join(f"{ordered_item.get_progress_display_string()}" for ordered_item in self.ordered_items)
	
	
	def is_finished(self) -> bool:
		for ordered_item in self.ordered_items:
			if not ordered_item.state == "finished":
				return False
		return True
	
	def get_total_price(self) -> int:
		return sum(item.menu_item.price * item.amount for item in self.ordered_items)
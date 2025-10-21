from dataclasses import dataclass
from burger_joint.model.food_item import MenuItem

@dataclass
class OrderedItem:
	menu_item: MenuItem
	amount: int = 1
	progress: int = 0
	quality: int = 100



@dataclass
class Order:
	ordered_items: list[OrderedItem]
	timer: int = 0
	state: str = "waiting"
	expected_quality: int = 50
	expected_timer: int = 1

	def display_item_string(self) -> str:
		return "\n".join(f"{ordered_item.menu_item.name} : {ordered_item.amount}" for ordered_item in self.ordered_items)
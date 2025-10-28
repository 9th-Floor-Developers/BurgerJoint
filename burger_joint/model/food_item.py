from dataclasses import dataclass
from typing import override, TYPE_CHECKING

if TYPE_CHECKING:
	from burger_joint.model.enums import FoodCategoryID, FoodItemID


@dataclass
class FoodItem:
	"""
	Represent the base food type, the types information like how hard is it to make
	"""
	name: str
	default_price: int
	difficulty: int
	required_progress: int
	category: 'FoodCategoryID'


@dataclass
class MenuItem:
	"""
	Represents a food item on a player's menu. may have different name, price,
	and prestige level than the base FoodItem depending on the joint
	"""
	
	food_item_ID: 'FoodItemID'
	name: str
	price: int
	prestige: int
	
	@override
	def __hash__(self):
		return hash(
			(
				self.food_item_ID,
				self.name,
				self.price,
				self.prestige
			)
		)

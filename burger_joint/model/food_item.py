from dataclasses import dataclass

from burger_joint.utils.enums import FoodCategoryID, FoodItemID


@dataclass
class FoodItem:
	name: str
	price: int
	difficulty: int
	category: FoodCategoryID


@dataclass
class MenuItem:
	"""
	Represents a food item on a player's menu. may have different name, price,
	and prestige level than the base FoodItem depending on the joint
	"""
	
	item_id: FoodItemID
	name: str
	price: int
	prestige: int

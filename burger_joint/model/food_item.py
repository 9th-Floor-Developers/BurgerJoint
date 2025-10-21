from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from model import FoodCategoryID, FoodItemID


@dataclass
class FoodItem:
	name: str
	price: int
	difficulty: int
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
